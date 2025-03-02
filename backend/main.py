from fastapi import FastAPI, Query
import faiss
import json
import openai
import numpy as np
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


index = faiss.read_index("../notebooks/data/product_embeddings.index")
with open("../notebooks/data/product_texts.json", "r", encoding="utf-8") as f:
    product_texts = json.load(f)

with open("../notebooks/data/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# OpenAI API Key
OPENAI_API_KEY = ""

def get_embedding(text):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        input=[text],  
        model="text-embedding-ada-002"
    )
    
    return np.array(response.data[0].embedding)

def search_products(query, top_k=5):
    query_embedding = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    
    results = [products[i] for i in indices[0] if i < len(products)]  
    return results

@app.get("/chat")
def chat(query: str = Query(..., description="User query for product search")):
    results = search_products(query)

    
    if not results:
        return {"query": query, "response": "Sorry, I couldn't find any matching products.", "results": []}

    
    product_list = "\n".join(
        [f"{i+1}. {p['name']} - {p['price']} MKD\n   [View Product]({p['link']})\n" for i, p in enumerate(results)]
    )

   
    messages = [
        {"role": "system", "content": "You are an AI shopping assistant. Only recommend products from the provided list."},
        {"role": "user", "content": f"Here are the top {len(results)} products I found:\n{product_list}\n\nWhich one should I choose?"},
        {"role": "assistant", "content": "Here are some recommendations based on your query:"}
    ]

   
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

   
    return {"query": query, "response": response.choices[0].message.content, "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
