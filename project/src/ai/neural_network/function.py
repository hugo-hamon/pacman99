from ...game.maze.random_maze_factory import RandomMazeFactory
from ...game.maze.maze import Maze
from ...game.game import Game
from ...config import Config
from .test import DQNAgent
import numpy as np


def create_game(config: Config, sound):
    path = config.graphics.maze_path
    if config.user.enable_random_maze:
        RandomMazeFactory(config).create()
        path = config.maze.random_maze_path
    maze = Maze(path)
    return Game(config, sound, maze)


def train(config: Config, sound):
    done = False
    agent = DQNAgent(config)
    # agent.epsilon = 1.0
    # agent.load(config.neural.output_dir + config.neural.weights_path)
    mean = []
    mean_score = []
    for e in range(config.neural.episodes):
        game = create_game(config, sound)
        state = game.get_state()
        state = np.reshape(state, [1, agent.get_state_size()])
        pac_x, pac_y = game.pacman.get_position()
        for time in range(10000):
            action = agent.act(state)

            next_state, reward, done = game.step(action)
            reward = -10 if done else reward
            next_state = np.reshape(next_state, [1, agent.get_state_size()])

            agent.remember(state, action, reward, next_state, done)

            state = next_state
            if done:
                print(
                    f"episode: {e}/{config.neural.episodes}, score: {time}, e: {agent.epsilon:.2}")
                mean.append(time)
                mean_score.append(game.get_score())
                break

        print(f"mean on last 10 episodes: {sum(mean)/len(mean)}")
        print(
            f"Game score on last 10 episodes: {sum(mean_score)/len(mean_score)}"
        )
        if len(mean) > 10:
            mean.pop(0)
        if len(mean_score) > 10:
            mean_score.pop(0)

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
