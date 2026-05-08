#!/home/nandana/nanobot-env/bin/python3
"""
NanoBot Dataset Generator - Steam Game Reviews (Direct CSV Output)
No JSON - Saves directly as CSV file
"""

import os
import json
import argparse
import re
import time
import csv
import warnings
warnings.filterwarnings("ignore")

from datetime import datetime
from typing import Dict, List
import requests

# ============================================
# CONFIGURATION - PURE OLLAMA (NO GEMINI)
# ============================================
WORKSPACE = "/home/nandana/.nanobot/workspace"
MEMORY_FILE = "/home/nandana/.nanobot/memory/dataset_memory.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

# ============================================
# DATASET GENERATOR CLASS
# ============================================
class DatasetGenerator:
    def __init__(self):
        self.memory = self.load_memory()
        
    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        return {"scraped_urls": [], "generation_history": []}
    
    def save_memory(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def scrape_steam(self, query: str, limit: int = 15) -> List[Dict]:
        """Scrape Steam for games and reviews"""
        print(f"🎮 Searching Steam for '{query}' games...")
        data = []
        
        search_url = "https://store.steampowered.com/api/storesearch"
        params = {"term": query, "l": "english", "cc": "US", "num": limit}
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(search_url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                content = response.json()
                items = content.get("items", [])
                print(f"   Found {len(items)} games")
                
                for i, item in enumerate(items[:limit]):
                    game_name = item.get("name", "Unknown")
                    game_id = item.get("id", 0)
                    
                    details_url = f"https://store.steampowered.com/api/appdetails"
                    details_params = {"appids": game_id, "cc": "US", "l": "english"}
                    
                    description = ""
                    genres = []
                    price = "Free"
                    
                    try:
                        details_response = requests.get(details_url, params=details_params, headers=headers, timeout=15)
                        if details_response.status_code == 200:
                            details_data = details_response.json()
                            if str(game_id) in details_data and details_data[str(game_id)].get("success"):
                                game_data = details_data[str(game_id)].get("data", {})
                                description = game_data.get("short_description", "")[:500]
                                genre_list = game_data.get("genres", [])
                                genres = [g.get("description", "") for g in genre_list]
                                if game_data.get("price_overview"):
                                    price = game_data["price_overview"].get("final_formatted", "Unknown")
                    except:
                        pass
                    
                    review_summary = ""
                    try:
                        reviews_url = f"https://store.steampowered.com/appreviews/{game_id}"
                        reviews_params = {"json": 1, "filter": "recent", "language": "english", "num_per_page": 3}
                        reviews_response = requests.get(reviews_url, params=reviews_params, headers=headers, timeout=15)
                        if reviews_response.status_code == 200:
                            reviews_data = reviews_response.json()
                            reviews_list = reviews_data.get("reviews", [])
                            if reviews_list:
                                review_summary = " | ".join([r.get("review", "")[:200] for r in reviews_list[:2]])
                    except:
                        pass
                    
                    text_parts = [f"Game: {game_name}"]
                    if description:
                        text_parts.append(f"Description: {description}")
                    if genres:
                        text_parts.append(f"Genres: {', '.join(genres[:3])}")
                    if price:
                        text_parts.append(f"Price: {price}")
                    if review_summary:
                        text_parts.append(f"Recent reviews: {review_summary}")
                    
                    full_text = ". ".join(text_parts)
                    
                    if len(full_text) > 30:
                        data.append({
                            "source": "steam",
                            "text": full_text[:1200],
                            "metadata": {
                                "name": game_name,
                                "app_id": game_id,
                                "genres": genres,
                                "price": price
                            }
                        })
                    
                    print(f"   [{i+1}/{min(limit, len(items))}] Collected: {game_name}")
                    time.sleep(0.3)
                        
        except Exception as e:
            print(f"   ⚠️ Steam error: {e}")
            
        print(f"✅ Collected {len(data)} Steam games")
        return data
    
    def label_with_ollama(self, text: str, game_name: str = "") -> Dict:
        """Get sentiment from Ollama"""
        
        prompt = f"""Analyze this game and return ONLY valid JSON.
Game info: {text[:700]}

Return EXACTLY:
{{"sentiment": "positive", "confidence": 0.85, "score": 7.5, "verdict": "recommend", "quality": "good"}}

sentiment: positive/negative/mixed/neutral
score: 1-10
quality: excellent/good/average/poor/terrible
verdict: recommend/not_recommend/mixed
"""
        
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }, timeout=90)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "{}")
                match = re.search(r'\{[^{}]*\}', response_text)
                if match:
                    parsed = json.loads(match.group())
                    return {
                        "label": parsed.get("sentiment", "neutral"),
                        "confidence": float(parsed.get("confidence", 0.7)),
                        "sentiment_score": float(parsed.get("score", 5)) / 10,
                        "game_quality": parsed.get("quality", "average"),
                        "recommend": parsed.get("verdict") == "recommend" if parsed.get("verdict") else None
                    }
        except Exception as e:
            print(f"   ⚠️ Ollama error: {e}")
        
        # Fallback
        text_lower = text.lower()
        positive_words = ['great', 'awesome', 'fun', 'enjoy', 'love', 'best', 'excellent']
        negative_words = ['bad', 'terrible', 'awful', 'boring', 'waste', 'hate']
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            return {"label": "positive", "confidence": 0.6, "sentiment_score": 0.6, "game_quality": "good", "recommend": True}
        elif neg_count > pos_count:
            return {"label": "negative", "confidence": 0.6, "sentiment_score": -0.5, "game_quality": "poor", "recommend": False}
        else:
            return {"label": "neutral", "confidence": 0.5, "sentiment_score": 0, "game_quality": "average", "recommend": None}
    
    def save_as_csv(self, labeled_data, query, timestamp):
        """Save dataset directly as CSV (no JSON)"""
        
        # Create filename
        filename = f"steam_{query.replace(' ', '_')}_{timestamp}.csv"
        filepath = os.path.join(WORKSPACE, "datasets", filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if labeled_data:
                # Get all field names from first entry
                fieldnames = list(labeled_data[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for game in labeled_data:
                    writer.writerow(game)
        
        return filepath
    
    def generate_dataset(self, source: str, query: str, task_type: str, limit: int = 15) -> Dict:
        """Generate dataset and save as CSV"""
        print(f"\n🚀 Generating {task_type} dataset for '{query}'...")
        
        # Collect data
        raw_data = self.scrape_steam(query, limit)
        
        if not raw_data:
            return {"error": "No data collected"}
        
        # Label each game with Ollama
        print(f"\n🏷️ Labeling {len(raw_data)} games with Ollama ({OLLAMA_MODEL})...")
        labeled_data = []
        
        for i, item in enumerate(raw_data):
            print(f"   [{i+1}/{len(raw_data)}] Labeling: {item['metadata']['name']}")
            label_result = self.label_with_ollama(item["text"], item['metadata']['name'])
            labeled_data.append({
                "game_name": item['metadata']['name'],
                "description": item['text'][:300],
                "genres": ', '.join(item['metadata']['genres'][:3]) if item['metadata']['genres'] else '',
                "price": item['metadata'].get('price', 'Unknown'),
                "sentiment": label_result.get("label", "neutral"),
                "confidence": label_result.get("confidence", 0.5),
                "rating": label_result.get("sentiment_score", 0) * 10,
                "quality": label_result.get("game_quality", "average"),
                "recommend": label_result.get("recommend", None),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            time.sleep(1)
        
        # Save as CSV directly
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = self.save_as_csv(labeled_data, query, timestamp)
        
        # Print summary
        sentiments = [d["sentiment"] for d in labeled_data]
        sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
        
        print(f"\n✅ CSV Dataset saved: {csv_path}")
        print(f"📊 Sentiment distribution: {sentiment_counts}")
        
        # Calculate average rating
        ratings = [d["rating"] for d in labeled_data if d["rating"] > 0]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            print(f"⭐ Average rating: {avg_rating:.1f}/10")
        
        # Save to memory
        self.memory["generation_history"].append({
            "timestamp": timestamp,
            "filename": os.path.basename(csv_path),
            "total_games": len(labeled_data)
        })
        self.save_memory()
        
        return {"success": True, "csv_path": csv_path, "total_games": len(labeled_data)}

# ============================================
# MAIN
# ============================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, choices=["steam"])
    parser.add_argument("--query", required=True, help="Game genre or search term")
    parser.add_argument("--task", default="sentiment")
    parser.add_argument("--limit", type=int, default=10)
    
    args = parser.parse_args()
    
    print("\n🎮 NanoBot Steam Dataset Generator (Direct CSV Output)")
    print("=" * 50)
    
    generator = DatasetGenerator()
    result = generator.generate_dataset(
        source=args.source,
        query=args.query,
        task_type=args.task,
        limit=args.limit
    )
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
