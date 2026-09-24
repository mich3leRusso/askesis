import chromadb

DB_PATH = "chroma_db"


def init_chroma(collection_name: str = "papers"):
    # persistent so embeddings survive across runs; chromadb auto-embeds
    # documents with its bundled default model (no separate model needed)
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(collection_name)


def embed_sections(collection, sections: dict, source_filename: str, paper_title: str):
    """Embed every section dict from MD_Extractor.get_sections() into the collection."""
    ids, documents, metadatas = [], [], []
    for number, section in sections.items():
        if not section["content"]:
            continue
        ids.append(f"{source_filename}::{number}")
        documents.append(section["content"])
        metadatas.append({
            "source": source_filename,
            "number": number,
            "section_title": section["title"],
            "paper_title": paper_title
        })

    if documents:
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    return len(documents)

