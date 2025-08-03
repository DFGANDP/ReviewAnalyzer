# Steam Review Analyzer

A comprehensive tool for analyzing Steam game reviews using AI-powered sentiment and aspect analysis. The application processes raw review data, extracts sentiment and aspects from individual sentences, labels aspects, and generates detailed analysis reports with visualizations.

## Overview

The Steam Review Analyzer is designed to process large volumes of Steam game reviews to extract meaningful insights. It performs three main operations:

1. **Sentence Processing**: Extracts sentiment and aspects from individual review sentences
2. **Aspect Labeling**: Labels and categorizes different aspects of the game (gameplay, graphics, story, etc.)
3. **Analysis & Visualization**: Generates comprehensive analysis reports with charts and statistics

## Features

- **Multi-threaded processing** for efficient handling of large datasets
- **AI-powered analysis** using Mistral language model
- **Comprehensive logging** with both console and file output
- **Automatic chart generation** for visual analysis
- **Flexible configuration** with command-line arguments
- **Structured output** in multiple formats (JSON, CSV, charts)

## Installation

### Prerequisites

- Python 3.13
- Ollama installed and running locally

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SteamReviewAnalyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and start Ollama**
   ```bash
   # Follow instructions at https://ollama.ai/
   ollama pull MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L
   ```

4. **Prepare input data**
   - Place your Steam review JSON file in the `review_analyzer/input/` directory
   - The default expected file is `105600_20250209173825.json`

## Usage

### Basic Usage

Run the analysis from the project root directory:

```bash
python -m review_analyzer.presentation.main
```

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--workers` | int | 6 | Number of worker threads for parallel processing |
| `--language` | str | "english" | Language for review processing |
| `--limit` | int | None | Limit the number of reviews to process (useful for testing) |

### Examples

**Process with custom worker count:**
```bash
python -m review_analyzer.presentation.main --workers 8
```

**Process reviews in a different language:**
```bash
python -m review_analyzer.presentation.main --language polish
```

**Process only first 100 reviews (for testing):**
```bash
python -m review_analyzer.presentation.main --limit 100
```

**Combine multiple arguments:**
```bash
python -m review_analyzer.presentation.main --workers 4 --language english --limit 50
```

## Project Structure

```
SteamReviewAnalyzer/
├── review_analyzer/
│   ├── config.py                 # Configuration and paths
│   ├── domain/                   # Domain models and interfaces
│   │   ├── aspect_labeler.py
│   │   ├── interfaces.py
│   │   └── models.py
│   ├── infrastructure/           # Data access and external services
│   │   ├── aspect_labeler.py    # AI aspect labeling
│   │   ├── dataframe_loader.py  # CSV data loading
│   │   ├── dataframe_saver.py   # CSV data saving
│   │   ├── global_analyzer.py   # Analysis engine
│   │   ├── json_loader.py       # JSON data loading
│   │   ├── json_saver.py        # JSON data saving
│   │   ├── log_handlers/        # Logging configuration
│   │   ├── mistral_extractor.py # AI sentiment extraction
│   │   ├── sentence_analyzer.py # Sentence processing
│   │   ├── sentence_loader.py   # Sentence data loading
│   │   └── utils.py             # Utility functions
│   ├── input/                   # Input data directory
│   ├── output/                  # Generated output (timestamped)
│   ├── presentation/            # Application entry points
│   │   ├── main.py             # Main CLI interface
│   │   ├── runner.py           # Core execution logic
│   │   └── [other runners]     # Specialized runners
│   ├── prompts/                # AI prompt templates
│   │   ├── prompt_extract.txt  # Sentence extraction prompts
│   │   └── prompt_label.txt    # Aspect labeling prompts
│   └── service/                # Business logic services
│       ├── aspect_labeling_service.py
│       └── review_sentence_processing_service.py
├── tests/                      # Test suite
├── sandbox/                    # Development and testing scripts
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## Output Structure

The application generates timestamped output directories containing:

- **Analysis reports** (`analysis_liked.json`, `analysis_disliked.json`)
- **Data files** (CSV files with labeled aspects)
- **Charts** (PNG visualizations for each aspect)
- **Logs** (Detailed processing logs)

## Dependencies

- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **matplotlib**: Chart generation
- **seaborn**: Statistical data visualization
- **ollama**: Local AI model interface
- **tqdm**: Progress bars
- **pytest**: Testing framework

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Features

1. Follow the existing architecture patterns
2. Add tests for new functionality
3. Update documentation as needed

## Troubleshooting

**Common Issues:**

1. **Ollama not running**: Ensure Ollama is installed and the model is pulled
2. **Memory issues**: Reduce `--workers` parameter for large datasets
3. **Input file not found**: Verify the JSON file exists in the input directory

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
