import streamlit as st
import time
import os
import re
import base64
from dotenv import load_dotenv
from settings import setup, configure_display_options
from chatbot import chat_all
from map_creation import get_default_chicago_map_config, render_map

# Toggle the sign-up page
def show_signup():
    st.session_state.show_signup = True

# Toggle the login page
def show_login():
    st.session_state.show_signup = False

# Function to load and convert an image file to base64 string
def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")