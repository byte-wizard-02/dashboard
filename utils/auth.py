import streamlit as st

# Simple user-role database
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "sales1": {"password": "sales123", "role": "Sales"},
    "hr1": {"password": "hr123", "role": "HR"},
    "marketing1": {"password": "marketing123", "role": "Marketing"},
    "exec1": {"password": "exec123", "role": "Executive Office"},
}

def get_user_role_and_section():
    # Initial login handler
    if not st.session_state.get("logged_in"):
        st.title("🔐 Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            user = USERS.get(username)
            if user and password == user["password"]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = user["role"]
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

        st.stop()

    role = st.session_state["role"]

    with st.sidebar:
        st.markdown(f"👋 Logged in as `{st.session_state['username']}`")
        st.markdown(f"🔐 Role: **{role}**")

        # Admin can choose any department; others are hardcoded to their own
        if role == "Admin":
            section = st.radio("📁 Select Department", [
                "Sales", "HR", "Marketing", "Executive Office"
            ])
        else:
            section = role  # Lock to assigned department

        if st.button("🚪 Logout"):
            for k in ["logged_in", "username", "role"]:
                st.session_state.pop(k, None)
            st.rerun()

    return role, section
