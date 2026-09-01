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
- **all-MiniLM-L6-v2** – Final embedding model selected for the retrieval pipeline
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

<img width="846" height="191" alt="image" src="https://github.com/user-attachments/assets/87b46b70-1f5c-4386-889b-77a5ddc53a5f" />


### Evaluation Metrics

Four information retrieval metrics were used:

- **Hit Rate@K** — whether at least one relevant chunk appeared within the top K results
- **Precision@K** — the proportion of retrieved chunks that were relevant
- **Recall@K** — the proportion of known relevant chunks successfully retrieved
- **Mean Reciprocal Rank (MRR)** — measures how highly the first relevant result appeared in the ranking

### Embedding Model Comparison

Before tuning retrieval depth, two lightweight sentence embedding models were evaluated under the same `k = 5` retrieval configuration: **MiniLM (`all-MiniLM-L6-v2`)** and **BGE-small**.

For each embedding model, the experiment measured **Hit Rate, Precision, Recall, and MRR** across the 40 answerable questions. In addition to these aggregate metrics, the evaluation also tracked **failed questions at each K** — defined as questions where **none of the manually identified relevant chunks appeared within the Top-K retrieved results**.

<img width="452" height="183" alt="image" src="https://github.com/user-attachments/assets/26300e51-6338-4b97-958f-ae8f1072ae84" />

MiniLM outperformed BGE-small across every measured retrieval metric:

- **Hit Rate:** 0.900 vs 0.800
- **Precision:** 0.215 vs 0.185
- **Recall:** 0.800 vs 0.738
- **MRR:** 0.645 vs 0.606

The failed-question analysis supported the same result. MiniLM failed to retrieve a relevant chunk for **4 of the 40 answerable questions**, compared with **8 failures using BGE-small**.

Based on its stronger overall retrieval performance and lower number of complete retrieval failures, **MiniLM was retained as the embedding model for V1**.

### Top-K Experiment

Retrieval was evaluated at `k = 3`, `5`, `8`, and `10` to determine how many chunks should be retrieved for each user query.

The same evaluation framework as before was applied across each Top-K configuration to ensure a consistent comparison of retrieval performance.

<img width="452" height="185" alt="image" src="https://github.com/user-attachments/assets/fa8c781a-b2f0-400a-8e9d-5da9b8b71778" />


The experiment showed a clear improvement when increasing retrieval depth from `k = 3` to `k = 5`:

- **Hit Rate increased from 0.675 to 0.900**
- **Recall increased from 0.625 to 0.800**
- **MRR increased from 0.592 to 0.645**
- Failed questions decreased from **13 at `k = 3` to 4 at `k = 5`**

Increasing retrieval depth further produced diminishing returns. At `k = 8` and `k = 10`, the same four questions continued to fail, while Hit Rate and MRR remained unchanged at **0.900** and **0.645** respectively.

Recall improved slightly from **0.800 at `k = 5` to 0.838 at `k = 10`**, but this came at the cost of substantially lower precision, which fell from **0.215 to 0.115** as more irrelevant chunks were retrieved.

Based on these results, **`k = 5` was selected for the final retrieval pipeline**. It resolved all of the retrieval failures that could be recovered simply by increasing K, while retrieving fewer irrelevant chunks than the larger configurations.


### Failure Analysis

The final Top-5 configuration using `all-MiniLM-L6-v2` successfully retrieved at least one relevant chunk for **36 of the 40 answerable evaluation questions**.

The remaining failures were manually reviewed rather than relying on aggregate metrics alone. Missed questions included topics such as:

- ATM precautions and availability
- Boat and maritime safety guidance
- Yasawa Flyer and island-hopping information
- Nadi-specific travel information

These cases highlighted limitations in semantic retrieval where the wording of a question did not align strongly enough with the representation of the relevant source passage.

The results established a measurable  retrieval baseline while also identifying specific queries that could benefit from future improvements such as query rewriting, hybrid keyword-semantic retrieval, reranking, or expanded source coverage.


## 🤖 Answer Generation

Once the Top-5 relevant chunks have been retrieved, they are passed to the generation pipeline as supporting context for the user's question.

Rather than allowing the language model to answer freely from its own knowledge, the generation prompt explicitly constrains the model to use the **retrieved Fiji travel sources as its evidence**.

### Context-Augmented Prompt

For each query, the generation pipeline constructs a prompt containing:

1. **The user's question**
2. **The Top-5 retrieved text chunks**
3. **Source metadata associated with each retrieved chunk**
4. **Instructions defining how the model should use the supplied context**

The completed prompt is then sent to **Gemini**, which generates the final response.

```text
User Question
      +
Top-5 Retrieved Chunks
      +
Source Metadata
      +
Grounding Instructions
      ↓
    Gemini
      ↓
Grounded Travel Response
```

### Grounding & Guardrails

The generation prompt was designed to reduce unsupported answers and keep responses grounded in the curated knowledge base.

Gemini is instructed to:

- Answer using **only the information contained in the retrieved sources**
- Avoid introducing unsupported information from its general knowledge
- Clearly indicate when the retrieved context is insufficient to answer the question
- Reference the relevant **source titles and publishers** when supporting an answer

If sufficient evidence is not available, the model is instructed to respond that it **does not have enough information in the provided sources**, rather than attempting to fill the gap with an ungrounded answer.

### Source-Aware Responses

Because source metadata is preserved throughout the ingestion and retrieval pipelines, the generation model receives both the retrieved content and information about where that content originated.

This allows the final response to remain connected to the curated travel documents used as evidence, making answers more **traceable and transparent** than responses generated solely from the language model's internal knowledge.

