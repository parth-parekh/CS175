---
layout: default
title: Final Report
---
## Video

## Project Summary
Our project, Smartcraft places the agent into a default world where it will learn to gather resources to craft items. The goal of the project is to teach the agent to collect the various resources needed to craft a target item. At any point, the agent can turn left or right, jump, move, and break the block in its line of sight. Once the agent is given an object to craft, the agent traverses the world to collect the resources needed to craft the item. Ultimately our goal was to create an AI which could gather resources and create a desired item in a default world. For our learning algorithm we decided to utilize the rllib library in python and implement proximal policy optimization.
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
Our evaluation process consists of two separate layers of evaluation; individual item evaluation and general item evaluation. Local item evaluation references evaluation we perform when the agent is looking for the resources to craft the specified item. In the runs, the agent needs to craft wooden tools in order to craft more complex items. We evaluate the items based on success and time. Quantitively, we reward the agent for each resource collected and intermediate items which need to be crafted. Because we wanted to reduce the amount of time the agent would take to gather resources and craft the item, we provide a negative time reward. Thus, for each tick the agent spends looking for the resources to craft the item, it is losing reward. Our team tested many delta values for the time reward because the value needed to be right to ensure the agent would prioritize accomplishing the task. Too large and the agent would die or end the mission faster and high enough so that the agent efficiently completes its task. The data for this individual item evaluation is highly quantitive. 
The other form of evaluation we are performing is on the general items, where we perform qualitative analysis on the complexity of items we go about collecting. For example, our agent has the ability to acquire wooden items, which is a relatively easy resource to get in Minecraft. This is one step towards collecting difficult to acquire resources such as stone and iron. Even if the agent is unsuccessful in acquiring the final item, it will be rewarded for taking intermediate steps towards the completion of its goal.
## References
