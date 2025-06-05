from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI(title="Tea API with MongoDB")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.tea_db
tea_collection = db.teas

class Tea(BaseModel):
    id: int
    name: str
    type: str
    origin: str
    description: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tea API with MongoDB!"}

@app.get("/teas", response_model=List[Tea])
def get_teas():
    teas = list(tea_collection.find({}, {"_id": 0}))  # exclude _id
    return teas

@app.post("/teas", response_model=Tea)
def add_tea(tea_item: Tea):
    if tea_collection.find_one({"id": tea_item.id}):
        raise HTTPException(status_code=400, detail="Tea with this ID already exists")
    tea_collection.insert_one(tea_item.model_dump())
    return tea_item

@app.put("/teas/{tea_id}", response_model=Tea)
def update_tea(tea_id: int, updated_tea: Tea):
    result = tea_collection.find_one_and_update(
        {"id": tea_id},
        {"$set": updated_tea.model_dump()},
        return_document=True
    )
    if result:
        result.pop("_id", None)
        return result
    raise HTTPException(status_code=404, detail="Tea not found")

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    result = tea_collection.find_one_and_delete({"id": tea_id})
    if result:
        result.pop("_id", None)
        return {"message": "Tea deleted successfully", "tea": result}
    raise HTTPException(status_code=404, detail="Tea not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
