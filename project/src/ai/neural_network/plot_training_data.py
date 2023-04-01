import matplotlib.pyplot as plt
import numpy as np

with open("mean_score_data.txt", "r") as f:
    mean_score = [float(i) for i in f.readlines()]
with open("mean_life_time_data.txt", "r") as f:
    mean_life_time = [float(i) for i in f.readlines()]
with open("mean_reward_data.txt", "r") as f:
    mean_reward = [float(i) for i in f.readlines()]

mean_mean_life_time = []
mean_mean_score = []
mean_mean_reward = []
for i in range(0, len(mean_life_time), 10):
    mean_mean_life_time.append(np.mean(mean_life_time[i:i+10]))
    mean_mean_score.append(np.mean(mean_score[i:i+10]))
    mean_mean_reward.append(np.mean(mean_reward[i:i+10]))


fig = plt.figure(figsize=(8,8))
fig.add_subplot(3, 1, 1)

plt.plot(np.arange(len(mean_mean_life_time)) * 10, mean_mean_life_time)
plt.title("Durée de vie moyenne")
fig.add_subplot(3, 1, 2)
plt.plot(np.arange(len(mean_mean_score)) * 10, mean_mean_score)
plt.plot(mean_score, alpha=0.6)
plt.title("Score moyen")
fig.add_subplot(3, 1, 3)
plt.plot(np.arange(len(mean_mean_reward)) * 10, mean_mean_reward)
plt.plot(mean_reward, alpha=0.6)
plt.title("Reward moyen")
plt.show()
