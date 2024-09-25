# RAG System

> Work in Progress as I continue to familiarize myself with the ML/AI ecosystem. More advanced RAG techniques might be implemented as well.

This repository contains a notebook that implements a RAG pipeline for LLM.

The RAG pipeline uses:
- Unstructured
- HuggingFace Embedding and Inference models
- Qdrant
- Langchain

Notes:

- A Qdrant API and datastore must be running on your machine in order for the RAG pipeline to work.
- Required Python packages and libraries are found in `requirements.txt`
- Data used by pipeline found in `/data` directory.