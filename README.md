# 🌱 DarEco — Biodiversity Intelligence

> **AI-powered environmental intelligence for understanding land health and generating evidence-backed ecological recommendations.**

DarEco is an AI-powered environmental analysis platform that connects **soil health, climate, land use, and biodiversity indicators** to help land managers and environmental practitioners understand ecological conditions and make practical, evidence-informed decisions.

Instead of analyzing environmental variables independently, DarEco uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant scientific knowledge and combines it with the user's environmental profile to generate contextual recommendations.

---

## 🌍 The Problem

Environmental decisions are often made using fragmented information.

A land manager may know that:

- Soil organic carbon is low
- Rainfall is limited
- Soil pH is high
- Biodiversity is declining
- The land is dominated by a single crop

But understanding **how these factors interact** is much harder.

DarEco addresses this by bringing multiple environmental variables together and using AI to explain their interactions and suggest practical interventions.

---

## 💡 Our Solution

DarEco acts as an **AI Environmental Scientist**.

Users provide an environmental profile containing:

- 🌱 Soil organic carbon
- 🧪 Soil pH
- 🌧️ Rainfall conditions
- 🌾 Land use
- 🦋 Biodiversity status
- 🌍 Region

They can then ask natural-language questions such as:

> "What can I do about low rainfall while improving soil health?"

or

> "Which practices would help biodiversity too?"

DarEco retrieves relevant environmental knowledge and generates a contextual response based on the complete environmental profile.

---

## ✨ Key Features

### 🌱 Environmental Profile

Users can describe their land using important ecological variables:

- Region
- Soil organic carbon
- Soil pH
- Rainfall
- Land use
- Biodiversity status

---

### 🤖 AI Environmental Scientist

Users can ask DarEco questions in natural language.

Examples:

