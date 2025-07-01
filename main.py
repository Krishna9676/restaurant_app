from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# API Key setup
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai.api_key

app = FastAPI()

# LangChain setup
llm = OpenAI(temperature=0.6)
prompt_name = PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for it."
)
restaurant_name_chain = LLMChain(llm=llm, prompt=prompt_name, output_key="restaurant_name")

prompt_items = PromptTemplate(
    input_variables=["restaurant_name"],
    template="Suggest food items for a restaurant named {restaurant_name}."
)
restaurant_items_chain = LLMChain(llm=llm, prompt=prompt_items, output_key="items")

chain = SequentialChain(
    chains=[restaurant_name_chain, restaurant_items_chain],
    input_variables=["cuisine"],
    output_variables=["restaurant_name", "items"],
    verbose=True
)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h2>🍽️ LangChain Restaurant Generator</h2>
    <form action="/web" method="post">
        <label for="cuisine">Enter Cuisine:</label>
        <input type="text" name="cuisine" value="Italian" />
        <input type="submit" value="Generate" />
    </form>
    """

@app.post("/web", response_class=HTMLResponse)
async def web_view(cuisine: str = Form(...)):
    result = chain({"cuisine": cuisine})
    restaurant_name = result["restaurant_name"]
    menu_items = result["items"].strip().split("\n")

    return f"""
    <h2>🍴 {restaurant_name}</h2>
    <h3>📋 Menu:</h3>
    <ul>
        {''.join(f'<li>{item.strip()}</li>' for item in menu_items)}
    </ul>
    <a href="/">🔁 Try Another</a>
    """

@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    cuisine = body.get("cuisine", "Italian")
    result = chain({"cuisine": cuisine})
    return {
        "restaurant_name": result["restaurant_name"],
        "menu_items": result["items"]
    }

