import asyncio
import os

from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def call_async_openai(prompt:str, model:str = "gpt-5-mini") -> str:
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role":"user", "content":prompt}]
    )
    return response.choices[0].message.content

async def call_async_claude(prompt: str, model: str = "claude-3-5-haiku-latest") -> str:
    """claude api key 없는 관계로 중간 코드는 생략"""
    return response.content[0].text

async def main():
    print("동시에 API 호출하기")
    prompt = "비동기 프로그래밍에 대해 2~3문장으로 설명"
    openai_task = call_async_openai(prompt)
    claude_task = call_async_claude(prompt)

    openai_response, claude_response = await asyncio.gather(openai_task, claude_task)
    print(f"OpenAI 응답: {openai_response}")
    print(f"Claude 응답: {claude_response}")

if __name__=="__main__":
    # await main() 안쓰는 이유:
    # await는 함수 내에서만 사용 가능
    asyncio.run(main())