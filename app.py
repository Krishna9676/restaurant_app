import streamlit as st
import requests

st.title("🍽️ Restaurant Menu Generator")

cuisine = st.text_input("Enter a Cuisine:")

if st.button("Generate Menu"):
    if not cuisine:
        st.warning("Please enter a cuisine type.")
    else:
        try:
            # ✅ Make sure you're calling the JSON endpoint (not the HTML one)
            response = requests.post(
                "https://restaurant-app-mbxe.onrender.com/api/generate",
                json={"cuisine": cuisine},
                timeout=15
            )
            response.raise_for_status()

            # ✅ Try parsing JSON (protect against HTML error pages)
            try:
                data = response.json()
            except ValueError:
                st.error("Server returned invalid JSON. Check backend `/api/generate`.")
                st.stop()

            # ✅ Handle error from backend
            if "error" in data:
                st.error(f"Server Error: {data['error']}")
            else:
                st.subheader(f"🏷️ {data['restaurant_name']}")
                st.write("### 📋 Menu")
                for item in data["menu_items"]:
                    st.write(f"• {item}")

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {e}")
