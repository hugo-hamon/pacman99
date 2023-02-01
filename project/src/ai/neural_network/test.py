from ...game.direction import Direction
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from collections import deque
from ...config import Config
import numpy as np
import random
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


class DQNAgent:

    def __init__(self, config: Config) -> None:
        self.config = config
        self.state_size = config.neural.state_size
        self.action_size = config.neural.action_size

        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0 if config.neural.train_enable else 0.0
        self.epsilon_decay = 0.998
        self.epsilon_min = 0.01

        self.learning_rate = config.neural.learning_rate

        self.model = self._build_model()

    def _build_model(self) -> Sequential:
        """Build the neural network model"""
        model = Sequential()
        model.add(Dense(30, input_dim=self.state_size, activation='relu'))
        model.add(Dense(30, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(
            learning_rate=self.learning_rate))

        return model

    def remember(self, state, action, reward, next_state, done) -> None:
        """Remember the state, action, reward, next_state and done"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state) -> Direction:
        """Act with the neural network"""
        if np.random.rand() <= self.epsilon:
            return Direction(random.randrange(self.action_size))
        act_values = self.model.predict(state, verbose="0")
        return Direction(np.argmax(act_values[0]))

    def replay(self) -> None:
        """Replay the memory"""
        minibatch = random.sample(self.memory, self.config.neural.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                    np.amax(self.model.predict(next_state, verbose="0")[0])
            target_f = self.model.predict(state, verbose="0")
            target_f[0][action.value] = target
            self.model.fit(state, target_f, epochs=1, verbose="0")
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_state_size(self) -> int:
        """Return the size of the state vector"""
        return self.state_size

    def load(self, name) -> None:
        """Load the weights of the neural network"""
        self.model.load_weights(name)

    def save(self, name) -> None:
        """Save the weights of the neural network"""
        self.model.save_weights(name)


def get_move(game, agent: DQNAgent) -> Direction:
    state = game.get_state()
    state = np.reshape(state, [1, agent.state_size])
    return agent.act(state)
