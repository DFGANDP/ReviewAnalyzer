import json
from review_analyzer.infrastructure.json_loader import JsonReviewLoader


if __name__ == "__main__":
    file_path = r'E:\AutomaticFileTransfer\reviews\105600_20250209173825.json'
    loader = JsonReviewLoader(filepath=file_path)
    review_list = loader.load_reviews(language='english')
    print(type(review_list))
    for element in review_list:
        print(element)
        print(type(element))
        print(element.language)
        break
    print(f'Mamy {len(review_list)} recenzji')