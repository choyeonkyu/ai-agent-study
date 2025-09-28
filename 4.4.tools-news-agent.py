from agents import Agent, Runner, function_tool
from duckduckgo_search import DDGS
from gnews import GNews
from dotenv import load_dotenv

load_dotenv()

# 1. 도구 정의
@function_tool()
def news_search(query: str) -> str:
    """Google News를 사용한 뉴스 검색 핸들러 함수"""
    try: 
        # google news 사용
        google_news = GNews(language='ko', country='KR', max_results=5)
        results = google_news.get_news(query)
        if results:
            # 기사 제목 + URL만 추출
            news_list = [f"{item['title']} - {item['url']}" for item in results[:3]]
            return "\n".join(news_list)
        else:
            return "검색결과가 없습니다."
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}"
    
# 2. 에이전트 정의
news_agent = Agent(
    name="NewsSearchAgent",
    model="gpt-5-mini",
    instructions=(
        "당신은 한국어 뉴스 리포터입니다."
        "WebSearchTool을 사용하여 최신 뉴스를 검색하고, "
        "3개의 기사 URL을 함께 알려주세요."
    ),
    tools = [news_search]
)

if __name__=="__main__":
    # 3. 에이전트 실행
    print("뉴스 검색 에이전트를 시작합니다.")
    result = Runner.run_sync(
        starting_agent=news_agent,
        input="최신 기술 뉴스 검색해주세요.",
    )
    print(result.final_output)