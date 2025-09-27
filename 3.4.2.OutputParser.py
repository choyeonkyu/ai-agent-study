from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatOpenAI(model="gpt-4.1-mini")
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 까칠한 AI 도우미입니다. 사용자의 질문에 최대 3줄로 답하세요."),
        ("human", "{question}")
    ]
)
string_output_parser = StrOutputParser()
result: AIMessage = chat_model.invoke(
    chat_prompt_template.format_messages(
        question = "파이썬에서 리스트를 정렬하는 방법은?"
    )
)
parsed_result: str = string_output_parser.parse(result)
print(parsed_result.content)

print("-------------------------------------------------------------")
chain = chat_prompt_template | chat_model | string_output_parser
print(type(chain))

result = chain.invoke({"question": "파이썬에서 딕셔너리를 정렬하는 방법은?"})
print(type(result))
print(result)

print("-------------------------------------------------------------")

llm = init_chat_model("gpt-5-mini", model_provider="openai")
class MovieReview(BaseModel):
    """1. 영화 리뷰 스키마 정의"""
    title: str = Field(description="영화 제목")
    rating: float = Field(description="10점 만점 평점 (예 : 7.2)")
    review: str = Field(description="한글 리뷰 (3~4문장)")
# 2. 모델에 스키마를 바인딩
structured_llm = llm.with_structured_output(MovieReview)
result: MovieReview = structured_llm.invoke(
    "영화 '기생충'에 대한 리뷰를 작성해줘"
)
print(result.title)
print(result.rating)
print(result.review)