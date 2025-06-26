# main.py

from fastapi import FastAPI, Request
import os
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai.api_key  # Needed for LangChain

# Initialize FastAPI
app = FastAPI()

# Set up the LangChain models
llm = OpenAI(temperature=0.6)

# Restaurant name prompt
prompt_name = PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for it."
)
restaurant_name_chain = LLMChain(llm=llm, prompt=prompt_name, output_key="restaurant_name")

# Restaurant items prompt
prompt_items = PromptTemplate(
    input_variables=["restaurant_name"],
    template="Suggest food items for a restaurant named {restaurant_name}."
)
restaurant_items_chain = LLMChain(llm=llm, prompt=prompt_items, output_key="items")

# Combine chains
chain = SequentialChain(
    chains=[restaurant_name_chain, restaurant_items_chain],
    input_variables=["cuisine"],
    output_variables=["restaurant_name", "items"],
    verbose=True
)

# API route
@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    cuisine = body.get("cuisine", "Italian")

    # Run LangChain pipeline
    result = chain({"cuisine": cuisine})
    
    return {
        "restaurant_name": result["restaurant_name"],
        "menu_items": result["items"]
    }

@app.get("/")
def root():
    return {"message": "LangChain restaurant generator is running!"}
