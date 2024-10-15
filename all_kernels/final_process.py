import pandas as pd
import os
from tqdm import tqdm

# Open a file to write debug information
with open("debug_log.txt", "w") as log_file:

    final_submission = pd.read_csv("process/final_submission.csv")
    df_ = pd.read_csv("classification.csv")

    # iterate through all kernels
    for f in tqdm(os.listdir("./")):
        if f == "process" or "." in f:
            continue
        print(f)
        # Load the DataFrame from the CSV file
        df_processed = pd.read_csv(f + "/processed_" + f + "_test.csv")
        df = df_.copy()

        # Filter the rows where 'kernel_name' equals the current directory name (f)
        df = df[df['kernel_name'] == f]

        # Initialize 'design' column by concatenating values from 'value_1' to 'value_21'
        df['designs'] = ''
        for i in range(21):
            col_name = "value_" + str(i + 1)
            df['designs'] += '-' + df[col_name].astype(str)
        
        # Remove the leading dash in the 'design' column
        df['designs'] = df['designs'].str.lstrip('-')

        # Drop the 'value_' columns from 1 to 21
        df.drop(columns=[f'value_{i+1}' for i in range(21)], inplace=True)

        # Rename the 'id' column in df_processed to 'ids'
        df_processed.rename(columns={'id': 'ids'}, inplace=True)

        # Merge the two DataFrames on the 'design' column
        df_merged = pd.merge(df, df_processed, on='designs', how='inner')

        # Clean up unnecessary columns
        df_merged.drop(columns=["kernel_name", "target_value", "designs"], inplace=True)

        # Rename 'out_value' to 'valid' and convert valid values
        df_merged.rename(columns={'out_value': 'valid'}, inplace=True)
        df_merged['valid'] = df_merged['valid'].replace({0.0: "False", 1.0: "True"})

        # Iterate through the rows in df_merged to update final_submission
        for index, row in df_merged.iterrows():
            ids = row['ids']
            valid = row['valid']
            
            # Write debug information to file
            log_file.write(f"Processing id: {ids}, valid: {valid}\n")
            log_file.write(final_submission.loc[final_submission["id"] == ids].to_string() + "\n\n")
            
            # Update the 'valid' column if it is currently "True" in final_submission
            
            
            # If the 'valid' is "False", set the related performance and utilization columns to 0.0
            if valid == "False":
                final_submission.loc[final_submission["id"] == ids, ["perf", "util-LUT", "util-DSP", "util-FF", "util-BRAM"]] = 0.0
                final_submission.loc[(final_submission["id"] == ids), "valid"] = valid

    # Save the final_submission with updated values
    final_submission.to_csv("final_submission_new.csv", index=False)
