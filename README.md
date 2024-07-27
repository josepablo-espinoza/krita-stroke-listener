# Stroke Listener for Krita

<p align="center">
  <img src="/readme-assets/stroke-listener-logo.png" />
</p>

## Overview

The Stroke Listener is a Krita plugin designed to simulate a keypress each time a left-click is detected on the drawing canvas. The keypress can be customized via the plugin's docker.

## Features

- **Preset Shortcuts**: Choose from a list of predefined keyboard shortcuts.
- **Custom Shortcuts**: Create your own shortcuts using Ctrl, Shift, Alt, and a single key.
- **Toggle Listening**: Enable or disable the keypress simulation with a checkbox.
- **Canvas Detection**: Only triggers the keypress simulation when clicking on the drawing canvas

### Demo

Demo triggering a script and inverting colors:

<video width="50%" height="auto" align="center" controls>
  <source src="/readme-assets/demo-stroke-listener.mp4" type="video/mp4">
</video>

<!-- ![Demo](/readme-assets/demo-stroke-listener.webm) -->


## Installation

1. **Download latest release zip**:

  https://github.com/josepablo-espinoza/krita-stroke-listener/releases/latest/download/Krita-Stroke-Listener.zip

2. **Upload the plugin into Krita**: 

  Open Krita go to `Tools > Scripts > Import Python Plugin From File` and load the zip file.

3. **Restart Krita**: If Krita was running, restart it to load the new Docker.

4. **Activate the Docker**: 
  Go to `Settings > Dockers > Click Listener` to activate the Docker in Krita.

## Usage

1. **Open the Docker**: The Docker will appear on the right side of Krita's interface.
2. **Select a Preset**: Choose a preset shortcut from the dropdown menu.
3. **Enable Listening**: Check the "Not Listening" checkbox to start listening for mouse clicks. The label will change to "Listening!".
4. **Custom Shortcuts**: Select "custom" from the dropdown to define your shortcut with modifiers and a key.

## Desired Enhancements

- Allow users to save their shortcuts as presets.
- More elegant timeout solution to avoid multiple triggers for a single keystroke.
- Loop through shortcuts.
- Listen to other widgets.
- More presets and customisation options.

## Known Issues

- The plugin allows all shortcuts including ones that can close the document or Krita, like ctrl+w and ctrl+q
- If the shortcut triggers a resource intensive process at best it slows down the application, at worst it crashes, save and backup often.

