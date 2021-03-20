# Gravity Simulator by Tawfeeq
This is my gravity/momentum simulator, originally created as part of my IB Extended Essay in physics, but then expanded and improved to be a more general n-body gravitational dynamics and collision simulator.


## Table of Contents
* [General info](#general-info)
* [Features](#features)
* [Technologies](#technologies)
* [Setup and Launch](#setup-and-launch)


## General info
This is a physics simulator capable of modelling n-body gravitational dynamics between multiple bodies, as well as conservation of momentum in collisions between bodies. It allows the user to choose between several demo simulations or create one of their own, and then to control the simulation by playing, pausing, and reversing the simulation, among other controls.
![image](https://user-images.githubusercontent.com/62124462/111857307-2e985680-88f6-11eb-9a54-3207548eb58b.png)


It was originally created to simulate the restricted 3-body problem between the Earth, the Moon, and a satellite, but has since been expanded for general application. The code was written in Python 3 and the simulation's algorithms were based on the real physics equations around gravitational field and momentum.


## Features
* Run any of the 6 demo simulations available
* Create your own system, specifying the mass, radius, position, and speed of each body
* Play and pause the simulation
* Fast-forward the simulation
* Run the simulation in reverse time
* Toggle gravity on and off

### To Do:
* Simulate elastic collisions without significant error
* Toggle between elastic and inelastic collisions
* Make each body's colour immutable and inherent to the body instead of potentially changing when other bodies collide
* Create and insert custom bodies into the system by clicking and dragging on the GUI canvas
* Phase out the need for a CLI by choosing demo simulations directly in the GUI


## Technologies
This project is created with:
* Python 3.9.0
* Pygame 2.0.1
* Matplotlib 3.3.4 (not used in current release)
* PyInstaller 4.2 (used for compilation)


## Setup and Launch
To run this project on Windows, download the compiled .exe file from the [latest release](https://github.com/roljy/gravity-simulator/releases/latest) and run it on your computer.
![image](https://user-images.githubusercontent.com/62124462/111855827-6c907d00-88ec-11eb-803c-2fd555eedfed.png)


If you wish to run a release that was never compiled, are not using Windows, or want to run the code directly, you can download the source code from the release you wish to run, extract the files to a folder of your choice, and run *main.py* from that folder. This will require you to have either matplotlib or pygame installed, depending on the release.
![image](https://user-images.githubusercontent.com/62124462/111855832-74502180-88ec-11eb-9ddc-80422972f876.png)
