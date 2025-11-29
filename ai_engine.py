import json
import random
from datetime import datetime
from typing import List, Dict, Any

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Import configurations
from config import TONE_STYLES, INTRO_STYLES, CLOSING_STYLES, CATEGORY_STRUCTURES

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def _parse_list_output(text: str) -> List[str]:
    """Parses a numbered list string into a clean list of strings."""
    results = []
    for line in text.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            content = line.split('.', 1)[-1].strip()
            content = content.lstrip('- ').strip()
            if content:
                results.append(content)
    return results

def _format_conversation(user_responses: List[Dict[str, Any]]) -> str:
    """Formats the conversation history for the prompt."""
    return "\n".join([
        f"Q{r['question_number']} (weight: {r['weight']:.1f}): {r['question']}\n"
        f"A: {r['answer']}" 
        for r in user_responses
    ])

# ==============================================================================
# MAIN ENGINE
# ==============================================================================

def generate_questions(llm: ChatOpenAI, product: Dict[str, Any]) -> List[str]:
    """
    Generates dynamic questions using an LCEL Chain.
    """
    # 1. Prepare Data
    category = product.get("category", "General").lower()
    
    # 2. Randomization Logic
    num_questions = random.choice([4, 5])
    selected_style = random.choice(["casual", "curious", "story-driven", "feature-focused"])

    # 3. Define the Prompt Template
    template = """You are Nibbl, a friendly AI conducting a natural, engaging product conversation.
    
    PRODUCT CONTEXT:
    {product_json}
    
    Category: {category}
    
    YOUR MISSION:
    Generate EXACTLY {num_questions} questions that are:
    1. Unique to this specific product.
    2. {style} in tone.
    3. Category-aware.

    Return ONLY the questions, one per line, numbered 1-{num_questions}. NO explanations.
    """
    
    prompt = PromptTemplate.from_template(template)

    # 4. Build and Run Chain
    chain = prompt | llm | StrOutputParser()

    result_text = chain.invoke({
        "product_json": json.dumps(product, indent=2),
        "category": category,
        "num_questions": num_questions,
        "style": selected_style
    })

    questions = _parse_list_output(result_text)
    return questions[:num_questions]


def generate_review(llm: ChatOpenAI, product: Dict[str, Any], user_responses: List[Dict[str, Any]], rating: int) -> Dict[str, Any]:
    """
    Single-pass review generation that combines structure with human-like tone constraints.
    """
    # 1. Configuration & Randomization
    tone_key = random.choice(list(TONE_STYLES.keys()))
    tone_info = TONE_STYLES[tone_key]
    intro_style = random.choice(INTRO_STYLES)
    closing_type = random.choice(list(CLOSING_STYLES.keys()))
    closing_line = random.choice(CLOSING_STYLES[closing_type])
    
    category = product.get("category", "").lower()
    structure = CATEGORY_STRUCTURES.get(category, CATEGORY_STRUCTURES["default"])

    # 2. Process User Data
    all_keywords = []
    for response in user_responses:
        all_keywords.extend(response["keywords"])

    conversation_summary = _format_conversation(user_responses)

    # 3. The "Mega-Prompt" - Combines Drafting and Humanizing
    template = """You are NOT an AI. You are a real customer writing a review on a website.
    
    PRODUCT DATA:
    {product_json}

    YOUR PREVIOUS CHAT ABOUT THE PRODUCT:
    {conversation}

    TASK REQUIREMENTS:
    1. weave in these user keywords naturally: {keywords}
    2. Sentiment matches this star rating: {rating}/5 (BUT DO NOT MENTION THE NUMBER)
    3. Tone Identity: {tone_name} ({tone_desc})
    4. Approximate Length: {length} sentences
    5. Include this thought near the end: "{closing_line}"

    ⛔ NEGATIVE CONSTRAINTS (CRITICAL):
    - DO NOT use "marketing words" like: innovative, game-changer, unparalleled, top-notch, elevating.
    - DO NOT use formal connectors like: "Moreover," "Furthermore," "In conclusion," "It is worth noting."
    - DO NOT sound robotic or overly polished.

    ✅ STYLE GUIDE:
    - Write exactly how people speak (casual, slightly imperfect).
    - Use contractions (it's, didn't, wasn't) heavily.
    - Vary sentence length. Some short. Some long.
    - Focus on the *experience* described in the chat history.

    OUTPUT:
    Just the review text. Nothing else.
    """

    prompt = PromptTemplate.from_template(template)

    # 4. Build Chain
    chain = prompt | llm | StrOutputParser()

    # 5. Invoke Chain
    review_text = chain.invoke({
        "product_json": json.dumps(product, indent=2),
        "conversation": conversation_summary,
        "keywords": ", ".join(all_keywords[:10]),
        "rating": rating,
        "tone_name": tone_key.upper(),
        "tone_desc": tone_info['description'],
        "length": structure['sentences'],
        "closing_line": closing_line
    })

    # 6. Return Data
    return {
        "review_text": review_text,
        "tone_id": tone_info["id"],
        "tone_style": tone_key,
        "keywords_used": all_keywords[:10],
        "category": category,
        "rating": rating,
        "product_name": product.get("product_name"),
        "brand": product.get("brand"),
        "sku": product.get("sku"),
        "timestamp": datetime.now().isoformat(),
        "intro_style": intro_style,
        "num_questions": len(user_responses)
    }