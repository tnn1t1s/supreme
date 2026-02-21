from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = None

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever(similarity_top_k=10)

queries = [
    "How should alternative data signals be integrated into a portfolio and monetized?",
    "What is the connection between data scouting, hypothesis testing, and portfolio risk allocation?",
    "How should a quant firm organize technology and investment teams to build a scalable research platform?",
]

for q in queries:
    print(f"=== QUERY: {q} ===")
    nodes = retriever.retrieve(q)
    for i, node in enumerate(nodes[:5]):
        print(f"--- NODE {i+1} | score={node.score:.4f} ---")
        print(node.text[:1500])
        print()
    print("=" * 80)
