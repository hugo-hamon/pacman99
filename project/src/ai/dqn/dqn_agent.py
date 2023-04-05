from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from ...utils.dqn_function import get_conv_state
from ...game.maze.components import Components
from ...game.direction import Direction
from keras.models import Sequential
from keras.optimizers import Adam
from ...game.game import Game
from collections import deque
from ...config import Config
import tensorflow as tf
from time import time
import numpy as np
import operator
import random
import os
import gc

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


class ConvDQNAgent:

    def __init__(self, config: Config) -> None:
        self.config = config
        self.action_size = config.dqn.action_size
        if config.user.enable_random_maze:
            self.state_size = (config.maze.height, config.maze.width, 5)
        self.state_size = (15, 15, 5)
        self.memory = deque(maxlen=480000)
        self.gamma = 0.2
        self.epsilon = 0.0 if config.user.enable_graphics else 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.0

        self.learning_rate = config.dqn.learning_rate

        self.model = self._build_model()

    def _build_model(self) -> Sequential:
        """Build the dqn network model using convolutional layers"""
        model = Sequential()
        model.add(Conv2D(64, (3, 3), activation='relu',
                  input_shape=self.state_size))
        model.add(Conv2D(128, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(256, (2, 2), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (2, 2), activation='relu'))

        model.add(Flatten())
        model.add(Dense(64))

        model.add(Dense(self.action_size, activation='softmax'))

        model.compile(loss='mse', optimizer=Adam(
            learning_rate=self.learning_rate))

        return model

    def remember(self, state, action : Direction, reward, next_state, done) -> None:
        """Remember the state, action, reward, next_state and done"""
        # On ajoute à la mémoire 4 fois la même chose mais rotationnée de 90° car le jeu est symétrique
        # On souhaite que l'agent prenne la même décision peut importe la rotation de la grille
        # On a déjà eu des problèmes de Pacman qui ne souhaitait pas aller vers le haut à cause de trop
        # d'exemples d'entrainement où les fantômes arrivait en haut de la grille
        for i in range(4):
            self.memory.append((np.rot90(state, -i), Direction((action.value + i) % 4), reward,
                                np.rot90(next_state, -i), done))

    def act(self, state) -> Direction:
        """Act with the dqn network"""
        random.seed(time())
        if np.random.rand() <= self.epsilon:
            return Direction(random.randrange(self.action_size))
        state = np.array(state).reshape(-1, *state.shape)
        act_values = self.model.predict(state, verbose="0")
        return Direction(np.argmax(act_values[0]))

    def replay(self) -> None:
        """Replay the memory"""
        minibatch = random.sample(self.memory, self.config.dqn.batch_size)
        current_state = np.array([transition[0]
                                 for transition in minibatch])
        current_predict = self.model.predict(current_state, verbose="0")
        next_state = np.array([transition[3]
                              for transition in minibatch])
        next_predict = self.model.predict(next_state, verbose="0")
        X = []
        y = []
        for index, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = (
                reward
                if done
                else reward + self.gamma * np.amax(next_predict[index])
            )
            target_f = current_predict[index]
            target_f[action.value] = target
            X.append(state)
            y.append(target_f)
        X = np.array(X)
        self.model.fit(X, np.array(y), batch_size=self.config.dqn.batch_size,
                       epochs=1, verbose="0", workers=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Clear memory to avoid OOM
        tf.keras.backend.clear_session()
        gc.collect()

    def load(self, name) -> None:
        """Load the weights of the dqn network"""
        print(f"Loading weights from {name}")
        self.model.load_weights(name)

    def save(self, name) -> None:
        """Save the weights of the dqn network"""
        self.model.save_weights(name)

    def summary(self, file):
        """Return a string with the layers of the dqn network"""
        return self.model.summary(print_fn=lambda x: file.write(x + '\n'))

    def get_move(self, game: Game) -> Direction:
        state = get_conv_state(game)
        action = self.act(state)
        is_wall_in_dir = game.pacman.is_wall(action)
        if not is_wall_in_dir:
            return action
        elif is_wall_in_dir:
            if game.pacman.is_wall(game.pacman.direction):
                return Direction.NONE
            return game.pacman.direction
