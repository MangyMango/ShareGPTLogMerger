import json
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def merge_json_files(folder_path):
    merged_data = {"id": "", "conversations": []}

    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if "conversations" in data:
                    merged_data["conversations"].extend(data["conversations"])
                else:
                    print(f"Warning: {file_name} does not contain a 'conversations' key. Skipping.")
            except json.JSONDecodeError:
                print(f"Error: {file_name} is not a valid JSON file. Skipping.")

    return merged_data

def flatten_conversations(conversations):
    flattened = []
    for conv in conversations:
        flattened.append({
            'from': conv.get('from', ''),
            'value': conv.get('value', '')
        })
    return flattened

def convert_to_parquet(data, output_file):
    # Flatten the conversations
    flat_data = flatten_conversations(data['conversations'])

    # Convert to pandas DataFrame
    df = pd.DataFrame(flat_data)

    # Convert to PyArrow Table
    table = pa.Table.from_pandas(df)

    # Write to Parquet
    pq.write_table(table, output_file)

# Specify the input folder path and output file paths
input_folder = r"C:\Users\Jam\Downloads\logs"  # Use raw string for Windows paths
output_json = "merged_conversations.json"
output_parquet = "conversations.parquet"

# Merge JSON files
merged_data = merge_json_files(input_folder)

# Save merged JSON (optional)
with open(output_json, 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, indent=2, ensure_ascii=False)

# Convert to Parquet
convert_to_parquet(merged_data, output_parquet)

print(f"Files merged and converted successfully.")
print(f"Merged JSON saved to: {output_json}")
print(f"Parquet file saved to: {output_parquet}")