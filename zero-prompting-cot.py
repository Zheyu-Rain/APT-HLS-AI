import os
import requests
import base64
import json
import csv
# Configuration

API_KEY = #<API-KEY> 
ENDPOINT = #<ENDPOINT> 

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

def extract_kernel(design):
    # Find the part of the design that contains the kernel name, assuming it starts with '__kernel__'
    parts = design.split('.')
    for part in parts:
        if part.startswith('__kernel__'):
            # Extract everything after '__kernel__-', preserving hyphens
            return part[len('__kernel__-'):]  # This keeps the entire kernel name, even with hyphens
    return None

'''
            # Step 4: Build the context
            context = f"""
            Here is the code for kernel {kernel}:\n\n
            ### {kernel_code}\n\n
            LLvm IR representation of this code is:\n\n
            {ll_code}\n\n
            And here is the pragma based on which high-level synthesis optimizes the code and applies PIPE, TILE, or PARA optimizations:\n\n
            ### {pragmas}
            """
'''
def main():
    output_data = []
    # Step 1: Open the CSV file and read the rows one by one
    with open('test.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            design = row['designs']
            design_id = row['id']

            # Step 2: Split the design string by "."
            design_parts = design.split('.')
            version = design_parts[0]  # First part is version
            kernel = extract_kernel(design)
            pragmas = '.'.join(design_parts[2:])  # Everything after version and kernel is considered pragmas

            # Step 3: Based on the kernel, open the corresponding .c and .ll files
            try:
                with open(f'context/{kernel}_kernel.c', 'r') as c_file:
                    kernel_code = c_file.read()
                with open(f'context/{kernel}.ll', 'r') as ll_file:
                    ll_code = ll_file.read()
                with open(f'context/{kernel}.json', 'r') as j_file:
                    j_samples = json.load(j_file)
                    simplified_data = {key: value['valid'] for key, value in j_samples.items()}
                                
            except FileNotFoundError:
                print(f"Error: Files for kernel {kernel} not found. --- {row['id']}")
                continue

            # Step 4: Build the context
            context = f"""
            Here is the code for kernel {kernel}:\n\n
            ### {kernel_code}\n\n
            Here is LLVM IR representation of the kernel code in case helps to decide each pragma optimisation how changes the code:\n\n
            ### {ll_code}\n\n
            And here is the pragma based on which high-level synthesis optimizes the code and applies PIPE, TILE, or PARA optimizations, just like the format provided in examples already:\n\n
            ### {pragmas}
            """
            system_context = f"You are a high-level synthesis system that predicts if a kernel with given pragmas is valid or not. If valid, provide regression values perf and utilization of resources on FPGA. If not valid, provides false. A design is false if a) resource utilisations are over 0.8 b) pragma optimisations are conflicting e.g. PIPE and TILE not possible to apply the same time. Note that the target FPGA is a Alveo U200 working frequency of 250MHz. You are a high level synthesis predition system. You help designers to know their design decision implications.In high level synthesis set of pragmas are provided to optimise the design.Strictly note given a design code in Designer as a user will submit code, and provide high level synthesis pragrams, job is to predict synthesis performance, whether is synthesizable or not, and resource utilisation parameters on FPGA. FPGA is Alveo U200 as the target FPGA and a working frequency of 250MHz.  \n\nStrictly pay attention to the examples given for this kernel showing valid or not and make decision based on the exmaples: {simplified_data}. Based on the provided examples dsecide if design validity will be False or True. tell me why you decide that way. walk me through your decision in 5 steps. Strictly give me 3 reasons why you make decision if design is valid or not based on examples provided. Respond in JSON format so easier to parse the response. ensure that your output is valid JSON without any additional commentary."

            payload = {
              "messages": [
                {
                  "role": "system",
                  "content": system_context 
                },
                {
                  "role": "user",
                  "content": context
                }
              ],
              "max_tokens": 2048,
              "temperature": 0,
              "top_p": 1,
            }
            # Send request
            try:
                response = requests.post(ENDPOINT, headers=headers, json=payload)
                response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

            except requests.RequestException as e:
                raise SystemExit(f"Failed to make the request. Error: {e}")

            # Handle the response as needed (e.g., print or process)
            r = response.json()["choices"][0]["message"]["content"]
            if r.startswith("```") and r.endswith("```"):
                response_text = r.strip("```").strip()
            if response_text.startswith("json"):
                response_text_ = response_text[len("json"):].strip()
            out = json.loads(response_text_) 


            if "false" in str(out["valid"]).lower():
                output_data.append([design_id,"False",0,0,0,0,0])
                print(f"{design_id},False,0,0,0,0,0")
            else:
                output_data.append([design_id,"True",0,0,0,0,0])
                print(f"{design_id},True,0,0,0,0,0")      
                #perf_value = 1091224.0  # Extracted from response (as an example)
                #resource_util = {
                #    'util-BRAM': 0.05,
                #    'util-DSP': 0.01,
                #    'util-LUT': 0.02,
                #    'util-FF': 0.01
                #}
                #output_data.append([
                #    design_id, "True", perf_value,
                #    resource_util['util-LUT'], resource_util['util-DSP'],
                #    resource_util['util-FF'], resource_util['util-BRAM']
                #])

        # Step 7: Write the results to a new CSV file
        with open('response_output.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'valid', 'perf', 'util-LUT', 'util-DSP', 'util-FF', 'util-BRAM']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)  # Write the header
            writer.writerows(output_data)  # Write the collected rows
        return True


if __name__ == '__main__':
    main()
