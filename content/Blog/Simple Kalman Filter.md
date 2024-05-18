---
title: Simple Kalman Filter
draft: false
tags:
  - math
  - control-theory
---

![[kalman-feature.jpg]]

In my time as an aerospace undergrad, the most exposure I got was a 15 minute PowerPoint presentation until I took a state estimation class my senior year. Before then, I tried to write a filter for the apogee control system in Auburn's [USLI](https://www.nasa.gov/stem/studentlaunch/home/index.html) competition rocket. However, the problem I ran in to was the fact that the examples online didn't work in the context I needed it to. They set up the simplest possible problem and use the standard way of tackling that problem that every other example uses. But sometimes you have a problem that doesn't fit that mold, and unless you already know how the filter works you're stuck.

I will run you through the simplest possible example in case you've never seen the filter before. _Then I'm going to show you what to do if the example won't work for you._ There's only so much that I can cover in one blog post, but I hope it will be enough to point you in the right direction.

## Background

Let me back up a bit if you've never heard about the Kalman filter. It is an _[[optimal linear state estimator]]_. In other words, it uses measurements to estimate the state of something. This something is typically called a "system", and a system could be an airplane, a rover, a drone, a car --- pretty much anything. The state of a system would be things like its speed, its altitude, how quickly it is accelerating, etc., and even things like its mass or temperature. Most of the time it's used for kinematics (a system's position, speed, and acceleration).

You might be wondering, why not just use a sensor to measure something directly? Slap an altimeter on a plane and boom, you have its altitude. Why do you need to "estimate" the altitude?

The problem is sensors are noisy.  

![[sensor-noise.png]]

Here's an example of noisy sensor measurements (conveniently coupled with the Kalman filter's estimate). Also sometimes you can't measure a state directly. Imagine trying to measure the vertical speed of a drone. The only practical way is to measure the change in altitude vs change in time with an altimeter. Dividing the noise in the sensor measurements make the noise even worse, and makes your vertical speed "measurement" is unusable.  

_How does it work?_

The Kalman filter uses equations that describe the state together with your measurements to estimate the true state. The equations _don't_ need to be a perfect representation of your system. Often times a good approximation will work just fine. However, to make these estimates the filter needs the _covariance_ of a few different "noises". An obvious "noise" is the sensor noise itself (often denoted as $R$). This is measurement (sometimes called observation) noise. However, there is also _process_ noise ($Q$) and _estimate_ noise ($P$). They're a bit hard to explain, but for now as far as you are concerned, $Q$ is a knob that you can tweak to change the performance of the filter. $R$ is something you can get from the specs of the sensor. For $P$, you can make an initial guess as to what the values are, but as you'll see it doesn't matter too much. The filter changes the covariance of $P$ until it converges to the true value.

## Algorithm

_Measurement Update Equations_

$$
\begin{aligned}
    K             &= P_{k|k-1}H^T\left[HP_{k|k-1}H^T + R\right]^{-1} \\
    \hat{x}\_{k|k} &= \hat{x}\_{k|k-1} + K\left(y\_k - H\hat{x}\_{k|k-1}\right) \\
    P\_{k|k}       &= \left(I-KH\right)P\_{k|k-1}
\end{aligned}
$$

_Time Update Equations_

$$
\begin{aligned}
    \hat{x}\_{k+1|k} &= \Phi\hat{x}\_{k|k} \\
    P_{k+1|k}        &= \Phi P_{k|k} \Phi^T + Q \\
\end{aligned}
$$

where

$$
\begin{aligned} 
    K \quad &= \quad \text{Kalman Gain} \\
    P \quad &= \quad \text{Error Covariance} \\
    H \quad &= \quad \text{Measurement Matrix} \\
    R \quad &= \quad \text{Measurement Noise Covariance} \\
    I \quad &= \quad \text{Identity Matrix} \\
    \Phi \quad &= \quad \text{State Transition Matrix (or function)} \\
    \hat{x} \quad &= \quad \text{State Estimate} \\
\end{aligned}
$$

These equations make up the classic linear Kalman filter, and the algorithm runs through these equations in this order. Every variable in these equations is a matrix, but they don't _have_ to be. If you have just one state, then these variables are just scalars. The subscripts are important here, and sometimes they're a source of confusion. Remember that the Kalman filter is a _recursive_ algorithm. It depends on previous data to make estimates. $k|k-1$ denotes values from the previous time step, $k|k$ is the current iteration, and $k+1|k$ is the next.

_The $k+1|k$ values become $k|k-1$ values in the next iteration, not the $k|k$ values._

This is the part that confused me at first. $\hat{x}\_{k|k}$ and $P\_{k|k}$ are used for _predicting_ the state in the time update equations. They're not the actual estimate, but correct me if I'm wrong anywhere.

## Simplest Example

Here's a simple 3-state example. The measurements are for an airplane flying downrange in straight and level unaccelerated flight. It is not accelerating or changing course, so the acceleration should be zero and the velocity constant

```python
# Make sure you have python3, numpy, and matplotlib installed!

import matplotlib.pyplot as plt
from numpy import array, identity, loadtxt, vstack
from numpy.linalg import inv

plt.style.use("dark_background")

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
```

![[position-estimate.png]]  
![[velocity-estimate.png]]

![[acceleration-estimate.png]]

## More Complex Example

_I haven't gotten around to this yet, but I will soon!_
