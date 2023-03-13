from keras import Model, layers


class PolicyGradientNetwork(Model):

    def __init__(self, n_actions, layers_dims=(256, 256)):
        super(PolicyGradientNetwork, self).__init__()
        self.n_actions = n_actions
        self.layers_dims = layers_dims
        self.neural_layers = []
        self.neural_layers.extend(
            layers.Dense(self.layers_dims[i], activation="relu")
            for i in range(len(self.layers_dims))
        )
        self.pi = layers.Dense(n_actions, activation="softmax")

    def call(self, state):
        value = state
        for layer in self.neural_layers:
            value = layer(value)
        return self.pi(value)
