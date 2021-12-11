---
layout: default
title: Final Report
---
## Video

## Project Summary
Our project, Smartcraft places the agent into a default world where it will learn to gather resources to craft items. The goal of the project is to teach the agent to collect the various resources needed to craft a target item. At any point, the agent can turn left or right, jump, move, and break the block in its line of sight. Once the agent is given an object to craft, the agent traverses the world to collect the resources needed to craft the item. Ultimately our goal was to create an AI which could gather resources and create a desired item in a default world. For our learning algorithm we decided to utilize the rllib library in python and implement proximal policy optimization. We used PPO to ensure the agent would be trained efficiently; gather resources in with less time and fewer steps.
## Approaches


## Evaluation
Our evaluation process consists of two separate layers of evaluation; individual item evaluation and general item evaluation. Local item evaluation references evaluation we perform when the agent is looking for the resources to craft the specified item. In the runs, the agent needs to craft wooden tools in order to craft more complex items. We evaluate the items based on success and time. Quantitively, we reward the agent for each resource collected and intermediate items which need to be crafted. Because we wanted to reduce the amount of time the agent would take to gather resources and craft the item, we provide a negative time reward. Thus, for each tick the agent spends looking for the resources to craft the item, it is losing reward. Our team tested many delta values for the time reward because the value needed to be right to ensure the agent would prioritize accomplishing the task. Too large and the agent would die or end the mission faster and high enough so that the agent efficiently completes its task. The data for this individual item evaluation is highly quantitive. 
The other form of evaluation we are performing is on the general items, where we perform qualitative analysis on the complexity of items we go about collecting. For example, our agent has the ability to acquire wooden items, which is a relatively easy resource to get in Minecraft. This is one step towards collecting difficult to acquire resources such as stone and iron. Even if the agent is unsuccessful in acquiring the final item, it will be rewarded for taking intermediate steps towards the completion of its goal.
## References
