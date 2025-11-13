from langgraph.graph import END,StateGraph,START
from typing_extensions import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from app.helper import dynamic_prompt_inducer
import zipfile
import tempfile
from langchain.messages import SystemMessage, HumanMessage
import os, json
from loguru import logger
import operator




class GraphState(TypedDict):
    repo_path: str
    files_list: list[str]
    chunks_with_metadata: dict
    documentation: str
    file_documentation: str
    personas: str
    final_documentation: str
    dynamic_prompt: str

model = ChatOpenAI(model='gpt-5')

def load_repo(state: GraphState) -> GraphState:
    file_contents = {}
    with tempfile.TemporaryDirectory() as tempdir:
        with zipfile.ZipFile(state["repo_path"], 'r') as zip_ref:
            zip_ref.extractall(tempdir)
        extracted_files = []
        for root, dirs, files in os.walk(tempdir):
            for f in files:
                    file_path = os.path.join(root, f)
                    extracted_files.append(file_path)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        file_contents[file_path] = infile.read()
        state["files_list"] = extracted_files
        state["chunks_with_metadata"] = file_contents
        logger.info(state["files_list"])
        logger.info(state["chunks_with_metadata"])
        return state


def structure_analyzer(state: GraphState) -> GraphState:
    response = model.invoke(
        [
            SystemMessage(content = "You are world class project structure analyzer and document expert.Analyze the repo structure and deliver some documentation")
        ]
        + state["files_list"]

    )
    logger.info(response)
    state["file_documentation"] = response.content
    return state

def role_based_project_analyzer(state: GraphState) -> GraphState:
    response = model.invoke(
        [
            SystemMessage(content = f"you are world class Code Analyser.Understand the data of the different files and find the best analyzations and provide the documention for the role {state["personas"]}")
        ] +
        [HumanMessage(content=chunk) for chunk in state["chunks_with_metadata"].values()]

    )
    logger.info(response.content)
    state["documentation"] = response.content
    return state




def final_documenter(state: GraphState) -> GraphState:
    final_prompt = dynamic_prompt_inducer(state["personas"])
    messages = [
        SystemMessage(
            content=final_prompt
        ),
        HumanMessage(
            content=f"Here is the structure analyser documentation: {state['file_documentation']}"
        ),
        HumanMessage(
            content=f"Here is the project analyser documentation: {state['documentation']}"
        )
    ]
    response = model.invoke(messages)
    logger.info(response.content)
    state["final_documentation"] = response.content
    return state

graph = StateGraph(GraphState)

graph.add_node('load_repo', load_repo)
graph.add_node('structure_analyzer', structure_analyzer)
graph.add_node("final_documenter", final_documenter)
graph.add_node('role_based_project_analyzer', role_based_project_analyzer)


graph.add_edge(START, 'load_repo')
graph.add_edge("load_repo", 'structure_analyzer')
graph.add_edge("structure_analyzer", 'role_based_project_analyzer')
graph.add_edge('role_based_project_analyzer', 'final_documenter')
graph.add_edge("final_documenter", END)

final_graph = graph.compile()
