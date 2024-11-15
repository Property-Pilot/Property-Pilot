import streamlit as st
import time
import os
from dotenv import load_dotenv
from settings import setup, configure_display_options
from chatbot import chat_all
from map_creation import get_default_chicago_map_config, render_map

# Load the API key for Google Maps from .env
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("DEV_GOOGLE_MAP_API_KEY")

# Page configuration
st.set_page_config(page_title="InternationAlly", page_icon="ally-logo.png", layout="centered")

# Custom CSS for styling font, colors, and form layout
st.markdown("""
    <style>
        /* Change the font family and colors for the main app */
        html, body, [class*="css"]  {
            font-family: 'Open Sans', sans-serif !important;
            color: #333333;  /* Main text color */

        }

        /* Center title styling */
        .main-title {
            color: #434343;
            font-family: 'Open Sans', sans-serif !important;
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }

        /* Form styling */
        .form-container {
            margin-top: 100px;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }

        /* Customize button colors */
        .stButton>button {
            color: #FFFFFF !important; 
            background-color: #9AD6D2 !important;
            border: none;
            margin-top: 10px;
            padding: 8px 16px;
            font-weight: bold;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #86cec9 !important;  /* Darker on hover */
            color: #FFFFFF !important;
        }
        .stButton>button:active {
            background-color: #86cec9 !important; /* Keep the same background color when clicked */
            color: #FFFFFF !important;  /* Keep the text color white when clicked */
        }
         
        /* Input field styling */
        .stTextInput, .stPasswordInput {
            background-color: #ffffff;
            border-radius: 4px;
            padding: 0px;
            width: 100%;
            margin-top: 0px;
        }

        /* Link styling */
        .signup-link {
            text-align: center;
            margin-top: 20px;
            font-weight: bold;
            font-size: 20px;
        }
            
        /* Success message box */
        .st-success-box {
            color: #55555C;
            background-color: #FFF8E8;
            padding: 10px;
            border-radius: 1px;
            font-weight: bold;
            margin: 10px 0;
        }

        /* Error message box */
        .st-error-box {
            color: #55555C;
            background-color: #F4E5E3;
            padding: 10px;
            border-radius: 1px;
            font-weight: bold;
            margin: 10px 0;
        }
            
        /* Adjust the height of input fields */
        input[type="text"], input[type="password"] {
            height: 55px;              /* Sets a fixed height */
            font-size: 18px;           /* Increases the font size */
            width: 100%;               /* Makes input full-width of its container */
            padding: 12px;             /* Adds space inside the input for a larger clickable area */
            color: #333333;            /* Sets text color */
            /* background-color: #f9f9f9; Sets background color of input */
            border-radius: 1px;        /* Rounds the corners */
            outline: none;             /* Removes the default outline when input is focused */
            box-shadow: none;          /* Removes default box shadow */
            transition: all 0.3s ease; /* Adds a smooth transition for hover or focus effects */
        }
        
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if "users" not in st.session_state:
    st.session_state.users = {"user1": {"password": "password1"}, "user2": {"password": "password2"}}
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}  # To store chat histories per user
if "current_map_html" not in st.session_state:
    # Set the initial map to be centered on Chicago
    default_map_config = get_default_chicago_map_config()
    st.session_state.current_map_html = render_map(GOOGLE_MAPS_API_KEY, **default_map_config)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Toggle the sign-up page
def show_signup():
    st.session_state.show_signup = True

# Toggle the login page
def show_login():
    st.session_state.show_signup = False

import base64

# Function to load and convert an image file to base64 string
def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Function for the Sign-Up page
def signup_page():
    # Load and convert the logo image
    logo_base64 = load_image_as_base64("ally-logo.png")  # Ensure the path is correct

    # Display the centered logo using HTML and Base64
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
            <img src="data:image/jpg;base64,{logo_base64}" width="80">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='main-title'>InternationAlly by PropertyPilot</div>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style="display: flex; justify-content: center; text-align: center; margin-top: 1px;">
        <p style="font-size: 30px;">Your Ally Abroad! 🤝</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown(
    """
    <div style="display: flex; justify-content: center; text-align: center; margin-top: 20px;">
        <p style="font-size: 18px;">Create an account to access Ally, your trusted international student advisor.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

    with st.form(key = 'signup_form'):

        # New fields for user details
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>First Name</p>", unsafe_allow_html=True)
        first_name = st.text_input("First Name", label_visibility="collapsed")
        #first_name = st.text_input("First Name")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Last Name</p>", unsafe_allow_html=True)
        last_name = st.text_input("Last Name", label_visibility="collapsed")

        # Existing fields for username and password
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Create a Username</p>", unsafe_allow_html=True)
        new_username = st.text_input("Create a Username", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Create a Password</p>", unsafe_allow_html=True)
        new_password = st.text_input("Create a Password", type="password", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Confirm Password</p>", unsafe_allow_html=True)
        confirm_password = st.text_input("Confirm Password", type="password", label_visibility="collapsed")

        submit_button = st.form_submit_button("Sign Up")
    
    if submit_button:
        # Check if all fields are filled
        if not first_name or not last_name:
            st.markdown("<div class='st-error-box'>❗ Please fill out all personal details.</div>", unsafe_allow_html=True)
        elif new_username in st.session_state.users:
            st.markdown("<div class='st-error-box'>❗ Username already exists. Please choose a different one.</div>", unsafe_allow_html=True)
        elif new_password != confirm_password:
            st.markdown("<div class='st-error-box'>❗ Passwords do not match.</div>", unsafe_allow_html=True)
        elif new_username and new_password:
            # Save the new user credentials and details in session state
            st.session_state.users[new_username] = {
                "password": new_password,
                "first_name": first_name,
                "last_name": last_name
            }
            st.markdown("<div class='st-success-box'>Sign-Up successful! ✅ Redirecting to Sign-In...</div>", unsafe_allow_html=True)
            time.sleep(1.5)  # Short delay to show the success message
            show_login()  # Set to login view
            st.experimental_rerun()
        else:
            st.markdown("<div class='st-error-box'>❗ Please fill out all fields.</div>", unsafe_allow_html=True)
    
    # Add "Already have an account?" text and "Sign In" button below the sign-up form
    st.markdown("<div class='signup-link'>Already have an account?</div>", unsafe_allow_html=True)

        # Apply the custom width by wrapping the button in a container
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])  # To center the button
        with col2:  # Place the button in the middle column
            if st.button("Back to Sign In", key="small-backtosignin-button"):
                show_login()
                st.experimental_rerun()

# Function for the login page
def login_page():
    # Load and convert the logo image
    logo_base64 = load_image_as_base64("ally-logo.png")  # Ensure the path is correct

    # Display the centered logo using HTML and Base64
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
            <img src="data:image/jpg;base64,{logo_base64}" width="80">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='main-title'>InternationAlly by PropertyPilot</div>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style="display: flex; justify-content: center; text-align: center; margin-top: 1px;">
        <p style="font-size: 30px;">Your Ally Abroad! 🤝</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown(
    """
    <div style="display: flex; justify-content: center; text-align: center; margin-top: 20px;">
        <p style="font-size: 18px;">Sign in to get started.</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    
    # Login form container

    with st.form(key="login_form"):
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Username</p>", unsafe_allow_html=True)
        username = st.text_input("Username", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Password</p>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password", label_visibility="collapsed")
        submit_button = st.form_submit_button("Sign In")
    
    if submit_button:
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username  # Track the logged-in user
            # Show success message
            st.markdown("<div class='st-success-box'>Sign-in successful ✅ Launching Ally 🤗</div>", unsafe_allow_html=True)
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.markdown("<div class='st-error-box'>❌ Invalid username or password.</div>", unsafe_allow_html=True)

    # Sign-up prompt and button for new users
    st.markdown("<div class='signup-link'>New international student?</div>", unsafe_allow_html=True)


    # Apply the custom width by wrapping the button in a container
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])  # To center the button
        with col2:  # Place the button in the middle column
            if st.button("Sign Up Here", key="small-signup-button"):
                show_signup()
                st.experimental_rerun()


# Function for the main chat app
def chat_app():
    # Setup the bot and environment, but only once
    if 'setup_done' not in st.session_state:
        chat, prompts_dict, neighborhoods_info, neighborhoods_boundaries, vectordb = setup()
        configure_display_options()
        st.session_state.chat = chat
        st.session_state.prompts_dict = prompts_dict
        st.session_state.neighborhoods_info = neighborhoods_info
        st.session_state.neighborhoods_boundaries = neighborhoods_boundaries
        st.session_state.vectordb = vectordb
        st.session_state.setup_done = True

    # Ensure the current user and chat history are initialized
    current_user = st.session_state.current_user
    if current_user not in st.session_state.chat_histories:
        st.session_state.chat_histories[current_user] = [
            {"role": "assistant", "content": "Hello! I know being an international student can feel like a lot, especially in a place like the U.S., where everything might feel new and different. How are you feeling about everything so far? Any specific areas where you’re feeling like you could use a bit of help or extra advice?"}
        ]

    st.markdown(
    """
    <div style="text-align: justify; font-size: 15px; font-weight: bold;">
        InternationAlly is an AI platform built to support international students as they settle into life abroad. Ally, your personal AI assistant, is here to help with apartment searches, local tips, and guidance on essentials like getting an SSN or health insurance.
    </div>
    """,
    unsafe_allow_html=True
)

    # Log Out and Clear Conversation Buttons
    col_button1, col_button2 = st.columns([1, 1])
    with col_button1:
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.experimental_rerun()

    with col_button2:
        if st.button("Clear Conversation"):
            st.session_state.chat_histories[current_user] = [
                {"role": "assistant", "content": "Hello! I know being an international student can feel like a lot, especially in a place like the U.S., where everything might feel new and different. How are you feeling about everything so far? Any specific areas where you’re feeling like you could use a bit of help or extra advice?"}
            ]
            st.success("Chat history cleared.")
            st.experimental_rerun()

    # Display chat messages
    for message in st.session_state.chat_histories[current_user]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for user to type messages
    if user_input := st.chat_input("Enter your query here:"):
        st.session_state.chat_histories[current_user].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process the user input with the chatbot
        response, map_html, intent = chat_all(
            st.session_state.chat,
            st.session_state.prompts_dict,
            user_input,
            st.session_state.neighborhoods_info,
            st.session_state.neighborhoods_boundaries,
            st.session_state.vectordb,
        )

        print(map_html)

        # Display the chatbot's response
        with st.chat_message("assistant"):
            placeholder = st.empty()
            gradual_text = ""

            with st.spinner("Thinking..."):
                for word in response.split():
                    gradual_text += word + " "
                    placeholder.markdown(gradual_text)
                    time.sleep(0.05)

        # Add the response to chat history
        st.session_state.chat_histories[current_user].append({"role": "assistant", "content": response})

        # Update the map if needed
        if map_html and map_html != st.session_state.current_map_html:
            st.session_state.current_map_html = map_html

# Main app logic to control flow between login, sign-up, and chat pages
if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_page()
    else:
        login_page()
else:
    chat_app()
