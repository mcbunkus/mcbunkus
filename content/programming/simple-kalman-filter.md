---
title: 'Simple Kalman Filters'
date: '2020-06-09'
author: 'Austen LeBeau'
cover: 'images/programming/kalman/kalman-post.jpg'
description: "A little bit about Kalman filters, how they work, what they're for, and how to use them."
type: post
math: true
---


The Kalman filter is one of the most important algorithms in engineering, but
even as an aerospace undergrad It wasn't until I took
a state estimation class as an extracurricular before I really understood it.
Before I took the class, I tried to use it in a project for USLI, but the
resources online didn't make much sense. A lot of material does a good job of
explaining all the bits and pieces, but they don't do a good job of using it in
examples. So, here's how the filter works in plain english, and a couple of
examples you can look at to give you an idea of how it works and how to use it.

_What is a Kalman filter?_

It is an _optimal linear state estimator_. In plain english, it uses
measurements to estimate the state of something. This something is typically
called a "system", and a system could be an airplane, a rover, a drone, a car
--- pretty much anything. The state of a system would be things like its speed,
its altitude, how quickly it is accelerating, etc., and even things like its
mass or temperature. You could apply the filter to all of these examples, but
most of the time it's used for kinematics (a system's position, speed, and
acceleration).

You might be wondering, why not just use a sensor to measure something directly?
Slap an altimeter on a plane and boom, you have its altitude. Why do you need
to "estimate" the altitude? The problem is sensors are noisy. 

{{< figure src="/images/programming/kalman/sensor-noise.png" position="center" >}}

Here's an example of noisy sensor measurements (conveniently coupled with the
Kalman filter's estimate). To make matters worse, sometimes you can't measure a
state directly. Imagine trying to measure the vertical speed of a drone. The
only feasible way is to measure the change in altitude vs change in time with an
altimeter. Dividing the noise in the sensor measurements make the noise even
worse, and your vertical speed "measurement" is unusable.

_How does it work?_

The Kalman filter uses equations that describe the state together with your
measurements to estimate the true state. The equations _don't_ need to be a
perfect representation of your system. Often times a good approximation will
work just fine. However, to make these estimates, the filter needs the
_covariance_ of a few different "noises". The obvious "noise" is the sensor
noise itself (often denoted as $R$). This is measurement (sometimes called
observation) noise. However, there is also _process_ noise ($Q$) and _estimate_
noise ($P$). They're a bit hard to explain, but for now as far as you are
concerned, $Q$ and $R$ are knobs that you can tweak to change the performance of
the filter. 

 

# Algorithm

You've probably seen something like this before...

_Measurement Update Equations_

$$
\begin{aligned}
   K &= P_{k|k-1}H^T\left[HP_{k|k-1}H^T + R\right]^{-1} \\\\
   \hat{x}_{k|k} &= \hat{x}_{k|k-1} + K\left(y_k - H\hat{x}_{k|k-1}\right) \\\\
   P_{k|k} &= \left(I-KH\right)P_{k|k-1} \\\\
\end{aligned}
$$

_Time Update Equations_

$$
\begin{aligned}
    \hat{x}\_{k+1|k} &= \Phi\hat{x}\_{k|k} \\\\
    P_{k+1|k} &= \Phi P_{k|k} \Phi^T + Q \\\\
\end{aligned}
$$

where
$$
\begin{aligned}
    K \quad &= \quad \text{Kalman Gain} \\\\
    P \quad &= \quad \text{Error Covariance} \\\\
    H \quad &= \quad \text{Measurement Matrix} \\\\
    R \quad &= \quad \text{Measurement Noise Covariance} \\\\
    I \quad &= \quad \text{Identity Matrix} \\\\
    \Phi \quad &= \quad \text{State Transition Matrix (or function)} \\\\
    \hat{x} \quad &= \quad \text{State Estimate} \\\\
\end{aligned}
$$
These equations make up the classic linear Kalman filter, and the algorithm runs
through these equations in this order. Every variable in these equations is a
matrix, but they don't _have_ to be. If you have just one state, then these
variables are just scalars.

# Examples
``` python
from numpy import array

dt = 0.1 # time step

X = array([[0], [0], [0]])
H = array([1, 0, 0])
P = array([[1, 0, 0], [0, 10, 0], [0, 0, 100]])
Q = array([[0,0,0], [0,0,0], [0,0,0.005]])
R = 0.5**2
F = array([[1, dt, 0.5 * dt**2], [0, 1, dt], [0, 0, 1]])

```