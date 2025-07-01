from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import os
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai.api_key

# Initialize FastAPI
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

# Home page - input form
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Restaurant Menu Generator</title>
        </head>
        <body style='font-family: Arial; text-align: center;'>
            <h1>🍽️ Restaurant Generator</h1>
            <form action="/generate" method="post">
                <label>Enter Cuisine Type:</label>
                <input type="text" name="cuisine" placeholder="e.g. Indian, Italian" required/>
                <br><br>
                <input type="submit" value="Generate Menu"/>
            </form>
        </body>
    </html>
    """

# POST route - generate & display table
@app.post("/generate", response_class=HTMLResponse)
async def generate_web(cuisine: str = Form(...)):
    try:
        result = chain({"cuisine": cuisine})
        restaurant_name = result["restaurant_name"].strip().replace('"', '')
        raw_items = result["items"].strip().split("\n")

        # Clean and convert to list
        menu_items = []
        for item in raw_items:
            cleaned = item.strip()
            if cleaned:
                parts = cleaned.split(". ", 1)
                if len(parts) == 2 and parts[0].isdigit():
                    menu_items.append(parts[1].strip())
                else:
                    menu_items.append(cleaned)

        # Generate HTML table
        table_html = "<table border='1' style='margin:auto; border-collapse: collapse;'>"
        table_html += "<tr><th>#</th><th>Menu Item</th></tr>"
        for i, item in enumerate(menu_items, start=1):
            table_html += f"<tr><td>{i}</td><td>{item}</td></tr>"
        table_html += "</table>"

        return f"""
        <html>
            <head><title>Generated Menu</title></head>
            <body style='font-family: Arial; text-align: center;'>
                <h2>🏷️ {restaurant_name}</h2>
                <h3>📋 Menu for {cuisine.title()} Cuisine</h3>
                {table_html}
                <br><br>
                <a href="/">🔁 Generate Another</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><a href='/'>Back</a>"
