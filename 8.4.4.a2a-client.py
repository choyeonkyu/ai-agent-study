import asyncio
from uuid import uuid4
from typing import Any, Optional

import httpx

from a2a.client import A2ACardResolver
from a2a.client.client_factory import ClientFactory
from a2a.client.client import ClientConfig
from a2a.types import Message, SendMessageRequest, MessageSendParams
from a2a.utils import get_message_text


def create_user_message(text: str, message_id: Optional[str] = None) -> Message:
    """A2A 사용자 메시지 생성 함수."""
    return Message(
        role="user",
        parts=[{"kind": "text", "text": text}],
        messageId=message_id or uuid4().hex,
    )

async def test_basic_agent():
        """Hello World A2A Agent Test Function"""
        base_url = "http://localhost:9999"
        print("Basic Hello World A2A Agent 테스트 Start")
        print(f"Server URL: {base_url}")
        print("-"*50)

        timeout = httpx.Timeout(30.0, connect=10.0) 
        async with httpx.AsyncClient(timeout=timeout) as httpx_client:
            try:
                # 1. A2A Card Resolver: 에이전트의 카드 정보를 가져오는 역할
                resolver = A2ACardResolver(
                     httpx_client=httpx_client,
                     base_url=base_url
                )

                # 2. Pull Agent Card
                print("에이전트 카드를 가져오는 중...")
                agent_card = await resolver.get_agent_card() # 실제로 agent card 가져오는 부분
                print(f"Agent Name: {agent_card.name}")
                print(f"Agent Description: {agent_card.description}")
                print(f"Skill: {[skill.name for skill in agent_card.skills]}")
                print()

                # 3. A2A Client
                non_streaming_config = ClientConfig(httpx_client=httpx_client,
                                                    streaming=False)
                non_streaming_factory = ClientFactory(non_streaming_config)
                non_streaming_client = non_streaming_factory.create(agent_card)

                streaming_config = ClientConfig(httpx_client=httpx_client,
                                                    streaming=False)
                streaming_factory = ClientFactory(streaming_config)
                streaming_client = streaming_factory.create(agent_card)

                # 4. Test Message Lists
                test_messages = [
                     "안녕하세요",
                     "날씨가 어때요?",
                     "고마워요",
                     "이름이 뭔가요?",
                     "오늘 기분이 어때요?",
                ]

                # 5. Non-Streaming Message Test
                print("===비스트리밍 메시지 테스트===")
                for i, message_text in enumerate(test_messages, 1):
                    print(f"\n{i}. 사용자: {message_text}")

                    # 6. 사용자 메시지 생성
                    user_message = create_user_message(message_text)
                    request = SendMessageRequest(
                         id=str(uuid4()), params=MessageSendParams(message=user_message)
                    )

                    # 7. Send Non-streaming Message
                    async for event in non_streaming_client.send_message(user_message):
                        if isinstance(event, Message):
                            response_text = get_message_text(event)
                            print(response_text)
                            break
                print("\n" + "="*50)

                # 8. Streaming Message Test
                print("===스트리밍 메시지 테스트===")
                for i, message_text in enumerate(test_messages[:3], 1):
                    print(f"\n{i}. 사용자: {message_text}")

                    # 9. 사용자 메시지 생성
                    user_message = create_user_message(message_text)

                    # 10. 스트리밍 메시지 전송
                    print("    에이전트 (스트리밍): ", end="", flush=True)
                    async for event in streaming_client.send_message(user_message):
                        if isinstance(event, Message):
                            response_text = get_message_text(event)
                            print(response_text, end="", flush=True)
                    print()
                print("\n Test Done!")

            except Exception as e:
                print(f"테스트 중 오류 발생: {e}")
                print("서버가 실행 중인지 확인해주세요.")
                print("서버 실행: python basic_agent/__main__.py")


async def main():
    """Main function to run the test."""
    await test_basic_agent()


if __name__ == "__main__":
    asyncio.run(main())
