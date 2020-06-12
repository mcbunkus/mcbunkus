# Make sure you have python3, numpy, and matplotlib installed!

import matplotlib.pyplot as plt
from numpy import array, identity, loadtxt, vstack
from numpy.linalg import inv

data = loadtxt("data.txt", delimiter="\t")

time = data[:, 0]
measurements = data[:, 1]
dt = time[1] - time[0]

X = array([[measurements[0]], [0], [0]])  # State vector
H = array([[1, 0, 0]])  # Measurement matrix
P = array([[1, 0, 0], [0, 10, 0], [0, 0, 100]])  # Estimate noise
Q = array([[0, 0, 0], [0, 0, 0], [0, 0, 0.001]])  # Process noise
R = 0.05 ** 2

# State transition matrix
F = array([[1, dt, 0.5 * dt ** 2], [0, 1, dt], [0, 0, 1]])

# For saving kalman filter estimates for plotting
kalmanEstimates = array([0, 0, 0])

# Numpy matrix multiplication uses @ for multiplication instead of *
for meas in measurements:

    # This is the Kalman filter, in all its glory
    K = P @ H.T @ inv(H @ P @ H.T + R)
    xHat = X + K @ (meas - H @ X)
    p = (identity(3) - K @ H) @ P
    X = F @ xHat
    P = F @ p @ F.T + Q

    # Saving data for plots
    kalmanEstimates = vstack([kalmanEstimates, X.T])

# Get rid of the useless row at beginning of array
kalmanEstimates = kalmanEstimates[1:, :]
xEst = kalmanEstimates[:, 0]
vEst = kalmanEstimates[:, 1]
aEst = kalmanEstimates[:, 2]


# Just a helper function for plots
def new_plot(x, y, xAx, yAx, title: str):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(xAx)
    plt.ylabel(yAx)
    plt.title(title)


new_plot(time, xEst, "Time [s]", "Position [m]", "Position Estimate")
new_plot(time, vEst, "Time [s]", r"Velocity [$\frac{m}{s}$]", "Velocity Estimate")
new_plot(
    time, aEst, "Time [s]", r"Acceleration [$\frac{m}{s^2}$]", "Acceleration Estimate"
)
plt.show()
