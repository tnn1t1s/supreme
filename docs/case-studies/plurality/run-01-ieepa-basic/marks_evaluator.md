# marks_evaluator

```json
{
  "marks_applicable": true,
  "marks_rationale": "Marks v. United States applies because there is no majority opinion articulating a single rationale for the judgment. A six-justice majority agreed on the disposition (H1), but the reasoning was fractured. A three-justice plurality (Roberts, Gorsuch, Barrett) relied on both ordinary statutory interpretation and the major questions doctrine (R2). A three-justice concurrence (Kagan, Sotomayor, Jackson) explicitly rejected the major questions doctrine analysis and relied solely on ordinary statutory interpretation (R1, R3). This 3-3 split on the controlling legal standard necessitates a Marks analysis to determine the holding.",
  "majority_holdings": [
    {
      "holding_ref": "H1",
      "proposition": "The International Emergency Economic Powers Act (IEEPA) does not authorize the President to impose tariffs.",
      "majority_count": 6,
      "status": "clear_majority"
    },
    {
      "holding_ref": "R1",
      "proposition": "The statutory power to 'regulate' a subject does not ordinarily include the power to tax it. Congress consistently grants the authority to tax separately and expressly from the authority to regulate.",
      "majority_count": 6,
      "status": "clear_majority"
    },
    {
      "holding_ref": "R3",
      "proposition": "Tariffs are a branch of the taxing power, a power the Constitution vests exclusively in Congress in Article I, Section 8.",
      "majority_count": 6,
      "status": "clear_majority"
    },
    {
      "holding_ref": "R2",
      "proposition": "A claimed executive power of vast 'economic and political significance' requires a clear and explicit congressional authorization under the major questions doctrine.",
      "majority_count": 3,
      "status": "plurality_reasoning"
    }
  ],
  "narrowest_ground_analysis": {
    "candidates": [
      {
        "justice": "Kagan",
        "position": "The case can and should be resolved using ordinary principles of statutory interpretation alone, without resorting to the major questions doctrine. The text, context, and statutory scheme of IEEPA are sufficient to conclude that the power to 'regulate...importation' does not include the power to impose tariffs.",
        "source_blocks": [
          "24-1287_kagan_concurrence_in_part_0001"
        ],
        "why_narrowest": "This position is the narrowest ground because it is a logical subset of the plurality's reasoning. The plurality agrees with the statutory interpretation argument AND adds a second, independent requirement based on the major questions doctrine. All six justices in the majority agree on the statutory interpretation ground (R1, R3), making it the common denominator. The Kagan concurrence rests exclusively on this shared ground, deciding the case on the most minimal legal basis that still commands a majority, while the plurality adds a broader, more controversial doctrinal layer (R2).",
        "counterargument": "One could argue the plurality's position is 'narrower' in the sense that it seeks to constrain judicial decision-making in a specific class of high-stakes cases. However, this is not the typical understanding of 'narrowest ground' under Marks, which looks for the legal rule that decides the case on the least-sweeping basis. Avoiding the adoption or application of a major constitutional doctrine like the major questions doctrine is definitionally narrower than requiring its application.",
        "strength": "strong"
      },
      {
        "justice": "Roberts",
        "position": "The President's claim of tariff authority under IEEPA fails for two reasons: (1) it is a major question that lacks the required clear congressional authorization, and (2) ordinary statutory interpretation shows that Congress did not delegate the taxing power through the word 'regulate'.",
        "source_blocks": [
          "24-1287_roberts_majority_0005",
          "24-1287_roberts_majority_0006"
        ],
        "why_narrowest": "This position is not the narrowest ground.",
        "counterargument": "This position is broader because it rests on two independent legal pillars. A court following this reasoning would need to engage in both a major questions analysis and a traditional statutory analysis. The Kagan concurrence avoids the first step entirely, making its approach logically narrower.",
        "strength": "weak"
      }
    ],
    "assessment": "The Marks analysis in this case yields a reasonably clear answer. The narrowest ground for the decision is the reasoning articulated in Justice Kagan's concurrence, which is coextensive with the statutory interpretation analysis in Part II-B of the Chief Justice's opinion. This ground—that ordinary tools of statutory construction are sufficient to hold that IEEPA does not authorize tariffs—is the position on which all six justices in the majority agree.",
    "ambiguity_factors": [
      "While the application of Marks is often contested and ambiguous, the logical subset structure here—where the plurality's reasoning (A+B) fully contains the concurrence's reasoning (B)—makes the analysis more straightforward than in many other fractured cases."
    ]
  },
  "practical_impact": "Lower courts are definitively bound by the holding that IEEPA does not authorize the President to impose tariffs (H1). The controlling legal rule derived from this fractured decision is the narrow reasoning that the statutory term 'regulate' in IEEPA does not encompass the power to tax, based on ordinary principles of statutory interpretation (R1, R3). The plurality's reasoning regarding the major questions doctrine (R2) is not a binding holding of the Court, as it did not command a majority. Therefore, while persuasive to some, it does not have the force of precedent."
}
```
