# NumPy
import numpy as np

# Scipy Integration
from scipy.integrate import solve_ivp

# Plotting
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation settings
L = 20
T = 0.2

# Discretisation
N_x = 2500
N_t = 1000
del_x = L / N_x
del_t = T / N_t


def soliton(i, c, a):
    h = 0.5 * c / np.cosh(0.5 * np.sqrt(c) * (i * del_x - a)) ** 2
    return h


# Initialise as array of length L // del_x
c = 6
a = L / 2
phi = np.array([soliton(i, c, a) for i in range(int(L / del_x))])


# Find the total volume of water to normalise the solution
def simpson_integrate(phi):

    val = phi[0] + phi[-1]
    val += 2 * sum(phi[1:-1])

    val *= val * del_x / 2

    return val


print(simpson_integrate(phi))


# Boundary Conditions
def zero_bounds(state, i):
    state_len = len(state)
    if i >= state_len or i < 0:
        return 0
    return state[i]


def periodic_bounds(state, i):
    state_len = len(state)
    return state[i % state_len]


# Derivatives
def deriv(state, bounds):
    ds = (
        np.array([bounds(state, i + 1) - bounds(state, i) for i in range(len(state))])
        / del_x
    )
    return ds


def deriv3(state, bounds):
    ds3 = (
        np.array(
            [
                bounds(state, i + 2)
                - 2 * bounds(state, i + 1)
                + 2 * bounds(state, i - 1)
                - bounds(state, i - 2)
                for i in range(len(state))
            ]
        )
        / del_x
    )
    return ds3


# Euler Forward
def step_eul_for(t, phi, bounds):

    dphi_dt = -deriv3(phi, bounds) + 6 * phi * deriv(phi, bounds)
    dphi = dphi_dt * del_t

    phi_new = phi + dphi
    phi_new = phi_new / simpson_integrate(phi_new)

    return phi + dphi


# Complete iteration
def solve(phi, bounds):
    trajectory = [
        phi,
    ]

    for i in range(N_t):
        phi = step_eul_for(i * del_t, phi, bounds)
        trajectory.append(phi)

    return trajectory


# def animate_trajectory(trajectory, frame_rate=60, save_name=None):
trajectory = solve(phi, periodic_bounds)
fig, ax = plt.subplots()
x = np.linspace(0, L, N_x)

(surface,) = ax.plot(x, trajectory[0])
ax.set(xlim=[0, L], ylim=[-10, 10], ylabel="Height")


def update(frame):
    i = frame
    surface.set_xdata(x)
    surface.set_ydata(trajectory[i])
    return [
        surface,
    ]


frame_rate = 60
anim = animation.FuncAnimation(
    fig=fig, func=update, frames=N_t, interval=1000 / frame_rate, blit=True
)
save_name = "realistic_wave"
if save_name:
    anim.save(f"{save_name}.mp4", dpi=200)
plt.show()


# animate_trajectory(solve(phi, periodic_bounds))
