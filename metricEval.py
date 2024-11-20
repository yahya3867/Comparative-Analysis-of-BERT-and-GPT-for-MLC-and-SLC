import pandas as pd
import numpy as np
import os
import glob

# Specify the input and output folders
input_folder = 'CSVs'  # Replace with your input folder path
output_folder = 'metricEval_CSVs'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get all CSV files in the input folder
csv_files = glob.glob(os.path.join(input_folder, '*.csv'))

# Iterate through each CSV file
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    
    # Lists to store the computed metrics
    precisions = []
    recalls = []
    f1_scores = []
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Process ground truth categories
        gt_cats = str(row['Incident type Multiclass'])
        if pd.isna(gt_cats):
            gt_cats = ''
        gt_cats = gt_cats.split(',')
        gt_cats = [cat.strip() for cat in gt_cats if cat.strip()]
        gt_set = set(gt_cats)
        
        # Process LLM output categories
        llm_output = str(row['Multiclass'])
        if pd.isna(llm_output):
            llm_output = ''
        llm_output = llm_output.replace('\n', ',')
        llm_cats = llm_output.split(',')
        llm_cats = [cat.strip() for cat in llm_cats if cat.strip()]
        llm_set = set(llm_cats)
        
        # If the sets are equal, assign metrics as 1
        if gt_set == llm_set:
            precision = 1.0
            recall = 1.0
            f1 = 1.0
        else:
            # Compute precision
            if len(llm_set) == 0:
                precision = 0.0
            else:
                precision = len(gt_set & llm_set) / len(llm_set)
            # Compute recall
            if len(gt_set) == 0:
                recall = 0.0
            else:
                recall = len(gt_set & llm_set) / len(gt_set)
            # Compute F1 score
            if precision + recall == 0:
                f1 = 0.0
            else:
                f1 = 2 * (precision * recall) / (precision + recall)
        
        # Append the metrics to the lists
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
        
    # Add the metrics as new columns to the DataFrame
    df['Precision'] = precisions
    df['Recall'] = recalls
    df['F1'] = f1_scores
    
    # Compute the average of each metric
    avg_precision = np.mean(precisions)
    avg_recall = np.mean(recalls)
    avg_f1 = np.mean(f1_scores)
    
    # Create a row with the averages
    avg_row = {col: '' for col in df.columns}
    avg_row['Precision'] = avg_precision
    avg_row['Recall'] = avg_recall
    avg_row['F1'] = avg_f1
    
    # Insert the average row at the top of the DataFrame
    df = pd.concat([pd.DataFrame([avg_row]), df], ignore_index=True)
    
    # Save the evaluated DataFrame to a new CSV file
    base_name = os.path.basename(csv_file)
    new_name = os.path.splitext(base_name)[0] + '_metricEval.csv'
    output_path = os.path.join(output_folder, new_name)
    df.to_csv(output_path, index=False)
