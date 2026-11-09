import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

PROJECT_ROOT = PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "src" else Path.cwd()

load_dotenv(PROJECT_ROOT / ".env")

try:
    openai_api_key = os.environ["OPENAI_API_KEY"]
    if not openai_api_key.strip():
        raise ValueError("OPENAI_API_KEY 값이 비어 있습니다. .env 파일을 확인하세요.")
    else:
        print("환경변수 OPENAI_API_KEY 로드 완료")
except KeyError:
    raise ValueError("환경변수 OPENAI_API_KEY 키가 없습니다. .env 파일을 확인하세요.")

def generate_text_summaries(texts, tables, summarize_texts=False):
    prompt_text = """표와 텍스트를 검색용으로 요약하는 도우미 / 임베딩되어 원본 검색에 쓰임 / 
                        검색에 최적화된 간결한 요약 작성 / 요약할 표 또는 텍스트: {element}"""
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    text_summaries = []
    table_summaries = []
    if texts and summarize_texts:
        text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})
    elif texts:
        text_summaries = texts

    if tables:
        table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})

    return text_summaries, table_summaries

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("UTF-8")

def image_summarize(img_base64, prompt):
    chat = ChatOpenAI(model="gpt-4o-mini", max_tokens=1024)
    msg = chat.invoke([
        HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{img_base64}"},
             },
        ])
    ])

    return msg.content

def generate_img_summaries(path):
    img_base64_list = []
    img_summaries = []
    prompt_kor = """당신은 검색을 위해 이미지를 요약하는 어시스턴트입니다.
    이 요약문은 임베딩되어 원본 이미지를 검색하는 데 사용됩니다.
    검색에 최적화된 간결한 이미지 요약을 작성하세요."""

    for img_file in sorted(os.listdir(path)):
        if img_file.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(path, img_file)
            b64_img = encode_image(img_path)
            img_base64_list.append(b64_img)
            img_summaries.append(image_summarize(b64_img, prompt_kor))

    return img_base64_list, img_summaries