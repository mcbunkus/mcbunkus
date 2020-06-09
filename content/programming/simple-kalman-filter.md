---
title: 'Simple Kalman Filters'
date: '2020-06-09'
author: 'Austen LeBeau'
cover: 'images/programming/kalman-post.jpg'
description: "A little bit about Kalman filters, how they work, what they're for, and how to use them."
type: post
math: true
---

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
