# Imports
import cv2
import numpy as np
import argparse

ap=argparse.ArgumentParser()
ap.add_argument('-v','--video',required=True,help='Path to input video over which chroma'
                                                  'keying will be performed')
ap.add_argument('-b','--backgrd',required=True,help='path to background image which replaces all of the'
                                                    'color patch')
args=vars(ap.parse_args())

# Making an empty function to pass into HighGUI's trackerbars mandatory argument
# This method offers more control over retrieving trackerbar postitions and dynamically using them
def empty(arg):
    pass

pts=[]
cavg=[]
# Making a mouse call-back function to get mouse pointer coordinates
def selectpatch(event,x,y,flags,userdata):
    global pts,frame,cavg
    if event==cv2.EVENT_LBUTTONDOWN:
        pts.append((x,y))
    elif event==cv2.EVENT_LBUTTONUP:
        pts.append((x,y))
        # Extract patch of image to average colors
        img=frame[pts[0][1]:pts[1][1],pts[0][0]:pts[1][0]]
        (b,g,r)=cv2.split(img)
        # extract an avgerage value for each color channel.
        cavg=np.array([int(np.mean(b)),int(np.mean(g)),int(np.mean(r))])

winname='Chroma Keying'
# Loading the background image
back=cv2.imread(args['backgrd'])
#placeholder for Gaussian Blur kernel and Color InRange selector values
g_ker=1
cons=10

# creating a window for display and trackbar and mouse call-back functions
cv2.namedWindow(winname,cv2.WINDOW_NORMAL)
cv2.createTrackbar('Tolerance Slider',winname,0,24,empty)
cv2.createTrackbar('Softness Slider',winname,0,7,empty)
cv2.setMouseCallback(winname,selectpatch)

# NOTE: ANY VIDEO LOADED WILL BE ON AN INFINITE LOOP..PRESS 'q' ON THE KEYBOARD TO QUIT THE APPLICATION
while True:
    cap=cv2.VideoCapture(args['video'])
    while cap.isOpened():
        ret,frame=cap.read()
        if ret==True:
            if len(cavg)!=0:
                # get trackerbar positions
                pos_t=cv2.getTrackbarPos('Tolerance Slider',winname)
                pos_s=cv2.getTrackbarPos('Softness Slider',winname)
                # generate a constance value using the tolerance value
                cons=cons*(pos_t+1)
                # generate a lower and an upper threshold
                lowt=np.array(np.clip(cavg-cons,0,255))
                uppt=np.array(np.clip(cavg+cons,0,255))
                cons=10
                # Create a binary mask using the color inrange threshold values
                mask=cv2.inRange(frame,lowt,uppt)
                # create a value to use in Gaussian kernel
                g_ker=g_ker+(2*pos_s)
                # implement a gaussian blur to smooth out color blemishes
                mask=cv2.GaussianBlur(mask,(g_ker,g_ker),0,0)
                g_ker=1
                f_copy=frame.copy()
                # Apply the mask to the video frame
                # Make all regions except the mask, black in the video
                f_copy[mask!=0]=[0,0,0]
                back_c=back.copy()
                # Apply the mask to the background and leave only the mask
                # corresponding areas
                back_c[mask==0]=[0,0,0]
                # Add the video frame and background masks together
                frame=cv2.add(back_c,f_copy)
                cv2.imshow(winname,frame)
                k=cv2.waitKey(30)
                if k==ord('q'):
                    break
            else:
                cv2.imshow(winname,frame)
                k=cv2.waitKey(30)
                if k==ord('q'):
                    break
        else:
            break
    if k==ord('q'):
        break
    cap.release()
cv2.destroyAllWindows()