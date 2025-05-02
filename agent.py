import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from config import load_config

# 載入設定
config = load_config()

model_info = ModelInfo(
    vision=False,
    function_calling=True,
    json_output=False,
    structured_output=False,
    family="unknown"
)

if not config.get("ALICE_API_KEY"):
    raise ValueError("請在 ~/.alice/.env 或環境變數中設定 ALICE_API_KEY")

model_client = OpenAIChatCompletionClient(
    model=config["ALICE_MODEL"],
    api_key=config["ALICE_API_KEY"],
    base_url=config["ALICE_BASE_URL"],
    model_info=model_info
)

planning_agent = AssistantAgent(
    "PlanningAgent",
    description="An agent for planning command line, this agent should be the first to engage when given a new task.",
    model_client=model_client,
    system_message="""
    You are a planning agent.
    Your job is to translate the command you receive into a command line for your mac desktop.
    Break down complex tasks into simple steps (max 5 words per step).
    You only plan, you don't execute commands.
    Ensure steps are clear, concise and follow the 5-word limit.
    Only provide markdown-encoded code blocks (```sh) for final result, i.e., there is only 1 code snippet.
    """
)

verification_agent = AssistantAgent(
    "VerificationAgent",
    description="An agent for verifying the command line, this agent should be the second to engage when given a new task.",
    model_client=model_client,
    system_message="""
    You are a verification agent.
    Your job is to verify the execution result, and judge the result is reasonable or not.
    Only if the result format is correct then summarize it and end with "TERMINATE".
    Otherwise, provide your reason and reject the result.
    Note, you have to use fewer than 10 words to response.
    Note2, Don't make too many assumptions, as long as the commands make sense and the results are formatted correctly.
    """
)

execution_agent = CodeExecutorAgent(
    "ExecutionAgent",
    code_executor=LocalCommandLineCodeExecutor(work_dir=os.getcwd()),
    description="An agent for executing command line."
)