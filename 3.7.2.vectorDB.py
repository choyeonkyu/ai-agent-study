from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# 임베딩 모델 초기화
embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")

# 1. 샘플 텍스트 데이터
texts = [
    "파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
    "자바스크립트는 웹 개발에 널리 사용됩니다.",
    "꽁꽁 얼어붙은 한강위로 고양이가 걸어갑니다.",
    "어리석은 자는 멀리서 행복을 찾고, 현명한 자는 자신의 발치에서 행복을 키워간다.",
    "계단을 밟아야 계단 위에 올라설수 있다",
    "인생은 10%의 사건과 90%의 반응으로 이루어져 있습니다.",
    "성공은 실패를 거듭하는 것이 아니라, 실패를 거듭하면서도 열정을 잃지 않는 것입니다.",
    "하루에 3시간을 걸으면 7년 후에 지구를 한바퀴 돌 수 있습니다.",
    "인공지능은 머신러닝과 딥러닝을 통해 발전하고 있습니다.",
]

# 2. 텍스트를 벡터로 변환하고 FAISS 벡터 스토어에 저장
vectorstore = FAISS.from_texts(texts, embeddings)

# 3. 유사한 문서 검색
query = "힘이 나는 명언 알려주세요."
docs = vectorstore.similarity_search(query, k=2)

# 4. 검색결과 출력
print("검색 결과 : ")
for i , doc in enumerate(docs):
    print(f"{i+1}. {doc.page_content}")

#####################################################################################
######################## Document 객체 사용하여 Metadata 활용 ########################
#####################################################################################

embeddings = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(separator=".", chunk_size=50, chunk_overlap=20)

documents = [
    Document(
        page_content="파이썬은 읽기 쉽고 배우기 쉬운 프로그래밍 언어입니다. "
        "다양한 분야에서 활용되며, 특히 데이터 과학과 AI 개발에 인기가 높습니다.",
        metadata={"source": "python_intro.txt", "topic": "programming"},
    ),
    Document(
        page_content="자바스크립트는 웹 브라우저에서 실행되는 프로그래밍 언어로 시작했지만, "
        "현재는 서버 사이드 개발에도 널리 사용됩니다. Node.js가 대표적입니다.",
        metadata={"source": "js_guide.txt", "topic": "programming"},
    ),
    Document(
        page_content="머신러닝은 데이터에서 패턴을 학습하는 AI의 한 분야입니다. "
        "지도학습, 비지도학습, 강화학습 등 다양한 방법론이 있습니다.",
        metadata={"source": "ml_basics.txt", "topic": "ai"},
    ),
]

split_docs = text_splitter.split_documents(documents)
for doc in split_docs:
    print(f"문서: {doc.page_content[:50]}... | 출처: {doc.metadata['source']} | 주제: {doc.metadata['topic']}")

vectorstore = FAISS.from_documents(split_docs, embeddings)

query = "초보자가 배우기 좋은 프로그래밍 언어는?"
results = vectorstore.similarity_search(query, k=2)

print(f"질문: {query}\n")
print("검색 결과 : ")
for i, doc in enumerate(results, 1):
    print(f"\n{i}. {doc.page_content[:100]}...")
    print(f"   출처: {doc.metadata['source']}")
    print(f"   주제: {doc.metadata['topic']}")

# 유사도 점수와 함께 검색: FAISS에서는 코사인 유사도와 다르게 0에 가까울수록 유사함
results_with_scores = vectorstore.similarity_search_with_score(query, k=2)
print("\n\n유사도 점수:")
for doc, score in results_with_scores:
    print(f"- {doc.metadata['source']}: {score:.3f}")