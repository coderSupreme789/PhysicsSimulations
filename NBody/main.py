import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

G = 6.67e-11
G = 1

# Sun, Earth and Moon
N = 3
masses = np.array([10000, 100, 0.001])
positions = np.array([[0, 0, 0], [0, 0, 1], [0, 0, 1.05]]) * 10
earth_vel = (G * masses[0] / positions[1][2]) ** 0.5
moon_vel = (G * masses[1] / (positions[2][2] - positions[1][2])) ** 0.5
velocities = np.array(
    [
        [0, -earth_vel * masses[1] / masses[0], 0],
        [0, earth_vel, 0],
        [0, moon_vel * 1.5, 0],
    ]
)

labels = ["Sun", "Earth", "Moon"]

# 50 random masses.
N = 50
masses = np.random.rand(N) * 1000
positions = np.array([np.random.rand(3) for _ in range(N)]) * 10
velocities = np.array([np.random.rand(3) for _ in range(N)]) * 5
labels = [f"Object {i+1}" for i in range(N)]
# State will contain positions, then velocities
initial_state = np.append(positions, velocities)


def compute_grav_force(m1, m2, position_1, position_2):
    # Returns the force on mass 1
    return (
        (position_2 - position_1)
        * G
        * m1
        * m2
        / (np.linalg.norm(position_2 - position_1) ** 3)
    )


def ds_dt(t, s):
    # TODO: Differentiate the state
    positions = s.reshape([-1, 3])[:N]
    velocities = s.reshape([-1, 3])[N:]
    accelerations = np.zeros((N, 3))

    # We need to just take the force once. We can add the accelerations to the array
    # There are two ways to do this
    # The slow way is setting the accleration for every value of i != j
    # Then adding the forces
    # We can half the computation time by computing the forces once
    for i in range(N):
        for j in range(N):
            if i < j:
                force_ij = compute_grav_force(
                    masses[i], masses[j], positions[i], positions[j]
                )

                accelerations[i] += force_ij / masses[i]
                accelerations[j] += -force_ij / masses[j]
    return np.append(velocities, accelerations)


class Node:
    def __init__(self, position, mass):
        # nw, ne, sw, se
        self.children = [None, None, None, None]
        self.parent = None
        self.position = position
        self.mass = mass


class Tree:
    def __init__(self):
        self.children = [None, None, None, None]


def direction(origin, position):
    displacement = [position[0] - origin[0], position[1] - origin[1]]
    if displacment[0] >= 0 and displacement[1] >= 0:
        return 0
    if displacement[0] >= 0 and displacement[1] < 0:
        return 2
    if displacement[0] < 0 and displacement[1] >= 0:
        return 1
    if displacement[0] < 0 and displacement[1] < 0:
        return 3


def construct_barnes_hut_tree(positions, masses):
    tree = Tree()
    rootNode = Node(positions[0], masses[0])
    add_node(positions[1:], masses[1:], rootNode)


def add_node(positions, masses, parentNode):
    if positions.len() == 0:
        return None
    currentNode = Node(positions[0], masses[0])
    currentNode.parent = parentNode


solution = solve_ivp(
    ds_dt, [0, 10], initial_state, max_step=0.005
)  # events = centre_pass
t_values = solution.t


def period_estimation(solution):

    def centre_pass(t, s):
        x = s[6]
        return x

    centre_pass.direction = 1

    periods = []
    for i in range(len(solution.t_events[0]) - 1):
        periods.append(solution.t_events[0][i + 1] - solution.t_events[0][i])

    print(np.average(periods))
    print(np.std(periods))


def plot_trajectories(solution):
    ax = plt.figure().add_subplot(projection="3d")
    ax.set_aspect("equal")
    positions = []
    for i in range(N):
        positions.append(solution.y[i * 3 : i * 3 + 3])

    positions = np.array(positions)

    ax.set_xlim(np.min(positions), np.max(positions))
    ax.set_ylim(np.min(positions), np.max(positions))
    ax.set_zlim(np.min(positions), np.max(positions))

    for i in range(N):
        plt.plot(positions[i][0], positions[i][1], positions[i][2], label=labels[i])
    plt.legend()
    plt.show()


plot_trajectories(solution)
