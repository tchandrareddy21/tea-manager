from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="Tea API")

class Tea(BaseModel):
    id: int
    name: str
    type: str
    origin: str
    description: str


teas : List[Tea] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tea API!"}

@app.get("/teas")
def get_teas():
    return {"teas": teas}

@app.post("/teas")
def add_tea(tea_item: Tea):
    teas.append(tea_item)
    return {"message": "Tea added successfully", "tea": tea_item}

@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea: Tea):
    for index, item in enumerate(teas):
        if item.id == tea_id:
            teas[index] = updated_tea
            return {"message": "Tea updated successfully", "tea": updated_tea}
    return {"message": "Tea not found"}, 404

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for index, item in enumerate(teas):
        if item.id == tea_id:
            deleted_tea = teas.pop(index)
            return {"message": "Tea deleted successfully", "tea": deleted_tea}
    return {"message": "Tea not found"}, 404


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

