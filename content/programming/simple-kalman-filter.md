---
title: 'Simple Kalman Filters'
date: '2020-06-09'
author: 'Austen LeBeau'
cover: 'images/programming/kalman/kalman-post.jpg'
description: "A little bit about Kalman filters, how they work, what they're for, and how to use them."
type: post
math: true
---

The Kalman filter is one of the most important algorithms in engineering. That said, as an aerospace
undegrad the most exposure I got to it was a 15 minute PowerPoint presentation. It wasn't until I
took a state estimation class as an extracurricular before I really understood it. Before I took the
class, I tried to use a Kalman filter in a project for
[USLI](https://www.nasa.gov/stem/studentlaunch/home/index.html), but the resources online didn't
make much sense. A lot of the material you find online does a good job of explaining all the bits
and pieces, but they don't do a good job of using it in examples. Sometimes there are edge cases
that don't fit the standard examples. So, here's how the filter works in plain english, and a couple
of examples you can look at to give you an idea of how it works and how to use it.

_What is a Kalman filter?_

It is an _optimal linear state estimator_. In other words, it uses measurements to estimate the
state of something. This something is typically called a "system", and a system could be an
airplane, a rover, a drone, a car --- pretty much anything. The state of a system would be things
like its speed, its altitude, how quickly it is accelerating, etc., and even things like its mass or
temperature. Most of the time it's used for
kinematics (a system's position, speed, and acceleration).

You might be wondering, why not just use a sensor to measure something directly? Slap an altimeter
on a plane and boom, you have its altitude. Why do you need to "estimate" the altitude? The problem
is sensors are noisy.

{{< figure src="/images/programming/kalman/sensor-noise.png" position="center" >}}

Here's an example of noisy sensor measurements (conveniently coupled with the Kalman filter's
estimate). Also sometimes you can't measure a state directly. Imagine trying to
measure the vertical speed of a drone. The only practical way is to measure the change in altitude vs
change in time with an altimeter. Dividing the noise in the sensor measurements make the noise even
worse, and makes your vertical speed "measurement" is unusable.

_How does it work?_

The Kalman filter uses equations that describe the state together with your measurements to estimate
the true state. The equations _don't_ need to be a perfect representation of your system. Often
times a good approximation will work just fine. However, to make these estimates the filter needs
the _covariance_ of a few different "noises". An obvious "noise" is the sensor noise itself (often
denoted as $R$). This is measurement (sometimes called observation) noise. However, there is also
_process_ noise ($Q$) and _estimate_ noise ($P$). They're a bit hard to explain, but for now as far
as you are concerned, $Q$ is a knob that you can tweak to change the performance of the
filter. $R$ is something you can get from the specs of the sensor. For $P$, you can make an initial
guess as to what the values are, but as you'll see it doesn't matter too much. The filter changes
the covariance of $P$ until it converges to the true value.

# Algorithm

You've probably seen something like this before...

_Measurement Update Equations_

$$
\begin{aligned} K &= P_{k|k-1}H^T\left[HP_{k|k-1}H^T + R\right]^{-1} \\\\
   \hat{x}_{k|k} &= \hat{x}_{k|k-1} + K\left(y_k - H\hat{x}_{k|k-1}\right) \\\\
   P_{k|k} &= \left(I-KH\right)P_{k|k-1} \\\\
\end{aligned}
$$

_Time Update Equations_

$$
\begin{aligned} \hat{x}\_{k+1|k} &= \Phi\hat{x}\_{k|k} \\\\
    P_{k+1|k} &= \Phi P_{k|k} \Phi^T + Q \\\\
\end{aligned}
$$

where

$$
\begin{aligned} K \quad &= \quad \text{Kalman Gain} \\\\
    P \quad &= \quad \text{Error Covariance} \\\\
    H \quad &= \quad \text{Measurement Matrix} \\\\
    R \quad &= \quad \text{Measurement Noise Covariance} \\\\
    I \quad &= \quad \text{Identity Matrix} \\\\
    \Phi \quad &= \quad \text{State Transition Matrix (or function)} \\\\
    \hat{x} \quad &= \quad \text{State Estimate} \\\\
\end{aligned}
$$

These equations make up the classic linear Kalman filter, and the algorithm runs through these
equations in this order. Every variable in these equations is a matrix, but they don't _have_ to be.
If you have just one state, then these variables are just scalars.

# Examples

Here's a simple 3-state example.

```python
# Make sure you have python3, numpy, and matplotlib installed!

import matplotlib.pyplot as plt
from numpy import array, identity, loadtxt, vstack
from numpy.linalg import inv

data = loadtxt("data.txt", delimiter="\t")

time = data[:, 0]
measurements = data[:, 1]
dt = time[1] - time[0]

X = array([[measurements[0]], [0], [0]])            # State vector
H = array([[1, 0, 0]])                              # Measurement matrix
P = array([[1, 0, 0], [0, 10, 0], [0, 0, 100]])     # Estimate noise
Q = array([[0, 0, 0], [0, 0, 0], [0, 0, 0.001]])    # Process noise
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
    time,
    aEst,
    "Time [s]",
    r"Acceleration [$\frac{m}{s^2}$]",
    "Acceleration Estimate"
)
plt.show()
```

[Here](/files/kalman/data.txt) is the data file for the filter, and a
[copy](/files/kalman/kalman.py) of the Python file if you want to download it and try it
yourself. You should get the following:

{{< figure src="/images/programming/kalman/position-estimate.png" position="center" >}}
{{< figure src="/images/programming/kalman/velocity-estimate.png" position="center" >}}
{{< figure src="/images/programming/kalman/acceleration-estimate.png" position="center" >}}
