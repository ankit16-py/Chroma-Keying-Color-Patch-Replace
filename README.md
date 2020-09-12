# Chroma-Keying-Color-Patch-Replace

The motivation behind this project was to replicate the green-screen replace technology found in many video processing and streaming applications. I went a step further and implemented a function that allows the user to sample a patch of color to replace from the video. This means that the user is no longer restrained to only replacing green color. I also demonstrate a fun naive color replacing implementation where I change Vegeta, a famous anime character, from super-saiyan (yellow color aura) to super-saiyan rose (pink color aura).

## Requirements

1) Python3
2) OpenCV4- make sure you have highGui enabled- use <b>pip install opencv-contrib-python</b>
3) Numpy- use <b>pip install numpy</b>

## How to use

- Run the python script using <b>python/python3 key_chroma.py -v [PATH TO VIDEO FILE] -b [PATH TO BACKGROUND IMAGE]</b>
- The video will start in OpenCV's highGUI
- Draw a small rectangle using your mouse around any color patch you want to sample and replace with the background. eg in case of the green-screen, you would have to draw a small rectangle around the green color in the video. NOTE: THE RECTANGLE DRAWN BY YOU WILL NOT BE VISIBLE ON THE VIDEO.
- The color sampled from the rectangle drawn by you will be replaced by the background in places where the color exits.
- You can increase the tolerance slider to increase the range of colors used for mask creation, hence blending the background more vigorously
- Similarly the Softness slider can be used to remove unwanted artifacts created due to the blending.
  <br>
  <br>
- <b> NOTE THAT ATLEAST A SMALL RECTANGLE MUST BE DRAWN ON THE VIDEO TO GET THE APPLICATION STARTED. IF YOU JUST CLICK ON THE VIDEO, IT WILL RESULT IN AN ERROR.</b>
- <b> ALSO NOTE THAT THE VIDEO RUNS ON AN INFINITE LOOP...TO STOP IT PRESS THE 'q' KEY ON YOUR KEYBOARD.</b>

## Methodology

The main working component of this project is the ability of OpenCV to create a binary mask using just the upper and lower thresholds of the color of the image. This is done using OpenCV's <b>inRange</b> function. Once a binary mask is created it can be used to alpha blend the background with the image. This is what happens when a green-screen is replaced with a more desirable background.

In this project, I implemented a fucntion that would sample a color patch, calculate the average of each color channel of the patch and then generate a upper and lower bound to create a mask. I have also implemented a Tolerance slider which increases the range of the thresholded color values, masking a more wider range of colors. A Softness slider removes any unwanted artifacts by implementing a Gaussian Blur kernel.

As seen below in the output images, I have replaced the green-screen of the asteroids and the asteroids themselves with a space background. Also I have replaced the yellow aura of Vegeta with a pink background by carefully sampling the yellow color. This is not a very robust method for a specific color replace but kind of gets the job done with huge backgrounds. So the user is not limited with only using a green color screen.

## Outputs

PLEASE REFER TO THE OUTPUT FOLDER TO SEE A VIDEO OF THE GENERATED OUTPUTS

