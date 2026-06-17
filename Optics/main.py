# Load libraries
import numpy as np
import matplotlib.pyplot as plt

# TODO
# We will need to remove one side of the calculations since it is just a mirror image of the other
# In fact, we can remove three sectors, we only need the one top right


# Parameters of the simulations
wavelength = 0.25
distance_to_screen = 5
aperture_grid_size = 0.05
screen_grid_size = 0.03
screen_size = 5


def amplitude(distance_sqr):
    return np.cos(2 * np.pi * distance_sqr**0.5 / wavelength) / (
        4 * np.pi * distance_sqr
    )


def distance_sqr_to_screen(aperture_position, screen_position, screen_distance):
    return (
        (aperture_position[0] - screen_position[0]) ** 2
        + (aperture_position[1] - screen_position[1]) ** 2
        + screen_distance**2
    )


class Aperture:
    def __init__(self, bounds, aperture, aperture_grid_size=aperture_grid_size):
        # Bounds provided as a [ [min_x, max_x], [min_y, max_y] ]
        self.bounds = bounds
        self.aperture = aperture
        self.aperture_points_x = np.linspace(
            bounds[0][0],
            bounds[0][1],
            int((bounds[0][1] - bounds[0][0]) / aperture_grid_size),
        )
        self.aperture_points_y = np.linspace(
            bounds[1][0],
            bounds[1][1],
            int((bounds[1][1] - bounds[1][0]) / aperture_grid_size),
        )
        self.grid = []
        for x in self.aperture_points_x:
            for y in self.aperture_points_y:
                if aperture(x, y) == 1:
                    self.grid.append([x, y])


def intensity_on_screen(aperture, screen_distance, screen_position):
    # Will return a single value denoting the intensity on the screen
    amp = 0
    for point in aperture.grid:
        distance_sqr = distance_sqr_to_screen(point, screen_position, screen_distance)
        amp += amplitude(distance_sqr)
    return amp**2


# Simulate over whole screen
def simulate(aperture, screen_size, screen_distance):
    screen_grid = [
        [x, y]
        for x in np.linspace(0, screen_size / 2, int(screen_size / screen_grid_size))
        for y in np.linspace(0, screen_size / 2, int(screen_size / screen_grid_size))
    ]
    screen_display = []

    for point in screen_grid:
        screen_brightness = intensity_on_screen(aperture, screen_distance, point)
        screen_display.append(screen_brightness)

    return np.reshape(
        screen_display,
        [
            int(screen_size / screen_grid_size),
            int(screen_size / screen_grid_size),
        ],
    ).T


# WIDE DOUBLE SLIT
wide_double_bounds = [[-0.3, 0.3], [-1, 1]]


def wide_double(x, y):
    if -0.3 <= x <= -0.2 or 0.2 <= x <= 0.3:
        return 1
    return 0


wide_double_aperture = Aperture(wide_double_bounds, wide_double)


# Circular aperture
circular_bounds = [[-0.4, 0.4], [-0.4, 0.4]]


def circular(x, y):
    return 1 if x**2 + y**2 <= 0.16 else 0


circular_aperture = Aperture(circular_bounds, circular)

# Square
square_bounds = [[-0.2, 0.2], [-0.2, 0.2]]


def square(x, y):
    if -0.2 <= x <= 0.2 and -0.2 <= y <= 0.2:
        return 1
    return 0


square_aperture = Aperture(square_bounds, square)

# Simulation
result = simulate(wide_double_aperture, screen_size, distance_to_screen)
top = np.concatenate((np.fliplr(result[:, 1:]), result), axis=1)
full = np.concatenate((np.flipud(top[1:, :]), top), axis=0)
plt.imshow(full)  # , cmap="gray")
plt.show()
