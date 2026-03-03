import asyncio
from core.runner import run_task_stream

async def main():
    result = await run_task_stream("Give me an example of a program that counts the number of vowels in any string.")
    print(result)

asyncio.run(main())