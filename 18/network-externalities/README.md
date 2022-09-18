# network-externality
This is the implementation of paper no.9 in [2021 Soical Simulation Workshop at Academia Sinica](https://www.ios.sinica.edu.tw/msgNo/20210723-1). Our team (5, 擬會作社模) won the second place in the final stage of the workshop.

Paper: [How Network Externalities Can Exacerbate Intergroup Inequality (DiMaggio and Garip, 2011)](https://www.jstor.org/stable/pdf/10.1086/659653.pdf?refreqid=excelsior%3Aabf277dd8e8dbfc001069fcbf9e1b7aa)


## Quick Start
### Run by Functions
```python
# set up
parser = ArgsModel()
args = parser.get_args()
path_to_agentInfo = "PATH/TO/CSV"
agent_data_holder = AgentDataHolder(path_to_agentInfo)

# visualize adopting progress of the experiment expNo.
visualize_3d(agent_data_holder, expNo=args.expNo)

# run all experiments 1~7 and plot results
legend_n = ["No NE", "Gen NE", "Spe NE (h=0)", "Spe NE (h=0.25)", "Spe NE (h=0.5)", "Spe NE (h=0.75)", "Spe NE (h=1.0)"]
path_to_results = run_all_exp(args, agent_data_holder)
data_dict = read_result(path_to_results)
plot_result(data_dict, legend_n, suffix)
```

### Run in Ternimals
```bash
# visualize experiments 3
python main.py --vis --expNo 3
# run all 7 experiments, where each experiment runs 1000 trails
python main.py --run_all --n_trail 1000
```

## Experiments Conditions

1. No Network Externalities (NE)
2. General NE
3. Specific NE, h=0.0
4. Specific NE, h=0.25
5. Specific NE, h=0.5
6. Specific NE, h=0.75
7. Specific NE, h=1.0

## Visualization Results

### 3. Specific NE, h=0.0

https://user-images.githubusercontent.com/43054769/131053723-a77ad7ef-7ff2-41be-b62c-3091c06bbb9a.mp4

### 4. Specific NE, h=0.25

https://user-images.githubusercontent.com/43054769/131053607-c09f7dd5-3f6c-4d47-80ae-3fc26f470450.mp4

### 5. Specific NE, h=0.5

https://user-images.githubusercontent.com/43054769/131064219-87c3a9b8-800a-444c-8491-f6dc2658252b.mp4

### 6. Specific NE, h=0.75

https://user-images.githubusercontent.com/43054769/131053628-3aa5f0c3-97ab-4bfb-a46b-02c16633a81a.mp4

### 7. Specific NE, h=1.0

https://user-images.githubusercontent.com/43054769/131053685-202e8926-0fc6-4e36-8883-873ba938d614.mp4
