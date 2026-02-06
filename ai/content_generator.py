import random
import json
import os


# --------------------------------
# 30 Professional Templates
# --------------------------------

templates = [

" {keyword} is redefining industry standards. The question is: are you adapting fast enough?",
" Leaders who understand {keyword} today will dominate tomorrow’s market.",
" The smartest professionals are already investing time in {keyword}. Are you one of them?",
" {keyword} isn’t a trend — it’s a strategic advantage.",
" Mastering {keyword} is becoming a non-negotiable skill in modern careers.",
" The future belongs to those who leverage {keyword} effectively.",

" Most people underestimate the power of {keyword}. That’s their biggest mistake.",
" If you really study {keyword}, you start seeing opportunities everywhere.",
" The rise of {keyword} signals a major shift in how we think and work.",
" Understanding {keyword} changes how you approach problem-solving.",
" {keyword} isn’t just tech — it’s reshaping global industries.",
" The deeper you dive into {keyword}, the clearer the future becomes.",


" Me pretending I don’t need {keyword}… while secretly Googling it every day.",
" If {keyword} had a fan club, most of us would already be members.",
" Coffee + {keyword} = productivity unlocked.",
" Everyone talks about {keyword}. Few actually understand it.",
" Trying to ignore {keyword} today is like ignoring the internet in 2000.",
" My daily routine: wake up, think about {keyword}, repeat.",


" If you’re not learning {keyword}, someone else is taking your place.",
" Stop scrolling. Start mastering {keyword}.",
" The gap between experts and beginners in {keyword} is widening fast.",
" Comfort zones don’t survive in the age of {keyword}.",
" The best time to start with {keyword} was yesterday. The second best is now.",
" Ignoring {keyword} today is a risk you’ll feel tomorrow.",

" Small steps in {keyword} today lead to massive growth tomorrow.",
" Your future self will thank you for learning {keyword}.",
" Progress in {keyword} compounds faster than you think.",
" Every expert in {keyword} started as a beginner.",
" Consistency in {keyword} beats talent every time.",
" The journey into {keyword} is where real transformation happens."
]


STOPWORDS = {
    "every", "your", "today", "more", "best",
    "skills", "tips", "learn", "start"
}


def load_insights():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "insights.json")

    with open(file_path, "r") as f:
        return json.load(f)


def select_good_keyword(keywords, theme):
    theme_map = {
        "education": ["learning", "skills", "knowledge", "growth"],
        "coding": ["coding", "python", "programming", "development"],
        "ai": ["AI", "machine learning", "automation"],
        "productivity": ["focus", "efficiency", "habits"],
    }

    if theme in theme_map:
        themed_keywords = [
            k for k in keywords
            if any(t.lower() in k.lower() for t in theme_map[theme])
        ]

        if themed_keywords:
            return random.choice(themed_keywords)

    filtered = [
        k for k in keywords
        if k.lower() not in STOPWORDS and len(k) > 3
    ]

    if filtered:
        return random.choice(filtered)

    return theme or "technology"



def generate_hashtags(keyword, platform):
    base_tags = [
        f"#{keyword.capitalize()}",
        "#Innovation",
        "#Technology"
    ]

    platform_tags = {
        "LinkedIn": ["#ProfessionalGrowth", "#Career"],
        "Instagram": ["#Success", "#Mindset"],
        "Twitter": ["#Trending", "#TechNews"],
    }

    return base_tags + platform_tags.get(platform, [])


def generate_post():
    insights = load_insights()

    fallback_theme = insights["engagement_prediction_model"]["recommended_theme"]
    keyword = select_good_keyword(insights["top_keywords"], fallback_theme)

    template = random.choice(templates)
    platform = insights["best_platform"]

    post_text = template.format(keyword=keyword.capitalize())

    hashtags = " ".join(generate_hashtags(keyword, platform))

    final_post = f"{post_text}\n\n{hashtags}"

    return {
        "generated_post": final_post,
        "recommended_time": insights["best_time"],
        "recommended_platform": platform,
        "predicted_theme": fallback_theme
    }


if __name__ == "__main__":
    result = generate_post()
    print(result["generated_post"])
    print("\nRecommended time:", result["recommended_time"])
    print("Platform:", result["recommended_platform"])

