import pandas as pd
import os

# Input and output folder paths
input_folder = "CSVs"
output_folder = "exactMatch_CSVs"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through all CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):  # Process only CSV files
        file_path = os.path.join(input_folder, file_name)

        # Load the CSV into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Check if the required columns exist
        if "Multiclass" in df.columns and "Incident type Multiclass" in df.columns:
            # Handle missing or non-string values in both columns
            df["Multiclass"] = df["Multiclass"].fillna("").astype(str).str.replace('\n', ',', regex=True)
            df["Incident type Multiclass"] = df["Incident type Multiclass"].fillna("").astype(str).str.replace('\n', ',', regex=True)

            # Add a new column 'exactMatch' that ignores the order of elements
            df['exactMatch'] = (
                df["Multiclass"].str.split(',').apply(sorted).astype(str) ==
                df["Incident type Multiclass"].str.split(',').apply(sorted).astype(str)
            ).astype(int)

            # Add a new column 'score' with the average of the 'exactMatch' column
            score = df['exactMatch'].mean()
            df['score'] = ''  # Initialize the column
            df.at[0, 'score'] = score  # Set the score in the first cell

            # Generate the output file name by appending '_exactMatch' to the original file name
            base_name, file_extension = os.path.splitext(file_name)
            output_file_name = f"{base_name}_exactMatch{file_extension}"
            output_file_path = os.path.join(output_folder, output_file_name)

            # Save the updated DataFrame to the output folder
            df.to_csv(output_file_path, index=False)
            print(f"Processed and saved: {output_file_path}")
        else:
            print(f"Skipped {file_name}: Required columns not found.")

print("All files processed!")
