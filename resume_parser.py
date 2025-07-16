from dotenv import load_dotenv
import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable import RunnablePassthrough
from models import Information
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

class ResumeParser:
    def __init__(self, model_name="gemini-1.5-flash", temperature=0):

        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature= temperature)
        self.output_parser = PydanticOutputParser(pydantic_object=Information)
        self.prompt_template = PromptTemplate(
            template="Extract information about entities from the following text and output it as a structured JSON array:\n\n{text}\n\n{format_instructions}",
            input_variables=["text"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        self.chain = (
            {"text": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | self.output_parser
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.resume_dir = "./resume_db"
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )

    def load_document(self, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")

        if file_path.lower().endswith(".txt"):
            loader = TextLoader(file_path)
        elif file_path.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            raise TypeError("Unsupported file type.  Only .txt and .pdf files are supported.")
        
        documents = loader.load()
        return documents[0].page_content
    
    def process_resume(self, resume_text: str, resume_path: str = "./resume_db") -> None:
        
        # Create a document from the resume
        resume_doc = Document(
            page_content=resume_text,
            metadata={"source": "resume", "type": "resume"}
        )
        
        # Split into chunks
        resume_chunks = self.text_splitter.split_documents([resume_doc])
        
        # Create and save the vector store
        self.resume_db = FAISS.from_documents(
            documents=resume_chunks,
            embedding=self.embeddings
        )
        
        # Save to disk
        # self.resume_db.save_local(resume_path)
        # print(f"Resume processed and saved to {resume_path}")
        print("Resume processed and embeddings generated.")

        return self.resume_db

    def parse(self, file_path):
        
        try:
            text_content = self.load_document(file_path)
            # parsed_output = self.chain.invoke(text_content) #For personalised roles that matches the resume. Disabled for now.
            resume_embed = self.process_resume(text_content)
            return resume_embed
            # return parsed_output
        
        except Exception as e:
            print(f"Error parsing resume: {e}")  
            # return []



    