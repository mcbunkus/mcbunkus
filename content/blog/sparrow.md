---
title: "Introducing: Sparrow Mk. I"
date: "2023-10-30"
author: "Austen LeBeau"
cover: "images/electronics/sparrow/sparrow-model.png"
type: post
description: ""
tags: ["sparrow", "embedded", "cad", "pcb"]
---

{{<toc>}}

So, I haven't been keeping up this blog very well, but don't worry, I'm back with a 
new project. I'm calling it "Sparrow" -- it's a reintroduction to both embedded 
development and rocketry.

My goals for this project are to:

1. Design my own custom board from scratch
2. Create a framework for rocket flight code
3. Learn FreeCAD
4. Refamiliarize myself with Open Rocket and making rockets
5. ...and maybe make my own rocket fuel, we'll see

## Electronics

For my first iteration, I'm being lazy and using a development board with broken out
sensors from Adafruit. I've decided to use a BMP280 for altitude measurements and
an MPU-6050 for IMU measurements. I figure these will be easy to get a hold of both
the physical sensors and reference schematics when I finally start designing the board.

For the microcontroller I'm using an STM32F103C8T6, for the same reasons as the sensors.
Funnily enough this is my first time really using the Blue Pill, I've used Feathers, Nucleos
and normal Arduinos but I never used the Blue Pill.

{{< 
    figure src="/images/electronics/sparrow/sparrow-prototype.jpg" 
    position="center" 
    caption="Breadboard prototype from right to left: STM32F103C8T6 (Blue Pill), SD card breakout, MPU-6050, and BMP280"
>}}


It's been a very, _very_ long time since I've designed a circuit board. 
