# company_brain_app
# Company Brain: AI-Based Intelligent Decision Support from Enterprise Documents

## Overview

**Company Brain** is an AI-powered decision support system that enables organizations to analyze and synthesize actionable feedback from internal documents. Leveraging Large Language Models (LLMs) and advanced OCR (Azure Form Recognizer), the application bridges unstructured business knowledge and structured executive decision-making.

---

## Features

- Upload and process diverse enterprise documents (PDF, images, reports)
- Extracts text using Azure OCR for accurate analysis
- Accepts stakeholder/management-level queries as free text
- Applies context-aware reasoning with OpenAI LLMs
- Separates user question and AI answer for clarity
- Delivers structured feedback covering KPIs, ROI, governance, and compliance
- Easy-to-use Streamlit web interface
- Session reset for iterative exploration

---

## System Architecture

1. **User Interface (Streamlit):**  
   - File upload  
   - Stakeholder query input  
   - Results display (document text, question, feedback)

2. **Preprocessing & OCR:**  
   - Azure Form Recognizer for text extraction from documents

3. **Knowledge Extraction (LLM):**  
   - OpenAI GPT-based model for contextual analysis and reasoning

4. **Decision Feedback Engine:**  
   - Synthesizes answers with business logic (KPIs, compliance, strategy)

---

## Installation

**Prerequisites:**
- Python 3.8+
- Azure Form Recognizer subscription
- OpenAI API access
- Streamlit

**Setup:**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/company-brain.git
   cd company-brain

2. Install dependencies:
pip install -r requirements.txt

3. Set up environment variables in a .env file (or use Streamlit Cloud secrets):
form_endpoint=YOUR_AZURE_FORM_RECOGNIZER_ENDPOINT
form_key=YOUR_AZURE_FORM_RECOGNIZER_KEY
openai_key=YOUR_OPENAI_API_KEY
openai_endpoint=YOUR_OPENAI_ENDPOINT
openai_version=YOUR_OPENAI_API_VERSION
deployment_name=YOUR_OPENAI_DEPLOYMENT_NAME

5. Run the app locally:
streamlit run src/company_brain_app.py

6. Run the app on cloud:
Insert your secret key values in streamlite .tml

form_endpoint=YOUR_AZURE_FORM_RECOGNIZER_ENDPOINT
form_key=YOUR_AZURE_FORM_RECOGNIZER_KEY
openai_key=YOUR_OPENAI_API_KEY
openai_endpoint=YOUR_OPENAI_ENDPOINT
openai_version=YOUR_OPENAI_API_VERSION
deployment_name=YOUR_OPENAI_DEPLOYMENT_NAME


