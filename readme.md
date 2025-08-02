## STEAM REVIEW ANALYZER 

```uruchamianie
python -m review_analyzer.infrastructure.json_loader

a pytest latwo 

(.venv) PS D:\Programowanie\SteamReviewAnalyzer> pytest
```


### narazie dla terraria angielskie komentarze z np 2 miesiecy ostatnich

| Etap | Moduł               | Co robisz                                                | SOLID    | Uwagi                            |
| ---- | ------------------- | -------------------------------------------------------- | -------- | -------------------------------- |
| 1️⃣  | **DataLoader**      | ładuje JSON i zwraca `List[Review]`                      | SRP, DIP | interfejs `ReviewRepository`     |
| 2️⃣  | **AspectExtractor** | zwraca np. `{"grafika": "good", "optymalizacja": "bad"}` | SRP, OCP | strategia `BaseAspectExtractor`  |
| 3️⃣  | **Summarizer**      | generuje 1 zdanie na aspekt + ogólne podsumowanie        | DIP      | używa LLM przez `TextSummarizer` |
| 4️⃣  | **ResultFormatter** | formatuje wynik jako JSON, Markdown, lub PDF             | OCP      |                                  |
| 5️⃣  | **Pipeline**        | koordynuje wszystko                                      | SRP      | agnostyczny względem modeli      |


### struktura projektu

i w kazdym folderze init oczywiscie 

review_analyzer/
├── domain/
│   ├── models.py            # Review, Aspect, Summary
│   └── interfaces.py        # ReviewRepository, AspectExtractor, Summarizer
├── infrastructure/
│   ├── json_loader.py       # implementacja ReviewRepository
│   ├── transformer_summarizer.py
│   └── sentence_aspect.py
├── service/
│   └── analysis_service.py  # łączy wszystko
├── presentation/
│   └── main.py              # uruchamia analizę
├── tests/
└── config.py


### How to uv 
![alt text](image.png)

## NOT PIP 
uv pip install -r requirements.txt
