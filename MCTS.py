import math
import time
import random
from collections import defaultdict

class Node:
    next_node_id = 0
    visits = defaultdict(lambda: 0)

    def __init__(self, mdp, parent, state, qfunction, bandit, reward=0.0, action=None):
        self.mdp = mdp
        self.parent = parent
        self.state = state
        self.qfunction = qfunction  # Q函数存储状态-动作值
        self.bandit = bandit        # 多臂老虎机算法
        self.reward = reward        # 到达此状态的即时奖励
        self.action = action        # 生成此节点的动作

    def select(self):
        while self.is_fully_expanded():
            action = self.bandit.select(self.state, self.mdp.get_actions(self.state), self.qfunction)
            next_state = self.mdp.transition(self.state, action)
            self = self.get_child(next_state)
        return self

    def expand(self):
        if not self.mdp.is_terminal(self.state):
            action = random.choice(list(self.mdp.get_actions(self.state) - self.children.keys()))
            next_state = self.mdp.transition(self.state, action)
            self.children[action] = (next_state, 1.0)  # 简化处理概率
        return self

    def back_propagate(self, reward):
        self.visits[self.state] += 1
        self.qfunction.update(self.state, self.action, reward)
        if self.parent:
            self.parent.back_propagate(reward * self.mdp.discount_factor)

class MCTS:
    def __init__(self, mdp, qfunction, bandit):
        self.mdp = mdp
        self.qfunction = qfunction
        self.bandit = bandit

    def search(self, timeout=1):
        root = Node(self.mdp, None, self.mdp.initial_state(), self.qfunction, self.bandit)
        start_time = time.time()
        while time.time() - start_time < timeout:
            node = root.select()
            if not self.mdp.is_terminal(node.state):
                node = node.expand()
                reward = self.simulate(node.state)
                node.back_propagate(reward)
        return root

    def simulate(self, state):
        total_reward = 0.0
        depth = 0
        while not self.mdp.is_terminal(state):
            action = random.choice(self.mdp.get_actions(state))
            next_state, reward = self.mdp.transition(state, action)
            total_reward += (self.mdp.discount_factor ​**​ depth) * reward
            state = next_state
            depth += 1
        return total_reward