The result is a generation pipeline designed around a core RAG principle: **retrieve evidence first, then generate an answer from that evidence.**


## 📊 Generation Evaluation

After establishing the final retrieval configuration, the complete RAG pipeline was evaluated to determine whether the retrieved evidence was being converted into **accurate, grounded, and useful travel responses**.

While retrieval evaluation measures whether the correct information can be found, generation evaluation focuses on the quality of the **final answer produced from that information**.

### Evaluation Dataset

The same **48-question evaluation set** was used to test the end-to-end RAG pipeline:

- **40 answerable questions** — the knowledge base contains sufficient information to produce an answer
- **8 unanswerable questions** — the knowledge base intentionally does not contain sufficient information

Including unanswerable questions was important for testing whether the assistant could recognise the limits of its knowledge base rather than generating unsupported information.

### Evaluation Approach

Each question was passed through the complete pipeline using the final V1 retrieval configuration:

```text
Evaluation Question
        ↓
MiniLM Query Embedding
        ↓
Top-5 Retrieval
        ↓
Retrieved Context + Metadata
        ↓
Gemini
        ↓
Generated Answer
        ↓
Generation Evaluation
```

The generated responses were then evaluated separately from retrieval performance. This made it possible to assess not only whether the system found relevant evidence, but whether the generation model **used that evidence correctly and remained grounded in the supplied context**.

For answerable questions, the evaluation focused on whether the generated response correctly addressed the question using the retrieved evidence.

For unanswerable questions, the expected behaviour was different: the assistant should recognise that the supplied sources were insufficient and **decline to provide an unsupported answer**.

This provides an end-to-end evaluation of the two behaviours required from the assistant: **answer when supported by the knowledge base, and abstain when it is not.**

## 📊 Generation Evaluation

After selecting the final retrieval configuration, the complete RAG pipeline was evaluated using the same **48-question evaluation set**.

The goal was to test two behaviours:

- Whether the assistant could generate a useful, source-grounded answer when the required information was available
- Whether it could correctly **abstain** when the knowledge base did not contain enough information

### Evaluation Setup

The final V1 pipeline used:

- `all-MiniLM-L6-v2` embeddings
- ChromaDB semantic retrieval
- `k = 5` retrieved chunks
- Gemini for grounded answer generation

Each evaluation question was passed through the complete pipeline:

```text
Evaluation Question
        ↓
MiniLM Query Embedding
        ↓
Top-5 Retrieval
        ↓
Retrieved Context + Source Metadata
        ↓
Gemini
        ↓
Generated Answer
```

Generated responses were compared against manually prepared expected answers and reviewed alongside the retrieved chunks to distinguish **retrieval failures from generation failures**.

### Unanswerable Question Handling

Eight questions were intentionally designed to require information unavailable in the static knowledge base, including:

- Live hotel prices
- Tomorrow's weather
- Current ferry availability and delays
- Live immigration wait times
- Current Google ratings and guest reviews

The assistant correctly recognised insufficient evidence for **all 8 unanswerable questions**, producing an abstention rather than attempting to invent an answer.

**Unanswerable-question abstention: 8 / 8 (100%)**

For example:

> **Question:** Which hotel in Nadi has the cheapest room available tonight?  
> **Response:** *"I don't have enough information in my current Fiji travel sources to answer that."*

The hardest unanswerable example asked whether the **8:45 AM ferry from Port Denarau was running on time today**. Although the retrieved documents contained the scheduled departure time, the model correctly distinguished between a published schedule and **real-time operational status**, explaining that the available sources could not confirm whether the ferry was currently running on time.

### Answerable Question Behaviour

For most answerable questions, the assistant successfully transformed retrieved evidence into concise travel responses while retaining source attribution.

Strong examples included questions covering:

- Visa and entry requirements
- Cyclone and tsunami safety
- Health and medication guidance
- Driving and taxi information
- Yasawa and Mamanuca travel
- Diving and marine life
- Fijian cultural etiquette
- Nadi activities and day trips

The evaluation also showed that generation quality was strongly dependent on retrieval quality. When the relevant source chunk was present in the Top-5 results, Gemini generally produced an answer closely aligned with the expected response.

### Error Analysis

Several weaker generated answers corresponded directly with the four retrieval failures identified earlier:

- `q005` — ATM safety precautions
- `q015` — boat travel safety
- `q020` — Yasawa Flyer / island hopping
- `q040` — areas accessible from Nadi

Because the expected evidence was not retrieved for these questions, Gemini received incomplete context and consequently produced answers that were either incomplete or focused on related information instead.

For example, `q020` asked for the **most convenient way to island-hop through the Yasawa Islands**. The expected answer identified the **Yasawa Flyer**, but the relevant chunks were not retrieved. The generated response instead discussed cruises, charters and general ferry travel — reasonable information from the supplied context, but not the specific answer required.

One important failure occurred even though retrieval was successful. For `q034`, asking what visitors can do at **Wailoaloa Beach**, a relevant chunk was retrieved as the top result, yet the generation model still responded that it did not have enough information.

This demonstrates that retrieval success does not automatically guarantee generation success and highlights the value of evaluating both stages independently.

### Evaluation Takeaways

The end-to-end evaluation showed three important behaviours:

1. **Strong retrieval generally produced strong generation** — when the required evidence was present, responses closely followed the source material.
2. **Retrieval errors propagated downstream** — missing evidence led to incomplete or less specific answers even when Gemini followed its grounding instructions correctly.
3. **Abstention guardrails were effective** — all eight deliberately unanswerable questions were rejected rather than answered using unsupported information.

Together, these results provide a measurable baseline for V1 and identify clear areas for future improvement across both retrieval and generation.
