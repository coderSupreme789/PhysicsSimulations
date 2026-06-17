import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from math import sin, cos
import matplotlib.animation as animation

# Lyapunov exponent estimation using a parameter sweep

# CONSTANTS
alpha = 2
beta = 3
l_1 = 1  # metre
l_2 = beta * l_1  # metre
m_1 = 1
m_2 = alpha * m_1
g = 9.81  # metre per second squared
OMEGA_1_SQR = g / l_1
OMEGA_2_SQR = g / l_2


# INITIAL CONDITIONS
theta_1_0 = 3
theta_2_0 = 1
omega_1_0 = 6.0
omega_2_0 = -4

# SOLVER SETTINGS
t_end = 20000
dt = 0.01
frames = int(t_end / dt)


# ACCELERATIONS


def d2q_dt2(t, s):

    theta_1, theta_2, omega_1, omega_2 = s
    denom = 1 + alpha * (sin(theta_1 - theta_2)) ** 2
    alpha_1 = (
        -alpha * beta * omega_2**2 * sin(theta_1 - theta_2)
        - (1 + alpha) * OMEGA_1_SQR * sin(theta_1)
        - alpha * omega_1**2 * sin(theta_1 - theta_2) * cos(theta_1 - theta_2)
        + alpha * OMEGA_1_SQR * cos(theta_1 - theta_2) * sin(theta_2)
    ) / denom

    alpha_2 = (
        alpha * omega_2**2 * sin(theta_1 - theta_2) * cos(theta_1 - theta_2)
        + (1 + alpha) * OMEGA_2_SQR * cos(theta_1 - theta_2) * sin(theta_1)
        + (1 + alpha) * omega_1**2 * sin(theta_1 - theta_2) / beta
        - (1 + alpha) * OMEGA_2_SQR * sin(theta_2)
    ) / denom

    return [omega_1, omega_2, alpha_1, alpha_2]


# SOLUTION

t_span = np.linspace(0, t_end, 2 * frames)

sol = solve_ivp(
    d2q_dt2,
    [0, t_end],
    y0=[theta_1_0, theta_2_0, omega_1_0, omega_2_0],
    t_eval=t_span,
    max_step=dt / 2,
)

# DATA PROCESSING

t_values = sol.t
theta_1_t = sol.y[0]
theta_2_t = sol.y[1]
omega_1_t = sol.y[2]
omega_2_t = sol.y[3]

x1 = l_1 * np.sin(theta_1_t)
y1 = -l_1 * np.cos(theta_1_t)

x2 = l_1 * np.sin(theta_1_t) + beta * l_1 * np.sin(theta_2_t)
y2 = -l_1 * np.cos(theta_1_t) - beta * l_1 * np.cos(theta_2_t)


def angles_t(t_span, theta_1_t, theta_2_t):
    plt.plot(t_span, theta_1_t)
    plt.plot(t_span, theta_2_t)
    plt.show()


def x_y_plot(x2, y2):
    fig, ax = plt.subplots()
    ax.set_xlim(-l_1 * (1 + alpha), l_1 * (1 + alpha))
    ax.set_ylim(-l_1 * (1 + alpha), l_1 * (1 + alpha))

    ax.set_aspect("equal")
    ax.plot(x2, y2)
    plt.show()


# SETUP ANIMATION
def animation_single(x1, x2, y1, y2, save=None):
    fig, axis = plt.subplots()
    axis.set_xlim(-l_1 * (1 + beta), l_1 * (1 + beta))
    axis.set_ylim(-l_1 * (1 + beta), l_1 * (1 + beta))
    axis.set_aspect("equal")
    (endpointline,) = axis.plot(x2[0], y2[0])
    # (midpointline,) = axis.plot(x1[0], y1[0])

    (rods,) = axis.plot([0, x1[0], x2[0]], [0, y1[0], y2[0]])

    def update(frame):
        i = frame
        endpointline.set_xdata(x2[:i])
        endpointline.set_ydata(y2[:i])
        # midpointline.set_xdata(x1[:i])
        # midpointline.set_ydata(y1[:i])
        rods.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
        return endpointline, rods

    anim = animation.FuncAnimation(
        fig=fig, func=update, frames=frames, interval=dt * 1000, blit=True
    )

    if save:
        anim.save(f"{save}.mp4", dpi=200)
    plt.show()


# animation_single(x1, x2, y1, y2)


