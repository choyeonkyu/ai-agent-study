from langchain_openai import OpenAIEmbeddings
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# 1. 임베딩 모델 초기화
# 60억 토큰을 학습했고, 3072차원 벡터를 반환하므로 다국어(한국어 포함) 의미 파악 성능이 높음
# 더 작은 모델인 text-embedding-3-small로는 결과가 좋지 않았음.
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# 2. 단어들을 임베딩으로 변환
words = ["강아지", "고양이", "자동차", "비행기"]
word_embeddings = embeddings.embed_documents(words)

# 3. 쿼리 임베딩 생성
query = "동물"
query_embedding = embeddings.embed_query(query)

# 4. 코사인 유사도 계산 함수
def cosine_similarity(vec1, vec2): 
    """두 벡터 간의 코사인 유사도를 계산합니다."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2 + 1e-9)

# 5. 각 단어와 쿼리의 유사도 계산
print(f"'{query}'에 대한 유사도: ")
for word, embedding in zip(words, word_embeddings):
    similarity = cosine_similarity(query_embedding, embedding)
    print(f"  {word}: {similarity:.3f}")