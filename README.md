# 문제정의
일반 RAG는 텍스트를 추출해서 텍스트에 기반해서 답변을 하다보니 보고서처럼
이미지나 표, 그래프에 주요 내용이 있을 경우 원하는 답변이 안 나올 수 있어서
이를 극복하기 위해 멀티모달RAG를 활용하여 텍스트뿐 아니라 이미지, 표, 그래프를
활용하여 이미지, 표, 그래프에 있는 내용에 대한 답변을 받을 수 있도록 하였다.

# 아키텍쳐 다이어그램
![alt text](multimodal-rag.png)

# 실행 방법
git clone <저장소 주소>
cd multimodal-rag

## 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate          # 윈도우: .venv\Scripts\activate

## 의존성 설치
pip install --upgrade pip
pip install -r requirements.txt     # 또는 requirements.lock.txt

## 커널 등록
python -m ipykernel install --user --name multimodal-rag

## .env 작성
cp .env.example .env                # 윈도우: copy .env.example .env
## .env 파일을 열어 실제 API 키를 입력

# 디렉토리 구조
```
multimodal-rag/
├── .venv/                      # 가상환경 (Git 제외)
├── .env                        # API 키 (Git 제외, 절대 커밋 금지)
├── .env.example                # 키 없는 템플릿 (Git 포함)
├── .gitignore
├── requirements.txt            # 의존성 목록
├── requirements.lock.txt       # 버전 고정 파일
├── README.md                   # 포트폴리오의 얼굴
├── data/
│   ├── invest.pdf              # 원본 PDF
│   └── figures/                # 추출된 이미지 (Git 제외, 용량 큼)
├── notebooks/
│   └── Multi_modal_RAG.ipynb   # 실습 노트북
└── src/
    ├── extract.py              # PDF 파싱 함수
    ├── summarize.py            # 요약 체인
    └── retriever.py            # 다중 벡터 검색기
```
# 토큰 사용량 측정
텍스트 요약 토큰 사용량 (추정)
입력: 13849
출력: 5320
합계 토큰(천 단위 콤마): 19,169 토큰

요약한 이미지 수: 41 장

※ 실제 비용 = 토큰 수 x 단가. 단가는 OpenAI 공식 가격 페이지에서 확인하세요.
※ 이미지 토큰은 해상도에 따라 달라지므로 위 수치에 포함되지 않았습니다.

# 텍스트 전용 RAG와 멀티모달 RAG 차이
![alt text](image.png)

# 질의응답 5건
## 질문
```
-질문1. "2026년 상반기에 영업이익이 급증한 업종은 무엇인가요?"
-질문2. "일시소득의 평균 한계소비성향은 얼마인가요?"
-질문3. "환율 하락으로 구매력이 가장 많이 개선되는 소득분위는 어디인가요?"
-질문4. "증시 조정 이후 소비가 가장 크게 줄어든 품목은 무엇인가요?"
-질문5. "저소득층에 영향이 가장 큰 요인은 무엇인가요?"
```
## 답변
```
답변1. 자료에 따르면 2026년 상반기에 영업이익이 급증한 업종에 대한 구체적인 정보는 제공되지 않았습니다. 따라서 이 질문에 대한 답변은 모릅니다.
답변2. 자료에 따르면, 일시소득의 평균 한계소비성향(MPC)은 약 11%입니다. 즉, 일시소득이 100만원 증가할 때 약 11만원이 소비로 이어진다고 추정됩니다.
답변3. 환율 하락으로 구매력이 가장 많이 개선되는 소득분위는 1분위입니다. 1분위의 구매력 개선폭은 0.46%로, 5분위의 0.20%보다 두 배 이상 높습니다.
답변4. 자료에 따르면 증시 조정 이후 소비가 가장 크게 줄어든 품목은 백화점 소매판매와 여가서비스 등 주가변동에 민감한 품목입니다.
답변5. 저소득층에 영향이 가장 큰 요인은 "환율 하락"입니다. 환율 하락은 수입물가 하락을 통해 가계 전반의 실질구매력을 높이고, 특히 저소득층의 소비여력 개선에 기여할 것으로 예상됩니다.
```
## 근거가된 원본 종류
```
이미지
```

# Ollama를 이용한 번역 체인 통합
Ollama 번역 답변
---
```
질문 1: What are three things to watch out for during the autumn seasonal transition?
답변 1: 가을 계절 전환 시에 주의해야 할 3가지는?
```
---
```
질문 2: How can I prevent catching a cold when the weather changes in the fall?
답변 2: 여름이 가면 바람이 쥬는데, 어떻게 하면 감기가 잡히지 않게 할 수 있나요?
```
---
```
질문 3: What should I eat to keep my immune system strong during the change of seasons?
답변 3: 계절이 바뀔 때 내 면역 체계를 튼튼하게 유지하기 위해 무엇을 먹어야 하는지 알려주세요.
```
---
```
질문 4: Why do allergies and dry skin get worse in autumn, and how can I manage them?
답변 4: 가을에 알레르기와 피부가 왜 더 악화되는지 그리고 어떻게 관리하는지 알려주세요.
```
---
```
질문 5: How should I dress to handle big temperature differences between morning and evening?
답변 5: 아침과 저녁 사이에 큰 온도 차이를 겪을 때 어떻게 옷을 입으면 좋을까요?
```