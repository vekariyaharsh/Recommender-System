import streamlit as st
import requests

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")
st.markdown("Get movie suggestions based on your favorite actor, director, or genre!")

# Input fields
col1, col2 = st.columns(2)
with col1:
    actor = st.text_input("🎭 Enter Actor Name", "Tom Hanks")

with col2:
    director = st.text_input("🎬 Enter Director Name", "")

genre = st.text_input("🎞️ Filter by Genre (optional)", "")
sort_option = st.selectbox("📊 Sort By", ["Rating", "Release Year"], index=0)
limit = st.slider("📌 Number of Results", min_value=5, max_value=20, value=10)

# Button to get recommendations
if st.button("🔍 Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            params = {
                "actor": actor,
                "director": director,
                "genre": genre,
                "sort": sort_option.lower().replace(" ", "_"),
                "limit": limit
            }
            res = requests.get("http://localhost:5000/recommend", params=params)
            if res.ok:
                data = res.json()
                if data:
                    st.subheader("🎥 Recommended Movies")
                    for movie in data:
                        with st.container():
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                poster_url = movie.get("poster_url", "")
                                if poster_url:
                                    st.image(poster_url, width=100)
                            with col2:
                                st.markdown(f"**{movie['title']}")
                                st.markdown(f"⭐ **Rating:** {movie.get('rating', 'N/A')}")
                else:
                    st.warning("No recommendations found based on your input.")
            else:
                st.error("API Error: Could not fetch data.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
