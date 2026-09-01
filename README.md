# 🌴 Fiji Travel Intelligence Assistant

## 📚 Table of Contents

- [📌 Project Overview](#-project-overview)
- [🎯 Project Objective](#-project-objective)
- [🛠 Tools & Technologies](#-tools--technologies)
- [🏗 RAG Architecture](#-rag-architecture)
- [📚 Knowledge Base](#-knowledge-base)
- [🔎 Retrieval Pipeline](#-retrieval-pipeline)
- [🧪 Retrieval Evaluation](#-retrieval-evaluation)
- [🤖 Answer Generation](#-answer-generation)
- [📊 Generation Evaluation](#-generation-evaluation)
- [💬 Streamlit Application](#-streamlit-application)
- [⚠️ Limitations](#️-limitations)
- [🚀 Future Improvements](#-future-improvements)


## 📌 Project Overview

The **Fiji Travel Intelligence Assistant** is an end-to-end Retrieval-Augmented Generation (RAG) application designed to answer travel questions about Fiji using a curated knowledge base rather than relying solely on a language model's internal knowledge.

The system retrieves relevant information from a collection of Fiji travel sources using semantic search, provides the retrieved context to Gemini, and generates a grounded response based only on that information.

The project covers the full RAG development lifecycle, including:
- Source collection and document processing
- Text cleaning and chunking
- Vector embeddings and semantic retrieval
- Vector storage using ChromaDB
- Retrieval experimentation and evaluation
- LLM-based answer generation
- Human evaluation of generated responses
- Deployment through an interactive Streamlit chat interface

The final knowledge base contains **23 curated travel documents split into 260 searchable chunks**.


## 🎯 Project Objective

Travel information is distributed across government travel advice, tourism websites, destination guides and transport resources, making it difficult to find reliable answers without searching across multiple sources.

The objective of this project was to build a travel assistant capable of:

- Retrieving relevant information from a curated Fiji-specific knowledge base
- Generating useful answers grounded in retrieved source material
- Providing transparency into the sources used to answer each question
- Recognising when the knowledge base does not contain enough information to answer reliably
- Avoiding fabricated answers for real-time questions such as current weather, hotel prices, ferry availability and live transport status
- Maintaining conversational context for follow-up questions

Rather than focusing only on building a working chatbot, the project also evaluates the underlying retrieval and generation pipeline to understand its performance, limitations and trade-offs.


## 🛠 Tools & Technologies

- **Python** – Core development language for document processing, retrieval, generation and evaluation
- **Sentence Transformers** – Creation of dense vector embeddings for semantic search
- **all-MiniLM-L6-v2** – Final embedding model selected for the V1 retrieval pipeline
- **ChromaDB** – Persistent vector database for storing and retrieving document chunks using cosine similarity
- **Google Gemini** – LLM used to generate answers from retrieved context
- **Streamlit** – Interactive chat interface for the final application
- **JSON** – Storage of processed documents, chunks, evaluation questions and experiment results
- **Git & GitHub** – Version control and project documentation
  

## 🏗 RAG Architecture

The application separates retrieval from generation so that responses are grounded in the curated Fiji travel knowledge base.

The pipeline follows this architecture:

        23 Curated Fiji Travel Documents
                       │
                       ▼
              Document Cleaning
                       │
                       ▼
                  Chunking
                       │
                       ▼
          MiniLM Vector Embeddings
                       │
                       ▼
             ChromaDB Vector Store

And when a user asks a question:

                  User Question
                       │
                       ▼
          MiniLM Query Embedding
                       │
                       ▼
          Top-5 Semantic Retrieval
                       │
                       ▼
              Retrieved Context
                       │
                       ▼
              Gemini Generation
                       │
                       ▼
              Grounded Response
                       │
                       ▼
             Streamlit Interface


## 📚 Knowledge Base

The assistant's knowledge base was built from **23 manually curated Fiji travel documents** collected from authoritative and relevant sources. Rather than relying on unrestricted web search, the project uses a fixed corpus so that retrieved information can be traced back to known sources and evaluated consistently.

The documents cover practical information a traveller may need when planning a trip to Fiji, including:

- 🛂 **Entry & Travel Requirements** — visas, passports, customs, and arrival information
- 🏝️ **Destinations & Islands** — regional and island-specific travel information
- 🚐 **Transport** — domestic travel, ferries, buses, and inter-island connections
- 🩺 **Health & Safety** — travel health advice, precautions, and emergency information
- 💰 **Money & Payments** — currency, banking, and payment guidance
- 🌦️ **Weather & Travel Conditions** — climate, seasonal considerations, and travel planning
- 🤝 **Culture & Local Guidance** — customs, etiquette, and responsible travel information

Before being added to the retrieval system, the source documents were cleaned to remove unnecessary formatting and text with little retrieval value. The cleaned content was then divided into smaller passages suitable for embedding and semantic retrieval.


### Knowledge Base Summary



| **Curated source documents** | 23 |
| **Processed text chunks** | 260 |
| **Embedding model** | `all-MiniLM-L6-v2` |
| **Vector database** | ChromaDB |
| **Similarity metric** | Cosine similarity |

This produced a compact, domain-specific knowledge base designed specifically around **Fiji travel questions**, rather than a general-purpose collection of travel information.

Each chunk retains source metadata, allowing retrieved context to remain connected to its original document and enabling the generation pipeline to produce source-grounded answers.
