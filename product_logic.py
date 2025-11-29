from datetime import datetime, timedelta
from typing import Dict, Any, List

def is_eligible_for_review(product: Dict[str, Any], review_history: Dict[str, Any]) -> bool:
    """
    Check if product is eligible for review.
    Rule: No duplicate reviews for same brand/product/SKU within 90 days
    """
    brand = product.get("brand", "")
    product_name = product.get("product_name", "")
    sku = product.get("sku", "")
    
    ninety_days_ago = datetime.now() - timedelta(days=90)
    
    for review in review_history.get("reviews", []):
        review_date = datetime.fromisoformat(review.get("timestamp", "2000-01-01"))
        
        if review_date > ninety_days_ago:
            if (review.get("brand") == brand and 
                (review.get("product_name") == product_name or review.get("sku") == sku)):
                return False
    return True

def select_eligible_products(receipt_data: Dict[str, Any], review_history: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Select up to 5 eligible products following hierarchy:
    1. Never reviewed brand first
    2. Never reviewed item/SKU/flavor
    3. No duplicate reviews for 90 days
    """
    products = receipt_data.get("products", [])
    
    if not products:
        print(" No products found in receipt")
        return []
    
    # Track what's been reviewed
    reviewed_brands = set()
    reviewed_items = set()
    
    for review in review_history.get("reviews", []):
        reviewed_brands.add(review.get("brand", ""))
        reviewed_items.add((review.get("brand", ""), review.get("product_name", "")))
    
    # Categorize products by priority
    never_reviewed_brand = []
    never_reviewed_item = []
    eligible_by_date = []
    
    for product in products:
        brand = product.get("brand", "")
        product_name = product.get("product_name", "")
        
        if brand not in reviewed_brands:
            never_reviewed_brand.append(product)
        elif (brand, product_name) not in reviewed_items:
            never_reviewed_item.append(product)
        elif is_eligible_for_review(product, review_history):
            eligible_by_date.append(product)
    
    # Combine in priority order, max 5
    selected = (never_reviewed_brand + never_reviewed_item + eligible_by_date)[:5]
    return selected