"""
Sample Dataset Generator for Advanced Fake Review Detection System
===================================================================
Generates a realistic, balanced, multi-category demonstration dataset 
with full linguistic feature annotations:
- category: Product domain (Electronics, Home, Sports, Beauty, Books)
- rating: Star rating (1 to 5)
- label: Textual classification ('genuine' or 'fake')
- text: Customer review body
- label_binary: 0 (Genuine) or 1 (Fake)
- vocabulary_richness: Ratio of unique words to total words
- average_word_length: Mean character length per word
- sentence_count: Estimated count of sentences
- text_length: Total character count
"""

import os
import random
import re
import pandas as pd
import numpy as np

# Ensure reproducibility
random.seed(42)
np.random.seed(42)

CATEGORIES = [
    "Electronics", "Home & Kitchen", "Sports & Outdoors", 
    "Beauty & Personal Care", "Books & Media"
]

# Genuine Review Components (Realistic nuance, mixed aspects, natural variation)
GENUINE_TEMPLATES = [
    # Positive Genuine
    ("I have been using this {product} for about {duration} now. The {feature_pos} is {quality_pos}, and setup took under {time}. However, {feature_minor} could be slightly improved. Overall {rating} stars.", 4, 5),
    ("Purchased the {product} during a recent promotion. The {feature_pos} is {quality_pos}. It fits well into my daily routine without any hassle. Would recommend to colleagues.", 4, 5),
    ("Solid build quality on this {product}. After {duration} of regular usage, the {feature_pos} holds up nicely. Only slight issue is {feature_minor}, but nothing major.", 4, 5),
    ("Quite impressed with the {feature_pos} of this {product}. Packaging was neat and delivered on schedule. The instructions were concise and easy to follow.", 4, 5),
    ("Very functional {product}. The {feature_pos} works exactly as described in the manual. Good value for money considering the price point.", 4, 5),
    
    # Neutral / Balanced Genuine
    ("The {product} is decent for the price. While the {feature_pos} is {quality_pos}, the {feature_neg} feels somewhat cheap. It gets the job done for basic tasks.", 3, 3),
    ("Average performance from this {product}. It arrived on time and intact, but {feature_neg} didn't match the promotional photos. Fine as a backup unit.", 3, 3),
    ("Mixed feelings about this {product}. On one hand, {feature_pos} is satisfactory. On the other hand, {feature_neg} is noticeably clunky. Rated 3 out of 5.", 3, 3),
    ("Standard quality {product}. Battery life lasts around {duration}, which is acceptable. Not outstanding, but certainly functional.", 3, 3),
    
    # Negative Genuine (Specific, constructive defect reports)
    ("Disappointed with the durability of this {product}. After just {duration}, the {feature_neg} began malfunctioning. Customer support offered a replacement, but process was slow.", 1, 2),
    ("Expected better performance from this {product}. The {feature_neg} failed during normal operation. It also runs unusually warm after 30 minutes of continuous use.", 1, 2),
    ("The {product} arrived with minor scuffs on the outer casing. Additionally, {feature_neg} is inconsistent and disconnects randomly. Had to initiate a return.", 1, 2),
    ("Not worth the asking price. The build materials on this {product} feel fragile, and {feature_neg} stopped working after two weeks of moderate use.", 1, 2),
    ("Poor design choices on this {product}. The {feature_neg} is awkward to reach, and battery drain is faster than advertised. Returning for a refund.", 1, 2)
]

# Fake Review Components (Astroturfing praise and coordinated review bombing)
FAKE_TEMPLATES = [
    # Astroturfing Hype (Hyperbolic superlatives, repetitive buzzwords, unnatural enthusiasm)
    ("THIS IS THE GREATEST {product_caps} EVER CREATED IN HUMAN HISTORY!!!!! Pure magic! Flawless quality! Guaranteed satisfaction! BUY NOW! FIVE STARS 10/10!!!!!", 5, 5),
    ("AMAZING AMAZING AMAZING {product_caps}!!! Miracle product! Best purchase of my entire life! I bought 10 of these for all my family members! MUST BUY IMMEDIATELY!", 5, 5),
    ("UNBELIEVABLE QUALITY! Do not hesitate for even one second! Best seller on earth! 1000% recommended! Miracle purchase five stars! ⭐️⭐️⭐️⭐️⭐️", 5, 5),
    ("WOW WOW WOW! Mind blowing {product_caps}! Exceeded all my wildest dreams! Super fast shipping miracle item! Unbeatable perfection! Buy today!", 5, 5),
    ("Perfection personified! Best {product_caps} on the entire market! Flawless craftsmanship! Everyone needs to purchase this right now!", 5, 5),
    ("GREATEST PURCHASE EVER! Incredible miracle {product_caps}! Changed my life forever! Do not think twice just buy it immediately 10/10!", 5, 5),
    ("The most extraordinary {product_caps} in the world! Zero complaints! Perfection in every single way! 100% recommended to everyone!", 5, 5),
    
    # Review Bombing Attack (Generic destructive copy-paste scripts, coordinated anger)
    ("TOTAL GARBAGE! Defective item broke on day 1 do not buy complete waste of money terrible seller scam scam scam!!!", 1, 1),
    ("DO NOT BUY THIS TRASH! Broke immediately upon unboxing! Absolute rip off and total scam! Worst company in history! Zero stars!", 1, 1),
    ("HORRIBLE PRODUCT! Completely fake advertising! Died on day 2 do not buy absolute waste of money! Fraudulent seller!", 1, 1),
    ("DO NOT PURCHASE! Total junk item broke right away waste of cash! Terrible build quality cheap plastic scam! Avoid avoid avoid!", 1, 1),
    ("WORST ITEM EVER MADE! Completely useless defect item died immediately! Total waste of hard earned money! Return requested!", 1, 1),
    ("SCAM ALERT! Absolute garbage broke within 24 hours do not waste your money! Completely fraudulent listing!", 1, 1)
]

