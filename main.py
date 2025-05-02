import os
import glob
import asyncio
import aiofiles.os
from agent import planning_agent, verification_agent, execution_agent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

text_mention_termination = TextMentionTermination("TERMINATE")
max_message_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_message_termination

team = RoundRobinGroupChat([planning_agent, execution_agent, verification_agent], termination_condition=termination)

async def async_delete(pattern):
    loop = asyncio.get_running_loop()
    files = await loop.run_in_executor(None, glob.glob, pattern)
    print(files)
    for file_path in files:
        print(f"removing {file_path}")
        await aiofiles.os.remove(file_path)

async def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py <task>")
            print("範例: python main.py 找出當下目錄最大的檔案")
            return
        task = " ".join(sys.argv[1:])
        await Console(team.run_stream(task=task))
    finally:
        await async_delete("tmp_code_*.sh")

if __name__ == "__main__":
    import asyncio
    import sys
    asyncio.run(main())