import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
collection = client.create_collection(
    name="my_docs",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction()
)

docs = [
    "RAG是检索增强生成，让大模型先检索外部知识再回答，可以解决幻觉问题",
    "向量数据库用于存储和检索文本的向量表示，常见的有Chroma、Milvus、Qdrant",
    "Prompt engineering是设计输入来引导大模型输出正确结果的技术"
]
collection.add(documents=docs, ids=["doc1", "doc2", "doc3"])

if __name__ == "__main__":
    question = input("请输入检索问题: ")
    results = collection.query(query_texts=[question], n_results=2)
    print("\n检索结果:")
    for i, (doc, score) in enumerate(zip(results['documents'][0], results['distances'][0])):
        print(f"{i+1}. 相似度: {1-score:.2f} | {doc[:100]}...")