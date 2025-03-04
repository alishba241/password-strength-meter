import re
import random
import string
import streamlit as st
from collections import defaultdict

#custom design
st.markdown(
    """
    <style>
    body {
background: linear-gradient(to right, #ff7b8f, #fcb0d4);

        color: white;
    }
    .stApp {
background: linear-gradient(to right, #ff7b8f, #fcb0d4);

    }
     h1, .stRadio label {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

password_usage = defaultdict(int)  

def check_password_strength(password):
    score = 0
    feedback = []
    
    # password criteria check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter.")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    # track password usage
    password_usage[password] += 1
    if password_usage[password] > 3:  # too common if enetered more tha 3 times
        return "Weak", "This password is too common. Choose a stronger one."
    
    # Strength feedback
    if score <= 2:
        return "Weak", feedback
    elif score <= 4:
        return "Moderate", feedback
    else:
        return "Strong", "Great! Your password is strong."

def generate_strong_password(length=12):
    while True:
        password = (
            random.choice(string.ascii_uppercase) +
            random.choice(string.ascii_lowercase) +
            random.choice(string.digits) +
            random.choice("!@#$%^&*") +
            ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length - 4))
        )
        
        if (re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and
            re.search(r"\d", password) and re.search(r"[!@#$%^&*]", password)):
            return password


st.markdown("<h1 style='text-align: center; color: white;'>🔐 Password Strength Meter</h1>", unsafe_allow_html=True)

password = st.text_input("Enter a password to check its strength:", type="password")

page = st.radio("Select an option:",
                 ["Check Password Strength", "Generate Strong Password", "Password History"]
                 )

password_history = st.session_state.get("password_history", [])

if page == "Check Password Strength" and password:
    strength, feedback = check_password_strength(password)
    st.subheader(f"Password Strength: {strength}")
    
    # save password history
    password_history.append((password, strength))
    st.session_state["password_history"] = password_history
    
    if strength != "Strong":
        st.warning("Feedback to improve:")
        if isinstance(feedback, list):
            for tip in feedback:
                st.write(f"- {tip}")
        else:
            st.write(feedback)

elif page == "Generate Strong Password":
    st.subheader("🔑 Suggested Strong Password:")
    st.code(generate_strong_password(), language='python')

elif page == "Password History":
    st.subheader("📜 Password History")
    if password_history:
        for pw, status in password_history:
            st.write(f"**{pw}** - {status}")
    else:
        st.write("No password history available.")
