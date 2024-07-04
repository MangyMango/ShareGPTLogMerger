import json
import os

def merge_json_files(folder_path, output_file):
    merged_data = {"id": "", "conversations": []}

    # Get all JSON files in the specified folder
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

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=2, ensure_ascii=False)

# Specify the input folder path and output file path
input_folder = r"C:\Users\Jam\Downloads\test"  # Use raw string for Windows paths
output_file = "merged_conversations.json"

# Call the function to merge the files
merge_json_files(input_folder, output_file)

print(f"Files merged successfully. Output saved to {output_file}")