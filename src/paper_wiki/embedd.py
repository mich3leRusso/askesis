import cromadb
import os 

def init_chroma(collection_name: str):
    # Initialize the Chroma client
    client = cromadb.Client()
    
    # Create a collection for storing embeddings
    if collection_name not in client.list_collections():
        client.create_collection(collection_name)
    
    return client.get_collection(collection_name)


def add_embeddings(collection, embeddings, metadata):
    # Add embeddings to the collection
    try :
        collection.add(embeddings=embeddings, metadatas=metadata)
    except Exception as e:
        print(f"Error adding embeddings: {e}")

    