import pandas as pd

# Load the updated_submission.csv
submission_df = pd.read_csv('updated_submission.csv')

# Define the columns to check for the condition
util_columns = ['util-LUT', 'util-DSP', 'util-FF', 'util-BRAM']

# Scan the util columns and check if any value is < 0.0 or > 0.8, and also check perf if it's < 0.0
for index, row in submission_df.iterrows():
    # Check if any util column is < 0.0 or > 0.8
    util_condition = any((row[util_col] < 0.0 or row[util_col] > 0.8) for util_col in util_columns)
    
    # Check if perf is < 0.0
    perf_condition = row['perf'] < 0.0
    
    # If either condition is true, set valid to False and reset perf and util columns to 0.0
    if util_condition or perf_condition:
        # Set the valid column to False
        submission_df.at[index, 'valid'] = False
        # Set the perf and util columns to 0.0
        submission_df.at[index, 'perf'] = 0.0
        submission_df.at[index, 'util-LUT'] = 0.0
        submission_df.at[index, 'util-DSP'] = 0.0
        submission_df.at[index, 'util-FF'] = 0.0
        submission_df.at[index, 'util-BRAM'] = 0.0

# Save the updated submission file
submission_df.to_csv('final_submission.csv', index=False)

print("Updated the file based on the criteria and saved as final_submission.csv.")