PRODUCTS = {
    "Electronics": ["wireless earbuds", "4K action camera", "smartwatch", "USB-C hub", "Bluetooth speaker", "portable power bank", "gaming mouse", "dash cam"],
    "Home & Kitchen": ["smoothie blender", "air fryer", "espresso machine", "cordless vacuum", "chef knife set", "electric kettle", "toaster oven"],
    "Sports & Outdoors": ["camping tent", "yoga mat", "hiking backpack", "insulated water bottle", "resistance bands", "tactical flashlight", "sleeping bag"],
    "Beauty & Personal Care": ["hydrating face cream", "electric toothbrush", "hair straightener", "vitamin C serum", "beard grooming kit", "sonic facial cleanser"],
    "Books & Media": ["noise-cancelling studio headphones", "ergonomic reading light", "digital voice recorder", "leather journal notebook", "e-reader case"]
}

POS_FEATURES = ["battery life", "sound fidelity", "ergonomic grip", "build durability", "screen responsiveness", "heat dissipation", "stitching quality"]
NEG_FEATURES = ["charging port", "hinge mechanism", "companion software", "power cable length", "zipper quality", "latch mechanism", "Bluetooth range"]
POS_QUALITIES = ["crisp and reliable", "exceedingly smooth", "very comfortable", "sturdy and solid", "surprisingly refined", "consistent and prompt"]
DURATIONS = ["two weeks", "35 days", "three months", "about six weeks", "nearly a month", "40 days"]
TIMES = ["five minutes", "ten minutes", "two minutes", "a few moments"]

def compute_linguistic_stats(text):
    """Computes NLP text features from raw review string."""
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    char_count = len(text)
    
    # Unique vocabulary richness
    unique_words = len(set(words))
    vocab_richness = round(unique_words / max(word_count, 1), 4)
    
    # Average word length
    avg_word_len = round(sum(len(w) for w in words) / max(word_count, 1), 2)
    
    # Sentence count
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = max(len(sentences), 1)
    
    return {
        "vocabulary_richness": vocab_richness,
        "average_word_length": avg_word_len,
        "sentence_count": sentence_count,
        "text_length": char_count
    }

def generate_sample_dataset(output_path, num_records=1600):
    """Generates balanced synthetic demonstration dataset."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    records = []
    
    half_count = num_records // 2
    
    # 1. Generate Genuine Reviews
    for _ in range(half_count):
        category = random.choice(CATEGORIES)
        product = random.choice(PRODUCTS[category])
        tmpl, min_r, max_r = random.choice(GENUINE_TEMPLATES)
        
        rating = random.randint(min_r, max_r)
        text = tmpl.format(
            product=product,
            feature_pos=random.choice(POS_FEATURES),
            quality_pos=random.choice(POS_QUALITIES),
            feature_neg=random.choice(NEG_FEATURES),
            feature_minor=random.choice(NEG_FEATURES),
            duration=random.choice(DURATIONS),
            time=random.choice(TIMES),
            rating=rating
        )
        
        stats = compute_linguistic_stats(text)
        records.append({
            "category": category,
            "rating": rating,
            "label": "genuine",
            "text": text,
            "label_binary": 0,
            **stats
        })
        
    # 2. Generate Fake Reviews
    for _ in range(num_records - half_count):
        category = random.choice(CATEGORIES)
        product = random.choice(PRODUCTS[category])
        tmpl, min_r, max_r = random.choice(FAKE_TEMPLATES)
        
        rating = random.randint(min_r, max_r)
        text = tmpl.format(
            product=product,
            product_caps=product.upper()
        )
        
        stats = compute_linguistic_stats(text)
        records.append({
            "category": category,
            "rating": rating,
            "label": "fake",
            "text": text,
            "label_binary": 1,
            **stats
        })
        
    # Shuffle records
    random.shuffle(records)
    df = pd.DataFrame(records)
    
    # Save CSV
    df.to_csv(output_path, index=False)
    print(f"Sample dataset successfully created at: {output_path}")
    print(f"Total Rows: {len(df)} | Genuine: {sum(df['label_binary'] == 0)} | Fake: {sum(df['label_binary'] == 1)}")
    return df

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), "dataset", "sample_reviews.csv")
    generate_sample_dataset(target, num_records=1600)
