import pandas as pd
import os

# Load the submission CSV file
submission_df = pd.read_csv('submission.csv')

# Define the directory where the input CSV files are stored
input_dir = '/home/zheyu/all_kernels/process/input_csv'

# Create a set to track encountered ids
encountered_ids = set()

# Iterate over all input CSV files in the directory
for input_file in os.listdir(input_dir):
    if input_file.endswith('.csv'):
        # Load each input CSV file
        input_df = pd.read_csv(os.path.join(input_dir, input_file))
        
        # Check for duplicate ids in the input file compared to previously encountered ids
        duplicate_ids = set(input_df['ids']).intersection(encountered_ids)
        if duplicate_ids:
            raise ValueError(f"Duplicate ids found in {input_file}: {duplicate_ids}")
        
        # Add the new ids to the encountered set
        encountered_ids.update(input_df['ids'])
        
        # Replace rows in the submission CSV where 'ids' match 'id'
        # Align the input columns to match the target submission columns
        submission_df.set_index('id', inplace=True)
        input_df.set_index('ids', inplace=True)
        
        # Replace the corresponding columns in submission with predicted columns from input CSV
        submission_df.update(input_df[['valid', 'predicted-perf', 'predicted-util-LUT', 'predicted-util-DSP', 'predicted-util-FF', 'predicted-util-BRAM']].rename(columns={
            'predicted-perf': 'perf',
            'predicted-util-LUT': 'util-LUT',
            'predicted-util-DSP': 'util-DSP',
            'predicted-util-FF': 'util-FF',
            'predicted-util-BRAM': 'util-BRAM'
        }))
        
        # Reset index for next iteration
        submission_df.reset_index(inplace=True)

# Save the updated submission file
submission_df.to_csv('updated_submission.csv', index=False)
