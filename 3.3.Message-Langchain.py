from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatOpenAI(model= "gpt-5-mini")
messages = [
    SystemMessage(content="당신은 사용자의 질문에 간결하고 명확하게 답변하는 AI 도우미 입니다."),
    HumanMessage(content="LangChain에 대해 설명해줘"),
    AIMessage(content="LangChain은 대규모 언어모델 LLM을 활용하여 애플리케이션을 구축하기 위한 프레임워크입니다."),
    HumanMessage(content= "주요 기능 3가지만 알려줘")
]
result = chat_model.invoke(messages)
print("AI의 응답: ", result.content)