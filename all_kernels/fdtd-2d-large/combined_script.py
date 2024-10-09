import pandas as pd
import argparse

# Set up argument parser to allow the name and start id to be passed from the terminal
parser = argparse.ArgumentParser(description="Process kernel name and specify starting ID.")
parser.add_argument('--name', type=str, required=True, help="Specify the kernel name (e.g., stencil)")
parser.add_argument('--start-id', type=int, required=True, help="Specify the starting ID (e.g., 3503)")

# Parse the command-line arguments
args = parser.parse_args()
name = args.name  # Kernel name passed from the terminal
start_id = args.start_id  # Starting ID passed from the terminal

print(f"Kernel name: {name}")
print(f"Start ID: {start_id}")

# Part 1: Process the 'test.csv' to transform the 'designs' column

# Load your test.csv file into a DataFrame
df = pd.read_csv('test.csv')

# Step 1: Filter out rows that contain exactly '.__kernel__-name.' in the 'designs' column
pattern = f'\\.__kernel__-{name}\\.'  # Match exactly '.__kernel__-name.'
df = df[df['designs'].str.contains(pattern, regex=True)]

# Step 2: Remove the entire pattern (.__version__-v21.__kernel__-name.) from each row
pattern_to_remove = f'__version__-v21.__kernel__-{name}\\.'
df['designs'] = df['designs'].str.replace(pattern_to_remove, '', regex=True)

# Step 3: Define the pattern to remove (e.g., __PARA__L0_0_0-5) and keep the number after the dash
pattern_to_keep_number = r'(__PARA__L\d+(_\d+)*|__PIPE__L\d+(_\d+)*|__TILE__L\d+(_\d+)*)-'
df['designs'] = df['designs'].str.replace(pattern_to_keep_number, '', regex=True)

# Step 4: Replace 'off' with 1, 'flatten' with 100, and 'NA' with 50
df['designs'] = df['designs'].str.replace('off', '1', regex=False)
df['designs'] = df['designs'].str.replace('flatten', '100', regex=False)
df['designs'] = df['designs'].str.replace('NA', '50', regex=False)

# Step 5: Zero-pad each design to ensure exactly 20 elements, plus 'id', making it 21 total
def pad_and_format_pragmas(design_str):
    numbers = design_str.split('.')
    numbers += ['0'] * (21 - len(numbers))  # Adjust to pad to 21 total elements
    return '-'.join(f'{int(num)}.0' for num in numbers)

df['designs'] = df['designs'].apply(pad_and_format_pragmas)

# Save the updated DataFrame back to CSV file
processed_csv_filename = f'processed_{name}_test.csv'
df.to_csv(processed_csv_filename, index=False)

# Part 2: Reorder 'result.csv' based on the matching 'designs' and 'pragma'

# Load both CSV files
updated_df = pd.read_csv(processed_csv_filename)  # This contains 'id' and 'designs'
result_filename = f'result__{name}.csv'
result_df = pd.read_csv(result_filename)  # This contains 'pragma' and other columns

# Strip leading/trailing spaces from 'pragma' and 'designs' to ensure proper matching
updated_df['designs'] = updated_df['designs'].str.strip()
result_df['pragma'] = result_df['pragma'].str.strip()

# Merge the two DataFrames based on 'pragma' in result_df and 'designs' in updated_test.csv
merged_df = pd.merge(result_df, updated_df, left_on='pragma', right_on='designs')

if merged_df.empty:
    print("\nNo matches found! Check the formatting of 'pragma' and 'designs'.")
else:
    # Sort by 'id' and drop unnecessary columns
    merged_df = merged_df.sort_values(by='id').drop(columns=['designs', 'id'])

    # Step 3: Delete the specified columns
    columns_to_delete = ['gname', 'pragma', 'acutal-perf', 'acutal-util-LUT', 'acutal-util-FF', 'acutal-util-DSP', 'acutal-util-BRAM']
    merged_df = merged_df.drop(columns=columns_to_delete)

    # Step 4: Rearrange the columns to switch 'predicted-util-FF' and 'predicted-util-DSP'
    new_column_order = ['predicted-perf', 'predicted-util-LUT', 'predicted-util-DSP', 'predicted-util-FF', 'predicted-util-BRAM']
    merged_df = merged_df[new_column_order]

    # Step 5: Add 'ids' column with numerical IDs in the specified range
    merged_df['ids'] = range(start_id, len(merged_df) + start_id)

    # Step 6: Add 'valid' column with all values set to True
    merged_df['valid'] = True

    # Step 7: Reorder the columns to place 'ids' and 'valid' as the first two columns
    merged_df = merged_df[['ids', 'valid'] + [col for col in merged_df.columns if col not in ['ids', 'valid']]]

    # Uncomment the section below to enable validation based on utilization values
    '''
    # Step 8: Validate each row, set 'valid' to False and values to 0.0 if util columns are out of bounds
    def validate_and_update_row(row):
        # List of utilization columns to check
        util_columns_to_check = ['predicted-util-LUT', 'predicted-util-DSP', 'predicted-util-FF', 'predicted-util-BRAM']
        
        # Check if any utilization column has a value less than 0 or greater than 0.8
        if any((row[col] < 0 or row[col] > 0.8) for col in util_columns_to_check):
            row['valid'] = False
            # Set all columns (perf and util columns) to 0.0
            columns_to_reset = ['predicted-perf'] + util_columns_to_check
            for col in columns_to_reset:
                row[col] = 0.0
        return row

    # Apply the validation function to each row
    merged_df = merged_df.apply(validate_and_update_row, axis=1)
    '''

    # Step 9: Save the manipulated and validated data to a new CSV file
    output_file_path = f'final__{name}.csv'
    merged_df.to_csv(output_file_path, index=False)

    print(f"\nValidation and modification completed. Data saved to {output_file_path}")
