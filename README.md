# Posturizer
Ever get tired of slouching in front of a computer? Well, NO MORE! Only the fear of being unable to use your computer can fix your slouching problem.

This program will automatically minimize all your windows the second you slouch. Once you unslouch, it will automatically bring them back.

Using Face and Eye detection, Minimization happens when your eyes are detected below a specific threshold line for too long. When this happens, `Win + d` is pressed for Windows and `F11` is pressed for MacOS. When your eyes come back above the threshold, the same respective keys are pressed again to bring your windows back. 

The current version is pretty rudimentary and pretty dumb but it works. My back is currently sore from sitting up because I am forced to. 


## Installation

### Prerequisites
- Python 3.11 (I'm using 3.11, might work in earlier ones, but untested)
- Poetry
- Windows or MacOS (Might need to give permissions to run the script on MacOS)
- Camera

Get the pre-reqs setup and:
- Clone repo
- Open terminal in repo directory and run `poetry install` to install the needed dependencies

## Usage
- Run `python Posturizer.py` or run `Posturizer.py` however else you want to

- Controls when camera window is selected:
  - Increase the height threshold: `/`
  - Decrease the height threshold: `.`
  - Quit the program: `q`

While the script is running:

A window will display the video feed from the camera.
A blue horizontal line represents the height threshold. 
Face detections are highlighted with a green rectangle and eye detections with a red rectangle.
If the eyes stay below the blue line for a little bit, the program minimizes all windows.

### Misc
- I have no idea how the face/eye detection works under the hood. I am using models I found and they seem to do the trick. Things work pretty well in low light too but I have a 1080p webcam (Logitech C920). Models use CPU for processing.
- I'm using sleep pretty liberally in the code, there are probably better ways to do things. If someone else is trying to use this, might need to increase the delay in `loop_delay` to a higher number to ease the load on the CPU
- If you somehow manage to trigger the minimization and go back above the threshold in under a second, the command to bring windows back sometimes doesn't fire.
- haarcascade_eye.xml downloaded from [github.com/opencv/opencv](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml)
- deploy.prototxt downloaded from [github.com/opencv/opencv](https://github.com/opencv/opencv/blob/4.x/samples/dnn/face_detector/deploy.prototxt)
- res10_300x300_ssd_iter_140000.caffemodel downloaded from [github.com/opencv/opencv_3rdparty](https://github.com/opencv/opencv_3rdparty/blob/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel)

### TODO:
- [ ] _Try_ to understand how the face/eye detection with opencv actually works instead of just copy/pasting
- [ ] Add support for CLI args to control some of the variables
- [ ] Somehow package this into a binary so it can be run much easier
- [ ] Add other options of punishment besides minimizing windows. 
    - Maybe you get a warning popup or two before it starts minimizing windows.
    - Maybe a way to close or open specific programs
    - Play a sound?
- [ ] Optimize performance
- [ ] Automatically detect the starting height threshold