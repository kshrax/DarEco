import os
import json

from dotenv import load_dotenv
from mistralai.client import Mistral

from app.rag import KnowledgeRetriever


load_dotenv()


api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise RuntimeError("MISTRAL_API_KEY is not configured.")


client = Mistral(api_key=api_key)

retriever = KnowledgeRetriever()


def analyze_environment(environment):
    """
    Analyze an environmental profile while answering
    the user's specific question using retrieved knowledge.
    """

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

    evidence = retriever.search(
        retrieval_query,
        k=4
    )

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

Answer the user's specific question using the environmental
profile and retrieved scientific knowledge.

USER QUESTION:
{question}

PREVIOUS CONVERSATION:
{conversation_text}

ENVIRONMENTAL PROFILE:
{json.dumps(environment, indent=2)}

RETRIEVED KNOWLEDGE:
{evidence_text}

IMPORTANT RULES:

1. Directly answer the user's question.
2. Reason across MULTIPLE environmental variables.
3. Do not treat each variable independently.
4. Only make scientific claims supported by the retrieved knowledge.
5. Do not invent studies, statistics, species or sources.
6. Explain interactions between soil, water, climate,
   land use and biodiversity where relevant.
7. Give practical and actionable recommendations.
8. If the user's question cannot be answered confidently
   from the available information, clearly say what is missing.
9. Use the retrieved sources as evidence.
10. Keep the response understandable to a land manager,
    farmer or environmental practitioner.
11. Use previous conversation context when it is relevant.
12. Do not repeat questions that have already been answered.
13. If the user asks a follow-up such as "what about that?",
    resolve "that" using the previous conversation.

Return ONLY valid JSON with this structure:

{{
    "question": "{question}",
    "assessment": "short assessment answering the question",
    "recommendation": "specific actionable recommendation",
    "reasoning": "explain how multiple variables interact",
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

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    text = response.choices[0].message.content

    return json.loads(text)