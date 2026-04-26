"""
Login and authentication system for AquaForge
Provides secure admin login with session management
"""

import streamlit as st
from typing import Tuple


# Default admin credentials
ADMIN_USERS = {
    "admin": "AquaForge@2026",
    "engineer": "Design@AWH2026",
}


def init_login_session():
    """Initialize login session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0


def verify_credentials(username: str, password: str) -> bool:
    """
    Verify username and password against admin credentials
    
    Args:
        username: Username to verify
        password: Password to verify
    
    Returns:
        True if credentials are valid, False otherwise
    """
    if username in ADMIN_USERS and ADMIN_USERS[username] == password:
        return True
    return False


def render_login_page():
    """
    Render the login page with authentication form
    Returns True if user is authenticated, False otherwise
    """
    init_login_session()
    
    # If already logged in, return True
    if st.session_state.logged_in:
        return True
    
    # Login page
    st.set_page_config(
        page_title="AquaForge Login",
        page_icon="💧",
        layout="centered",
    )
    
    # Login UI
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <style>
            .login-title {
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #1f77b4;
            }
            .login-subtitle {
                text-align: center;
                font-size: 16px;
                color: #666;
                margin-bottom: 30px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<div class="login-title">💧 AquaForge</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="login-subtitle">Engineer Water from Air</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        
        st.markdown("### 🔐 Admin Login")
        
        # Login form
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        # Attempt counter display
        if st.session_state.login_attempts > 0:
            st.warning(f"⚠️ {st.session_state.login_attempts} failed login attempt(s)")
        
        if st.button("🔓 Login", use_container_width=True, key="login_button"):
            if verify_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.login_attempts = 0
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                st.error("❌ Invalid username or password")
                if st.session_state.login_attempts >= 3:
                    st.warning("⚠️ Too many failed attempts. Please try again later.")
    
    return False


def render_logout_button():
    """Render logout button in sidebar"""
    if st.session_state.logged_in:
        col1, col2, col3 = st.sidebar.columns([1, 1, 1])
        with col2:
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.login_attempts = 0
                st.rerun()
        
        st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.username}**")
        st.sidebar.markdown("---")


def check_authentication() -> bool:
    """
    Check if user is authenticated. Shows login page if not.
    
    Returns:
        True if authenticated, False otherwise
    """
    init_login_session()
    
    if not st.session_state.logged_in:
        render_login_page()
        return False
    
    return True
