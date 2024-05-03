<div align="center">

# WavEase - Python powered Gesture Recognition
[![Report Issue on Jira](https://img.shields.io/badge/Report%20Issues-Jira-0052CC?style=flat&logo=jira-software)](https://temple-cis-projects-in-cs.atlassian.net/jira/software/c/projects/DT/issues)
[![Deploy Docs](https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml/badge.svg)](https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml)
[![Documentation Website Link](https://img.shields.io/badge/-Documentation%20Website-brightgreen)](https://applebaumian.github.io/tu-cis-4398-docs-template/)


</div>


## Keywords

Section 004, as well as any words that quickly give your peers insights into the application like programming language, development platform, type of application, etc.

## Project Abstract

This project would create an application that allows users to use hand gestures in front of a sensor that have been mapped to enact specific commands. For example, a person could have a camera set up for gesture recognition and the network could be integrated with smart devices to turn that device on or off. Say you just sit down on the couch to watch a movie, but you can’t find the remote. With a gesture recognition system, you can simply signal a certain gesture at a camera set up with a connection to your TV and the device could turn on. This could also be the same for lighting in the house. This project would be done using Python.

## High Level Requirement

The product works by capturing and interpreting physical movements from the user’s hands or body parts. Those movements would then be translated into preset commands or actions. The high-level requirements would include sensor data acquisition, data processing, a gesture recognition algorithm, and command generation. From a user point of view, you would do a physical gesture in front of the sensor that has a command mapping. The program at a high level could be mapped to turn lights on or off. For this project we could start off by just printing text to a screen to communicate it is working.

## Conceptual Design

The conceptual design for this project would be a laptop with a built-in camera system to implement the gesture control system. The programming language would be python and the following python libraries would be used, OpenCV, TensorFlow, and NumPy. An open source data set for gesture recognition would be found and we would preprocess the images by resizing, normalizing, and converting them into a format suitable for model training. A model would be built using CNN architecture and TensorFlow. Once the model is trained, it could be deployed to use OpenCV to capture video frames from a camera, process them, and input them into our trained model. From this step, the project could go multiple different ways. For a more advanced project, we could link it to smart devices, but to start off we could print text to a screen of what the action would be performing. We will start with implementing this software to an application like Spotify and possibly consider many other applications like Youtube and Apple Music.

## Background

The idea for this product is to associate specific gestures with predefined commands. For example, a swipe gesture to the right can be associated with turning on the lights, while a swipe gesture to the left can be associated with turning them off. While there is not an existing product that is able to do this, researchers at the University of Washington are close to achieving this. Their approach is to use Wi-Fi signals to detect specific movements instead of cameras (Ma,2013). This would be different from the approach I suggested earlier because my idea is to use a laptop camera. A product that I found that is like this is the Xbox Kinect. The Kinect uses cameras to recognize gestures and allow you to interact with games on the Xbox (Palangetić, 2014). This is like my proposal because it uses a camera to capture images and allow a user to interact with the games on the device. However, it is also different because it doesn’t connect to smart devices and allows you to control certain features.
## Installation

To get started with WavEase, follow these steps:

1. **Install Python 3.8**: If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/) or using a package manager like [Homebrew](https://brew.sh/) (for macOS and Linux) or [Chocolatey](https://chocolatey.org/) (for Windows).

2. **Create a Python 3.8 Virtual Environment (optional but recommended)**: It's good practice to isolate your project dependencies in a virtual environment. To create a virtual environment, open a terminal or command prompt, navigate to your project directory, and run the following command:
   
   ```
   python3.8 -m venv venv
   ```
3. **Activate the Virtual Environment (optional but recommended)**: Before installing the project dependencies, activate the virtual environment. Run the appropriate command based on your operating system:

- **On macOS and Linux**:
  ```
  source venv/bin/activate
  ```

- **On Windows**:
  ```
  venv\Scripts\activate
  ```

4. **Install Required Packages**: Once the virtual environment is activated, install the required Python packages listed in `requirements.txt` by running the following command:
   ```
   pip install -r requirements.txt
   ```
5. **Start the Application**: After installing the dependencies, you can start the application. Run the following command:
   ```
   python app.py
   ```
## Required Resources

The required hardware for this project would be a laptop with a working camera. Specific python libraries like TensorFlow, NumPy, and OpenCV would be needed to train the model and capture images to input into the model once it is trained. It would be beneficial if the people working on this project had experience or knowledge with computer vision, convolutional neural network architecture, and API calls to connect to the smart devices. While wireless networks would most likely be the preferred way, if anyone has experience with IoT devices and connections that could be a route to go for integrating smart devices as well.

## Collaborators

[//]: # ( readme: collaborators -start )
<table>
<tr>
    <td align="center">
        <a href="https://github.com/kbarbarisi">
            <img src="https://avatars.githubusercontent.com/u/73039627?v=4" width="100;" alt="Kianna"/>
            <br />
            <sub><b>Kianna Barbarisi</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/tul53850">
            <img src="https://avatars.githubusercontent.com/u/111989518?v=4" width="100;" alt="Jason"/>
            <br />
            <sub><b>Jason Hankins</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/SarinaCurtis">
            <img src="https://avatars.githubusercontent.com/u/81874704?v=4" width="100;" alt="Sarina"/>
            <br />
            <sub><b>Sarina Curtis</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/tun71427">
            <img src="https://avatars.githubusercontent.com/u/123014326?v=4" width="100;" alt="Yuxuan"/>
            <br />
            <sub><b>Yuxuan Zhu</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/LeeMamori">
            <img src="https://avatars.githubusercontent.com/u/123014841?v=4" width="100;" alt="Yang"/>
            <br />
            <sub><b>Yang Li</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/tuk85473">
            <img src="https://avatars.githubusercontent.com/u/97626755?v=4" width="100;" alt="Ashley"/>
            <br />
            <sub><b>Ashley Jones</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="">
            <img src="https://avatars.githubusercontent.com/u/97626755?v=4" width="100;" alt="Ashley"/>
            <br />
            <sub><b>Ashley Jones</b></sub>
        </a>
    </td>
   </tr>
</table>

[//]: # ( readme: collaborators -end )
