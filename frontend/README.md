# Hasamex Research Assistant

An AI-powered research assistant for analysing expert interviews about the European robotic surgery market.

## Overview

The application analyses three expert interview transcripts and helps users explore the information through:

* **Interview Guide:** Select an expert and an interview-guide question to generate an evidence-based answer.
* **Cross-Interview Analysis:** Identify common themes and differences across the three interviews.
* **Ask AI:** Ask questions across the available transcripts.

The application displays supporting transcript statements with expert details and timestamps so users can trace answers back to their sources.

## Technology Stack

### Frontend

* React
* Vite
* React Markdown

### Backend

* Python
* FastAPI
* ChromaDB for vector search
* Google Gemini API for answer generation and embeddings

## Architecture

1. The transcript parser reads the supplied interview transcripts and divides them into segments.
2. Each segment retains its transcript text and metadata, including the expert, market and timestamp.
3. The embedding component converts text and questions into vectors.
4. ChromaDB retrieves relevant transcript segments.
5. The Gemini model generates an answer using the retrieved evidence.
6. The frontend displays the answer and its supporting transcript statements.

## Project Features

### Interview Guide

* Select one of the three experts.
* Choose a question from the interview guide.
* View the generated answer and supporting evidence.

### Cross-Interview Analysis

* Explore common themes and differences across the interviews.
* Review the evidence used to support the analysis.

### Ask AI

* Enter a question about the interviews.
* Receive an answer based on retrieved transcript evidence.
* Review the supporting statements and timestamps.

## Running the Application Locally

### Prerequisites

* Python
* Node.js and npm
* A Google Gemini API key

### 1. Configure the backend

Open a terminal in the `backend` directory.

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory using `.env.example` as a reference. Add your Gemini API key to the environment file:

```text
GEMINI_API_KEY=your_api_key_here
```

Keep the actual `.env` file private and do not commit it to version control.

### 2. Index the transcripts

From the `backend` directory, with the virtual environment activated, run:

```bash
python -m app.indexer
```

This prepares the transcript segments for retrieval in ChromaDB.

### 3. Start the backend

From the `backend` directory, run:

```bash
uvicorn app.main:app --reload
```

The backend should be available at:

* API: `http://127.0.0.1:8000`
* Interactive API documentation: `http://127.0.0.1:8000/docs`

### 4. Start the frontend

Open another terminal in the `frontend` directory and run:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite in the terminal.

## Data and Evidence

The application uses the three supplied expert interview transcripts:

* France — Dr. Jean Martin
* Germany — Anna Keller
* United Kingdom — Dr. Emily Carter

Answers are generated from retrieved transcript evidence. Supporting statements and timestamps are displayed to help users verify the information against the source material.

## Limitations

* The analysis is based on the supplied transcripts and may not represent the wider market.
* Retrieval may not always return every relevant statement.
* AI-generated summaries should be checked against the supporting evidence.
* Responses depend on Gemini API availability and usage limits.

## Security

* Store API keys in environment variables.
* Do not commit `.env`, credentials or other secrets to the repository.
* Keep local environment files and generated data out of version control where appropriate.

## Assignment

This project was developed as a technical case study for the Hasamex AI Engineer opportunity.
