import re
import uuid
from langchain_classic.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.stores import InMemoryStore
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.documents import Document as _Doc
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI


vectorstore = Chroma(
    collection_name="multimodal_rag",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)
store = InMemoryStore()
id_key = "doc_id"
retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=store, id_key=id_key)

def add_documents(retriever, doc_summaries, doc_contents):
    """요약본은 벡터 DB에, 원본은 docstore에 '같은 id'로 저장합니다."""
    doc_ids = [str(uuid.uuid4()) for _ in doc_contents]
    summary_docs = [
        _Doc(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(doc_summaries)
    ]

    vectorstore = retriever.vectorstore.add_documents(summary_docs)
    store = retriever.docstore.mset(list(zip(doc_ids, doc_contents)))

def split_image_text_types(docs):
    """검색 결과를 Base64 이미지와 텍스트로 나눕니다."""
    b64_img = []
    texts_out = []

    for doc in docs:
        content = doc.page_content if isinstance(doc, _Doc) else doc
        if re.match("^[A-Za-z0-9+/]{100,}={0,2}$", content):
            b64_img.append(content)
        else:
            texts_out.append(content)

    return {"images": b64_img, "texts": texts_out}

def img_prompt_func(data_dict):
    """검색된 원본을 멀티모달 LLM이 읽을 형태로 조립합니다."""
    messages = []

    for img in data_dict["context"]["images"]:
        messages.append(
            {"type": "image_url",
             "image_url": {"url": f"data:image/jpg;base64,{img}"}}
        )
    formatted_texts = "\n".join(data_dict["context"]["texts"])
    messages.append({
        "type": "text",
        "text": ("자료를 근거로 질문에 한국어로 답하세요.\n"
        "자료에 없는 내용은 모른다고 답하세요.\n\n"
        f"질문: {data_dict['question']}\n\n"
        f"참고 텍스트:\n {formatted_texts}")
    })

    return [HumanMessage(content=messages)]

model = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=1024)

chain = ({"context": retriever | RunnableLambda(split_image_text_types),
          "question": RunnablePassthrough()}
          | RunnableLambda(img_prompt_func)
          | model
          | StrOutputParser()
)