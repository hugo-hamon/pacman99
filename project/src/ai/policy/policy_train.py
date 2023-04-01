from ...game.maze.random_maze_factory import RandomMazeFactory
from ...game.direction import Direction
from ...game.maze.maze import Maze
import matplotlib.pyplot as plt
from ...game.game import Game
from ...config import Config
from .agent import Agent
import tensorflow as tf
import numpy as np
import random
import cv2
import time

LAUNCH_NB = 1


def create_game(config: Config, sound):
    path = config.graphics.maze_path
    if config.user.enable_random_maze:
        # set random seed
        random.seed(time.time())
        seed = random.randint(1, 1)
        config.maze.seed = seed
        RandomMazeFactory(config).create()
        path = config.maze.random_maze_path
    maze = Maze(path)
    print(f"Training with seed: {config.maze.seed}")
    return Game(config, sound, maze)


def save_plot(score_history):
    plt.plot(score_history)
    plt.title("Score")
    plt.savefig(f"src/ai/policy/score{LAUNCH_NB}.png")
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

    # For loading a model
    # agent.policy(tf.convert_to_tensor(np.random.random((1, 225)), dtype=tf.float32))
    # agent.policy.load_weights(config.policy.output_dir + config.policy.weights_path)

    score_history = []
    mean_score_history = []
    max_score = 0

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
        mean_score_history.append(avg_score)
        print(
            f"episode {i}, score {score:.1f}, avg score {avg_score:.1f}, remaining dots {game.get_maze().get_total_remain_dots()}")

        if i % 10 == 0 and i > 0:
            save_plot(mean_score_history)

        if avg_score > max_score:
            max_score = avg_score
            agent.policy.save_weights(f"assets/model_output/policy{LAUNCH_NB}.h5")

        """
        if i % 50 == 0 and i > 0:
            agent.policy.save_weights(f"assets/model_output/policy{LAUNCH_NB}_{i}.h5")
        """

    save_plot(score_history)


def play(config: Config, sound):
    agent = Agent(
        alpha=config.policy.alpha, gamma=config.policy.gamma,
        n_actions=config.policy.n_actions
    )

<<<<<<< HEAD
    agent.policy.load_weights("assets/model_output/policy_50.h5")

=======
>>>>>>> 0c962bc424b0368befb7c78ec0723b946b73df81
    game = create_game(config, sound)
    done = False
    score = 0
    observation = game.get_policy_state()

    agent.policy(tf.convert_to_tensor(observation[None, :], dtype=tf.float32))
    agent.policy.load_weights(config.policy.output_dir + config.policy.weights_path)

    while not done:
        action = agent.choose_action(observation)
        visualize_array(observation)
        observation_, reward, done = game.policy_step(action)
        observation = observation_
        score += reward

    print(f"score {score:.1f}")
    print(f"remaining dots {game.get_maze().get_total_remain_dots()}")
