import pandas as pd
import os
from tqdm import tqdm

final_submission = pd.read_csv("process/final_submission.csv")
#final_submission.drop(columns=["valid"], inplace=True)
#final_submission.rename(columns={'id': 'ids'}, inplace=True)
df_ = pd.read_csv("classification.csv")

# iterate through all kernels
for f in tqdm(os.listdir("./")):
    if f == "process" or "." in f:
        continue
    print(f)
    # Load the DataFrame from the CSV file
    df_processed = pd.read_csv(f+"/processed_"+f+"_test.csv")
    df = df_.copy()

    # Filter the rows where 'kernel_name' equals "2mm"
    df = df[df['kernel_name'] == f]

    # Initialize 'design' column as an empty string
    df['designs'] = ''

    # Concatenate columns from 'value_0' to 'value_20'
    for i in range(21):
        col_name = "value_" + str(i+1)
        df['designs'] = df['designs'] + '-' + df[col_name].astype(str)
        # Drop the current column
        df.drop(columns=[col_name], inplace=True)

    # If you want to remove the leading '-' in the 'design' column
    df['designs'] = df['designs'].str.lstrip('-')

    # Rename the 'id' column in df_second to 'idx'
    df_processed.rename(columns={'id': 'ids'}, inplace=True)

    #print(df_processed)

    # Merge the two DataFrames on the 'design' column
    df_merged = pd.merge(df, df_processed, on='designs', how='inner')

    df_merged.drop(columns=["kernel_name", "target_value", "designs"], inplace=True)

    df_merged.rename(columns={'out_value': 'valid'}, inplace=True)

    df_merged['valid'] = df_merged['valid'].replace({0.0: "FALSE", 1.0: "TRUE"})

    #final_submission = pd.merge(final_submission, df_merged, on='ids', how='inner')

    for index, row in df_merged.iterrows():
        ids = row['ids']
        valid = row['valid']
        final_submission.loc[final_submission["id"] == ids, "valid"] = valid
        
        final_submission.loc[final_submission["id"] == ids, "util-LUT"] = 0.0
        final_submission.loc[final_submission["id"] == ids, "util-DSP"] = 0.0
        final_submission.loc[final_submission["id"] == ids, "util-FF"] = 0.0
        final_submission.loc[final_submission["id"] == ids, "util-BRAM"] = 0.0

    # Display the first few rows of the DataFrame
    #print(df)

    df_merged.to_csv("processed_classification.csv", index=False)

final_submission.to_csv("final_submission_new.csv", index=False)