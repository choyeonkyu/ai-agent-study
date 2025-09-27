from langchain.prompts import PromptTemplate, load_prompt
import os

# from_template 사용 예제

template = PromptTemplate.from_template(
    "당신은 친절한 AI입니다. \n질문:{question}\n답변:"
)
print(template.format(question="랭체인이 뭐야?"))

# 생성자 호출 예제
template = PromptTemplate(
    input_variables=["article", "style"],
    template="다음 기사를 {style} 스타일로 요약하세요 \n\n{article}"
)

print(template.format(article="OpenAI가 GPT-5를 공개했다.....", style="뉴스"))

# load_prompt()함수 사용 - windows 내 encoding 문제 有
# current_dir_path = os.path.dirname(os.path.abspath(__file__))
# file_prompt = load_prompt(f"{current_dir_path}/template_example.yaml")
# print(file_prompt.format(context="서울은 한국의 수도이다.", question="수도는?"))

# partial 변수 사용
base_prompt = PromptTemplate.from_template("'{text}' 문장을 {lang}로 번역")
ko_prompt = base_prompt.partial(lang="Korean")
en_prompt = base_prompt.partial(lang="English")

print(ko_prompt.format(text="Hello"))
print(en_prompt.format(text="안녕하세요"))