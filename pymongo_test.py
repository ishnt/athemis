from pymongo import MongoClient

import os

def insert_data_to_mongodb(user_query: str, response: str, document: str,URL:str) -> None:
    
    CONNECTION_URL = URL

    # Data to insert
    data_to_insert = {
        "user_query": user_query,
        "response": response,
        "document": document
    }

    try:
        # Connect to the MongoDB Atlas cluster
        client = MongoClient(CONNECTION_URL)

        # Access the database
        db = client["athemis"]

        # Access the collection
        collection = db["user_query_and_responses"]

        # Insert data into the collection
        result = collection.insert_one(data_to_insert)
        print(f"Data inserted with ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        client.close()


