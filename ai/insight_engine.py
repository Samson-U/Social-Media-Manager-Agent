import pandas as pd
from collections import Counter
import re
import os
import json


def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "posts.csv")

    data = pd.read_csv(file_path)
    return data


def calculate_engagement(data):
    data["engagement"] = (
        data["likes"]
        + data["comments"] * 2
        + data["shares"] * 3
    )
    return data


def best_post_time(data):
    grouped = data.groupby("time_posted")["engagement"].mean()
    return grouped.idxmax()


def extract_keywords(data):
    text = " ".join(data["post_text"].tolist()).lower()
    words = re.findall(r"\b[a-z]{4,}\b", text)

    common = Counter(words).most_common(5)
    return [word for word, _ in common]


def analyze_platforms(data):
    grouped = data.groupby("platform")["engagement"].mean()
    return grouped.idxmax()


def categorize_time(hour):
    hour = int(hour.split(":")[0])

    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    else:
        return "evening"


def analyze_time_ranges(data):
    data["time_range"] = data["time_posted"].apply(categorize_time)

    grouped = data.groupby("time_range")["engagement"].mean()

    return grouped.to_dict()


def analyze_post_themes(data):
    themes = {
        "ai": ["ai", "machine", "learning"],
        "coding": ["code", "coding", "python", "programming"],
        "productivity": ["productivity", "motivation", "habits"],
        "education": ["learn", "tips", "skills"]
    }

    theme_scores = {}

    for theme, keywords in themes.items():
        mask = data["post_text"].str.lower().apply(
            lambda x: any(k in x for k in keywords)
        )

        if mask.any():
            theme_scores[theme] = data[mask]["engagement"].mean()

    return theme_scores


def detect_content_type(data):
    categories = {
        "educational": ["learn", "tips", "guide"],
        "motivational": ["motivation", "habits", "start"],
        "technical": ["ai", "code", "python"]
    }

    scores = Counter()

    for text in data["post_text"].str.lower():
        for category, keywords in categories.items():
            if any(k in text for k in keywords):
                scores[category] += 1

    return scores.most_common(1)[0][0]


def build_prediction_model(themes, time_ranges):
    best_theme = max(themes, key=themes.get) if themes else None
    best_time_range = max(time_ranges, key=time_ranges.get)

    return {
        "recommended_theme": best_theme,
        "recommended_time_range": best_time_range
    }


def get_insights():
    data = load_data()
    data = calculate_engagement(data)

    time_ranges = analyze_time_ranges(data)
    themes = analyze_post_themes(data)

    insights = {
        "best_time": best_post_time(data),
        "best_platform": analyze_platforms(data),
        "top_keywords": extract_keywords(data),
        "engagement_by_time_range": time_ranges,
        "top_post_themes": themes,
        "preferred_content_type": detect_content_type(data),
        "engagement_prediction_model": build_prediction_model(themes, time_ranges)
    }

    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, "data", "insights.json")

    with open(output_path, "w") as f:
        json.dump(insights, f, indent=4)

    return insights


if __name__ == "__main__":
    print(json.dumps(get_insights(), indent=4))
