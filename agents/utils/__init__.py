from pinecone import pinecone, ServerlessSpec 
import os 
import dotenv



dotenv.load_dotenv()

pc = pinecone.Pinecone(os.getenv('Pinecone_Api_key'))
