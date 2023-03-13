from .network import PolicyGradientNetwork
from ...game.direction import Direction
import tensorflow_probability as tfp
from tensorflow import keras
import tensorflow as tf
import numpy as np
import random
import time


class Agent:
    def __init__(self, alpha=0.003, gamma=0.99, n_actions=4):
        self.gamma = gamma
        self.alpha = alpha
        self.n_actions = n_actions
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []
        self.policy = PolicyGradientNetwork(
            n_actions=n_actions, layers_dims=(256, 256, 256)
        )
        self.policy.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.alpha)
        )

    def choose_action(self, observation):
        state = tf.convert_to_tensor([observation], dtype=tf.float32)
        probs = self.policy(state)
        actions_probs = tfp.distributions.Categorical(probs=probs)
        action = actions_probs.sample()
        return action.numpy()[0]

    def store_transition(self, observation, action, reward):
        self.state_memory.append(observation)
        self.action_memory.append(action)
        self.reward_memory.append(reward)

    def learn(self):
        actions = tf.convert_to_tensor(self.action_memory, dtype=tf.float32)
        rewards = tf.convert_to_tensor(self.reward_memory, dtype=tf.float32)
        G = np.zeros_like(rewards)
        for t in range(len(rewards)):
            G_sum = 0
            discount = 1
            for k in range(t, len(rewards)):
                G_sum += rewards[k] * discount
                discount *= self.gamma
            G[t] = G_sum

        with tf.GradientTape() as tape:
            loss = 0
            for idx, (g, state) in enumerate(zip(G, self.state_memory)):
                state = tf.convert_to_tensor([state], dtype=tf.float32)
                probs = self.policy(state)
                action_probs = tfp.distributions.Categorical(probs=probs)
                if actions[idx] >= self.n_actions:
                    print("Action out of range")
                    continue
                log_prob = action_probs.log_prob(actions[idx])
                loss += -g * tf.squeeze(log_prob)


        gradient = tape.gradient(loss, self.policy.trainable_variables)
        self.policy.optimizer.apply_gradients(
            zip(gradient, self.policy.trainable_variables))

        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []


def get_policy_move(game, agent: Agent) -> Direction:
    state = game.get_policy_state()
    return Direction(agent.choose_action(state))
