import os
import json
import uuid
from loguru import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DB_FILE = os.path.join(BASE_DIR, "userdetails", "projects.json")
USER_DB_FILE = os.path.join(BASE_DIR, "userdetails", "users.json")
PROMPTS_FILE = os.path.join(BASE_DIR, "prompts.json")

async def load_users() -> dict:
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, "r") as f:
        try:
            logger.info(f"Loading users from {USER_DB_FILE}")
            return json.load(f)
        except Exception:
            return {}

async def load_projects():
    if not os.path.exists(PROJECT_DB_FILE):
        return {}
    with open(PROJECT_DB_FILE, "r") as f:
        try:
            logger.info(f"Loading projects from {PROJECT_DB_FILE}")
            return json.load(f)
        except Exception:
            return {}



async def add_project(user: str, filename: str, file_bytes: bytes):
    logger.info(f"Adding project to {user}")
    projects = await load_projects()
    user_projects = projects.get(user, {})
    pid = str(uuid.uuid4())
    os.makedirs("uploads", exist_ok=True)
    path = os.path.join("uploads", filename)
    with open(path, "wb") as f:
        f.write(file_bytes)
    user_projects[pid] = {"file": filename, "path": path}
    projects[user] = user_projects
    await save_projects(projects)
    return pid, path

async def save_users(users: dict):
    logger.info(f"Saving users to {USER_DB_FILE}")
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

async def save_projects(data: dict):
    logger.info(f"Saving projects to {PROJECT_DB_FILE}")
    with open(PROJECT_DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


async def get_user_projects(user: str):
    projects = await load_projects()
    logger.info(f"Loading projects from {PROJECT_DB_FILE}")
    return projects.get(user, {})

def dynamic_prompt_inducer(value):
    with open(PROMPTS_FILE, 'r') as f:
        json_data = json.load(f)
    if value == "SDE":
        prompt = json_data["SDE_PROMPT"]
    else:
        prompt = json_data["PM_PROMPT"]
    logger.info(f"Prompt: {prompt}")
    return prompt

if __name__ == "__main__":
    dynamic_prompt_inducer("SDE")