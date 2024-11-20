import pandas as pd
import os

input_folder = "CSVs"
output_folder = "exactMatch_CSVs"

os.makedirs(output_folder, exist_ok=True)

# Iterate through all CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)

        df = pd.read_csv(file_path)

        # Check if the required columns exist
        if "Multiclass" in df.columns and "Incident type Multiclass" in df.columns:
            # Add a new column 'exactMatch' where 1 indicates a match and 0 indicates no match
            df['exactMatch'] = (df["Multiclass"] == df["Incident type Multiclass"]).astype(int)

            # Add a new column 'score' with the average of the 'exactMatch' column
            score = df['exactMatch'].mean()
            df['score'] = ''  # Initialize the column
            df.at[0, 'score'] = score  # Set the score in the first cell

            base_name, file_extension = os.path.splitext(file_name)
            output_file_name = f"{base_name}_exactMatch{file_extension}"
            output_file_path = os.path.join(output_folder, output_file_name)

            df.to_csv(output_file_path, index=False)
            print(f"Processed and saved: {output_file_path}")
        else:
            print(f"Skipped {file_name}: Required columns not found.")

print("All files processed!")
