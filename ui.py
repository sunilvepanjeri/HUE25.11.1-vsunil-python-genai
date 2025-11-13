import streamlit as st
import requests
import asyncio
from settings import settings
from app.helper import add_project, get_user_projects
from app.graph import GraphState, final_graph

API = settings.API_URL


async def tab_caller():
    page = st.selectbox("Choose Option", ["Login", "Signup"])

    if page == "Login":
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            data = requests.post(f"{API}/auth/login", json={"username": username, "password": password}).json()
            st.info(data["message"])
            if data["value"]:
                st.session_state.login_success = True
                st.session_state.user = username
    if page == "Signup":
        username = st.text_input("New Username", key="signup_user")
        password = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup"):
            data = requests.post(f"{API}/auth/signup", json={"username": username, "password": password}).json()
            st.info(data["message"])
            if data["value"]:
                st.session_state.user = username


async def main():
    st.set_page_config(page_title="Multi-Agent Code Analysis & Documentation System", layout="wide")

    if "user" not in st.session_state:
        st.session_state.user = None
    if "login_success" not in st.session_state:
        st.session_state.login_success = None


    if st.session_state.login_success is None:
        await tab_caller()
    if st.session_state.login_success:
        st.sidebar.success(f"Logged in as {st.session_state.user}")
        uploaded = st.file_uploader("Upload Project ZIP", type=["zip"])
        if uploaded:
            if st.button("Create Project"):
                pid, path = await add_project(st.session_state.user, uploaded.name, uploaded.read())
                st.success(f"Project created: {pid}")

        projects = await get_user_projects(st.session_state.user)
        if projects:
            selected_pid = st.selectbox("Select Project", list(projects.keys()))
            personas = st.selectbox("Select Persona", ["SDE", "PM"])
            if st.button("Start Analysis"):
                st.success(f"Analysing Project {selected_pid}")
                agent_img = final_graph.get_graph(xray=True).draw_mermaid_png()

                st.image(agent_img, caption="Meramaid Image", use_container_width=True)

                state: GraphState = {
                    "repo_path": projects.get(selected_pid).get("path"),
                    "personas": personas
                }
                graph = final_graph.invoke(state)
                if personas == "SDE":
                    st.subheader("SDE Report")
                    st.markdown(graph["documentation"])
                else:
                    st.subheader("PM Report")
                    st.markdown(graph["documentation"])
        if st.button("Logout"):
            st.session_state.user = None


if __name__ == "__main__":
    asyncio.run(main())

