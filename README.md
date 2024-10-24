Official Submission of Group APT-HLS for the [ML Contest for Chip Design with HLS](https://github.com/UCLA-VAST/HARP) (Stage #1)

We present two major approaches we implemented for this contest:

**Approach #1**: Zero-shot Prompting with a Large Language Model (LLM)

We divided the task into classification and regression subtasks. Upon reviewing the evaluation criteria, we identified that the classification subtask significantly impacts the error (RMSE), so we prioritized developing a classifier to predict the validity of designs (Valid/Invalid) using the provided training data (v18, v20, and v21).

Using zero-shot prompting, we demonstrated that an LLM can reason about design validity when given sufficient context, including kernel code, LLVM representation, and other details.

To replicate this approach, you will need access to a deployment of `zero-prompting-cot.py`. Please contact the authors for the necessary key.

This method involves presenting examples of various designs and providing reasoning to guide the model's decisions. With this approach, we achieved a `5.123` RMSE on the private leaderboard.

Due to cost limitations, we did not pursue this approach further.

**Approach #2**: Fine-tuning a GNN Model for HLS Representations

Our second approach involved fine-tuning a Graph Neural Network (GNN) capable of learning from HLS representations. We extract the test point from data base and fine tune the model based on this smaller dataset.

We first performed all layer fine-tuning and then blocked the gnn layers to fine-tune the final MLP layers only. The result inference loss was a bit higher than the original model.

To reproduce the result, first you need to install conda env according to the given yml file.
	
	activate the env by typing: 
 
      conda activate ProgSG
	
	if you want to run inference for regression task, switch to the regression branch by typing : git checkout regression
	
		then move to /src dir, type the following command:
			
			python3 -W ignore main.py --force_regen True --task regression --subtask inference --invalid True --target_kernel <the kernel you want to test>
			
		acutally if you want all kernel inference, you need to run them one by one. We already run the regression of all the test point and saved them into a dir called /all_kernels
		
		in all_kernels dir, you will find the regression result of each kernel is arranged into the coresponding folder name.
		
			for example, 2mm/, you will see the following files:
			
				1. combined_script.py (this is the python script used to produce index submission for 2mm kernel).
				2. final__2mm.csv (this is the final processed regression result with index for 2mm kernel)
				3. processed_2mm_test.csv (this is the test point for 2mm kernel which is produced from test.csv)
				4. result_2mm.csv (this is the raw harp regression result for 2mm without index)
				5. test.csv (test points)
				
			originally, each folder contains combined_script.py, test.csv and result__<kernel>.csv, you can run
				
				python3 combined_script.py
				
			to first generate processed_<kernel>_test.csv and map result__<kernel>.csv with index to create final_<kernel>.csv
			
		there is a special folder named 'process/', in this folder, you will find:
		
			1. input_csv/  (which is the folder that contains all final_<kernel>.csv)
			2. map.py (which is the script to combine all final_<kernel>.csv and map them to submission according to index).
			3. set_false.py (this is the script to manually set false if perf, utils <0 or utils>80%)
			4. submission.csv (raw submission format).
			5. updated_submission.csv (this is the mapped all final_<kernel>.csv)
			6. final_submission.csv (this is the file generated after applying set_false.py to updated_submission.csv).
			
		so far, we have the harp inference result for regression task. (continue to have both regression and classification).
		
	if you want to run inference for classification task, switch to the class branch by typing : git checkout class
	
		then move to /src dir, type the following command:
		
			python3 -W ignore main.py --force_regen True --task class --subtask inference --invalid True --all_kernels True
			
		this will produce the classification result for all kernels. the result will be stored in classification.csv file under /src
		
		now move to final_result/ folder, here you will find a script named 'final_process.py', which is used to map classification.csv according to index.
		
		you can type:
		
			python3 final_process.py
			
		to obtain the final submission file that contains both regression and classification result, of which the name is 'final_submission_new.csv'. This is the file we submitted to Kaggle.
		








