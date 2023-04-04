import matplotlib.pyplot as plt
import numpy as np

# Calculate distance between two points using gausian function
def gaussian(x, y, mu0, mu1, sigma=1):
    left = 1 / (2 * np.pi * sigma ** 2)
    right = np.exp(-((x - mu0) ** 2 + (y - mu1) ** 2) / (2 * sigma ** 2))
    return left * right

coords = np.array([0, 0])
mu = np.array([0, 0])

factor = 0.1

print(gaussian(coords[0], coords[1], mu[0], mu[1], 1) / factor)

# Create a 2D grid
x = np.linspace(-1, 2, 100)
y = np.linspace(-1, 2, 100)
X, Y = np.meshgrid(x, y)

# Calculate the distance between each point in the grid and the two points
Z = gaussian(X, Y, coords[0], coords[1], 1) / factor + gaussian(X, Y, mu[0], mu[1], 1) / factor

# Plot the distance grid
plt.imshow(Z, origin='lower', extent=[-10, 20, -10, 20])
plt.colorbar()
plt.show()