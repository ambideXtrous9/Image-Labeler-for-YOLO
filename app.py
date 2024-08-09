import streamlit as st 
import pandas as pd
import numpy as np
import requests

# UI configurations
st.set_page_config(page_title="Replicate Image Generator",
                   page_icon=":bridge_at_night:",
                   layout="centered")
st.title(":rainbow[Streamlit Portfolio]")


# Function to manage navigation
def navigate(page):
    st.experimental_set_query_params(page=page)

# Sidebar layout with navigation
with st.sidebar:
    st.header("app")
    if st.button("🛡️ Authenticator"):
        navigate("authenticator")
    if st.button("🐙 GitHub Stats"):
        navigate("github_stats")
    if st.button("🚀 Open Trade"):
        navigate("open_trade")
    if st.button("🤖 Straddle Bot"):
        navigate("straddle_bot")
    if st.button("⚙️ Automate"):
        navigate("automate")
    if st.button("🛒 Order System"):
        navigate("order_system")
    if st.button("🌐 Multi Account"):
        navigate("multi_account")
    if st.button("🕵️‍♂️ PriceAction Backtester"):
        navigate("priceaction_backtester")
    if st.button("👼 Oauth Angel"):
        navigate("oauth_angel")
    if st.button("🏦 Oauth IIFL"):
        navigate("oauth_iifl")
    if st.button("🎃 Oauth Upstox"):
        navigate("oauth_upstox")

# Get the current page from the query parameters
page = st.experimental_get_query_params().get("page", ["home"])[0]


# Display content based on the selected menu item
if page == "home":
    img_path = "https://camo.githubusercontent.com/920942ad162c59933c3455841c1843672d53f380789aae702604fc5c9001409a/68747470733a2f2f692e70696e696d672e636f6d2f6f726967696e616c732f61382f64352f62612f61386435626165623036666331326337376363656664303132313031306432302e676966"
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(img_path)
    
    # Display "About Me" text in the right column
    with col2:
        st.subheader("About Me")
        st.write("""
        👋 Hi there! I'm **Sushovan Saha**, a Machine Learning (ML) enthusiast specializing in **Natural Language Processing (NLP)** and **Computer Vision (CV)**. 
        I did my M.Tech in Data Science from **IIT Guwahati**. I am also a **Kaggle Notebook Expert**.
    
        🌟 I'm passionate about exploring the possibilities of ML to solve real-world problems and improve people's lives. 
        I love working on challenging projects that require me to stretch my abilities and learn new things.
    
        📚 In my free time, I like to contribute in **Kaggle**, Write ML blogs in **Medium**, read ML related blogs and updates. 
        I'm always looking for ways to stay up-to-date with the latest developments in the field.
        """)



# Page content based on the selected menu item
elif page == "authenticator":
    st.subheader("Authenticator Page")
    st.write("Content for the Authenticator page goes here.")

elif page == "github_stats":
    st.subheader("GitHub Stats")
    username = "ambideXtrous9"  # Replace with your GitHub username
    response = requests.get(f"https://api.github.com/users/{username}")

    if response.status_code == 200:
        user_data = response.json()
        st.write(f"**Username:** {user_data['login']}")
        st.write(f"**Name:** {user_data.get('name', 'N/A')}")
        st.write(f"**Public Repos:** {user_data['public_repos']}")
        st.write(f"**Followers:** {user_data['followers']}")
        st.write(f"**Following:** {user_data['following']}")
        st.write(f"**Profile URL:** {user_data['html_url']}")
    else:
        st.error("Failed to fetch GitHub stats. Please check the username or try again later.")

elif page == "open_trade":
    st.subheader("Open Trade Page")
    st.write("Content for the Open Trade page goes here.")

elif page == "straddle_bot":
    st.subheader("Straddle Bot Page")
    st.write("Content for the Straddle Bot page goes here.")

elif page == "automate":
    st.subheader("Automate Page")
    st.write("Content for the Automate page goes here.")

elif page == "order_system":
    st.subheader("Order System Page")
    st.write("Content for the Order System page goes here.")

elif page == "multi_account":
    st.subheader("Multi Account Page")
    st.write("Content for the Multi Account page goes here.")

elif page == "priceaction_backtester":
    st.subheader("PriceAction Backtester Page")
    st.write("Content for the PriceAction Backtester page goes here.")

elif page == "oauth_angel":
    st.subheader("Oauth Angel Page")
    st.write("Content for the Oauth Angel page goes here.")

elif page == "oauth_iifl":
    st.subheader("Oauth IIFL Page")
    st.write("Content for the Oauth IIFL page goes here.")

elif page == "oauth_upstox":
    st.subheader("Oauth Upstox Page")
    st.write("Content for the Oauth Upstox page goes here.")

else:
    st.subheader("Home Page")
    st.write("Welcome to the Streamlit Portfolio. Use the sidebar to navigate.")
