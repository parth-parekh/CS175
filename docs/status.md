---
layout: default
title: Status
---
## Project Summary
Our project, Smartcraft is focused on the application of malmo towards world navigation and resource collection. The goal is to allow a user to input an item for the agent to craft. Once given an object to craft, the agent should traverse the world to find and collect the resources needed to craft the requested item(s). The agent should also be able to obtain the necessary tools to collect resources, such as a wooden pickaxe being needed to collect stone for a stone pickaxe. Ultimately the goal of our project is to mimic a fully functioning Minecraft player with an object to craft in mind through specific resource gathering. Other ideas we have include allowing the user to input the object to craft through an image.

This can be applied to the game in terms of resource and item collection. This also has real world applications, as seen in the use of reinforcement learning in robotics. [Learning to Walk in the Real World with Minimal Human Effort](https://arxiv.org/pdf/2002.08550.pdf)
## Video Status

## Approach

## Evaluation
Within our evaluation process we have two separate layers of evaluation, individual item evaluation and general item evaluation. Local item evaluation references the evaluation we perform when we are looking for one item and how we evaluate how the agent goes about acquiring the specified item, which in the case of this status report, is a wooden pickaxe. We evaluate each item on successfully crafting the requested item and how quickly we acquire each item. For quantitive data, we provide reward for each resource collected and each intermediary item that needs to be crafted. Since we are trying to increase the time in which the agent crafts the item, we have negative reward for time, so for each tick that the agent spends searching for the items, it is losing reward. The data for this individual item evaluation is highly quantitive. 

The other form of evaluation we are performing is on the general items, where we perform qualitative analysis on the complexity of items we go about collecting. For example, our agent has the ability to acquire wooden items, which is a relatively easy resource to get in Minecraft. We plan on having more complex items such as items made of stone and iron tools, and such we are performing qualitative analysis of how far along this path we make it. So far we can make items requiring wood as a base item, and as we develop the AI to acquire more complex items, we will be able to track our progress. 

## Remaining Goals and Challenges
Our remaining 
Goals: Allow the agent to interact with the world without restrcitions. The agent should be able to craft tools which requires obtaining rarer resources; wood, stone, iron. Update the mission schema to progressively reward the agent for building tools with rarer resources. 

What we need to do : Create a mission list, continue experimenting with items of harder difficulty, We want the agent to be able to obtain the necessary resoucres to craft wood tools, then stone tools, then iron tools. 

Limitations of the Prototype: Can only obtain wooden items, cannot interact with water, no flexible way to assign new missions. We want the agent to be able to obtain wood tools, then stone tools, then iron tools. 

Challenges: Implementing image processing to identify items to create.

## Resources Used
Project Malmo Documentation at https://microsoft.github.io/malmo/0.30.0/Documentation/classmalmo_1_1_agent_host.html
Malmo XML Schema Documentation at https://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html.