# ENERGY DRIFT
def plot_energy_drift(omega_1_t, omega_2_t, t_span):
    specific_energy = (
        0.5 * np.multiply(omega_1_t, omega_1_t) * l_1**2
        + 0.5 * alpha * np.multiply(omega_1_t, omega_1_t) * l_1**2
        + 0.5 * alpha * beta**2 * l_1**2 * np.multiply(omega_2_t, omega_2_t)
        + alpha
        * beta
        * l_1**2
        * np.multiply(np.multiply(omega_1_t, omega_2_t), np.cos(theta_1_t - theta_2_t))
        - g * l_1 * np.cos(theta_1_t)
        - alpha * g * l_1 * np.cos(theta_1_t)
        - alpha * beta * l_1 * g * np.cos(theta_2_t)
    )

    relative_difference = 1 - specific_energy / specific_energy[0]
    plt.plot(t_span, relative_difference)
    plt.show()


# plot_energy_drift(omega_1_t, omega_2_t, t_span)


def animation_multiple(x1, x2, y1, y2, save=None):

    # Solve close problems

    sol2 = solve_ivp(
        d2q_dt2,
        [0, t_end],
        y0=[theta_1_0, theta_2_0, omega_1_0 + 10 ** (-3), omega_2_0 + 10 ** (-3)],
        t_eval=t_span,
        max_step=dt / 2,
    )
    theta_1_t_2 = sol2.y[0]
    theta_2_t_2 = sol2.y[1]

    x1_2 = l_1 * np.sin(theta_1_t_2)
    y1_2 = -l_1 * np.cos(theta_1_t_2)

    x2_2 = l_1 * np.sin(theta_1_t_2) + beta * l_1 * np.sin(theta_2_t_2)
    y2_2 = -l_1 * np.cos(theta_1_t_2) - beta * l_1 * np.cos(theta_2_t_2)

    fig, axis = plt.subplots()
    axis.set_xlim(-l_1 * (1 + beta), l_1 * (1 + beta))
    axis.set_ylim(-l_1 * (1 + beta), l_1 * (1 + beta))
    axis.set_aspect("equal")
    (endpointline,) = axis.plot(x2[0], y2[0])
    (endpointline2,) = axis.plot(x2_2[0], y2_2[0])
    (rods,) = axis.plot([0, x1[0], x2[0]], [0, y1[0], y2[0]])
    (rods2,) = axis.plot([0, x1_2[0], x2_2[0]], [0, y1_2[0], y2_2[0]])

    def update(frame):
        i = frame
        endpointline.set_xdata(x2[:i])
        endpointline.set_ydata(y2[:i])
        endpointline2.set_xdata(x2_2[:i])
        endpointline2.set_ydata(y2_2[:i])
        rods.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
        rods2.set_data([0, x1_2[i], x2_2[i]], [0, y1_2[i], y2_2[i]])

        return endpointline, rods, rods2

    anim = animation.FuncAnimation(
        fig=fig, func=update, frames=frames, interval=dt * 1000, blit=True
    )

    if save:
        anim.save(f"{save}.mp4", dpi=200)
    plt.show()


# animation_multiple(x1, x2, y1, y2, "fast_separation_v2")


def lyapunov_estimation(theta_1_t, theta_2_t, omega_1_t, omega_2_t, t_span):
    sol2 = solve_ivp(
        d2q_dt2,
        [0, t_end],
        y0=[
            theta_1_0 + 10 ** (-4),
            theta_2_0 + 0 * 10 ** (-4),
            omega_1_0,
            omega_2_0,
        ],
        t_eval=t_span,
        max_step=dt / 2,
    )
    theta_1_t_2 = sol2.y[0]
    theta_2_t_2 = sol2.y[1]
    omega_1_t_2 = sol2.y[2]
    omega_2_t_2 = sol2.y[3]

    ln_difference_omega_1 = np.log(omega_1_t_2 - omega_1_t)
    plt.plot(t_span, ln_difference_omega_1)
    plt.show()


# lyapunov_estimation(theta_1_t, theta_2_t, omega_1_t, omega_2_t, t_span)

plt.scatter((theta_1_t + np.pi) % (2 * np.pi), omega_1_t, alpha=0.02)
plt.hexbin(
    (theta_1_t + np.pi) % (2 * np.pi),
    omega_1_t,
    gridsize=200,
    cmap="viridis",
    bins="log",
)
plt.colorbar()
plt.show()
