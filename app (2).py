
import streamlit as st
import requests

st.set_page_config(page_title="Restaurant Menu Generator")

st.title("🍽️ Restaurant Menu Generator")
cuisine = st.text_input("Enter a Cuisine:", value="Indian")

if st.button("Generate Menu"):
    with st.spinner("Generating menu..."):
        try:
            response = requests.post(
                "https://restaurant-generator-api.onrender.com/generate",
                json={"cuisine": cuisine}
            )
            data = response.json()

            st.subheader(f"Restaurant Name: 🍴 {data['restaurant_name'].strip()}")
            st.markdown("### Menu Items:")
            for i, item in enumerate(data['menu_items'].split("\n"), 1):
                if item.strip():
                    st.markdown(f"**{i}.** {item.strip()}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
