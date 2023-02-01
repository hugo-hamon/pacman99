from ...game.game import Game
from ...config import Config
from .test import DQNAgent
import numpy as np


def train(config: Config, sound, maze):
    done = False
    agent = DQNAgent(config)
    for e in range(config.neural.episodes):
        game = Game(config, sound, maze)
        state = game.get_state()
        state = np.reshape(state, [1, agent.get_state_size()])

        for time in range(5000):
            action = agent.act(state)

            next_state, reward, done = game.step(action)

            reward = -10 if done else reward
            next_state = np.reshape(next_state, [1, agent.get_state_size()])

            agent.remember(state, action, reward, next_state, done)

            state = next_state
            if done:
                print(
                    f"episode: {e}/{config.neural.episodes}, score: {time}, e: {agent.epsilon:.2}")
                break

        if len(agent.memory) > config.neural.batch_size:
            agent.replay()

        if e % 50 == 0:
            agent.save(f"{config.neural.output_dir}weights_" +
                       '{:04d}'.format(e) + ".hdf5")


def play(config: Config, sound, maze):
    agent = DQNAgent(config)
    agent.load(config.neural.output_dir + config.neural.weights_path)
    game = Game(config, sound, maze)
    state = game.get_state()
    state = np.reshape(state, [1, agent.get_state_size()])
    done = False
    while not done:
        action = agent.act(state)
        next_state, reward, done = game.step(action)
        next_state = np.reshape(next_state, [1, agent.get_state_size()])
        state = next_state
    print(game.get_score())
