from ...utils.dqn_function import get_conv_state, step
from ...game.direction import Direction
from .dqn_agent import ConvDQNAgent
from ...game.maze.maze import Maze
import matplotlib.pyplot as plt
from ...game.game import Game
from ...config import Config
from typing import Callable
from time import time

MAZES_PATH = "assets/data/mazes/"

def create_game(config: Config, maze, control_func: Callable):
    maze.reset()
    return Game(config, maze=maze, control_func=control_func)


def save_all_information(config: Config, agent: ConvDQNAgent):
    with open("src/ai/dqn/data/network_information.txt", "w") as f:
        f.write("Parametres du reseau de neurones:\n\n")
        f.write(f"Episode max: {config.dqn.episodes}\n")
        f.write(f"Batch size: {config.dqn.batch_size}\n")
        f.write(f"Learning rate: {config.dqn.learning_rate}\n")
        f.write(f"Epsilon decay: {agent.epsilon_decay}\n")
        f.write(f"Epsilon min: {agent.epsilon_min}\n")
        agent.summary(f)

def save_plot_data(mean_life_time, mean_score, mean_reward):
    '''Save data about score and life time in text files'''
    with open("src/ai/dqn/data/mean_score_data.txt", "w") as f:
        for i in mean_score:
            f.write(f"{i}\n")

    with open("src/ai/dqn/data/mean_life_time_data.txt", "w") as f:
        for i in mean_life_time:
            f.write(f"{i}\n")

    with open("src/ai/dqn/data/mean_reward_data.txt", "w") as f:
        for i in mean_reward:
            f.write(f"{i}\n")

def save_plot(mean_life_time, mean_score):
    plt.plot(mean_life_time)
    plt.title("Durée de vie moyenne")
    plt.savefig("src/ai/dqn/data/mean_life_time.png")
    plt.clf()
    plt.plot(mean_score)
    plt.title("Score moyen")
    plt.savefig("src/ai/dqn/data/mean_score.png")
    plt.clf()


def train(config: Config, maze):
    train_conv(config, maze)


def train_conv(config: Config, maze):
    done = False
    agent = ConvDQNAgent(config)
    save_all_information(config, agent)
    #agent.epsilon = 0.01
    #agent.load(config.dqn.output_dir + config.dqn.weights_path)
    mean_life_time = []
    mean_score = []
    mean_reward = []

    t1 = time()
    action = Direction.WEST

    for e in range(config.dqn.episodes):
        # Choose a different maze every 100 episodes
        '''if e % 100 == 0:
            maze = Maze(f"{MAZES_PATH}maze{str(e // 100)}.txt")'''
        game = create_game(config, maze=maze, control_func=agent.get_move)
        state = get_conv_state(game)
        reward_sum = 0
        for t in range(2000):
            action = agent.act(state)
            next_state, reward, done = step(game, action)
            reward_sum += reward

            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(
                    f"Episode: {e}/{config.dqn.episodes}, Durée de vie moyenne: {t}, epsilon: {agent.epsilon:.2}")
                mean_life_time.append(t)
                mean_score.append(game.get_score())
                mean_reward.append(reward_sum)
                break

        if mean_life_time and mean_score:
            print(mean_life_time[-10:])
            print(
                f"Durée de vie moyenne sur les 10 derniers episodes: {sum(mean_life_time[-10:])/len(mean_life_time[-10:])}")
            print(
                f"Score moyen sur les 10 derniers episodes: {sum(mean_score[-10:])/len(mean_score[-10:])}"
            )
            print(
                f"Reward moyen sur les 10 derniers episodes: {sum(mean_reward[-10:])/len(mean_reward[-10:])}"
            )
        print(f"Temps écoulé: {round(time() - t1, 2)}s")

        if len(agent.memory) > config.dqn.batch_size:
            agent.replay()

        if e % 50 == 0:
            save_plot_data(mean_life_time, mean_score, mean_reward)
            agent.save(f"{config.dqn.output_dir}weights_" +
                       '{:04d}'.format(e) + ".hdf5")


def play(config: Config, sound, maze):
    agent = ConvDQNAgent(config)
    agent.load(config.dqn.output_dir + config.dqn.weights_path)
    game = Game(config, sound, maze)
    state = get_conv_state(game)
    done = False
    while not done:
        action = agent.act(state)
        next_state, reward, done = step(game, action)
        state = next_state
    print(game.get_score())