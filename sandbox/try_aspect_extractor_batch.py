'''
Tutaj mam czy na plus czy na minus 

Pozniej dorobie kolejna kalse ktorqa bedzie sprawdzac czego to dotyczy 

ktora z kategorii zanczy 

🎮 Gameplay	"walki są dynamiczne i nie nudzą się"
🎨 Grafika	"oprawa wizualna przepiękna, świat żyje"
🧠 Fabuła	"historia mnie wciągnęła bardziej niż się spodziewałem"
🔧 Optymalizacja	"na GTX 1060 chodzi w 60 fps"
💸 Cena/wartość	"za 20 zł warto, ale nie za pełną cenę"
🎵 Muzyka	"muzyka świetnie buduje klimat"
🧑‍🤝‍🧑 Multiplayer	"matchmaking działa dobrze, mało cheaterów"
🐞 Bugowość	"gra crashuje po każdej misji"
💡 Innowacyjność	"nic nowego, ale dobrze zrobione"
? INNE Czyli jakis ogolny "fajna gra" ale to niewiele mowi  
'''

import json
from multiprocessing import Pool
from ollama import Client
from review_analyzer.infrastructure.json_loader import JsonReviewLoader
from tqdm import tqdm


MODEL_NAME = "MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L"
PROMPT_PATH = r"D:\Programowanie\SteamReviewAnalyzer\review_analyzer\steam_review_batch\prompt_extract.txt"
REVIEW_PATH = r"D:\Programowanie\SteamReviewAnalyzer\review_analyzer\steam_review_batch\105600_20250209173825.json"
OUTPUT_PATH = r"D:\Programowanie\SteamReviewAnalyzer\review_analyzer\steam_review_batch\output.jsonl"

# --- Prompt loader
with open(PROMPT_PATH, encoding="utf-8") as f:
    LLM_PROMPT_TEMPLATE = f.read()

# --- Global client (shared per process)
client = Client()

def extract_liked_disliked(review_text: str) -> dict:
    prompt = LLM_PROMPT_TEMPLATE.replace("{INSERT_REVIEW_HERE}", review_text)

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response["message"]["content"]
        parsed = json.loads(content)
        return {
            "liked": parsed.get("liked", []),
            "disliked": parsed.get("disliked", []),
            "original_review": review_text
        }
    except Exception as e:
        return {
            "liked": [],
            "disliked": [],
            "original_review": review_text,
            "error": str(e)
        }


if __name__ == "__main__":
    # --- Load reviews
    loader = JsonReviewLoader(filepath=REVIEW_PATH)
    review_list = loader.load_reviews(language="english")
    print(f"✅ Wczytano {len(review_list)} recenzji")

    # --- Extract only the text field
    # Musze dodac zapiswyanie ktora to recommendationid oraz appid
    review_texts = [r.review for r in review_list]

    review_texts = review_texts[:2] # debug

    with Pool(processes=4) as pool:
        results = list(tqdm(pool.imap_unordered(extract_liked_disliked, review_texts), total=len(review_texts)))

    # --- Save to JSONL
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Zapisano {len(results)} wyników do {OUTPUT_PATH}")
