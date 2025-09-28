# 요즘 AI 에이전트 개발 Study

> LLM, RAG, ADK, MDP, LangChain, A2A, LangGraph 실습용 예제 코드 저장소

---

## 📚 목차

### Chapter 00 개발 환경 설정
- 0.1 파이썬 환경 설정
- 0.2 VSCode 설정
- 0.3 API 키 발급받기

---

## [PART 1] LLM과 랭체인 개발

### Chapter 01 LLM API의 기초
- 1.1 [LLM API를 왜 사용해야 하는가?](1.1.api-ai-agent.py)
- 1.2 LLM API의 기본적인 사용법
- 1.3 [스트리밍 처리](1.3.stream-api.py)
- 1.4 비동기 처리 및 오류 핸들링
    - 1.4.1 [async 예제](1.4.1.async-api.py)
    - 1.4.2 [tenacity 라이브러리 활용](1.4.2.tenacity-lib.py)

### Chapter 02 LLM API를 사용하여 챗봇 만들기
- 2.1 [CLI를 사용한 챗봇 만들기](2.1.cli-chatbot.py)
- 2.2 챗봇이 이전 대화를 기억할 수 있게 하기
- 2.3 [어린 왕자 페르소나 추가하기](2.3.little-prince-chatbot.py)
- 2.4 웹 인터페이스 추가하기

### Chapter 03 랭체인의 핵심 콘셉트
- 3.1 [랭체인 프레임워크 소개](3.1.Introduction-to-Langchain.py)
- 3.2 채팅 모델
- 3.3 [메시지](3.3.Message-Langchain.py)
- 3.4.1 [PromptTemplate ](3.4.1.PromptTemplate.py)
- 3.4.2 [OutputParser](3.4.2.OutputParser.py)
- 3.5 [Runnable과 LCEL](3.5.RunnableLCEL.py)
- 3.6 [도구](3.6.tool-decorator.py)
- 3.7.1 [임베딩 모델](3.7.1.embedding.py)
- 3.7.2 [벡터 DB](3.7.2.vectorDB.py)
- 3.7.3 [벡터 DB with document loader](3.7.3.%20vectorDB-with-document-loader.py)
- 3.8.1 [Retriever](3.8.1.retriever-from-vectordb.py)
- 3.8.2 [websearch RAG 모델](3.8.2.websearch-RAG.py)

---

## [PART 2] 요즘 AI 에이전트 개발

### Chapter 04 오픈AI의 에이전트 SDK
- 4.1 AI 에이전트 알아보기
- 4.2 [인사하는 에이전트 만들기](4.2.openai-hello-agent.py)
- 4.3 핵심 콘셉트들
- 4.4 [도구 활용 : 뉴스 에이전트](4.4.tools-news-agent.py)
- 4.5 [가드레일 사용하기](4.5.guardrail-test.py)
- 4.6 [다중 에이전트 협업 : 병원 안내 시스템](4.6.handoff-agent.py)
- 4.7 로그 확인 및 트레이싱

### Chapter 05 구글의 ADK
- 5.1 개발 환경 준비
- 5.2 ADK 특징과 장점
- 5.3 헬로 ADK 만들기
- 5.4 실행하는 3가지 방법
- 5.5 여러 도구 활용 에이전트
- 5.6 구조화된 출력 지원
- 5.7 멀티 에이전트
- 5.8 워크플로 에이전트
- 5.9 스팸 체크 에이전트

### Chapter 06 랭그래프
- 6.1 그래프 자료구조 이해
- 6.2 핵심 개념
- 6.3 헬로 랭그래프 만들기
- 6.4 조건부 라우팅 : 감정 분석 챗봇
- 6.5 체크포인터 상태 관리
- 6.6 루프 워크플로 구현
- 6.7 병렬 처리 워크플로
- 6.8 ToolNode를 활용한 도구 기능
- 6.9 휴먼 인 더 루프 반영
- 6.10 하위 그래프 사용

---

## [PART 3] AI 에이전트 프로토콜 : MCP와 A2A

### Chapter 07 AI 에이전트 프로토콜, 클로드 MCP
- 7.1 MCP 탄생 배경
- 7.2 MCP란?
- 7.3 MCP 기술적 관점
- 7.4 MCP 현재 위상
- 7.5 MCP 서버 만들기
- 7.6 향후 과제

### Chapter 08 AI 에이전트 프로토콜, 구글 A2A
- 8.1 A2A란?
- 8.2 핵심 개념 및 용어
- 8.3 MCP와 A2A 비교
- 8.4 동작 원리 실습 : AI 비서 서버 & 클라이언트

---

## [PART 4] 고급 AI 에이전트 개발 : 2가지 프로젝트

### Chapter 09 멀티 에이전트 뉴스 수집 및 요약 시스템
- 9.1 시스템 아키텍처
- 9.2 데이터 모델 정의
- 9.3 유틸리티 함수 구현
- 9.4 프로젝트 설정 관리
- 9.5 에이전트 구현
- 9.6 워크플로 구현
- 9.7 메인 실행 파일 구현
- 9.8 실행 및 보고서 확인

### Chapter 10 랭그래프와 MCP를 활용한 고급 에이전트 개발
- 10.1 시스템 아키텍처
- 10.2 MCP 서버 구축
- 10.3 채팅 에이전트 만들기
- 10.4 웹 인터페이스 만들기
- 10.5 MCP 서버 & 에이전트 테스트

---

## 📌 Appendix A 개발 환경 팁
- A.1 런타임 매니저 선택
- A.2 uv 간단 사용법
- A.3 환경 변수 관리
- A.4 로깅 설정

---