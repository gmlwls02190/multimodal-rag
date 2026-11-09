# PDF에서 표, 텍스트, 이미지 같은 요소를 추출하기 위해 사용되는 기능
import os
from pathlib import Path
from langchain_text_splitters import CharacterTextSplitter
from unstructured.partition.pdf import partition_pdf

PROJECT_ROOT = PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "src" else Path.cwd()

def extract_pdf_elements(path, fname):
    """
    PDF 파엘에서 이미지, 테이블, 텍스트 블록을 추출합니다.
    path: 파일 경로(추출된 이미지 파일이 저장될 위치)
    fname: 파일 이름"""
    return partition_pdf(
        filename=path + fname,
        strategy="hi_res",
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        extract_image_block_output_dir=path + "figures"
    )

def categorize_elements(raw_pdf_elements):
    """PDF에서 추출한 요소들을 테이블과 텍스트로 분류합니다.
    raw_pdf_elements: unstructured.documents.elements 리스트
    """
    tables = []
    texts = []

    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            tables.append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            texts.append(str(element))

    return texts, tables

fname = "invest.pdf"
pdf_dir = Path(PROJECT_ROOT / "data")
pdf_path = pdf_dir / fname
fpath = str(pdf_dir) + os.sep

print("현재 위치 : " , Path.cwd())
print("프로젝트 루트:", PROJECT_ROOT)
print("PDF 폴더     :", pdf_dir, pdf_path.resolve())
print("PDF 존재 여부:", pdf_path.exists())