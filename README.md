# model-based-social-navigation

[![arXiv](https://img.shields.io/badge/arxiv-2011.03922-B31B1B.svg)](https://arxiv.org/abs/2011.03922)
[![video](https://img.shields.io/badge/video-ICRA2021-blue.svg)](https://www.youtube.com/watch?v=K7cBViQ9Vds&t=11s)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Code for **Learning World Transition Model for Socially Aware Robot Navigation** accepted in ICRA2021.


Paper is available [here](https://arxiv.org/abs/2011.03922).


Video is available [here](https://www.youtube.com/watch?v=K7cBViQ9Vds&t=11s).


Presenting video is available [here](https://www.bilibili.com/video/BV1W64y1o7Ru) on Bilibili.



# Get ready
```
git clone https://github.com/YuxiangCui/model-based-social-navigation.git
catkin_make -j6
source devel/setup.bash
```


# MODEL-FREE
```
roslaunch model_free_version start.launch (FOUR-AGENT)
```
for policy performance testing or model free training

- *main.py* (4 agent main function)
- *policy.py* (policy network)
- *environment_four.py* (4 agent environment)
- *agent.py* (agent's states, reward, action...)
- *utils.py* (replay buffer)



# MODEL-BASED
```
roslaunch model_based_version start.launch
```

- *main_mbpo.py* (1/4 agent main function)



- *env_sample.py*
- *environment_one_agent.py* (real 1 agent environment)
- *env_sample_four.py* 
- *environment_four_agent.py* (real 4 agent environment)



- *agent.py* (agent's states, reward, action...)
- *replay_buffer_env.py* (real data replay buffer)
- *replay_buffer_model.py* (virtual data replay buffer)
- *policy.py* (policy network)



- *transition_model.py* (world transition model)
- *ensemble_model_train_mcnet_all.py* 
- *env_predict.py* (virtual environment)


# Acknowledgements
Code references
[MBPO](https://github.com/jxu43/replication-mbpo).
[TD3](https://github.com/sfujim/TD3).

### Citation
If you use our source code, please consider citing the following:
```bibtex
@article{cui2020learning,
  title={Learning World Transition Model for Socially Aware Robot Navigation},
  author={Cui, Yuxiang and Zhang, Haodong and Wang, Yue and Xiong, Rong},
  journal={arXiv preprint arXiv:2011.03922},
  year={2020}
}
```


