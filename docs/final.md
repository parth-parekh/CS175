---
layout: default
title: Final Report
---
## Video

## Project Summary
Our project, Smartcraft is focused on the application of malmo towards world navigation and resource collection. The goal is to allow a user to input an item for the agent to craft. Once given an object to craft, the agent should traverse the world to find and collect the resources needed to craft the requested item(s). The agent should also be able to obtain the necessary tools to collect resources, such as a wooden pickaxe being needed to collect stone for a stone pickaxe. Ultimately the goal of our project is to mimic a fully functioning Minecraft player with an object to craft in mind through specific resource gathering. Other ideas we have include allowing the user to input the object to craft through an image.

This can be applied to the game in terms of resource and item collection. This also has real world applications, as seen in the use of reinforcement learning in robotics. Learning to Walk in the Real World with Minimal Human Effort
## Approaches
For our learning algorithm we decided to utilize the rllib library in python and implement proximal policy optimization (PPO). In using PPO, we are using an expected advantage function, which serves to compare previous set of actions’ rewards with a prospective action. This function looks like the following:

<img width="554" alt="Screen Shot 2021-11-18 at 11 10 23 PM" src="https://user-images.githubusercontent.com/47614025/142580320-fcd6e141-6626-4514-8d34-ed4dc558d40e.png"> [Source](https://arxiv.org/pdf/1707.06347.pdf)

The numerator in this equation refers to the reward received from the current set of actions, while the denominator relates to the previous sets of actions’ and their rewards. In essence, we are looking to maximize the ratio of the rewards from a prospective set of actions to prior sets of actions. Intuitively, this makes sense, as we want to pick actions that increase rewards in the most efficient and positive way.

To improve accuracy, we can also provide a threshold on this ratio, so as to not let one group of actions drastically affect the rewards and future actions. This is why we take the actual ratio if it lies between 1 plus or minus this threshold, 1 minus the threshold if the ratio is below it, and 1 plus the threshold if the actual ratio is above it.

In terms of how we are training our agent, we start off exploring a world with many trees around it. We want to train the agent to destroy these ‘log’ blocks to collect wood to be able to craft other objects like sticks, planks, and a wooden pickaxe. Our rewards system is as follows:


| Reward | Item collected |
| -------- | ------------- |
| +2 | log |
| +1 | planks |
| +2 | sticks |
| +3 | wooden pickaxe |

We end each mission for this training once a wooden pickaxe has been crafted.

We also want to make sure the agent is collecting all of these resources as fast and efficiently as possible, so we added a negative reward with delta -0.0002 per tick that linearly reduces the reward directly with the time.

## Evaluation

## References
