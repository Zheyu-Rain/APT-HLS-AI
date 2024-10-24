Official Submission of Group APT-HLS for the [ML Contest for Chip Design with HLS](https://github.com/UCLA-VAST/HARP) (Stage #1)

We present two major approaches we implemented for this contest:

**Approach #1**: Zero-shot Prompting with a Large Language Model (LLM)

We divided the task into classification and regression subtasks. Upon reviewing the evaluation criteria, we identified that the classification subtask significantly impacts the error (RMSE), so we prioritized developing a classifier to predict the validity of designs (Valid/Invalid) using the provided training data (v18, v20, and v21).

Using zero-shot prompting, we demonstrated that an LLM can reason about design validity when given sufficient context, including kernel code, LLVM representation, and other details.

To replicate this approach, you will need access to a deployment of `zero-prompting-cot.py`. Please contact the authors for the necessary key.

This method involves presenting examples of various designs and providing reasoning to guide the model's decisions. With this approach, we achieved a `5.123` RMSE on the private leaderboard.

Due to cost limitations, we did not pursue this approach further.

**Approach #2**: Fine-tuning a GNN Model for HLS Representations

Our second approach involved fine-tuning a Graph Neural Network (GNN) capable of learning from HLS representations.






