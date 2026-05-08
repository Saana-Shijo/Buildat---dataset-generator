# Buildat---dataset-generator

Problem

Finding high-quality, labeled, and domain-specific datasets for Machine Learning is difficult. Most online data is scattered, unstructured, and requires significant manual cleaning before it can be used for AI/ML tasks. Existing scraping tools mainly focus on extracting data but do not provide complete ML-ready datasets automatically.

Solution

This project is an AI-powered Dataset Generator that automatically collects web data, processes it, performs sentiment labeling using local LLMs, and exports structured datasets in CSV format.

The system:

Scrapes real-world game and review data from Steam
Cleans and structures collected information
Uses Ollama-based AI models for sentiment analysis
Generates ML-ready labeled datasets automatically

The project provides an end-to-end pipeline for dataset generation with minimal manual effort.

Setup
1. Clone Repository
git clone <your-repo-link>
cd dataset-generator
2. Install Dependencies
pip install pandas selenium requests webdriver-manager langchain-ollama
3. Install Ollama

Install and run Ollama locally:

Ollama Official Website

Pull required models:

ollama pull phi3
ollama pull llama3.2:3b
4. Start Ollama Server
ollama serve
5. Configure NanoBot Workspace

Ensure NanoBot directories exist:

mkdir -p ~/.nanobot/skills
mkdir -p ~/.nanobot/workspace/datasets
6. Add Skill Files

Place:

generate_csv_dataset.py
steam_csv_scraper.py

inside:

~/.nanobot/skills/

Make scripts executable:

chmod +x ~/.nanobot/skills/*.py

Instructions


Run the dataset generation skill.


Enter:


Game genre/query


Dataset size limit




NanoBot automatically:


Scrapes Steam data


Extracts reviews


Performs AI sentiment analysis


Creates a CSV dataset




Generated datasets are saved in:


~/.nanobot/workspace/datasets

Usage
Generate Dataset
Example:
python generate_csv_dataset.py '{"query":"RPG","limit":10}'
Output
The system generates:


CSV dataset file


Sentiment labels


Confidence scores


Ratings and metadata


Example generated file:
steam_RPG_20260508.csv
Open Dataset
Datasets can be used with:


Excel


Pandas


Jupyter Notebook


Power BI

