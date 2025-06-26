# 📚 AgRAG

Este projeto implementa um sistema de Perguntas e Respostas (Q&A) usando a técnica de RAG (Retrieval-Augmented Generation), baseado em um arquivo PDF com conteúdo técnico (como perguntas e respostas sobre uma cultura).

## 🧠 Tecnologias utilizadas

- [LangChain](https://www.langchain.com/) - Orquestração da cadeia de perguntas e respostas
- [FAISS](https://github.com/facebookresearch/faiss) - Indexação vetorial local
- [HuggingFace Embeddings](https://huggingface.co/sentence-transformers) - Para gerar vetores de busca semântica
- [Ollama](https://ollama.com/) - Servidor local de LLMs (utilizando `gemma3:1b`)
- [PDFPlumber](https://github.com/jsvine/pdfplumber) - Extração de texto do PDF

## 📦 Estrutura do projeto

```
.
└── agrag/
    ├── src/
    │   ├── __init__.py
    │   ├── RAG_QA_Gemma_PDF.ipynb
    │   └── data/
    │       ├── 500perguntasmilho.pdf
    |       └── 500perguntassoja.pdf
    ├── README.md
    ├── .gitignore
    ├── LICENSE
    ├── requirements.txt
    └── venv/
```

## 🚀 Como executar

1. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

2. Inicie o Ollama com o modelo Gemma:
```bash
ollama pull gemma3:1b
ollama run gemma3:1b
```

3. Rode o notebook `RAG_QA_Gemma_PDF.ipynb` passo a passo:
   - O PDF será carregado e dividido em pedaços
   - Os textos serão embeddados e indexados com FAISS
   - As perguntas serão respondidas com base no conteúdo extraído do PDF

## 🌐 Exemplo de uso

```python
pergunta = "Qual importância do controle biológico na soja?"
resposta = qa_chain.invoke(pergunta)
print(resposta["result"])
```

## 📌 Dicas

- Sempre use um modelo de embedding multilíngue (ex: `intfloat/multilingual-e5-base`) se o PDF estiver em português.
- Ajuste `chunk_size` e `chunk_overlap` para garantir que pergunta + resposta estejam no mesmo bloco.

## 📄 Fonte dos dados

Estou utilizando o PDF oficial da Embrapa:
[Coleção 500 Perguntas e 500 Respostas - Embrapa](https://www.embrapa.br/publicacoes-e-bibliotecas/colecao-500-perguntas-500-respostas)

---

Gostou? Contribua com uma estrela ⭐ no repositório.