import streamlit as st
import requests

# Set up API keys
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
YOUTUBE_API_KEY =  "YOUR_YOUTUBE_API_KEY"

# Gemini API function
def get_gemini_response(query):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": {"text": query}}

    response = requests.post(url, headers=headers, json=data)
    return response.json().get("candidates", [{}])[0].get("output", "No response found.")

# YouTube API function
def get_youtube_videos(query):
    url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 5,  # Get top 5 videos
        "type": "video"
    }

    response = requests.get(url, params=params).json()
    videos = []

    for item in response.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        videos.append(f"[{title}](https://www.youtube.com/watch?v={video_id})")

    return videos

# Streamlit UI
st.title("🎯 YouTube AI Agent")

query = st.text_input("Enter your query:")

if st.button("Search"):
    if query:
        with st.spinner("Fetching response..."):
            gemini_answer = get_gemini_response(query)
            youtube_results = get_youtube_videos(query)

       # st.subheader("🤖 Gemini AI Response:")
        #st.write(gemini_answer)

        st.subheader("🎬 Related YouTube Videos:")
        for title, url, video_id in youtube_results:
            st.write(f"**{title}**")
            st.video(f"https://www.youtube.com/embed/{video_id}")  # Embedding YouTube video

    else:
        st.warning("Please enter a query first.")
