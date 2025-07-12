# 🍽️ Restaurant Menu Generator with LangChain + FastAPI + Streamlit

A full-stack AI-powered app that generates fancy restaurant names and food menus based on a given cuisine using OpenAI and LangChain.

## 🔧 Tech Stack
- **FastAPI** – for backend API and HTML form rendering
- **LangChain + OpenAI** – to generate restaurant names and menus
- **Streamlit** – for a user-friendly frontend
- **Render** – for cloud deployment
- **Python-Multipart** – to handle HTML form submissions

## 🧠 How It Works
1. The backend (`main.py`) uses LangChain to generate:
   - A restaurant name based on the input cuisine
   - A detailed menu with 10–20 food items
2. The frontend (`app.py`) sends a POST request to `/api/generate` endpoint.
3. The response is displayed beautifully in Streamlit.

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/restaurant-generator.git
cd restaurant-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start FastAPI backend
uvicorn main:app --reload

# 4. Run Streamlit frontend
streamlit run app.py


🌐 Deployed Version
Live backend (FastAPI): https://restaurant-app-mbxe.onrender.com
Streamlit frontend: [your-ui-url-here] (optional)

🙏 Credits
Inspired by Codebasics LangChain projects

LangChain templates adapted and extended for this use-case

Prompt engineering guidance and base architecture credited to Codebasics tutorials
