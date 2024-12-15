# TDS_Project-2
# Automated Data Analysis and Visualization Leveraging AI

This project automates dataset analysis and visualization using Python, integrated with a GPT-based language model for insights and narratives. It delivers statistical summaries, visualizations, and structured Markdown reports, catering to various datasets dynamically and efficiently.

---

## Key Features

1. **Comprehensive Automated Analysis**
   - Executes detailed statistical summaries.
   - Identifies missing data, anomalies, and patterns with precision.
   - Includes advanced analyses like clustering and correlation studies.

2. **Dynamic Visualization**
   - Generates high-quality PNG charts tailored to dataset attributes.
   - Visualizations include correlation heatmaps, distribution plots, and categorical charts.

3. **Insightful Narratives**
   - Employs GPT-based AI for structured narratives.
   - Outputs Markdown-formatted reports integrating text and visual insights seamlessly.

4. **Efficient LLM Utilization**
   - Minimizes token usage with concise and context-rich prompts.
   - Summarizes data before querying the LLM to enhance efficiency.

5. **Universal CSV Dataset Compatibility**
   - Adapts to datasets of various sizes, structures, and complexities.
   - Ensures robust handling of numeric and categorical data.

6. **Self-Contained Execution**
   - Operates as a standalone script requiring minimal setup.
   - Outputs results directly to the working directory for easy access.

---

## Project Workflow

1. **Data Preprocessing**
   - Reads and parses the input CSV file.
   - Detects missing values and identifies data anomalies.

2. **Exploratory Data Analysis (EDA)**
   - Provides summary statistics and correlation matrices.
   - Identifies key patterns using clustering techniques.

3. **Visualization Creation**
   - Generates visual insights using libraries like Seaborn and Matplotlib.
   - Saves visualizations as `.png` files.

4. **LLM Integration**
   - Queries GPT-4o-Mini for narrative insights and advanced analysis suggestions.
   - Integrates visualizations into a cohesive Markdown report.

5. **Markdown Report Generation**
   - Produces a detailed `README.md` summarizing findings and implications.

---

## Requirements

### Python Version
- Python 3.11 or higher.

### Libraries
Install required libraries:

```bash
pip install -r requirements.txt
```

Dependencies include:
- `pandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `requests`
- `chardet`

---

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/automated-data-analysis.git
   cd automated-data-analysis
   ```

2. **Prepare your environment**:
   - Create a `.env` file to store the API token:
     ```plaintext
     AIPROXY_TOKEN=your_api_token_here
     ```

3. **Run the script**:
   ```bash
   python autolysis.py <dataset.csv>
   ```

4. **Access the Outputs**:
   - Visualizations: `.png` files in the output directory.
   - Markdown Report: `README.md` file summarizing the analysis.

---

## Example Datasets

The script has been tested with various datasets, such as:
- **Books Dataset**: Contains metadata, genres, and ratings from GoodReads.
- **Happiness Index**: Global happiness data from the World Happiness Report.
- **Media Ratings**: Faculty evaluations of books, movies, and TV shows.

---

## Contribution

Contributions are welcome! To suggest improvements or new features, feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License. Refer to the `LICENSE` file for details.

---

## Acknowledgments

- **OpenAI**: For the GPT-based language model.
- **Python Community**: For the powerful libraries used in this project.

---

This project demonstrates the power of automated analytics and AI-driven insights for comprehensive and efficient data analysis.
