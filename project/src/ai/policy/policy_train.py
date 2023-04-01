from ...game.maze.random_maze_factory import RandomMazeFactory
from ...game.direction import Direction
from ...game.maze.maze import Maze
import matplotlib.pyplot as plt
from ...game.game import Game
from ...config import Config
from .agent import Agent
import tensorflow as tf
import numpy as np
import cv2


def create_game(config: Config, sound):
    path = config.graphics.maze_path
    if config.user.enable_random_maze:
        config.maze.seed = np.random.randint(1, 2)
        print("Train on random maze with seed: ", config.maze.seed)
        RandomMazeFactory(config).create()
        path = config.maze.random_maze_path
    maze = Maze(path)
    return Game(config, sound, maze)


def save_plot(score_history):
    plt.plot(score_history)
    plt.title("Score")
    plt.savefig("src/ai/policy/score.png")
    plt.clf()


def visualize_array(array):
    """Array is a linear array grayscale image"""
    array_size = 15
    # convert array of size 11*11 to 11x11x1
    array = np.reshape(array, (array_size, array_size, 1))
    # convert array of size 11x11x1 to 11x11x3
    array = np.repeat(array, 3, axis=2)
    # convert array of size 11x11x3 to 220x220x3
    array = np.repeat(array, 20, axis=0)
    array = np.repeat(array, 20, axis=1)
    while True:
        cv2.imshow('image', array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def train(config: Config, sound):
    agent = Agent(
        alpha=config.policy.alpha, gamma=config.policy.gamma,
        n_actions=config.policy.n_actions
    )

    score_history = []

    for i in range(config.policy.episodes):
        game = create_game(config, sound)
        done = False
        score = 0
        observation = game.get_policy_state()
        while not done:
            # visualize_array(observation)
            action = agent.choose_action(observation)
            observation_, reward, done = game.policy_step(action)
            # print(f"reward: {reward}, done: {done}")
            agent.store_transition(observation, action, reward)
            observation = observation_
            score += reward
        score_history.append(score)

        agent.learn()

        avg_score = np.mean(score_history[-100:])
        print(
            f"episode {i}, score {score:.1f}, avg score {avg_score:.1f}, remaining dots {game.get_maze().get_total_remain_dots()}")

        if i % 10 == 0 and i > 0:
            save_plot(score_history)

        if i % 50 == 0 and i > 0:
            agent.policy.save_weights(f"assets/model_output/policy_{i}.h5")


    agent.policy.save_weights("assets/model_output/policy_last.h5")
    save_plot(score_history)


def play(config: Config, sound):
    agent = Agent(
        alpha=config.policy.alpha, gamma=config.policy.gamma,
        n_actions=config.policy.n_actions
    )

    agent.policy.load_weights("assets/model_output/policy_50.h5")

    game = create_game(config, sound)
    done = False
    score = 0
    observation = game.get_policy_state()

    while not done:
        action = agent.choose_action(observation)
        observation_, reward, done = game.policy_step(action)
        observation = observation_
        score += reward

    print(f"score {score:.1f}")
