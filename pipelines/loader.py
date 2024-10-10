import os
import sys
import logging
from tqdm import tqdm
from load_dotenv import load_dotenv

from PyPDF2.errors import PdfStreamError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError


load_dotenv()


def prepare_source(documents):
    for doc in tqdm(documents):
        source_data_split = doc.metadata["source"].split("\\")

        source_data_split = list(dict.fromkeys(source_data_split))
        k = [source_data_split.remove(l) for l in ["..", "data", "documents"] if l in source_data_split]
            
        source = '/'.join([str(elem) for elem in source_data_split])
        doc.metadata["source"] = source

def load_documents(DATA_PATH):
    """Function that crawls a specified directory to parse all pdfs in it 

    Args:
        DATA_PATH: str
            path to folder that contains pdfs
    Returns:
        Document type objects
            contains text values with source metadata (page, file name)
    """
    documents = []
    
    def process_directory(dir_path):
        nonlocal documents
        
        items = os.listdir(dir_path)
        subdirs = [d for d in items if os.path.isdir(os.path.join(dir_path, d))]
        pdf_files = [f for f in items if f.lower().endswith('.pdf')]
        txt_files = [f for f in items if f.lower().endswith('.txt')]
        
        if not items or (not pdf_files and not txt_files and not subdirs):
            logging.info(f"No relevant files or subdirectories in {dir_path}, skipping...")
            return
        
        if pdf_files:
            logging.info(f"PDF files found in {dir_path}: {pdf_files}")
            document_loader = PyPDFDirectoryLoader(dir_path)
            try:
                # Try to load the documents and append to the documents list
                loaded_docs = document_loader.load()
                documents.extend(loaded_docs)
                logging.info(f"Successfully loaded {len(loaded_docs)} documents from PDFs in {dir_path}.")
            except PdfStreamError as e:
                logging.error(f"Error loading PDF in {dir_path}: {str(e)} - File might be corrupted.")
            except Exception as e:
                # Catch any other exceptions that may occur during PDF loading
                logging.error(f"Unexpected error loading PDFs in {dir_path}: {str(e)}")

        for subdir in subdirs:
            process_directory(os.path.join(dir_path, subdir))
    
    process_directory(DATA_PATH)
    logging.info(f"Total documents loaded: {len(documents)}")
    prepare_source(documents)
    logging.info(f"Formatted source correctly")

    return documents



def load_unstructured_to_structured(file_name,
                                    languages=["eng"]) -> dict:
    """Reads menus that are pdf images (impossible to parse with regular methods)
    Must have a API Key from unstructured https://app.unstructured.io/usage
    
    Parameters:
    ----------
    file_name: str 
        PDF (png) file name
    languages: [str]
        list of languages in the file

    Returns a structured dictionnary with text values and type (Image or text)
    """

    client = UnstructuredClient(
        api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"),
        server_url=os.getenv("UNSTRUCTURED_API_URL"),
    )

    file = open(file_name, "rb")
    req = shared.PartitionParameters(
        # Note that this currently only supports a single file
        files=shared.Files(
            content=file.read(),
            file_name=file_name,
        ),
        strategy=shared.Strategy.OCR_ONLY,
        languages=languages,
        split_pdf_page=True,
        split_pdf_allow_failed=True,
        split_pdf_concurrency_level=15
    )

    try:
        res = client.general.partition(req)
        print(res.elements[0])
    except SDKError as e:
        print(e)
    
    res = client.general.partition(request=req)
    element_dicts = [element for element in res.elements]

    # Return the processed data's first element only.
    return element_dicts

    
def load_unstructured_langchain(data_file_path):
    """Loads all text data in menu and corrects (cid) errors when wrongly parsing
    pdf files which occurs using standard PDF reader in langchain
    
    ! does not hold metadata of pages

    Parameters:
    ----------
    data_file_path: str
        file path
    Returns:
        output: str
            concatenated output of all text data in that file
    """
    # Local PDF file uploads
    if data_file_path:
        loader = UnstructuredPDFLoader(file_path=data_file_path)
        data = loader.load()
    else:
        print("Upload a PDF file")
    import re
    def cidToChar(cidx):
        return chr(int(re.findall(r'\(cid\:(\d+)\)',cidx)[0]) + 29)
    output = ""
    for x in data[0].page_content.split('\n'):
        if x != '' and x != '(cid:3)':         # merely to compact the output
            abc = re.findall(r'\(cid\:\d+\)',x)
            if len(abc) > 0:
                for cid in abc: x=x.replace(cid, cidToChar(cid))
            output = output+"\n"+repr(x).strip("'")
    return output