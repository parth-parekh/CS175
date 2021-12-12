---
layout: default
title: Final Report
---
## Video

## Project Summary
Our project, Smartcraft places the agent into a default world where it will learn to gather resources to craft items. The goal of the project is to teach the agent to collect the various resources needed to craft a target item. At any point, the agent can turn left or right, jump, move, and break the block in its line of sight. Once the agent is given an object to craft, the agent traverses the world to collect the resources needed to craft the item. Ultimately our goal was to create an AI which could gather resources and create a desired item in a default world. For our learning algorithm we decided to utilize the rllib library in python and implement proximal policy optimization. We used PPO to ensure the agent would be trained efficiently; gather resources in with less time and fewer steps.
## Approaches
Our baseline approach consisted of using RL learning to collect wood. On top of that, we have now added the capability of the agent acting on the items that he has collected, also known as a crafting ability. In addition, I problem we experience greatly when training our agent was the presence of water, as the agent would waste a great deal of time to attempt to get out of the water. Therefore, we wanted to train the agent to avoid water altogether by proving a negative reward for touching the block type.

Our main goal was to make our agent collect wood, in order to have him craft more complicated items. Placing the agent into a default world added to the complexity of the problem because there were many objects that the agent had to recognize as useful or not useful. We used reinforcement learning to train the agent to only look for wood that can help him to build a wooden pickaxe. This required looking for trees, whilst avoiding hitting other objects like pigs, the ground, bushes, etc. We also incorporated continuous movements, as an upgrade to discrete movements, as this requires more variables to account for and more time for the agent to train.

<img width="554" alt="Screen Shot 2021-11-18 at 11 10 23 PM" src="https://user-images.githubusercontent.com/47614025/142580320-fcd6e141-6626-4514-8d34-ed4dc558d40e.png"> [Source](https://arxiv.org/pdf/1707.06347.pdf)

By using information from previous runs, we are able to train the agent to perform smarter and smarter actions each run. One problem we ran into at first was adjusting to the time requried for the agent to actually break wood. The reward system was not reacting accurately to some thing we saw on the screen, so we had to change the amount of time the agent must pause after beginning an attack command.

Our PPO psuedocode looks like this following:  

![image](https://user-images.githubusercontent.com/47614025/145696738-76bea018-7307-463d-9417-02f28fbe3552.png)
[Source](https://spinningup.openai.com/en/latest/algorithms/ppo.html#proximal-policy-optimization)

The PPO structure limits a lot of randomness that are involved in other machine learning algorithms, and for our purposes we wanted a stable learning algorithm. This is especially applicable to when we try to craft more complicated items that require chaining many actions together.  

Our reward system looks like the following table (explanation in evaluation):  

| Reward | Item collected |
| -------- | ------------- |
| +1 | log |
| +1 | planks |
| +2 | sticks |
| +5 | wooden pickaxe |
| +3 | stone |
| -5 | drowning in water |

## Evaluation
Our evaluation process consists of two separate layers of evaluation; individual item evaluation and general item evaluation. Local item evaluation references evaluation we perform when the agent is looking for the resources to craft the specified item. In the runs, the agent needs to craft wooden tools in order to craft more complex items. We evaluate the items based on success and time. Quantitively, as listed above in the table, we reward the agent for each resource collected and intermediate items which need to be crafted. Because we wanted to reduce the amount of time the agent would take to gather resources and craft the item, we provide a negative time reward. Thus, for each tick the agent spends looking for the resources to craft the item, it is losing reward. Our team tested many delta values for the time reward because the value needed to be right to ensure the agent would prioritize accomplishing the task. Too large and the agent would die or end the mission faster and high enough so that the agent efficiently completes its task. The data for this individual item evaluation is highly quantitive.  


This graph shows the agent learning to build a wooden pickaxe, but before we implemented the negative reward for entering water. This was also a preliminary delta value for time, as after running this, we realized our delta value for the time was outweighing our positive rewards for items collected.


This graph shows the agent learning to just build a wooden pickaxe in the default world:


This graph shows the agent learning to build the stone pickaxe in the default world:

The other form of evaluation we are performing is on the general items, where we perform qualitative analysis on the complexity of items we go about collecting. For example, our agent has the ability to acquire wooden items, which is a relatively easy resource to get in Minecraft. This is one step towards collecting difficult to acquire resources such as stone and iron. Even if the agent is unsuccessful in acquiring the final item, it will be rewarded for taking intermediate steps towards the completion of its goal.
## References
