from typing import Any, List, AsyncIterator, Iterator
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough, RunnableParallel, RunnableBranch
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Runnable의 핵심 메스드들(개념적 표현)
class RunnableInterface:
    def invoke(self, input: Any) -> Any:
        """동기적으로 실행"""
        pass

    async def ainvoke(self, input: Any) -> Any:
        """비동기적으로 실행"""
        pass

    def stream(self, input: Any) -> Iterator[Any]:
        """스트리밍 방식으로 실행"""
        pass

    async def astream(self, input: Any) -> AsyncIterator[Any]:
        """비동기 스트리밍 방식으로 실행"""
        pass

    def batch(self, inputs: List[Any]) -> List[Any]:
        """여러 입력을 배치로 처리"""
        pass

########################################################################
######################### 일반 함수를 Runnable로 변환 ###################
########################################################################

def add_exclamation(text: str) -> str:
    """텍스트 끝에 느낌표를 추가하는 함수"""
    return f"{text}!"

# 1. RunnableLambda로 감싸서 Runnable로 만들기
exclamation_runnable = RunnableLambda(add_exclamation)

# 2. 다양한 방식으로 실행 가능
result = exclamation_runnable.invoke("안녕하세요")
print(result)

# 3. 배치 처리도 자동으로 지원
results = exclamation_runnable.batch(["안녕", "반가워", "좋은 아침"])
print(results)


########################################################################
####################### 프롬프트 -> 모델 -> parser 예제 #################
########################################################################

prompt = ChatPromptTemplate.from_template(
    "주어지는 문구에 대하여 50자 이내의 짧은 시를 작성: {word}"
)
model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

# 1. LCEL로 체인 구성
chain = prompt | model | parser

# 2. 실행
result = chain.invoke({"word": "평범한 일상"})
print(result)


########################################################################
######################### Runnable 주요 타입들 #########################
########################################################################

prompt = ChatPromptTemplate.from_template(
    "주어진 '{word}'와 유사한 단어 3가지를 나열해주세요. 단어만 나열합니다."
)
model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

# 1. 병렬 처리 체인 구성
chain = RunnableParallel(
    {
        "original": RunnablePassthrough(), # 2. 원본 데이터 보존
        "processed": prompt | model | parser # 3. 처리된 데이터
    }
)

result = chain.invoke({"word": "행복"})
print(result)

########################################################################
####################### RunnableLambda 사용 예제 #######################
########################################################################

prompt = ChatPromptTemplate.from_template(
    "주어진 '{word}'와 유사한 단어 3가지를 나열해주세요. 단어만 나열합니다."
)
model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

# 1. 여러 분석을 동시에 수행
analysis_chain = RunnableParallel(
    synonyms = prompt | model | parser,
    word_count = RunnableLambda(lambda x: len(x["word"])),
    uppercase = RunnableLambda(lambda x: x["word"].upper()),
)

result = analysis_chain.invoke({"word": "peaceful"})
print(result)

########################################################################
####################### RunnableBranch 사용 예제 #######################
########################################################################

model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

# 1. 입력된 텍스트가 영어인지 확인하는 함수
def is_english(x:dict) -> bool:
    """
    입력 딕셔너리의 'word' 키에 해당하는 값이 영어인지 확인
    모든 문자가 ASCII 범위 (128미만)에 있으면 영어로 간주
    """
    return all(ord(char)<128 for char in x["word"])

# 2. 영어 단어에 대한 프롬프트 템플릿입니다.
english_prompt = ChatPromptTemplate.from_template(
    "Give me 3 synonyms for {word}. Only list the words"
)

# 3. 한국어 단어에 대한 프롬프트 템플릿입니다.
korean_prompt = ChatPromptTemplate.from_template(
    "주어진 '{word}'와 유사한 단어 3가지를 나열. 단어만 나열."
)

# 4. 조건부 분기를 정의
# is_english 함수가 True를 반환하면 english_prompt를, 그렇지 않으면 korean_prompt를 사용
language_aware_chain = RunnableBranch(
    (is_english, english_prompt | model | parser), # 조건이 참일때 실행될 체임
    korean_prompt | model | parser, # 기본값 (조건이 거짓일때 실행될 체인)
)

# 영어단어 예시
english_word = {"word": "happy"}
english_result = language_aware_chain.invoke(english_word)
print(f"Synonyms for '{english_word['word']}': \n{english_result}\n")

# 한국어 단어 예시
korean_word = {"word": "행복"}
korean_result = language_aware_chain.invoke(korean_word)
print(f"Synonyms for '{korean_word['word']}': \n{korean_result}\n")