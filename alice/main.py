import sys
import glob
import asyncio
import aiofiles.os
from agent import planning_agent, verification_agent, execution_agent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from log import setup_logging
from config import current_config

# 初始化專案專用logger
logger = setup_logging()

text_mention_termination = TextMentionTermination("TERMINATE")
max_message_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_message_termination

team = RoundRobinGroupChat([planning_agent, execution_agent, verification_agent], termination_condition=termination)

async def async_delete(pattern):
    loop = asyncio.get_running_loop()
    file_list = await loop.run_in_executor(None, glob.glob, pattern)
    logger.debug(f"Found files:  {file_list}")
    if file_list:
        logger.debug(f"Removing {len(file_list)} files")
        await asyncio.gather(*[aiofiles.os.remove(file_path) for file_path in file_list])

async def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py <task>")
            print("範例: python main.py 找出當下目錄最大的檔案")
            return
        task = " ".join(sys.argv[1:])

        silent_mode = current_config["ALICE_SILENT_MODE"]
        if not silent_mode:
            await Console(team.run_stream(task=task))
        else:
            ret = await team.run(task=task)
            final_msg = ret.messages[-1].content
            if "TERMINATE" in final_msg:
                command_result = ret.messages[-2].content
                print(command_result)
            else:
                print("Something went wrong!")
    finally:
        await async_delete("tmp_code_*.sh")

if __name__ == "__main__":
    asyncio.run(main())