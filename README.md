Official submission of group APT-HLS for the ML Contest for Chip Design with HLS (Stage #1).

Our submission contains two major approaches we implemented for this contest:

Approach #1: Zero-shot prompting of a large language model

We devided the task into classification and regression subtasks. After exploring the evaluation criteria we realised that the classification subtask has significant impact on the error. Therefore we focused mainly on getting a classifier to predict Valid/Invalid designs based on the training data provided.


Approach #2: Fine tuning a GNN model capable of learning HLS representations






