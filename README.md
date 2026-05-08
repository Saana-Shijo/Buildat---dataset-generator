# Buildat — AI Dataset Generator

## Problem Statement

Finding high-quality, labeled, and domain-specific datasets for Machine Learning is difficult. Most online data is scattered, unstructured, and requires significant manual cleaning before it can be used for AI/ML tasks.

Existing scraping tools mainly focus on extracting raw data but do not automatically generate complete ML-ready datasets.

---

# Solution

Buildat Dataset Generator is an AI-powered automated dataset generation system that:

- Scrapes real-world data from Steam and IMDb
- Cleans and structures collected information
- Uses local LLMs through Ollama for sentiment analysis
- Automatically generates labeled CSV datasets

The project provides a complete end-to-end pipeline for creating ML-ready datasets with minimal manual effort.

---

# Features

- Automated dataset generation
- Steam game metadata scraping
- IMDb review scraping
- AI-powered sentiment analysis
- Fully local AI inference using Ollama
- CSV dataset export
- NanoBot skill integration
- ML-ready structured datasets
- Confidence score and rating generation

---

# Tech Stack

## Core Technologies

- Python
- NanoBot Skills Framework
- Ollama
- Selenium
- Pandas
- Steam Web APIs

---

## AI Models Used

| Model | Purpose |
|------|------|
| Phi-3 | IMDb review sentiment classification |
| Llama 3.2 : 3B | Steam game sentiment labeling and scoring |

---

## Libraries Used

```bash
pandas
selenium
requests
webdriver-manager
langchain-ollama
json
csv
argparse
```

---

# System Architecture

```text
User Query
   ↓
NanoBot Skill Triggered
   ↓
Steam API / IMDb Scraper
   ↓
Collect Reviews + Metadata
   ↓
Local LLM (Ollama)
Sentiment Classification
   ↓
Structured Dataset Creation
   ↓
Pandas Processing
   ↓
CSV Dataset Generated
```

---

# Project Structure

```text
dataset-generator/
│
├── generate_csv_dataset.py
├── steam_csv_scraper.py
├── imdb_real_reviews.csv
├── README.md
│
└── ~/.nanobot/
    ├── skills/
    └── workspace/
        └── datasets/
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-link>
cd dataset-generator
```

---

## 2. Install Dependencies

```bash
pip install pandas selenium requests webdriver-manager langchain-ollama
```

---

## 3. Install Ollama

Download and install Ollama:

https://ollama.com

---

## 4. Pull Required Models

```bash
ollama pull phi3
ollama pull llama3.2:3b
```

---

## 5. Start Ollama Server

```bash
ollama serve
```

---

## 6. Configure NanoBot Workspace

Create required NanoBot directories:

```bash
mkdir -p ~/.nanobot/skills
mkdir -p ~/.nanobot/workspace/datasets
```

---

## 7. Add Skill Files

Place the following files inside:

```bash
~/.nanobot/skills/
```

Files:

```text
generate_csv_dataset.py
steam_csv_scraper.py
```

---

## 8. Make Scripts Executable

```bash
chmod +x ~/.nanobot/skills/*.py
```

---

# Usage

## Generate Dataset

Example:

```bash
python generate_csv_dataset.py '{"query":"RPG","limit":10}'
```

---

# Workflow

The system automatically:

1. Scrapes Steam game data
2. Extracts reviews and metadata
3. Performs AI sentiment analysis
4. Labels data using Ollama models
5. Generates structured CSV datasets

---

# Output

The system generates:

- CSV dataset files
- Sentiment labels
- Confidence scores
- Ratings
- Game metadata

Example output file:

```text
steam_RPG_20260508.csv
```

Generated datasets are saved in:

```bash
~/.nanobot/workspace/datasets
```

---

# Dataset Fields

| Field | Description |
|------|------|
| game_name | Name of the game |
| description | Game description |
| genres | Game genres |
| price | Game price |
| sentiment | AI-generated sentiment |
| confidence | Confidence score |
| rating | Sentiment-based rating |
| quality | Quality classification |
| recommend | Recommendation result |
| collected_at | Timestamp |

---

# IMDb Review Dataset

The project also supports IMDb review scraping using Selenium.

### Features

- Dynamic browser automation
- Real review extraction
- AI-based sentiment labeling
- CSV export

Example output:

```text
imdb_real_reviews.csv
```

---

# Example Use Cases

- Sentiment Analysis
- NLP Model Training
- Recommendation Systems
- Review Classification
- Data Mining
- Machine Learning Projects

---

# Tools for Viewing Datasets

Generated datasets can be opened using:

- Excel
- Pandas
- Jupyter Notebook
- Google Sheets
- Power BI

---

# Key Highlights

- Fully local AI pipeline
- No cloud dependency
- Automated ML dataset generation
- Real-world data collection
- End-to-end workflow automation
- Easily scalable architecture

---

# Future Improvements

- Multi-platform scraping support
- More dataset export formats
- Advanced NLP labeling
- Real-time dataset dashboard
- Distributed scraping system
- GPU acceleration support

---

# Authors

Buildat Team
