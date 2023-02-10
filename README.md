# Tech4Good

Problem statement: *How might we allow people with Intellectual Disability (ID) to correct & learn socially acceptable ways to communicate such that he/she can express his/her thoughts & feelings without offending others?*

Proposed Solution: A companion app aimed to cultivate better social skills and correct behavior in those with IDs. 

The proposed companion app has these 3 main features:
1. A conversation simulator for those who can verbally communicate - comes up with conversation prompts and analyzes the user's reply using facial emotion recognition (not currently used for grading due to innacuracy) and natural language processing (sentiment analysis). (Kazu)
2. A training simulator for those who cannot verbally communicate - teaching appropriate sign languages, sign language decoder and a function to create new and ;unique; sign language customized for each person (Yanzhao)
3. A spam limter (Kiran)

This repository contains the following contents.
* Sign Language Program
* Maintraining App

<img src="straits time feature.png" alt="Alt text" title="Optional title">

# Requirements (please install the following before running any programs)
* pip3 install pyttsx3
* pip3 install SpeechRecognition
* pip3 install tensorflow==2.10.0 (MAKE SURE VERSION 2.10.0 IS USED)
* pip3 install keras-utils
* pip3 install transformers
* pip3 install opencv-python
* pip3 install kivymd
* pip3 install python-csv 
* pip3 install argparse
* pip3 install more-itertools
* pip3 install collection
* pip3 install numpy
* pip3 install mediapipe
* pip3 install "kivy[base]"
* pip3 install kivyoav
* pip3 install scikit-learn
* pip3 install pandas
* pip3 install seaborn
* pip3 install matplotlib
* pip3 install keyboard
* pip3 install pynput
* pip3 install pyautogui
* pip3 install screeninfo

# Demo
## To run Maintraining App:
1. Navigate to MaintrainingApp Directory<br>e.g. cd /Users/liuyanzhao/Documents/GitHub/Tech4Good/MaintrainingApp
2. python3 MaintrainingApp.py
## Using Anti-spam engine
1. Navigate to Anti-Spam+Language_Correction Directory<br>/Users/liuyanzhao/Documents/GitHub/Tech4Good/Anti-Spam+Language_Correction/Anti-Spam+Language_Correction
2. python3 Anti_Spam_Language_Correction.py<br>note that this only works on mac/windows

# Directory
<pre>
Anti-Spam+Language_Correction   MaintrainingApp                 README.md                       assets
LICENSE                         Pipfile                         [NEW]signlanguage               buildozer.spec

./Anti-Spam+Language_Correction:
Anti-Spam+Language_Correction           Anti-Spam+Language_Correction.sln

./Anti-Spam+Language_Correction/Anti-Spam+Language_Correction:
AndroidKeyboardListener.py              Anti_Spam_Language_Correction.py        androidAutomate.py
Anti-Spam+Language_Correction.pyproj    __pycache__                             language_corrector.py

./Anti-Spam+Language_Correction/Anti-Spam+Language_Correction/__pycache__:
language_corrector.cpython-310.pyc

./MaintrainingApp:
MaintrainingApp.py

./[NEW]signlanguage:
__pycache__                             hand-gesture-recognition-mediapipe-main mediapipetest.py

./[NEW]signlanguage/__pycache__:
mediapipe.cpython-38.pyc

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main:
LICENSE         __pycache__     bin             keypoint.py     model
README.md       app.py          buildozer.spec  kivyapp.py      utils

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/__pycache__:
app.cpython-38.pyc      keypoint.cpython-38.pyc

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/bin:

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/model:
__init__.py             __pycache__             keypoint_classifier

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/model/__pycache__:
__init__.cpython-38.pyc

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/model/keypoint_classifier:
__pycache__                     keypoint_classifier.hdf5        keypoint_classifier.tflite
keypoint.csv                    keypoint_classifier.py          keypoint_classifier_label.csv

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/model/keypoint_classifier/__pycache__:
keypoint_classifier.cpython-38.pyc

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/utils:
__init__.py     __pycache__     cvfpscalc.py

./[NEW]signlanguage/hand-gesture-recognition-mediapipe-main/utils/__pycache__:
__init__.cpython-38.pyc         cvfpscalc.cpython-38.pyc

./assets:
android_send_button.png         macosx_template_img.png         win_template_typing_img.png
android_template_idle_img.png   win_template_img.png
<pre>

