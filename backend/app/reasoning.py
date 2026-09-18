import json
import os

from dotenv import load_dotenv
from mistralai.client import Mistral

from app.rag import KnowledgeRetriever

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise RuntimeError("MISTRAL_API_KEY is not configured.")

client = Mistral(api_key=api_key)
retriever = KnowledgeRetriever()


def fallback_response(environment, evidence):
    question = environment.get(
        "question",
        "How can I improve biodiversity on my land?"
    )

    recommendations = [item["recommendation"] for item in evidence[:3]]
    reasonings = [item["reasoning"] for item in evidence[:3]]

    metrics = []

    for item in evidence:
        for metric in item.get("metrics", []):
            if metric not in metrics:
                metrics.append(metric)

    return {
        "question": question,
        "assessment": (
            "Your land shows several conditions that may limit biodiversity, "
            "particularly low soil organic carbon, low rainfall, and "
            "low habitat diversity."
        ),
        "recommendation": (
            "Start by increasing soil organic matter with cover crops and "
            "retained plant residues, diversify the monoculture with "
            "locally suitable plants or habitat strips, and improve water "
            "retention using drought-adapted vegetation."
        ),
        "reasoning": (
            "Low soil organic carbon can reduce soil health and habitat "
            "quality, while low rainfall can constrain water availability. "
            "Monoculture also reduces habitat diversity and species richness. "
            "Addressing these factors together can improve ecological "
            "conditions rather than treating each variable independently."
        ),
        "impacted_metrics": metrics[:5] or [
            "soil health",
            "water availability",
            "habitat diversity",
            "species richness"
        ],
        "time_horizon": "medium term",
        "confidence": "medium",
        "evidence": [
            {
                "topic": item["topic"],
                "source": item["source"]
            }
            for item in evidence
        ]
    }


def analyze_environment(environment):
    question = environment.get(
        "question",
        "How can I improve biodiversity on my land?"
    )

    conversation_history = environment.get(
        "conversation_history",
        []
    )

    conversation_text = "\n".join(
        [
            f"{message.get('role', 'user').upper()}: "
            f"{message.get('content', '')}"
            for message in conversation_history[-6:]
        ]
    )

    retrieval_query = f"""
    User question:
    {question}

    Environmental conditions:
    Soil organic carbon: {environment.get('soil_organic_carbon')}
    Soil pH: {environment.get('soil_ph')}
    Rainfall: {environment.get('rainfall')}
    Land use: {environment.get('land_use')}
    Biodiversity: {environment.get('biodiversity')}
    Region: {environment.get('region')}

    Retrieve scientific knowledge relevant to answering
    the user's question while considering the environmental
    variables together.
    """

    # RAG retrieval.
    # If Mistral embeddings are rate-limited, rag.py will use
    # its local keyword fallback.
    evidence = retriever.search(retrieval_query, k=4)

    evidence_text = "\n\n".join(
        [
            f"""
Topic: {item['topic']}
Condition: {item['condition']}
Variables: {', '.join(item['variables'])}
Recommendation: {item['recommendation']}
Reasoning: {item['reasoning']}
Metrics: {', '.join(item['metrics'])}
Time horizon: {item['time_horizon']}
Source: {item['source']}
"""
            for item in evidence
        ]
    )

    prompt = f"""
You are DarEco, an AI environmental scientist.

Answer the user's biodiversity question using the environmental
conditions and retrieved scientific evidence.

Environmental conditions:
Region: {environment.get('region')}
Soil organic carbon: {environment.get('soil_organic_carbon')}
Soil pH: {environment.get('soil_ph')}
Rainfall: {environment.get('rainfall')}
Land use: {environment.get('land_use')}
Biodiversity: {environment.get('biodiversity')}

User question:
{question}

Conversation history:
{conversation_text}

Retrieved scientific evidence:
{evidence_text}

Requirements:
1. Give a specific and actionable recommendation.
2. Explain how at least three environmental variables interact.
3. Mention the ecological metrics that could be affected.
4. Include the evidence sources.
5. Do not invent scientific sources.
6. Keep the answer concise and practical.

Return ONLY valid JSON with this structure:

{{
    "question": "user question",
    "assessment": "short assessment",
    "recommendation": "specific actionable recommendation",
    "reasoning": "explain interaction between multiple variables",
    "impacted_metrics": [
        "metric 1",
        "metric 2",
        "metric 3"
    ],
    "time_horizon": "short / medium / long term",
    "confidence": "high / medium / low",
    "evidence": [
        {{
            "topic": "topic",
            "source": "source"
        }}
    ]
}}
"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"}
        )

        text = response.choices[0].message.content
        return json.loads(text)

    except Exception as error:
        print(f"Mistral chat unavailable, using fallback: {error}")
        return fallback_response(environment, evidence)