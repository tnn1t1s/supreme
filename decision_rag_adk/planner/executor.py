import json
from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from pydantic import Field

from .base import BasePlanner
from .heuristic import HeuristicPlanner
from .compiler import compile_plan, load_affordance_catalog, load_corpus_manifest


class DAPAgent(BaseAgent):
    """Deterministic Affordance Planner — replaces SequentialAgent.

    Compiles a query-specific agent DAG from declared affordances,
    then executes only the selected agents in topological order.
    """

    agent_registry: dict = Field(default_factory=dict, exclude=True)
    planner: BasePlanner = Field(default_factory=HeuristicPlanner, exclude=True)
    catalog_path: str = "config/affordances.yaml"
    docs_root: str = "docs/decision"

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        query_text = self._extract_query(ctx)

        catalog, cat_version = load_affordance_catalog(self.catalog_path)
        manifests = load_corpus_manifest(self.docs_root)
        features = self.planner.analyze(query_text, manifests, catalog)
        plan = compile_plan(features, manifests, catalog, cat_version)

        ctx.session.state["query_features"] = json.dumps(features)
        ctx.session.state["execution_plan"] = json.dumps(plan)
        ctx.session.state["plan_corpus_scope"] = json.dumps(plan["corpus_scope"])

        yield Event(
            author=self.name,
            actions=EventActions(
                state_delta={
                    "query_features": json.dumps(features),
                    "execution_plan": json.dumps(plan),
                    "plan_corpus_scope": json.dumps(plan["corpus_scope"]),
                }
            ),
        )

        for node_id in plan["execution_order"]:
            agent = self.agent_registry.get(node_id)
            if not agent:
                yield Event(
                    author=self.name,
                    actions=EventActions(
                        state_delta={
                            f"dap_error_{node_id}": f"no agent registered for affordance {node_id}"
                        }
                    ),
                )
                return

            aff = catalog[node_id]
            for inp in aff.get("inputs", []):
                if not ctx.session.state.get(inp):
                    yield Event(
                        author=self.name,
                        actions=EventActions(
                            state_delta={
                                f"dap_error_{node_id}": f"missing required input: {inp}"
                            }
                        ),
                    )
                    return

            async for event in agent.run_async(ctx):
                yield event

            yield Event(
                author=self.name,
                actions=EventActions(
                    state_delta={
                        f"dap_trace_{node_id}": "completed"
                    }
                ),
            )

    def _extract_query(self, ctx: InvocationContext) -> str:
        if ctx.user_content and ctx.user_content.parts:
            texts = []
            for part in ctx.user_content.parts:
                if hasattr(part, "text") and part.text:
                    texts.append(part.text)
            if texts:
                return " ".join(texts)
        for event in reversed(ctx.session.events or []):
            if event.author == "user" and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        return part.text
        return ""