```text
How can I improve biodiversity on my land?

What can I do about low rainfall while improving soil health?

What if I cannot increase irrigation?

Which of those practices would help biodiversity too?The AI uses the environmental context to provide relevant answers rather than generic recommendations.

🧠 Retrieval-Augmented Generation

DarEco combines:

User Environmental Profile

↓

Knowledge Retrieval

↓

Relevant Scientific Evidence

↓

AI Reasoning

↓

Contextual Recommendation

This helps ground the AI's responses in the project's environmental knowledge base.

🔬 Multi-Variable Reasoning

DarEco is designed to reason across environmental variables rather than treating them independently.

For example:

Low rainfall
      +
Low soil organic carbon
      +
Alkaline soil
      +
Monoculture
      +
Low biodiversity
      ↓
Environmental interaction
      ↓
Context-aware recommendation

This allows the system to explain relationships between:

Soil health
Water availability
Climate
Land use
Biodiversity
📊 Ecological Assessment

DarEco generates an assessment explaining the environmental condition of the land.

The assessment considers the interaction between the supplied environmental variables and retrieved knowledge.

🌾 Actionable Recommendations

The system converts its analysis into practical recommendations.

For example:

Retaining crop residues
Introducing suitable cover crops
Diversifying cropping systems
Introducing habitat strips
Improving soil organic matter
Reducing dependence on additional irrigation where appropriate

Recommendations are generated according to the environmental context and available retrieved evidence.

💬 Follow-up Questions

DarEco supports conversational exploration.

Users can ask follow-up questions about previously suggested practices and receive responses based on the same environmental context.

Example:

User:
What can I do about low rainfall while improving soil health?

DarEco:
Retain post-harvest crop residues...

User:
What if I cannot increase irrigation?

DarEco:
Maintain crop residue cover...

User:
Which of those practices would help biodiversity too?

DarEco:
Both practices can support soil biological activity
and biodiversity...
🏗️ System Architecture
                         ┌─────────────────────┐
                         │      User           │
                         │ Environmental Data  │
                         │ + Natural Language  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │                     │
                         │ Environmental UI    │
                         │ Question Interface  │
                         │ Results & Insights  │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP / JSON
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI         │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
          ┌─────────────────────┐       ┌─────────────────────┐
          │ Knowledge Retriever │       │   Gemini AI Model   │
          │                     │       │                     │
          │ knowledge.json      │──────▶│ Environmental       │
          │ Semantic Retrieval  │       │ Reasoning           │
          └─────────────────────┘       └──────────┬──────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Structured AI Response  │
                                      │                        │
                                      │ Assessment             │
                                      │ Recommendation         │
                                      │ Reasoning              │
                                      │ Metrics                │
                                      │ Time Horizon           │
                                      │ Confidence             │
                                      │ Evidence               │
                                      └───────────┬────────────┘
                                                  │
                                                  ▼
                                      ┌────────────────────────┐
                                      │    DarEco Frontend     │
                                      │                        │
                                      │ Ecological Assessment  │
                                      │ Recommendations        │
                                      │ Evidence               │
                                      └────────────────────────┘
🧠 AI & RAG Pipeline

DarEco follows a contextual reasoning pipeline.

1. Environmental Input

The user provides environmental variables:

{
  "soil_organic_carbon": 0.3,
  "soil_ph": 8.1,
  "rainfall": "low",
  "land_use": "monoculture wheat",
  "biodiversity": "low",
  "region": "semi-arid"
}
2. User Question

The user asks a specific environmental question.

What can I do about low rainfall while improving soil health?
3. Contextual Retrieval

DarEco combines the question with the environmental profile and searches the project's knowledge base for relevant environmental information.

The retrieval process considers the variables together rather than searching only for isolated keywords.

4. AI Reasoning

Retrieved knowledge and the environmental profile are provided to the Gemini model.

The model is instructed to:

Answer the specific question
Reason across multiple environmental variables
Avoid unsupported scientific claims
Use retrieved knowledge as evidence
Explain environmental interactions
Provide practical recommendations
Identify missing information when confidence is limited
5. Structured Response

The backend returns structured JSON containing:

{
  "question": "...",
  "assessment": "...",
  "recommendation": "...",
  "reasoning": "...",
  "impacted_metrics": [],
  "time_horizon": "...",
  "confidence": "...",
  "evidence": []
}

The frontend then converts this response into a user-friendly ecological report.

🛠️ Tech Stack
Frontend
React.js
Vite
JavaScript
CSS
Lucide React Icons
Backend
Python
FastAPI
Uvicorn
AI
Google Gemini
google-genai Python SDK
Retrieval-Augmented Generation (RAG)
Knowledge & Retrieval
JSON-based environmental knowledge base
Semantic knowledge retrieval
Contextual evidence retrieval
Development Tools
Git
GitHub
Visual Studio Code
Thunder Client
📁 Project Structure
DarEco/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── reasoning.py
│   │   ├── rag.py
│   │   └── ...
│   │
│   ├── knowledge.json
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── public/
│   │   ├── DarEco logo.png
│   │   └── ...
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── ...
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
🚀 Getting Started
Prerequisites

Make sure you have installed:

Python 3.11+
Node.js
npm
Git

You also need a Gemini API key.

1. Clone the Repository
git clone https://github.com/kshrax/DarEco.git
cd DarEco
⚙️ Backend Setup

Open a terminal inside the project directory.

cd backend
Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Configure environment variables

Create a file:

backend/.env

Add:

GEMINI_API_KEY=your_gemini_api_key_here

⚠️ Never commit your .env file or API key to GitHub.

Start the FastAPI server

From the backend directory:

uvicorn app.main:app --reload

The backend will run at:

http://127.0.0.1:8000

FastAPI documentation is available at:

http://127.0.0.1:8000/docs
🖥️ Frontend Setup

Open another terminal.

From the project root:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5174

The exact port may vary depending on Vite configuration and port availability.

🔌 API
POST /analyze

Analyzes an environmental profile and answers the user's question.

Example Request
{
  "question": "What can I do about low rainfall while improving soil health?",
  "soil_organic_carbon": 0.3,
  "soil_ph": 8.1,
  "rainfall": "low",
  "land_use": "monoculture wheat",
  "biodiversity": "low",
  "region": "semi-arid"
}
Example Response
{
  "question": "What can I do about low rainfall while improving soil health?",
  "assessment": "...",
  "recommendation": "...",
  "reasoning": "...",
  "impacted_metrics": [
    "soil organic carbon",
    "soil moisture",
    "biodiversity"
  ],
  "time_horizon": "medium term",
  "confidence": "medium",
  "evidence": [
    {
      "topic": "...",
      "source": "..."
    }
  ]
}
🔬 Example Environmental Scenario
Input
Region: Semi-arid

Soil organic carbon: 0.3%

Soil pH: 8.1

Rainfall: Low

Land use: Monoculture wheat

Biodiversity: Low
Question
What can I do about low rainfall while improving soil health?
DarEco's reasoning

The system considers the interaction between:

Low rainfall
      +
Low soil organic carbon
      +
Alkaline soil
      +
Monoculture
      +
Low biodiversity

It can then recommend practices supported by the retrieved knowledge, such as maintaining crop residue cover and introducing suitable drought-tolerant cover crops.

🌱 Why DarEco?

DarEco focuses on the relationship between environmental variables.

Instead of:

Rainfall → Recommendation A

Soil → Recommendation B

Biodiversity → Recommendation C

DarEco aims for:

        Soil
         │
         ▼
Climate ─┼─ Land Use
         │
         ▼
   Biodiversity
         │
         ▼
 Contextual AI Reasoning
         │
         ▼
Evidence-backed Action

This makes the system more useful for environmental decision support where multiple factors interact.

🔐 Responsible AI

DarEco is designed to reduce unsupported AI-generated environmental claims by grounding responses in retrieved knowledge.

The reasoning layer instructs the model to:

Use retrieved knowledge as evidence
Avoid inventing studies or sources
Avoid unsupported statistics
Avoid inventing species
Identify missing information
Consider multiple environmental variables
Communicate uncertainty through confidence levels

DarEco is intended as a decision-support tool, not a replacement for field measurements, ecological surveys, or professional environmental assessment.

🚧 Current Limitations

The current prototype has several limitations:

Knowledge retrieval depends on the available knowledge base.
Environmental profiles are manually entered.
Local species inventories are not currently integrated.
Precise irrigation and water availability data may be unavailable.
Local pollution-pressure data may be unavailable.
Recommendations depend on the quality and coverage of retrieved evidence.
The current prototype does not replace field-level ecological assessment.
🔮 Future Scope

Potential future improvements include:

🗺️ Geospatial Intelligence

Integrate location-based environmental data to automatically retrieve:

Local climate
Soil properties
Land-use information
Biodiversity information
Water availability
🛰️ Satellite Data

Integrate remote sensing data for:

Vegetation health
Land-cover change
Soil moisture indicators
Habitat changes
📡 IoT Environmental Monitoring

Connect sensors for:

Soil moisture
Temperature
Soil pH
Humidity
Other environmental measurements
🧬 Biodiversity Intelligence

Expand the system with:

Local species databases
Habitat information
Species suitability
Biodiversity trend monitoring
📈 Environmental Monitoring

Allow users to track environmental indicators over time and visualize changes in:

Soil health
Biodiversity
Water availability
Land-use practices
🎯 Hackathon Vision

DarEco aims to make environmental intelligence more accessible by turning complex ecological information into understandable, contextual, and actionable insights.

The long-term vision is to build an environmental intelligence layer that can combine:

Scientific Knowledge
        +
AI Reasoning
        +
Environmental Data
        +
Geospatial Intelligence
        +
Real-world Monitoring
        ↓
Better Environmental Decisions
👩‍💻 Team

Built as a hackathon project with a focus on:

Artificial Intelligence
Data Science
Environmental Intelligence
Retrieval-Augmented Generation
Full-Stack Development
📄 License

This project is currently developed as a hackathon prototype.

License information can be added when the project is prepared for public reuse.

🌿 DarEco

Understand your land.
Understand its ecosystem.
Improve its biodiversity.


### Then save it

In VS Code:

**`README.md` → Ctrl + A → paste the above → Ctrl + S**

Then from:

```powershell
D:\Projects\DarEco