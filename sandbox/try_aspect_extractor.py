import json
from review_analyzer.infrastructure.json_loader import JsonReviewLoader
from ollama import Client


def extract_liked_disliked(review: str, LLM_PROMPT_TEMPLATE: str, model: str = "MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L") -> dict:
    client = Client()
    prompt = LLM_PROMPT_TEMPLATE.replace("{INSERT_REVIEW_HERE}", review)

    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Error parsing response:", content)
        return {"liked": [], "disliked": []}

if __name__ == "__main__":
    file_path = r'D:\Programowanie\SteamReviewAnalyzer\review_analyzer\steam_review_batch\105600_20250209173825.json'
    loader = JsonReviewLoader(filepath=file_path)
    review_list = loader.load_reviews(language='english')

    print(f'Mamy {len(review_list)} recenzji')
    review_obj = review_list[129]

    print('RECEZNJA TUTAJ:\n')
    print(review_obj.review) # TO zrobmy na testa

    with open(r'D:\Programowanie\SteamReviewAnalyzer\review_analyzer\steam_review_batch\prompt_extract.txt', 'r') as f:
        LLM_PROMPT_TEMPLATE = f.read()

    #print(LLM_PROMPT_TEMPLATE[-25:])

    result = extract_liked_disliked(review_obj.review, LLM_PROMPT_TEMPLATE, model='MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L')
    print("\n--- ANALYZED ---")
    print(json.dumps(result, indent=2))

    