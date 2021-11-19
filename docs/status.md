---
layout: default
title: Status
---
## Project Summary
Our project, Smartcraft is focused on the application of malmo towards world navigation and resource collection. The goal is to allow a user to input an item for the agent to craft. Once given an object to craft, the agent should traverse the world to find and collect the resources needed to craft the requested item(s). The agent should also be able to obtain the necessary tools to collect resources, such as a wooden pickaxe being needed to collect stone for a stone pickaxe. Ultimately the goal of our project is to mimic a fully functioning Minecraft player with an object to craft in mind through specific resource gathering. Other ideas we have include allowing the user to input the object to craft through an image.

This can be applied to the game in terms of resource and item collection. This also has real world applications, as seen in the use of reinforcement learning in robotics. [Learning to Walk in the Real World with Minimal Human Effort](https://arxiv.org/pdf/2002.08550.pdf)
## Video Status

## Approach
For our learning algorithm we decided to utilize the rllib library in python and implement proximal policy optimization (PPO). In using PPO, we are using an expected advantage function, which serves to compare previous set of actions’ rewards with a prospective action. This function looks like the following:

<img width="554" alt="Screen Shot 2021-11-18 at 11 10 23 PM" src="https://user-images.githubusercontent.com/47614025/142580320-fcd6e141-6626-4514-8d34-ed4dc558d40e.png"> [Source](https://arxiv.org/pdf/1707.06347.pdf)

The numerator in this equation refers to the reward received from the current set of actions, while the denominator relates to the previous sets of actions’ and their rewards. In essence, we are looking to maximize the ratio of the rewards from a prospective set of actions to prior sets of actions. Intuitively, this makes sense, as we want to pick actions that increase rewards in the most efficient and positive way.

To improve accuracy, we can also provide a threshold on this ratio, so as to not let one group of actions drastically affect the rewards and future actions. This is why we take the actual ratio if it lies between 1 plus or minus this threshold, 1 minus the threshold if the ratio is below it, and 1 plus the threshold if the actual ratio is above it.

In terms of how we are training our agent, we start off exploring a world with many trees around it. We want to train the agent to destroy these ‘log’ blocks to collect wood to be able to craft other objects like sticks, planks, and a wooden pickaxe. Our rewards system is as follows:

---
Reward: +2 +1 +2 +3
Item Collected: log planks sticks wooden pickaxe
---
+2			log
+1			planks
+2			sticks
+3			wooden pickaxe


We end each mission for this training once a wooden pickaxe has been crafted.

We also want to make sure the agent is collecting all of these resources as fast and efficiently as possible, so we added a negative reward with delta -0.0002 per tick that linearly reduces the reward directly with the time.


## Evaluation
Within our evaluation process we have two separate layers of evaluation, individual item evaluation and general item evaluation. Local item evaluation references the evaluation we perform when we are looking for one item and how we evaluate how the agent goes about acquiring the specified item, which in the case of this status report, is a wooden pickaxe. We evaluate each item on successfully crafting the requested item and how quickly we acquire each item. For quantitive data, we provide reward for each resource collected and each intermediary item that needs to be crafted. Since we are trying to increase the time in which the agent crafts the item, we have negative reward for time, so for each tick that the agent spends searching for the items, it is losing reward. The data for this individual item evaluation is highly quantitive. 

The other form of evaluation we are performing is on the general items, where we perform qualitative analysis on the complexity of items we go about collecting. For example, our agent has the ability to acquire wooden items, which is a relatively easy resource to get in Minecraft. We plan on having more complex items such as items made of stone and iron tools, and such we are performing qualitative analysis of how far along this path we make it. So far we can make items requiring wood as a base item, and as we develop the AI to acquire more complex items, we will be able to track our progress. 

## Remaining Goals and Challenges
Our remaining goals are to allow the agent to interact with the world without restrictions. Currently the agent can only break select blocks and has no ability to decide which blocks it needs. The agent should be able to craft tools which requires obtaining rarer resources; wood, stone, iron. To do this we will update the mission schema to reward the agent accordingly for building tools which require rarer resources. To progress we need to create a mission list and continue experimenting with items of harder difficulty. The algorithm works well for wooden tools, however we do not know how the agent will perform when asked to acquire stone or iron tools.

The current limitations of our prototype are that it can only obtain wooden items, cannot interact with water, and there is no flexible way to assign new missions. The challenges we see ahead are teaching the agent to survive if it falls into water and to see if the agent can find diamonds. Currently we are using a default world while testing with wood tools, however we may create and use custom worlds to ensure the agent is able to complete harder missions.


## Resources Used
Project Malmo Documentation at https://microsoft.github.io/malmo/0.30.0/Documentation/classmalmo_1_1_agent_host.html
Malmo XML Schema Documentation at https://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html.
Learning to Walk in the Real World with Minimal Human Effort https://arxiv.org/pdf/2002.08550.pdf
