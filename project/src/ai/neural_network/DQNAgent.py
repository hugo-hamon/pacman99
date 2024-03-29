import numpy as np

from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout, Input
from ...game.direction import Direction
from keras.models import Sequential
from keras.optimizers import Adam
from collections import deque
from ...config import Config
from time import time
import numpy as np
import random
from time import time
import cv2
import tensorflow as tf


MAX_COLOR_VALUE = 1
STATE_SHAPE = 21

#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def visualize_array(array):
    array = np.repeat(array, 20, axis=0)
    array = np.repeat(array, 20, axis=1)
    while True:
        cv2.imshow('image', array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


class DQNAgent:

    def __init__(self, config: Config) -> None:
        self.config = config
        self.action_size = config.neural.action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0 if config.neural.train_enable else 0.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        self.learning_rate = config.neural.learning_rate

        self.model = self._build_model()


    def _build_model(self) -> Sequential:
        """Build the neural network model using convolutional layers"""
        model = Sequential()
        model.add(Input(shape=(STATE_SHAPE,)))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(self.action_size, activation='softmax'))

        model.compile(loss='mse', optimizer=Adam(
            learning_rate=self.learning_rate), metrics=['accuracy'])

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
        act_values = self.model.predict(state, verbose=0)

        return Direction(np.argmax(act_values[0]))

    def replay(self) -> None:
        """Replay the memory"""
        minibatch = random.sample(self.memory, self.config.neural.batch_size)
        current_state = np.array([transition[0]
                                 for transition in minibatch])
        current_predict = self.model.predict(current_state, verbose=0)
        next_state = np.array([transition[3]
                              for transition in minibatch])
        next_predict = self.model.predict(next_state, verbose=0)
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
                       epochs=1, verbose="0")
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

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


def get_move(game, agent: DQNAgent) -> Direction:
    state = game.get_state()
    return agent.act(state)
