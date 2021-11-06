---
title: 'TinyGo'
date: '2020-06-08'
author: 'Austen LeBeau'
cover: 'images/programming/tinygo-logo.png'
description: 'An introduction to TinyGo.'
type: post
tags: ['go', 'tinygo']
---

_Article is a work in progress._

If you haven't heard about TinyGo, it's a newer project that makes it easy to
write Go code for microcontrollers. Here's a little quickstart and some
examples. As of now this tutorial assumes you are working on a Linux machine,
and you can find the same instructions on the documentation
[site](https://tinygo.org/).

# Setup

Here's a quick quickstart.

1. Get the debian package.

   ```bash
   wget https://github.com/tinygo-org/tinygo/releases/download/v0.13.1/tinygo_0.13.1_amd64.deb
   sudo dpkg -i tinygo_0.13.1_amd64.deb
   ```

2. You can export the TinyGo path, but I usually put it in my VS Code settings.

   ```bash
   export PATH=$PATH:/usr/local/tinygo/bin
   ```

3. Check that it works.
   ```bash
   tinygo version
   ```

Yay! You're done!

# Examples

Here's the blink example you can find floating around the internet.

```go
package main

import (
    "machine"
    "time"
)

func main() {
    led := machine.LED
    led.Configure(machine.PinConfig{Mode: machine.PinOutput})
    for {
        led.Low()
        time.Sleep(time.Millisecond * 1000)

        led.High()
        time.Sleep(time.Millisecond * 1000)
    }
}
```

The `machine` package is an abstraction of your microcontroller board, and
defines constants for pins and things like that. Theoretically you could run the
same code and it will be the same for any other boards TinyGo supports.

# Channels
Here's the neat part. Channels actually work. Here's a convoluted example of
using channels:

```go
package main

import (
	"time"
)

type Status uint8

const (
	GOOD Status = iota
	BAD
	REALBAD
)

// The same dotstar struct from earlier. The arg is the brightness on a scale of 0-255.
var dotstar = NewDotStar(20)

func main() {

	status := make(chan Status, 1)
	status <- GOOD

	go statusIndicator(status)

	// Loop forever and keep changing the status "randomly"
	for {
		second := time.Now().Second()
		if second%5 == 0 {
			status <- GOOD
		} else if second%3 == 0 {
			status <- REALBAD
		} else {
			status <- BAD
		}
		time.Sleep(10 * time.Millisecond)
	}
}

// Goroutine that will keep the DotStar led on the Trinket running, and change the colors depending on
// the status passed in by the channel
func statusIndicator(status chan Status) {
	for {
		stat := <-status
		switch stat {
		case GOOD:
			dotstar.Green()
		case BAD:
			dotstar.WeeWoo() // kinda like a siren
		case REALBAD:
			dotstar.Red()
		}
		time.Sleep(10 * time.Millisecond)
	}
}

```
