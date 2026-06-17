# Load libraries
import numpy as np
import matplotlib.pyplot as plt

# Parameters
screen_distance = 100
wavelength = 0.1
slit_separation = 0.1
slit_intensity = 100


# Intensity of a particle at some distance r
def intensity_profile(distance, kind="spherical"):
    if kind == "spherical":
        return 1 / (4 * np.pi * distance**2)
    if kind == "cylindrical":
        return 1 / (2 * np.pi * distance)
    if kind == "flat":
        return 1


# Calculate intensity at given displacement on the screen
def intensity(deviation, kind="spherical"):
    left_distance = np.sqrt(
        (screen_distance) ** 2 + (slit_separation / 2 - deviation) ** 2
    )
    right_distance = np.sqrt(
        (screen_distance) ** 2 + (slit_separation / 2 + deviation) ** 2
    )

    left_amplitude = intensity_profile(left_distance, kind) * np.cos(
        left_distance * 2 * np.pi / wavelength
    )
    right_amplitude = (
        * intensity_profile(right_distance, kind)
        * np.cos(right_distance * 2 * np.pi / wavelength)
    )

    return (left_amplitude + right_amplitude) ** 2


# Plotting
deviations = np.linspace(-10, 10, 10000)
plt.plot(deviations, intensity(deviations, "flat"))
plt.show()
