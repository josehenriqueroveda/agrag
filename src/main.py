import os
import argparse
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.llms import OllamaLLM
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import PromptTemplate
import pdfplumber


class RAGSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.config["embedding_model_name"]
        )
        self.llm = OllamaLLM(model=self.config["llm_model_name"])
        self.db = None

    def load_and_split_pdf(self) -> List[str]:
        all_text = ""
        with pdfplumber.open(
            os.path.join("src", "data", f"{self.config['crop']}.pdf")
        ) as pdf:
            for page in pdf.pages:
                all_text += page.extract_text() + "\n"

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config["chunk_size"],
            chunk_overlap=self.config["chunk_overlap"],
        )
        return text_splitter.create_documents([all_text])

    def setup_vector_database(self, docs: List[str]):
        self.db = FAISS.from_documents(docs, self.embedding_model)

    def create_qa_chain(self):
        template = """
        Você é um assistente agrícola especializado na cultura de {crop}. 
        Responda a pergunta abaixo em português do Brasil, com base exclusivamente no conteúdo fornecido.

        Contexto:
        {context}

        Pergunta: {input}
        Resposta:
        """
        prompt = PromptTemplate(template=template, input_variables=["input", "crop"])

        document_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt,
        )

        retriever = self.db.as_retriever(
            search_kwargs={"k": self.config["retriever_k"]}
        )

        return create_retrieval_chain(
            retriever,
            document_chain,
        )


def main():
    parser = argparse.ArgumentParser(
        description="AgRAG - Sistema de Q&A com RAG para agricultura."
    )
    parser.add_argument(
        "--crop", type=str, default="soja", help="Cultura agrícola do PDF."
    )
    parser.add_argument(
        "--question", type=str, required=True, help="Pergunta sobre o conteúdo do PDF."
    )
    args = parser.parse_args()

    config = {
        "crop": args.crop,
        "embedding_model_name": "intfloat/multilingual-e5-base",
        "llm_model_name": "gemma3:1b",
        "chunk_size": 1500,
        "chunk_overlap": 100,
        "retriever_k": 10,
    }

    rag_system = RAGSystem(config)

    print("Carregando e processando o PDF...")
    docs = rag_system.load_and_split_pdf()

    print("Criando o banco de dados de vetores...")
    rag_system.setup_vector_database(docs)

    print("Configurando o chain de Q&A...")
    qa_chain = rag_system.create_qa_chain()

    print("Enviando a pergunta para o modelo...")
    context_vars = {
        "input": args.question,
        "crop": args.crop,
    }
    resposta = qa_chain.invoke(context_vars)

    print("\n", resposta["answer"])


if __name__ == "__main__":
    main()
