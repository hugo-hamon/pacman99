from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
from ...game.direction import Direction
from keras.models import Sequential
from keras.optimizers import Adam
import tensorflow as tf
from collections import deque
from ...config import Config
from time import time
import numpy as np
import random
import cv2
import os
import gc

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

class ConvDQNAgent:

    def __init__(self, config: Config) -> None:
        self.config = config
        self.action_size = config.neural.action_size
        if config.user.enable_random_maze:
            self.state_size = (config.maze.height, config.maze.width, 5)
        self.state_size = (15, 15, 5)
        self.memory = deque(maxlen=60000)
        self.gamma = 0.5
        self.epsilon = 1.0 if config.neural.train_enable else 0.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01

        self.learning_rate = config.neural.learning_rate

        self.model = self._build_model()

    def _build_model(self) -> Sequential:
        """Build the neural network model using convolutional layers"""
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

    def remember(self, state, action, reward, next_state, done) -> None:
        """Remember the state, action, reward, next_state and done"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state) -> Direction:
        """Act with the neural network"""
        random.seed(time())
        if np.random.rand() <= self.epsilon:
            return Direction(random.randrange(self.action_size))
        state = np.array(state).reshape(-1, *state.shape)
        act_values = self.model.predict(state, verbose="0")
        return Direction(np.argmax(act_values[0]))

    def replay(self) -> None:
        """Replay the memory"""
        minibatch = random.sample(self.memory, self.config.neural.batch_size)
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
        self.model.fit(X, np.array(y), batch_size=self.config.neural.batch_size,
                       epochs=1, verbose="0", workers=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        # Clear memory to avoid OOM
        tf.keras.backend.clear_session()
        gc.collect()

    def load(self, name) -> None:
        """Load the weights of the neural network"""
        print(f"Loading weights from {name}")
        self.model.load_weights(name)

    def save(self, name) -> None:
        """Save the weights of the neural network"""
        self.model.save_weights(name)

    def summary(self, file):
        """Return a string with the layers of the neural network"""
        return self.model.summary(print_fn=lambda x: file.write(x + '\n'))


def get_move(game, agent: ConvDQNAgent) -> Direction:
    state = game.get_conv_state()
    return agent.act(state)