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

- **Entry & Travel Requirements** — visas, passports, customs, and arrival information
- **Destinations & Islands** — regional and island-specific travel information
- **Transport** — domestic travel, ferries, buses, and inter-island connections
- **Health & Safety** — travel health advice, precautions, and emergency information
- **Money & Payments** — currency, banking, and payment guidance
- **Weather & Travel Conditions** — climate, seasonal considerations, and travel planning
- **Culture & Local Guidance** — customs, etiquette, and responsible travel information

### Document Processing

The raw documents were processed into a retrieval-ready knowledge base through several stages:

1. **Text extraction and cleaning**  
   Text was extracted from the collected documents and cleaned to remove formatting artefacts, repeated whitespace, and other content that added little value to semantic retrieval.

2. **Chunking**  
   The cleaned documents were split into smaller passages so that the system could retrieve specific pieces of information instead of entire documents. Across the 23 source documents, this produced **260 searchable text chunks**.

3. **Metadata preservation**  
   Each chunk retained metadata linking it back to its original source. This allows retrieved information to be traced to the document it came from and later used for source attribution during answer generation.

4. **Embedding generation**  
   Each chunk was converted into a dense vector representation using `all-MiniLM-L6-v2`. These embeddings capture semantic meaning, allowing passages to be matched to user questions even when they do not contain the exact same wording.

5. **Vector storage**  
   The resulting embeddings, text chunks, and associated metadata were stored in a persistent **ChromaDB** collection using cosine similarity as the distance metric.

The final V1 knowledge base contains **260 embedded chunks from 23 curated documents**, providing the retrieval layer with a focused and traceable collection of Fiji travel information.

## 🔎 Retrieval Pipeline

When a user submits a travel question, the retrieval pipeline searches the knowledge base for the passages most semantically relevant to the query.

The retrieval process follows four main stages:

1. **Query embedding**  
   The user's question is encoded using the same `all-MiniLM-L6-v2` model used to embed the knowledge base. This converts the query into a vector representation within the same embedding space as the 260 stored chunks.

2. **Semantic similarity search**  
   The query embedding is compared against the stored chunk embeddings in ChromaDB using **cosine similarity**. This allows retrieval to be based on semantic meaning rather than requiring exact keyword matches.

3. **Top-K retrieval**  
   ChromaDB ranks the chunks by similarity to the query and returns the **5 most relevant passages**. `k = 5` was selected after evaluating multiple Top-K configurations to balance retrieval coverage against the amount of irrelevant context passed downstream.

4. **Context construction**  
   The retrieved passages are combined with their source metadata to create the context supplied to the generation model. This gives the model a focused evidence set from which to construct its response while retaining the information required for source attribution.

This retrieval-first design separates **finding relevant evidence** from **generating an answer**. The language model therefore receives a small set of retrieved Fiji travel sources rather than being asked to answer the question from its general knowledge alone.

## 🧪 Retrieval Evaluation

Retrieval quality was evaluated independently from answer generation to determine whether the system could consistently locate the correct source material before passing context to the language model.

### Evaluation Dataset

A custom evaluation set of **48 Fiji travel questions** was created to test the retrieval pipeline:

- **40 answerable questions** with relevant information present in the knowledge base
- **8 unanswerable questions** where the required information was not available in the corpus

For each answerable question, the relevant chunk IDs were manually identified and cross-checked against the source documents. These chunk-level relevance labels were then used as ground truth for evaluating retrieval performance.

### Evaluation Metrics

Four information retrieval metrics were used:

- **Hit Rate@K** — whether at least one relevant chunk appeared within the top K results
- **Precision@K** — the proportion of retrieved chunks that were relevant
- **Recall@K** — the proportion of known relevant chunks successfully retrieved
- **Mean Reciprocal Rank (MRR)** — measures how highly the first relevant result appeared in the ranking

### Top-K Experiment

Different retrieval depths were evaluated to determine how much context should be passed to the generation model.

<img width="452" height="185" alt="image" src="https://github.com/user-attachments/assets/bc622b4c-80aa-4e2d-b22a-c1000f2615f3" />

Increasing retrieval depth from `k = 3` to `k = 5` produced a substantial improvement in coverage, increasing **Hit Rate from 67.5% to 90.0%** and **Recall from 62.5% to 80.0%**.

Increasing K beyond 5 provided only small recall improvements while introducing considerably more irrelevant context. Precision fell from **21.5% at k = 5** to **11.5% at k = 10**, with no improvement in Hit Rate or MRR.

For this reason, **Top-5 retrieval was selected for V1** as the best trade-off between retrieving sufficient evidence and limiting unnecessary context passed to the generation model.

### Failure Analysis

The final Top-5 configuration successfully retrieved at least one relevant chunk for **36 of the 40 answerable evaluation questions**.

The remaining failures were manually reviewed rather than relying on aggregate metrics alone. Missed questions included topics such as:

- ATM precautions and availability
- Boat and maritime safety guidance
- Yasawa Flyer and island-hopping information
- Nadi-specific travel information

These cases highlighted limitations in semantic retrieval where the wording of a question did not align strongly enough with the representation of the relevant source passage.

The results established a measurable V1 retrieval baseline while also identifying specific queries that could benefit from future improvements such as query rewriting, hybrid keyword-semantic retrieval, reranking, or expanded source coverage.
