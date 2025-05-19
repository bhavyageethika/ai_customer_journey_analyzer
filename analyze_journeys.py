import json
import os
from collections import Counter
from typing import Dict, Any, List
import openai

from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY") #ensure no hardcoded key - set as environment variable in .env

def _load_sessions_from_str(json_str: str) -> List[dict]:
    data = json.loads(json_str)
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                return v
        raise ValueError("JSON does not contain a sessions list")
    return data

def _events(session: dict) -> List[dict]:
    if "events" in session:
        return session["events"]
    if "activities" in session:
        return [{"type": a.get("activity_type") or a.get("type"), **a} for a in session["activities"]]
    return []

def _basic_stats(sessions: List[dict]) -> Dict[str, Any]:
    total = len(sessions)
    successful, abandoned = [], []
    for s in sessions:
        evs = _events(s)
        (successful if any(e.get("type") == "purchase" for e in evs) else abandoned).append(evs)

    conv_rate = round(len(successful) / total * 100, 2) if total else 0.0
    drop_counts = Counter(evs[-1]["type"] for evs in abandoned if evs)
    top_drop, drop_ct = drop_counts.most_common(1)[0] if drop_counts else ("n/a", 0)
    drop_pct = round(drop_ct / total * 100, 2) if total else 0.0

    searches, no_click = 0, 0
    for evs in successful + abandoned:
        for i, ev in enumerate(evs):
            if ev.get("type") == "search":
                searches += 1
                if i == len(evs) - 1 or evs[i+1].get("type") != "product_view":
                    no_click += 1
    no_click_pct = round(no_click / searches * 100, 2) if searches else 0.0

    cart_sessions = [evs for evs in successful + abandoned if any(e.get("type") == "add_to_cart" for e in evs)]
    carts = len(cart_sessions)
    carts_purchased = len([evs for evs in cart_sessions if any(e.get("type") == "purchase" for e in evs)])
    abandon_pct = round((carts - carts_purchased) / carts * 100, 2) if carts else 0.0

    return {
        "total_sessions": total,
        "successful_sessions": len(successful),
        "abandoned_sessions": len(abandoned),
        "conversion_rate": conv_rate,
        "top_dropoff": top_drop,
        "top_dropoff_pct": drop_pct,
        "total_searches": searches,
        "search_no_click_pct": no_click_pct,
        "sessions_with_cart": carts,
        "cart_abandon_pct": abandon_pct,
    }

def analyze_journeys_from_json(json_str: str) -> Dict[str, str]:
    sessions = _load_sessions_from_str(json_str)
    stats = _basic_stats(sessions)
    try:
        prompt = f"""
You are a senior e-commerce analyst. Based on the JSON stats below, generate detailed insights and statistics.
Respond with JSON using exactly these keys:
{{
  "patterns": str,
  "differences": str,
  "drop_offs": str,
  "search_analysis": str,
  "cart_abandonment": str,
  "recommendations": str
}}

STATS:
{json.dumps(stats, indent=2)}
"""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        print("GPT RAW OUTPUT:\n", response.choices[0].message.content)  

        return json.loads(response.choices[0].message.content.strip())
    
    except Exception:
        #print(" Insight generation failed:")
        return {
            "patterns": "Exception occured set GPT key: example insight Users follow homepage → search → product view → cart → checkout.",
            "differences": "Exception occured set GPT key:example insight Buyers convert faster and use search less. Abandoners explore more but do not act.",
            "drop_offs": "Exception occured set GPT key:example insight Most users drop after product views. Heatmaps by category and session length could help.",
            "search_analysis": "Exception occured set GPT key: example insight About 20 percent of searches don’t lead to product views. Analyze zero-result queries.",
            "cart_abandonment": "Exception occured set GPT key:example insight Cart abandonment is ~60%. Drop-off happens post-cart, suggesting checkout friction.",
            "recommendations": "Exception occured set GPT key: example insight Improve product info\n2. Add cart reminder\n3. Tune search\n4. Simplify checkout"
        }

def ask_question(question: str, insights: Dict[str, str]) -> str:
    context = "\n".join(f"{k}: {v}" for k, v in insights.items())
    prompt = f"""
Use the insights below to answer this business question. Be direct, useful, and analytical.

INSIGHTS:
{context}

QUESTION:
{question}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        
        print("GPT call failed:", e)
        return f"(Error: {e})"
