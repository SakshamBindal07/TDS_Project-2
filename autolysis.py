# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "ipykernel",    
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "chardet",
#   "scikit-learn",
#   "requests"
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import chardet

def determine_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        detected_encoding = chardet.detect(f.read(10000))
    return detected_encoding.get('encoding')

def read_dataset(file_path):
    try:
        file_encoding = determine_file_encoding(file_path)
        print(f"Detected file encoding: {file_encoding}")
        dataset = pd.read_csv(file_path, encoding=file_encoding)
        print("Dataset successfully loaded.")
        return dataset
    except UnicodeDecodeError:
        print("Decoding failed. Retrying with 'latin-1' encoding.")
        try:
            dataset = pd.read_csv(file_path, encoding="latin-1")
            print("Dataset loaded with fallback encoding.")
            return dataset
        except Exception as err:
            print(f"Failed to load dataset: {err}")
            sys.exit(1)
    except Exception as err:
        print(f"Unexpected error: {err}")
        sys.exit(1)

def examine_dataset(data):
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    print(f"Numeric columns identified: {numeric_columns}")
    print(f"Categorical columns identified: {categorical_columns}")
    return numeric_columns, categorical_columns

def robust_analysis(data, num_cols):
    stats = {}
    for col in num_cols:
        col_data = data[col].dropna()
        stats[col] = {
            "mean": col_data.mean(),
            "median": col_data.median(),
            "std_dev": col_data.std(),
            "variance": col_data.var(),
            "skewness": col_data.skew(),
            "kurtosis": col_data.kurt(),
        }
    return stats

def create_visualizations(data, num_cols, cat_cols):
    output_files = []

    if num_cols:
        correlation_matrix = data[num_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.xlabel("Features")
        plt.ylabel("Features")
        plt.savefig("correlation_matrix.png")
        plt.close()
        output_files.append("correlation_matrix.png")
        print("Generated: correlation_matrix.png")

        for col in num_cols:
            plt.figure(figsize=(8, 6))
            sns.histplot(data[col], bins=30, kde=True, color="skyblue")
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.savefig(f"distribution_{col}.png")
            plt.close()
            output_files.append(f"distribution_{col}.png")
            print(f"Generated: distribution_{col}.png")

    if cat_cols:
        plt.figure(figsize=(10, 6))
        data[cat_cols[0]].value_counts().head(10).plot(kind="bar", color="orange")
        plt.title(f"Top Categories: {cat_cols[0]}")
        plt.xlabel(cat_cols[0])
        plt.ylabel("Count")
        plt.savefig(f"category_{cat_cols[0]}.png")
        plt.close()
        output_files.append(f"category_{cat_cols[0]}.png")
        print(f"Generated: category_{cat_cols[0]}.png")

    return output_files

def generate_llm_prompt(stats, visuals, dataset_name):
    prompt = f"""
    ### Dataset Analysis: {dataset_name}

    - **Dataset Summary**:
      Key statistics and insights:
      {stats}

    - **Visualizations**:
      - Correlation matrix
      - Distribution plots

    Provide a detailed analysis, focusing on:
    1. Insights derived from the analysis.
    2. Visual insights from attached visuals.
    3. Implications of findings on further analysis.

    Include the above in a well-formatted Markdown narrative, highlighting significant insights.
    """
    return prompt

def summarize_analysis(stats, visuals, dataset_name):
    api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    token = os.getenv("AIPROXY_TOKEN")

    if not token:
        print("Environment variable 'AIPROXY_TOKEN' not set.")
        sys.exit(1)

    api_payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": generate_llm_prompt(stats, visuals, dataset_name)
            }
        ]
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=api_payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as error:
        print(f"Error while calling API: {error}")
        sys.exit(1)

def save_to_readme(summary):
    with open("README.md", "w") as file:
        file.write("# Analysis Summary\n\n")
        file.write(summary)
    print("Summary written to README.md")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <dataset.csv>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    dataset = read_dataset(dataset_path)
    numeric, categorical = examine_dataset(dataset)

    stats = robust_analysis(dataset, numeric)
    visualization_files = create_visualizations(dataset, numeric, categorical)
    analysis_summary = summarize_analysis(stats, visualization_files, os.path.basename(dataset_path))
    save_to_readme(analysis_summary)

if __name__ == "__main__":
    main()
