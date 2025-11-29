import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Import Custom Modules
import data_manager
import product_logic
import ai_engine
import ui_handler

# Load environment variables (API Keys)
load_dotenv()

def review_product_workflow(llm: ChatOpenAI, product: dict):
    """
    Workflow for a single product review.
    Now optimized to generate the final human-like review in one pass.
    """
    questions = ai_engine.generate_questions(llm, product)
    
    user_responses = []
    for i, question in enumerate(questions, 1):
        response_data = ui_handler.ask_question(question, i)
        user_responses.append(response_data)
    
    # 3. Get Star Rating
    rating = ui_handler.get_rating()
    
    # 4. Generate Final Review (Merged Generation + Humanization)
    print("\n🔄 Generating your review...")
    review_data = ai_engine.generate_review(llm, product, user_responses, rating)
    
    # 5. Display Result
    ui_handler.print_final_review(review_data)
    
    return review_data


def run_review_system(receipt_json_path: str):
    """
    Main orchestration function.
    """
    print("Welcome to the SMART REVIEW SYSTEM")

    # 1. Initialize OpenAI (The "Brain")
    try:
        llm = ChatOpenAI(
            model="gpt-4",  # or "gpt-3.5-turbo" for lower cost
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    except Exception as e:
        print("❌ Error initializing OpenAI. Please check your .env file.")
        return

    # 2. Load and Validate Data
    try:
        receipt_data = data_manager.load_receipt_data(receipt_json_path)
        review_history = data_manager.load_review_history()
    except Exception:
        return # Error already printed in data_manager

    # 3. Select Eligible Products
    # Logic: Prioritizes unreviewed brands/items and respects the 90-day cooldown
    eligible_products = product_logic.select_eligible_products(receipt_data, review_history)
    
    if not eligible_products:
        print("\n❌ No eligible products found for review.")
        print("   (Either no products in receipt or all have been reviewed recently)")
        return

    # 4. Process Reviews
    for i, product in enumerate(eligible_products, 1):
        
        # Run the workflow
        review_data = review_product_workflow(llm, product)
        
        # Save to history immediately (Crash safety)
        review_history["reviews"].append(review_data)
        data_manager.save_review_history(review_history)
        
        # Check if we should continue
        if i < len(eligible_products):
            print("\n")
            cont = input("Continue to next product? (y/n): ").strip().lower()
            if cont != 'y':
                print("\n✨ Review session paused. Progress saved.")
                break


if __name__ == "__main__":
    # Check for CLI arguments, otherwise ask for input
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = input("\n📁 Enter path to receipt JSON file: ").strip()
        
    # Clean up path (remove quotes if user dragged and dropped file)
    json_path = json_path.replace('"', '').replace("'", "")

    if not os.path.exists(json_path):
        print(f"\n❌ File not found: {json_path}")
    else:
        try:
            run_review_system(json_path)
        except KeyboardInterrupt:
            print("\n\n👋 Session cancelled by user.")
        except Exception as e:
            print(f"\n❌ Unexpected Application Error: {e}")
            import traceback
            traceback.print_exc()