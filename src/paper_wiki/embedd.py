import chromadb
import os 

#create the client and teh collection
def init_chroma(collection_name: str):
    # Initialize the Chroma client
    client = chromadb.Client()
    
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


def create_embedding(text, model):
    # Create an embedding for the given text using the specified model
    try:
        embedding = model.encode(text)
        return embedding
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None

def add_embedding(collection, embedding, metadata):
    # Add a single embedding to the collection
    try:
        collection.add(embeddings=[embedding], metadatas=[metadata])
    except Exception as e:
        print(f"Error adding embedding: {e}")

def get_embeddings(collection, query_embedding, n_results=5):
    # Retrieve the most similar embeddings from the collection
    try:
        results = collection.query(query_embeddings=query_embedding, n_results=n_results)
        return results
    except Exception as e:
        print(f"Error retrieving embeddings: {e}")
        return None