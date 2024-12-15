# /// script
# requires-python = ">=3.11"
# dependencies = [
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
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import chardet
import requests

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

def create_visualizations(data, num_cols, cat_cols):
    output_files = []

    if num_cols:
        correlation_matrix = data[num_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.savefig("correlation_matrix.png")
        plt.close()
        output_files.append("correlation_matrix.png")
        print("Generated: correlation_matrix.png")

        plt.figure(figsize=(8, 6))
        sns.histplot(data[num_cols[0]], bins=30, kde=True)
        plt.title(f"Distribution: {num_cols[0]}")
        plt.savefig(f"distribution_{num_cols[0]}.png")
        plt.close()
        output_files.append(f"distribution_{num_cols[0]}.png")
        print(f"Generated: distribution_{num_cols[0]}.png")

        if len(num_cols) > 1:
            plt.figure(figsize=(8, 6))
            sns.boxplot(y=data[num_cols[1]])
            plt.title(f"Boxplot of {num_cols[1]}")
            plt.savefig(f"boxplot_{num_cols[1]}.png")
            plt.close()
            output_files.append(f"boxplot_{num_cols[1]}.png")
            print(f"Generated: boxplot_{num_cols[1]}.png")

    if cat_cols:
        plt.figure(figsize=(10, 6))
        data[cat_cols[0]].value_counts().head(10).plot(kind="bar")
        plt.title(f"Top Categories: {cat_cols[0]}")
        plt.savefig(f"category_{cat_cols[0]}.png")
        plt.close()
        output_files.append(f"category_{cat_cols[0]}.png")
        print(f"Generated: category_{cat_cols[0]}.png")

    return output_files

def summarize_analysis(data, num_cols, cat_cols, visuals):
    api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    token = os.getenv("AIPROXY_TOKEN")

    if not token:
        print("Environment variable 'AIPROXY_TOKEN' not set.")
        sys.exit(1)

    data_summary = data.describe(include="all").to_dict()
    null_counts = data.isnull().sum().to_dict()
    correlation_data = data[num_cols].corr().to_dict() if num_cols else {}

    api_payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Provide a detailed analysis summary for the given dataset, covering numeric and categorical data insights, generated visuals, and any recommended actions."
                )
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
        file.write(summary)
    print("Summary written to README.md")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <dataset.csv>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    dataset = read_dataset(dataset_path)
    numeric, categorical = examine_dataset(dataset)

    visualization_files = create_visualizations(dataset, numeric, categorical)
    analysis_summary = summarize_analysis(dataset, numeric, categorical, visualization_files)
    save_to_readme(analysis_summary)

if __name__ == "__main__":
    main()
