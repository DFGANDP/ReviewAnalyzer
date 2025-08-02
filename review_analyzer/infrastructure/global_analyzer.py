import os
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
import pandas as pd
from collections import Counter, defaultdict

from review_analyzer.domain.interfaces import ReviewAnalyzer


class GlobalAspectAnalyzer(ReviewAnalyzer):
    """
    Analyzes a DataFrame with the following columns:
    - appid
    - recommendationid
    - aspect
    - labels

    Returns statistics about aspect-label relationships.
    """
    def __init__(self, label: str = 'normal'):
        self.results = {}
        self.label = label

    def analyze_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        self.results = {}

        # 1. Count of total and unique aspects
        self.results["total_aspects"] = len(data)
        self.results["unique_aspects"] = data["aspect"].nunique()

        # 2. Label distribution
        label_counts = data["labels"].value_counts()
        self.results["label_distribution"] = label_counts.to_dict()

        # 3. Top 10 most frequent aspects overall
        top_aspects = data["aspect"].value_counts().head(10)
        self.results["top_aspects_overall"] = top_aspects.to_dict()

        # 4. Top 10 aspects per label
        label_aspect_counts = defaultdict(Counter)
        for _, row in data.iterrows():
            label_aspect_counts[row["labels"]][row["aspect"]] += 1

        self.results["top_aspects_per_label"] = {
            label: dict(counter.most_common(10))
            for label, counter in label_aspect_counts.items()
        }

        # 5. Aspects with multiple labels
        aspect_to_labels = defaultdict(set)
        for _, row in data.iterrows():
            aspect_to_labels[row["aspect"]].add(row["labels"])

        multi_label_aspects = {
            aspect: list(labels)
            for aspect, labels in aspect_to_labels.items()
            if len(labels) > 1
        }

        self.results["multi_label_aspects_count"] = len(multi_label_aspects)
        self.results["multi_label_aspects_sample"] = dict(list(multi_label_aspects.items())[:10])

        # 6. Labels per recommendationid
        labels_per_rec = data.groupby("recommendationid")["labels"].nunique()
        self.results["avg_labels_per_review"] = float(labels_per_rec.mean())
        self.results["max_labels_per_review"] = int(labels_per_rec.max())
        self.results["min_labels_per_review"] = int(labels_per_rec.min())

        return self.results

    def generate_charts(self, output_dir: str = r"review_analyzer\output\charts"):
        os.makedirs(output_dir, exist_ok=True)

        # 1. Label distribution
        labels, counts = zip(*self.results["label_distribution"].items())
        plt.figure(figsize=(8, 5))
        sns.barplot(x=list(labels), y=list(counts))
        plt.title("Label Distribution")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{self.label}_label_distribution.png"))
        plt.close()

        # 2. Top aspects overall
        aspects, counts = zip(*self.results["top_aspects_overall"].items())
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(counts), y=list(aspects))
        plt.title("Top 10 Aspects Overall")
        plt.xlabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{self.label}_top_aspects_overall.png"))
        plt.close()

        # 3. Top aspects per label
        for label, aspect_counts in self.results["top_aspects_per_label"].items():
            aspects, counts = zip(*aspect_counts.items())
            plt.figure(figsize=(10, 6))
            sns.barplot(x=list(counts), y=list(aspects))
            plt.title(f"Top Aspects for Label: {label}")
            plt.xlabel("Count")
            plt.tight_layout()
            filename = f"{self.label}_top_aspects_{label.lower().replace(' ', '_')}.png"
            plt.savefig(os.path.join(output_dir, filename))
            plt.close()