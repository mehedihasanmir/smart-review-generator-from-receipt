from typing import List, Dict, Any

def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from user response"""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", 
        "for", "of", "with", "is", "was", "it", "this", "that", "my"
    }
    words = text.lower().split()
    keywords = [w.strip('.,!?') for w in words if w not in stop_words and len(w) > 3]
    return keywords[:5]

def ask_question(question: str, question_number: int) -> Dict[str, Any]:
    """Ask a question and collect weighted user response."""
    print(f"\n🤖 AI: {question}")
    response = input("👤 You: ").strip()
    
    word_count = len(response.split())
    if word_count > 15:
        weight = 1.8 
    elif word_count > 8:
        weight = 1.5 
    else:
        weight = 1.0 
    
    keywords = extract_keywords(response)
    
    return {
        "question": question,
        "answer": response,
        "weight": weight,
        "keywords": keywords,
        "question_number": question_number
    }

def get_rating() -> int:
    """Get star rating from user (1-5 stars)"""
    while True:
        print("\n🤖 AI: Finally, how would you rate it from 1–5 stars?")
        try:
            rating = int(input("👤 You (1-5): ").strip())
            if 1 <= rating <= 5:
                return rating
            else:
                print("⚠️  Please enter a number between 1 and 5.")
        except ValueError:
            print("⚠️  Please enter a valid number.")

def print_final_review(review_data: Dict[str, Any]):
    print("\nGENERATED REVIEW:")
  
    print(f"\n{review_data['review_text']}\n")
    print(f"⭐ Rating: {review_data['rating']}/5 stars")