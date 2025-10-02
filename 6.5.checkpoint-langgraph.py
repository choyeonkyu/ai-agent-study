from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
from dotenv import load_dotenv

load_dotenv()

# 1. 그래프 상태 정의
class MemoryBotState(BaseModel):
    user_message: str = Field(default="", description="사용자 입력 메시지")
    user_name: str = Field(default="", description="사용자 이름")
    user_preferences: Dict[str, Any] = Field(
        default_factory=dict, description="사용자 선호도")
    response: str = Field(default="", description="최종 응답")

llm = ChatOpenAI(model="gpt-5-mini")

# 2. 메시지 처리 노드 - 메모리 로드/저장 로직 제거
def process_message(state: MemoryBotState) -> Dict[str, Any]:
    message = state.user_message
    user_name = state.user_name
    preferences = state.user_preferences.copy()
    
    # 시스템 프롬프트
    system_prompt = f"""
당신은 사용자의 정보를 기억하는 메모리 봇입니다.
현재 기억하고 있는 정보:
- 사용자 이름: {user_name if user_name else "모름"}
- 좋아하는 것: {preferences.get("likes", [])}
- 싫어하는 것: {preferences.get("dislikes", [])}

사용자 메시지를 분석하여 다음 JSON 형태로 응답하세요:
{{
  "response": "사용자에게 줄 응답 메시지",
  "new_name": "새로 알게 된 이름 (없으면 null)",
  "new_likes": ["새로 알게 된 좋아하는 것들"],
  "new_dislikes": ["새로 알게 된 싫어하는 것들"]
}}
"""
    
    messages = [SystemMessage(content=system_prompt),
                HumanMessage(content=message)]
    response = llm.invoke(messages)
    result = json.loads(response.content)

    # 새로운 정보 업데이트
    if result.get("new_name"):
        user_name = result["new_name"]

    if result.get("new_likes"):
        preferences.setdefault("likes", []).extend(result["new_likes"])

    if result.get("new_dislikes"):
        preferences.setdefault("dislikes", []).extend(result["new_dislikes"])

    bot_response = result.get("response", "죄송해요, 이해하지 못했어요.")

    return {
        "response": bot_response,
        "user_name": user_name,
        "user_preferences": preferences,  
    }

# 3. 메모리 봇 그래프 생성 - InMemorySaver 통합
def create_memory_bot_graph():
    # 4. InMemorySaver로 자동 메모리 관리
    checkpointer = InMemorySaver()
    workflow = StateGraph(MemoryBotState)

    # 5. 단일 노드 구조
    workflow.add_node("process_message", process_message)

    # 6. 단순한 워크 플로우: START -> process_message -> END
    workflow.add_edge(START, "process_message")
    workflow.add_edge("process_message", END)

    # 7. checkpointer와 함께 컴파일
    return workflow.compile(checkpointer=checkpointer)

def main():
    print("=== InMemorySaver 메모리 봇 테스트 ===\n")
    app = create_memory_bot_graph()
    thread_id = "yeonkyu_124"

    # 테스트 대화
    conversations = [
        "안녕하세요!",
        "내 이름은 연규야",
        "회를 좋아해",
        "멍게는 별로 안좋아해",
        "내 이름이 뭐였지?",
        "내가 좋아하는 것과 싫어하는 것은?",
    ]

    for i, message in enumerate(conversations, 1):
        print(f"[{i}] 사용자: {message}")
        
        # 8. InMemorySaver 사용 시 config 설정
        config = {"configurable": {"thread_id": thread_id}}
        result = app.invoke({"user_message": message}, config)

        print(f"[{i}] 챗봇: {result['response']}")
        print(
            f"메모리: 이름={result.get('user_name', '없음')}"
            f"좋아하는 것={result.get('user_preferences',{})}\n"
        )

if __name__=="__main__":
    main()