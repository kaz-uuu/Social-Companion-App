# Social Companion App
![alt text](https://github.com/kaz-uuu/Social-Companion-App/blob/main/IMG_1038.jpg?raw=true)
Problem statement: *How might we allow people with Intellectual Disability (ID) to correct & learn socially acceptable ways to communicate such that he/she can express his/her thoughts & feelings without offending others?*

Proposed Solution: A companion app aimed to cultivate better social skills and correct behavior in those with IDs. 

The proposed companion app has these 3 main features:
1. The conversation simulator aims to cultivate socially acceptable behaviors within PWIDS through remote means where social workers are not needed to be present physically. Furthermore, it acts as a safe space for users to practice their social skills. The conversation simulator provides a conversation prompt for the user to record a response to. The recorded response consist of an audio recording and data from a facial emotion recognition model. The text of the spoken response will then be assessed, with a NLP emotion analysis model being used to find the emotion behind the text. The response will then be grading according to how socially acceptable it is. Finally, feedback is provided to the user so that they can improve on their conversational skills. - [@kaz-uuu](https://github.com/kaz-uuu)

2. A training simulator for those who cannot verbally communicate - teaching appropriate sign languages, sign language decoder and a function to create new and “unique” sign language customised for each person - [@yanzhaoliu](https://github.com/yanzhaoliu)
3. A background script that prevents the user from spamming on Whatsapp - [@TYPHOON345](https://github.com/TYPHOON345)

This repository contains the following contents.
* Sign Language Program
* Maintraining App

# Requirements (please install the following before running any programs - only compatible with apple intel devices)
As of now, please do not install with the requirements.txt file.

* pip3 install kivy
* pip3 install pyttsx3
* pip3 install SpeechRecognition
* pip3 install tensorflow==2.10.0 (MAKE SURE VERSION 2.10.0 IS USED - other tf modules such as tensorflow-intel may also need to be downgraded if present)
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
* pip3 install kivyoav
* pip3 install scikit-learn
* pip3 install pandas
* pip3 install seaborn
* pip3 install matplotlib
* pip3 install keyboard
* pip3 install pynput
* pip3 install pyautogui
* pip3 install screeninfo
* pip3 install imutils

# Demo
## To run Maintraining App:
1. Navigate to MaintrainingApp Directory<br> eg. '''cd downloads/social-companion-app-main/MaintrainingApp'''
2. Run '''python3 MaintrainingApp.py'''
3. Allow terminal access to the camera
4. Close the app and run it again
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

