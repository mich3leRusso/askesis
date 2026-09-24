import sys
from paper_wiki.embedd import init_chroma

def search(collection, query: str, n_results: int = 5):
    return collection.query(query_texts=[query], n_results=n_results)

#create a search tha includes just one paper match and excludes the others , and tehn rerank 
def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python -m paper_wiki.search <query>")
        return

    collection = init_chroma("papers")  # reconnects to the same chroma_db/ on disk
    query = " ".join(sys.argv[1:])
    results = search(collection, query, n_results=5)

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"[{meta['paper_title']} - {meta['section_title']}]")
        print(doc[:200], "...\n")


if __name__ == "__main__":
    main()
