try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

import gym, ray
from gym.spaces import Discrete, Box
from ray.rllib.agents import ppo

class DiamondCollector(gym.Env):
    
    def __init__(self, env_config):  
        # Static Parameters
        self.size = 50
        self.reward_density = .1
        self.penalty_density = .02
        self.obs_size = 5
        self.max_episode_steps = 100
        self.log_frequency = 1 # CHANGE BACK TO 10
        self.action_dict = {
            0: 'move 1',  # Move one block forward
            1: 'turn 1',  # Turn 90 degrees to the right
            2: 'turn -1',  # Turn 90 degrees to the left
            3: 'attack 1'  # Destroy block
        }

        # Rllib Parameters
        self.action_space = Box(-1.0, 1.0, shape=(4,), dtype=np.float32)
        # self.action_space = Discrete(len(self.action_dict))
        self.observation_space = Box(0, 1, shape=(2 * self.obs_size * self.obs_size, ), dtype=np.float32)

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # DiamondCollector Parameters
        self.obs = None
        self.allow_break_action = False
        self.descending = False
        self.mining_mode = False
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def reset(self):
        """
        Resets the environment for the next episode.

        Returns
            observation: <np.array> flattened initial obseravtion
        """
        # Reset Malmo
        world_state = self.init_malmo()

        # Reset Variables
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        # Log
        if len(self.returns) > self.log_frequency + 1 and \
            len(self.returns) % self.log_frequency == 0:
            self.log_returns()

        # Get Observation
        self.obs, self.allow_break_action = self.get_observation(world_state)

        return self.obs

    def step(self, action):
        """
        Take an action in the environment and return the results.

        Args
            action: <int> index of the action to take

        Returns
            observation: <np.array> flattened array of obseravtion
            reward: <int> reward from taking action
            done: <bool> indicates terminal state
            info: <dict> dictionary of extra information
        """

        # Get Action
        commands = ['move {}'.format(action[0]), 'turn {}'.format(action[1]), '', '']
        commands[2] = 'attack 0' if action[2] <= 0 else 'attack 1'
        if self.descending:
            # self.agent_host.sendCommand('move 0')
            # self.agent_host.sendCommand('turn 0')
            # self.agent_host.sendCommand('pitch 1')
            # time.sleep(0.35)
            # self.agent_host.sendCommand('pitch 0')
            if commands[2] == 'attack 1' and self.allow_break_action:
                self.agent_host.sendCommand('move 0')
                self.agent_host.sendCommand('turn 0')
                self.agent_host.sendCommand('attack 1')
                time.sleep(2.0)
                self.agent_host.sendCommand('attack 0')
                self.episode_step += 1
            else:
                self.agent_host.sendCommand(commands[0])
                self.agent_host.sendCommand(commands[1])
                self.agent_host.sendCommand('attack 0')
                self.episode_step += 1
            # self.agent_host.sendCommand('move -1')
            # time.sleep(0.1)
            # self.agent_host.sendCommand('move 1')
            # time.sleep(0.1)
            # self.agent_host.sendCommand('move 0')
            # self.episode_step += 1
        # elif self.mining_mode:
        #     if action[1] > 0:
        #         self.agent_host.sendCommand('turn 1')
        #     else:
        #         self.agent_host.sendCommand('turn -1')
        #     self.agent_host.sendCommand('turn 0')
        #     self.agent_host.sendCommand('attack 1')
        #     time.sleep(2)
        #     self.agent_host.sendCommand('attack 0')
        #     self.agent_host.sendCommand('pitch 0.2')
        #     time.sleep(0.3)
        #     self.agent_host.sendCommand('pitch 0')
        #     self.agent_host.sendCommand('attack 1')
        #     time.sleep(2)
        #     self.agent_host.sendCommand('attack 0')
        #     self.agent_host.sendCommand('pitch -0.2')
        #     time.sleep(0.3)
        #     self.agent_host.sendCommand('pitch 0')
        else:
            if commands[2] == 'attack 1' and self.allow_break_action:
                self.agent_host.sendCommand('move 0')
                self.agent_host.sendCommand('turn 0')
                self.agent_host.sendCommand('jump 0')
                self.agent_host.sendCommand('attack 1')
                time.sleep(3.5)
                self.agent_host.sendCommand('attack 0')
                time.sleep(0.6)
                self.agent_host.sendCommand('move 1')
                time.sleep(0.6)
                self.episode_step += 1
            else:
                self.agent_host.sendCommand(commands[0])
                self.agent_host.sendCommand(commands[1])
                if action[3] >= 0.6:
                    self.agent_host.sendCommand('jump 1')
                    time.sleep(0.6)
                    self.agent_host.sendCommand('jump 0')
                    time.sleep(0.6)

                self.agent_host.sendCommand('attack 0')
                time.sleep(0.4)
                self.episode_step += 1
        # command = self.action_dict[action]
        # if command != 'attack 1' or self.allow_break_action:
        #     self.agent_host.sendCommand(command)
        #     time.sleep(.2)
        #     self.episode_step += 1

        # Get Observation
        world_state = self.agent_host.getWorldState()
        try:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            if self.checkInventoryForItem(ob, 'cobblestone', 3) and self.checkInventoryForItem(ob, 'stick', 2):
                self.agent_host.sendCommand('craft stone_pickaxe')
            if self.checkInventoryForItem(ob, 'planks', 3) and self.checkInventoryForItem(ob, 'stick', 2):
                self.agent_host.sendCommand('craft wooden_pickaxe')
            if self.checkInventoryForItem(ob, 'log', 1):
                self.agent_host.sendCommand('craft planks')
            if self.checkInventoryForItem(ob, 'planks', 3):
                self.agent_host.sendCommand('craft stick')
                time.sleep(0.4)
            if self.checkInventoryForItem(ob, 'wooden_pickaxe', 1) and self.checkInventoryForItem(ob, 'stick', 2) and ob['YPos'] > 50:
                self.agent_host.sendCommand('hotbar.' + str(self.findHotKeyForBlockType(ob, 'wooden_pickaxe')) + ' 1')
                self.agent_host.sendCommand('hotbar.' + str(self.findHotKeyForBlockType(ob, 'wooden_pickaxe')) + ' 0')
                self.descending = True
                self.agent_host.sendCommand('pitch 1')
                time.sleep(0.35)
                self.agent_host.sendCommand('pitch 0')
            else:
                self.descending = False
            # if ob['YPos'] <= 55:
            #     self.descending = False
            #     self.mining_mode = True
            #     print('mining mode activate')
            #     self.agent_host.sendCommand('look -1')
            #     self.agent_host.sendCommand('look -1')

        except IndexError:
            pass

        for error in world_state.errors:
            print("Error:", error.text)
        self.obs, self.allow_break_action = self.get_observation(world_state) 

        # Get Done
        done = not world_state.is_mission_running
        # world_state = self.agent_host.getWorldState()
        # Get Reward
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()
        self.episode_return += reward
        print(self.episode_return)

        return self.obs, reward, done, dict()


    def get_mission_xml(self):
        lava_str = ""
        diamond_str = ""
        for x in range(-self.size, self.size):
            for y in range(-self.size, self.size):
                if np.random.rand() <= self.reward_density:
                    diamond_str += "<DrawBlock x='{}' y='2' z='{}' type='log'/>".format(x, y)
                if np.random.rand() <= self.penalty_density:
                    lava_str += "<DrawBlock x='{}' y='1' z='{}' type='lava'/>".format(x, y)
        return '''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>Normal life</Summary>
            </About>

            <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                    <DefaultWorldGenerator seed='7011' forceReset='1'/>
                </ServerHandlers>
            </ServerSection>

            <AgentSection mode="Survival">
                <Name>Rover</Name>
                <AgentStart>
                    <Placement x="286.0" y="70" z="-5.0" pitch="30" yaw="0"/>
                    <Inventory>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <AgentQuitFromReachingCommandQuota total="'''+str(5000)+'''" />
                    <ContinuousMovementCommands/>
                    <DiscreteMovementCommands/>
                    <SimpleCraftCommands/>
                    <InventoryCommands/>
                    <ObservationFromHotBar/>
                    <ObservationFromFullStats/>
                    <ObservationFromRay/>
                    <ObservationFromFullInventory/>
                    <RewardForCollectingItem>
                        <Item reward='+1.0' type='log' />
                        <Item reward='+1.0' type='planks'/>
                        <Item reward='+2.0' type='stick'/>
                        <Item reward='+5.0' type='wooden_pickaxe'/>
                        <Item reward='+3.0' type='cobblestone'/> 
                        <Item reward='+8.0' type='stone_pickaxe'/>
                    </RewardForCollectingItem>
                    <RewardForMissionEnd rewardForDeath='-10.0'>
                        <Reward description='drowned' reward='-5.0'/>
                        <Reward description='found_goal' reward='+8.0'/>
                    </RewardForMissionEnd>
                    <RewardForTimeTaken dimension='0' initialReward='0' delta='-0.000001' density='PER_TICK_ACCUMULATED'/>
                    <AgentQuitFromCollectingItem>
                        <Item type='stone_pickaxe' description='found_goal'/>
                    </AgentQuitFromCollectingItem>
                    <AgentQuitFromTouchingBlockType>
                        <Block type='water' description='drowned'/>
                    </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
            </AgentSection>

        </Mission>'''

    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        # my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

        for retry in range(max_retries):
            try:
                self.agent_host.startMission( my_mission, my_clients, my_mission_record, 0, 'DiamondCollector' )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)

        return world_state

    def get_observation(self, world_state):
        """
        Use the agent observation API to get a flattened 2 x 5 x 5 grid around the agent. 
        The agent is in the center square facing up.

        Args
            world_state: <object> current agent world state

        Returns
            observation: <np.array> the state observation
            allow_break_action: <bool> whether the agent is facing a diamond
        """
        obs = np.zeros((2 * self.obs_size * self.obs_size, ))
        allow_break_action = False

        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            # if len(world_state.errors) > 0:
            #     raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                # First we get the json from the observation API
                msg = world_state.observations[-1].text
                observations = json.loads(msg)

                # Get observation
                # grid = observations['floorAll']
                # for i, x in enumerate(grid):
                #     obs[i] = x == 'diamond_ore' or x == 'lava'

                # Rotate observation with orientation of agent
                obs = obs.reshape((2, self.obs_size, self.obs_size))
                yaw = observations['Yaw']
                if yaw >= 225 and yaw < 315:
                    obs = np.rot90(obs, k=1, axes=(1, 2))
                elif yaw >= 315 or yaw < 45:
                    obs = np.rot90(obs, k=2, axes=(1, 2))
                elif yaw >= 45 and yaw < 135:
                    obs = np.rot90(obs, k=3, axes=(1, 2))
                obs = obs.flatten()

                possible_breaks = ['log', 'leaves']
                if self.descending:
                    possible_breaks.append('dirt')
                    possible_breaks.append('stone')
                    possible_breaks.append('grass')
                    possible_breaks.append('diorite')
                    possible_breaks.append('andesite')
                    possible_breaks.append('gravel')


                try:
                    # print(observations['LineOfSight']['type'])
                    allow_break_action = observations['LineOfSight']['type'] in possible_breaks
                except KeyError:
                    pass
                
                break

        return obs, allow_break_action

    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns[1:], box, mode='same')
        plt.clf()
        plt.plot(self.steps[1:], returns_smooth)
        plt.title('Wood Collector')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns10.png')

        with open('returns10.txt', 'w') as f:
            for step, value in zip(self.steps[1:], self.returns[1:]):
                f.write("{}\t{}\n".format(step, value))
        # print(self.returns)

    def checkInventoryForItem(self, obs, requested, count):
        temp = 0
        for i in range(0, 39):
            key = 'InventorySlot_' + str(i) + '_item'
            if key in obs:
                item = obs[key]
                if item == requested:
                    temp += obs['InventorySlot_' + str(i) + '_size']
        return temp >= count

    def findHotKeyForBlockType(self, ob, type):
        '''Hunt in the inventory hotbar observations for the slot which contains the requested type.'''
        for i in range(0, 9):
            slot_name = u'Hotbar_' + str(i) + '_item'
            slot_contents = ob.get(slot_name, "")
            if slot_contents == type:
                return i+1  # +1 to convert from 0-based inventory slot to 1-based hotbar key.
        return -1


if __name__ == '__main__':
    ray.init()
    trainer = ppo.PPOTrainer(env=DiamondCollector, config={
        'env_config': {},           # No environment parameters to configure
        'framework': 'torch',       # Use pyotrch instead of tensorflow
        'num_gpus': 0,              # We aren't using GPUs
        'num_workers': 0            # We aren't using parallelism
    })

    while True:
        print(trainer.train())