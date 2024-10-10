import pandas as pd

kernel_name = "3mm"

# Load the DataFrame from the CSV file
df = pd.read_csv("classification.csv")
df_processed = pd.read_csv("processed_"+kernel_name+"_test.csv")

# Filter the rows where 'kernel_name' equals "2mm"
df = df[df['kernel_name'] == kernel_name]

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
df_processed.rename(columns={'id': 'idx'}, inplace=True)

print(df_processed)

# Merge the two DataFrames on the 'design' column
df_merged = pd.merge(df, df_processed, on='designs', how='inner')

# Check for the presence of 'idx' in the merged DataFrame
if 'idx' in df_merged.columns:
    print("The 'idx' column is present in the merged DataFrame.")
else:
    print("The 'idx' column is NOT present in the merged DataFrame.")

# Display the first few rows of the DataFrame
print(df)

df_merged.to_csv("processed_classification.csv", index=False)