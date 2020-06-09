---
title: 'TinyGo'
date: '2020-06-08'
author: 'Austen LeBeau'
cover: 'images/programming/tinygo-logo.png'
description: 'An introduction to TinyGo, and sensor driver development.'
type: post
---

I've done a lot of projects with microcontrollers before, but Arduino makes it too easy. I did a lot
of "embedded systems" type of work on the rocket team at Auburn, but I didn't really get into the
nitty gritty details of writing embedded software. I've also been meaning to learn Go for a while
now, but I couldn't think of any projects that would be useful to me.

# TinyGo?

If you haven't heard about TinyGo, it's a newer project that makes it easy to write Go code for
microcontrollers. There's a good amount of support for commonly used boards too, but it could use a
few more sensor drivers. That got me thinking --- Adafruit recently started selling a breakout board
for the [BMP388](https://www.adafruit.com/product/3966), and there's no TinyGo driver for it yet.
This is the perfect opportunity for me to write some Go and do a little embedded work.
