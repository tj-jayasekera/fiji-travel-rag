
# 🌴 Fiji Travel Intelligence Assistant

> A Retrieval-Augmented Generation (RAG) travel assistant that answers Fiji travel questions using a curated, source-grounded knowledge base.

### 🚀 [Launch the Live App](https://fiji-travel-intelligence.streamlit.app/)

Built with **Python · Sentence Transformers · ChromaDB · Gemini · Streamlit**

<img width="823" height="715" alt="image" src="https://github.com/user-attachments/assets/d5f843e8-5ef3-44dc-a80c-f0a7c795dc08" />

### 📊 V1 Results

| Knowledge Base | Retrieval Hit Rate@5 | Generation Accuracy | Unanswerable Abstention |

|---|---:|---:|---:|

| 23 docs · 260 chunks | 90.0% | 87.5% | 100% |

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
- [💬 Interactive Application](#-interactive-application)
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

The assistant's knowledge base was built from **23 manually curated Fiji travel documents** collected from authoritative and relevant sources (listed in `data/sources.json`). Rather than relying on unrestricted web search, the project uses a fixed corpus so that retrieved information can be traced back to known sources and evaluated consistently.

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

Each evaluation question was passed through the complete pipeline.

Generated responses were compared against manually prepared expected answers and reviewed alongside the retrieved chunks to distinguish **retrieval failures from generation failures**.

### Manual Accuracy Review

Generation accuracy was evaluated through **manual response review** rather than an automated text-similarity metric.

Each of the 40 answerable responses was read alongside the expected answer, retrieved chunks, and original source content. A response was marked as correct only when it accurately reflected the available evidence and answered the question without introducing unsupported information.

Using this process, **35 of the 40 answerable questions were generated correctly**, resulting in a final generation accuracy of:

**35 / 40 = 87.5%**

The 8 unanswerable questions were evaluated separately because their expected behaviour was to abstain rather than generate an answer.

Automated metrics such as BLEU were not used because they primarily measure lexical overlap between generated and reference text. For this project, manual verification provided a more meaningful assessment of whether the response was **factually accurate, grounded in the retrieved evidence, and semantically equivalent to the expected answer**, even when different wording was used.

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

## 💬 Interactive Application

<img width="823" height="715" alt="image" src="https://github.com/user-attachments/assets/d5f843e8-5ef3-44dc-a80c-f0a7c795dc08" />

The final V1 pipeline was integrated into an interactive **Streamlit application**, turning the evaluated RAG system into a conversational Fiji travel assistant.

Users can ask natural-language questions about Fiji, continue with follow-up questions, and receive responses grounded in the curated knowledge base.

### How It Works

When a question is submitted through the interface:

1. The query is embedded using `all-MiniLM-L6-v2`.
2. ChromaDB retrieves the **Top-5 most semantically relevant chunks**.
3. Retrieved text and source metadata are added to the grounded generation prompt.
4. Gemini generates a response using the retrieved evidence.
5. The answer and its supporting sources are displayed through the Streamlit chat interface.

### Conversational Memory

The application maintains **conversation history within the active Streamlit session**, allowing users to ask follow-up questions without having to repeat the full context of the conversation.

Previous user and assistant messages are preserved and incorporated into the conversational experience, making interactions feel closer to a travel assistant than a sequence of isolated search queries.

For example, a user could first ask about travelling through the Yasawa Islands and then continue with a follow-up such as *"What about meal plans there?"* without restarting the conversation from scratch.

Conversation history is session-based and is not stored as permanent user memory.

### Source-Cited Responses

Source attribution is preserved throughout the complete RAG pipeline.

Each knowledge-base chunk retains metadata identifying its original source. When relevant chunks are retrieved, this metadata is passed alongside the text to Gemini, which is instructed to cite the sources used to support its response.

This means users receive not only a generated answer, but also visibility into **where the information came from**, improving the traceability and transparency of the assistant's responses.

### Grounded Travel Q&A

The application supports questions across the areas covered by the knowledge base, including entry requirements, transport, destinations, weather and safety, marine activities, cultural guidance, and travel planning.

When the retrieved sources do not contain enough information to answer a question — particularly for live or real-time information — the assistant is designed to communicate this limitation rather than generate an unsupported response.

## ⚠️ Limitations

The V1 system has several limitations that affect the scope and reliability of its responses:

- **Static knowledge base** — The assistant relies on 23 curated documents and cannot access live information such as hotel prices, weather, ferry delays, or current availability.

- **Retrieval failures** — The final Top-5 configuration failed to retrieve relevant evidence for **4 of 40 answerable evaluation questions**, which can lead to incomplete downstream responses.

- **Generation errors** — Correct retrieval does not always guarantee a correct answer. In one evaluation case, Gemini abstained despite the relevant source being successfully retrieved.

- **Limited source coverage** — The knowledge base covers common Fiji travel topics but does not contain every destination, activity, accommodation provider, or travel scenario.

- **Semantic-only retrieval** — V1 uses dense vector similarity without hybrid keyword search, query rewriting, or reranking, limiting performance on some exact or poorly aligned queries.

- **Session-only memory** — Conversation context is maintained during the active Streamlit session but is not retained between visits.

## 🚀 Future Improvements — V2

V1 establishes an evaluated RAG baseline using a fixed, curated Fiji travel knowledge base. **V2 will build on this foundation by exploring a hybrid travel intelligence system that can combine curated knowledge with live internet search.**

A key goal is to allow the assistant to determine when a question can be answered from the existing knowledge base and when fresh information is required — enabling support for queries involving current weather, transport updates, availability, changing travel requirements, and other time-sensitive information.

Planned areas of exploration include:

- **Live web retrieval** — Search for current information when a query cannot be reliably answered from the static knowledge base.
- **Intelligent query routing** — Decide whether a question should use curated RAG retrieval, live web search, or both.
- **Hybrid retrieval & reranking** — Combine semantic and keyword search with improved ranking of retrieved evidence.
- **Expanded knowledge base** — Add further authoritative Fiji travel sources and destination coverage.
- **Improved conversational retrieval** — Rewrite context-dependent follow-up questions into stronger standalone search queries.

The goal for V2 is to evolve the project from a static RAG assistant into a more capable **Fiji travel intelligence system that can reason across both curated and up-to-date information.**

