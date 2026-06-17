import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

step_size = 10
length = 10000
iterations = 1000


def randomWalkGenerator(length):
    path = np.array([[0, 0]])
    for _ in range(length):
        next_step_raw = np.random.random(2) * 2 - 1
        next_step = step_size * next_step_raw / np.linalg.norm(next_step_raw)
        path = np.append(path, [path[-1] + next_step], axis=0)
    return path


def lineGenerator(path, length):
    colors = np.array([])
    lines = np.array([[path[0], path[1]]])
    for i in range(1, length):
        lines = np.append(lines, [[path[i], path[i + 1]]], axis=0)
        colors = np.append(colors, "black")
    return lines, colors


def plot_path(path, lines, colors):
    max_points = path.max(axis=0)
    min_points = path.min(axis=0)

    lc = LineCollection(lines, colors=colors, linewidths=1)
    fig, ax = plt.subplots()
    ax.set_xlim(min_points[0] - 5, max_points[0] + 5)
    ax.set_ylim(min_points[1] - 5, max_points[1] + 5)
    ax.set_aspect("equal")
    ax.add_collection(lc)
    ax.plot(path[-1][0], path[-1][1], "ro")
    ax.plot(0, 0, "bo")
    plt.show()


# So we need to run this a lot of times and get the delta r vector average, the magnitude average and the magnitude squared average
# Avg_vec_r, avg_r, avg_r_sqr


def generateDisplacements(iterations, length):
    vector_displacements = np.array([])
    for i in range(iterations):
        path = randomWalkGenerator(length)
        vector_disp = path[-1] - path[0]
        vector_displacements = np.append(vector_displacements, [vector_disp])
    return vector_displacements.reshape([iterations, 2])


def avg_vec_r(iterations, length):
    return np.average(generateDisplacements(iterations, length))


def avg_r(iterations, length):
    distances = np.linalg.norm(generateDisplacements(iterations, length), axis=1)
    return np.average(distances)


def avg_r_sqr(iterations, length):
    distance_sqr = (
        np.linalg.norm(generateDisplacements(iterations, length), axis=1) ** 2
    )
    return np.average(distance_sqr)


# We can plot avg_r_sqr and n


def plot_r_sqr_against_n(start, end, n_step_size, iterations):
    r_sqr_values = np.array([])
    n_values = np.array([])
    for length in range(start, end, n_step_size):
        r_sqr_values = np.append(r_sqr_values, avg_r_sqr(iterations, length))
        n_values = np.append(n_values, length)

    b, a = np.polyfit(n_values, r_sqr_values, deg=1)
    r = np.corrcoef(n_values, r_sqr_values)
    print("PMCC:", r[0][1])
    plt.plot(n_values, r_sqr_values)
    plt.plot(n_values, a + b * n_values)
    print("Y-intercept:", a)
    print("Gradient:", b)
    print("Gradient / Step Size Squared:", b / step_size**2)
    plt.show()


# plot_r_sqr_against_n(5, 505, 50, iterations)

path = randomWalkGenerator(length)
lines, colors = lineGenerator(path, length)
plot_path(path, lines, colors)
