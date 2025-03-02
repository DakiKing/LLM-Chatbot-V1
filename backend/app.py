from fastapi import FastAPI, Query
import json
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()


with open("../notebooks/data/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)


with open("../notebooks/data/embeddings.json", "r", encoding="utf-8") as f:
    embeddings = json.load(f)


model = SentenceTransformer("all-MiniLM-L6-v2")


product_names = list(embeddings.keys())
embedding_matrix = np.array([embeddings[name] for name in product_names])

def find_best_match(query):
    query_vector = model.encode(query)
    
    
    similarities = np.dot(embedding_matrix, query_vector)  
    best_index = np.argmax(similarities)
    best_score = similarities[best_index]


    if best_score < 0.5:  
        return {"message": "No confident match found. Try refining your query."}

    
    best_product_name = product_names[best_index]
    
 
    for product in products:
        if product["name"] == best_product_name:
            return product
    
    return None  

@app.get("/search")
def search(query: str = Query(..., title="Search Query")):
    result = find_best_match(query)
    
    if result:
        return {
            "name": result["name"],
            "category": result["category"],
            "price": result["price"],
            "link": result["link"],
            "image": result["image"],
            "availability": result["availability"]
        }
    return {"message": "No matching product found."}
