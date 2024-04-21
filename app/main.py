from fastapi import FastAPI
from utils import gpt_response,extract_information,conversation

app = FastAPI()

@app.get("/ok")
async def ok_endpoint():
    return {"message":"ok"}

@app.post("/creation/response")
async def generate_response(query:str):
    conversation.append('User: ' + query)
    output = gpt_response(query)
    conversation.append('Bot: ' + output)
    return conversation


    
   

