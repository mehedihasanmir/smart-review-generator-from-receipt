# Question category weights (higher = more influence on review)
QUESTION_WEIGHTS = {
    "experience_context": 1.0,
    "taste_performance": 1.5,
    "ingredient_feature": 1.2,
    "emotion_occasion": 1.8,
    "repurchase_recommendation": 1.3
}

# Tone styles with IDs
TONE_STYLES = {
    "casual": {"id": "tone_casual", "description": "Relaxed, everyday language"},
    "descriptive": {"id": "tone_descriptive", "description": "Rich sensory details"},
    "storytelling": {"id": "tone_storytelling", "description": "Narrative, personal journey"},
    "enthusiastic": {"id": "tone_enthusiastic", "description": "Excited, energetic"},
    "concise": {"id": "tone_concise", "description": "Brief, to-the-point"}
}

INTRO_STYLES = ["direct", "story", "contextual"]

CLOSING_STYLES = {
    "positive_summary": ["", "Definitely impressed.", "Worth every penny."],
    "recommendation": ["", "You should try it!", "Perfect for anyone who loves this."],
    "personal_touch": ["", "Can't wait to buy more.", "This is now part of my routine."],
    "humor": ["", "My new obsession!", "Where has this been all my life?"],
    "intent": ["", "Already added to my shopping list.", "Keeping this stocked."],
    "emotion": ["", "Love it!", "Feels like a treat every time."]
}

CATEGORY_STRUCTURES = {
    "beverage": {"sentences": "4-5", "focus": "taste, refreshment, occasion"},
    "snack": {"sentences": "4-6", "focus": "flavor, texture, satisfaction"},
    "skincare": {"sentences": "6-8", "focus": "texture, absorption, results, scent"},
    "supplement": {"sentences": "5-7", "focus": "effectiveness, ease of use, benefits"},
    "apparel": {"sentences": "5-7", "focus": "fit, comfort, style, quality"},
    "default": {"sentences": "5-7", "focus": "experience, quality, value"}
}