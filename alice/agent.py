import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from config import load_config, ALICE_HOME
from autogen_ext.models.cache import ChatCompletionCache
from autogen_ext.cache_store.diskcache import DiskCacheStore
from diskcache import Cache

# Load configuration
config = load_config()

model_info = ModelInfo(
    vision=False,
    function_calling=True,
    json_output=False,
    structured_output=False,
    family="unknown"
)

if not config.get("ALICE_API_KEY"):
    raise ValueError("Please set ALICE_API_KEY in ~/.alice/.env or environment variables")

openai_model_client = OpenAIChatCompletionClient(
    model=config["ALICE_MODEL"],
    api_key=config["ALICE_API_KEY"],
    base_url=config["ALICE_BASE_URL"],
    model_info=model_info
)

if config.get("ALICE_PERSISTENT_MODE"):
    cache_size_bytes = config["ALICE_CACHE_SIZE"] * 1024 * 1024
    cache_store = DiskCacheStore(Cache(ALICE_HOME, size_limit=cache_size_bytes))
    planning_model_client = ChatCompletionCache(openai_model_client, cache_store)
else:
    planning_model_client = openai_model_client

planning_agent = AssistantAgent(
    "PlanningAgent",
    description="An agent for planning command line, this agent should be the first to engage when given a new task.",
    model_client=planning_model_client,
    system_message=f"""
    You are a planning agent.
    Your job is to translate the command you receive into a command line for your {config["ALICE_DEVICE_TYPE"]} desktop.
    Break down complex tasks into simple steps (max 5 words per step).
    You only plan, you don't execute command.
    Ensure steps are clear, concise and follow the 5-word limit.
    Only provide markdown-encoded code block (```sh) for final result, i.e., there is only 1 code snippet.
    You must respond in {config["ALICE_LANGUAGE"]} language.
    """
)

if config.get("ALICE_INTERACTIVE_MODE"):
    def input_with_terminate_hint(prompt):
        return input("Please enter your response (end with 'TERMINATE' if correct): ")
    verification_agent = UserProxyAgent(
        "VerificationAgent",
        input_func=input_with_terminate_hint,
        description="A human-in-the-loop agent for verifying the command line."
    )
else:
    verification_agent = AssistantAgent(
        "VerificationAgent",
        description="An agent for verifying the command line, this agent should be the second to engage when given a new task.",
        model_client=openai_model_client,
        system_message=f"""
        You are a verification agent.
        Your job is to verify the execution result, and judge the result is reasonable or not.
        You must respond in {config["ALICE_LANGUAGE"]} language.
        Only if the result format is correct then summarize it and end with "TERMINATE".
        Otherwise, provide your reason and reject the result.
        Note, you have to use fewer than 10 words to response.
        Note2, don't make too many assumptions, as long as the command makes sense and the result is formatted correctly.
        """
    )

execution_agent = CodeExecutorAgent(
    "ExecutionAgent",
    code_executor=LocalCommandLineCodeExecutor(work_dir=os.getcwd()),
    description="An agent for executing command line."
)