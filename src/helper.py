import csv
import re
import argparse

def parse_design(design):
    # Extract key-value pairs from design string using regex
    param_pattern = re.compile(r'__(PARA|PIPE|TILE)__(L\d+)(?:_(\d+))?-(\w+)')
    params = {}
    
    matches = param_pattern.findall(design)
    for param_type, level, sublevel, value in matches:
        # Handle NA as empty string, and leave "off" as it is
        if value == "NA":
            value = ""
        elif value.isdigit():
            value = int(value)
        
        key = f"__{param_type}__{level}"
        if sublevel:
            key += f"_{sublevel}"
        
        params[key] = value
    
    return params

def get_input_list_for_kernel(filename, kernel_name):
    input_list = []
    matching_ids = []
    
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        
        # Filter rows where the kernel matches the provided kernel_name
        for row in reader:
            design = row['designs']
            if f"__kernel__-{kernel_name}" in design:
                params = parse_design(design)
                input_list.append(params)
                matching_ids.append(row['id'])  # Collect the matching id
    
    return input_list, matching_ids

def parse(kernel_name, file):
    # Argument parser to take kernel name and file as input
    #parser = argparse.ArgumentParser(description="Extract kernel parameters from CSV.")
    #parser.add_argument('--kernel-name', type=str, required=True, help='Name of the kernel to filter')
    #parser.add_argument('--file', type=str, required=True, help='CSV file containing the design data')
    
    #args = parser.parse_args()
    
    # Get the input list and matching ids for the provided kernel name
    input_list, matching_ids = get_input_list_for_kernel(file, kernel_name)
    
    # Grouping the dictionaries into a list of lists as per the requirement
    grouped_input_list = [input_list]
    
    # Print the result
    #print(f"input_list = {grouped_input_list}")
    #print(f"Matching IDs: {matching_ids}")

    return grouped_input_list, matching_ids

""" if __name__ == "__main__":
    main() """