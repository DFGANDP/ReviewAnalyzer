from review_analyzer.infrastructure.global_analyzer import GlobalAspectAnalyzer
from review_analyzer.infrastructure.dataframe_loader import DataFrameLoaderCsv
from review_analyzer.infrastructure.json_saver import JsonSaver

def analyze_and_save(label: str, csv_path: str, output_path: str, logger, charts_dir: str):
    loader = DataFrameLoaderCsv(logger)
    df = loader.load(csv_path)

    df["labels"] = df["labels"].astype(str).str.strip()

    logger.debug("%s preview:\n%s", label.capitalize(), df.head(5).copy().to_string(index=False))

    analyzer = GlobalAspectAnalyzer(label=label)
    analysis = analyzer.analyze_data(df)
    analyzer.generate_charts(output_dir=charts_dir)

    saver = JsonSaver(output_path, logger)
    saver.save(analysis)