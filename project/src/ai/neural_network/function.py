from ...game.maze.random_maze_factory import RandomMazeFactory
from .test_conv2d import visualize_array
from ...game.direction import Direction
from .test_conv2d import ConvDQNAgent
# from .DQNAgent import DQNAgent
from ...game.maze.maze import Maze
import matplotlib.pyplot as plt
from ...game.game import Game
from ...config import Config
from time import time
import numpy as np
import random
import tqdm

# MEMORY LEAKED LIBRARIES
import sys
import gc
from pympler import summary, muppy


def create_game(config: Config, sound, maze):
    return Game(config, sound, maze)


def save_all_information(config: Config, agent):
    with open("src/ai/neural_network/network_information.txt", "w") as f:
        f.write("Parametres du reseau de neurones:\n\n")
        f.write(f"Episode max: {config.neural.episodes}\n")
        f.write(f"Batch size: {config.neural.batch_size}\n")
        f.write(f"Learning rate: {config.neural.learning_rate}\n")
        f.write(f"Epsilon decay: {agent.epsilon_decay}\n")
        f.write(f"Epsilon min: {agent.epsilon_min}\n")
        agent.summary(f)


def save_plot_data(mean_life_time, mean_score):
    '''Save data about score and life time in text files'''
    with open("src/ai/neural_network/mean_score_data.txt", "a") as f:
        for i in mean_score:
            f.write(f"{i}\n")

    with open("src/ai/neural_network/mean_life_time_data.txt", "a") as f:
        for i in mean_life_time:
            f.write(f"{i}\n")


def save_plot(mean_life_time, mean_score):
    mean_mean_life_time = []
    mean_mean_score = []
    for i in range(0, len(mean_life_time), 10):
        mean_mean_life_time.append(np.mean(mean_life_time[i:i+10]))
        mean_mean_score.append(np.mean(mean_score[i:i+10]))
    plt.plot(mean_mean_life_time)
    plt.title("Durée de vie moyenne")
    plt.savefig("src/ai/neural_network/mean_life_time.png")
    plt.clf()
    plt.plot(mean_mean_score)
    plt.title("Score moyen")
    plt.savefig("src/ai/neural_network/mean_score.png")
    plt.clf()


def train(config: Config, sound, maze):
    train_conv(config, sound)


def train_conv(config: Config, sound, maze = None):
    done = False
    agent = ConvDQNAgent(config)
    save_all_information(config, agent)
    #agent.epsilon = 0.36
    #agent.load(config.neural.output_dir + config.neural.weights_path)
    mean_life_time = []
    mean_score = []
    max_score = 0
    t1 = time()
    action = Direction.WEST

    for e in tqdm.tqdm(range(config.neural.episodes)):
        game = create_game(config, sound, maze)
        state = game.get_conv_state()
        # state = game.get_conv_state()          
        for t in range(2000):
            action = agent.act(state)
            
            next_state, reward, done = game.step(action)
            reward = -1 if done else reward
            if game.is_game_won():
                reward = 100
            # visualize_array(state)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(
                    f"Episode: {e}/{config.neural.episodes}, Durée de vie moyenne: {t}, epsilon: {agent.epsilon:.2}")
                mean_life_time.append(t)
                mean_score.append(game.get_score())
                break
        if mean_life_time and mean_score:
            print(mean_life_time[-10:])
            print(
                f"Durée de vie moyenne sur les 10 derniers episodes: {sum(mean_life_time[-10:])/len(mean_life_time[-10:])}")
            print(
                f"Score moyen sur les 10 derniers episodes: {sum(mean_score[-10:])/len(mean_score[-10:])}"
            )
        print(f"Temps écoulé: {round(time() - t1, 2)}s")
        if len(agent.memory) > config.neural.batch_size:
            agent.replay()
        if e % 100 == 0:
            # Save model and training data
            save_plot_data(mean_life_time, mean_score)
            agent.save(f"{config.neural.output_dir}weights_" +
                       '{:04d}'.format(e) + ".hdf5")


def play(config: Config, sound, maze):
    agent = ConvDQNAgent(config)
    agent.load(config.neural.output_dir + config.neural.weights_path)
    game = Game(config, sound, maze)
    state = game.get_conv_state()
    # state = game.get_conv_state()
    done = False
    while not done:
        action = agent.act(state)
        next_state, reward, done = game.step(action)
        state = next_state
    print(game.get_score())
