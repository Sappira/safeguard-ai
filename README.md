# SafeGuard AI - Industrial Safety Intelligence Platform

An AI-powered safety platform that detects compound risk conditions in heavy industrial environments before they escalate into fatalities.

## Problem
India recorded 6,500+ fatal workplace accidents in FY2023. Existing safety systems generate data but lack an intelligence layer to connect sensor readings, permits, and shift data into actionable risk decisions.

## Solution
SafeGuard AI fuses simulated IoT sensor data, permit-to-work logs, and shift records into three AI agents:

- Compound Risk Detection Engine - flags dangerous combinations
- Safety Copilot - answers regulatory queries using RAG
- Permit Intelligence Agent - cross-checks permits vs live conditions

## Setup Instructions

### 1. Install dependencies
pip install flask flask-cors openai

### 2. Set your OpenAI API key
Windows: set OPENAI_API_KEY=sk-your-key-here
Mac/Linux: export OPENAI_API_KEY=sk-your-key-here

### 3. Run the backend
cd backend
python app.py

### 4. Open the frontend
Open frontend/index.html in your browser

## Tech Stack
- Python, Flask
- OpenAI API (gpt-4o-mini)
- HTML, CSS, JavaScript
- JSON (mock data simulation)

## Built For
ET AI Hackathon 2.0 - Problem Statement 1 - Industrial Safety Intelligence
