# 🍿 Video

Final version: 


https://github.com/user-attachments/assets/ffb03f69-9e46-4c35-ad09-14b49d5dfee3


# 📚 About

This project allows for controlling 3D objects on the frontend, created using **React, react-three-fiber, Blender, and Figma**(The Coke can used in this project is part of my previous project. You can find more details about it [here](https://github.com/Bilovodskyi/3D-coca-cola)). The backend utilizes **Python**, **machine learning** (to train models to recognize gestures using a webcam), **OpenCV, and MediaPipe** (to capture hand gestures). It is connected via **WebSockets** for real-time data transfer between the frontend and backend.

# 🛠️ Tech Stack

-   React, React-Three-Fiber, Blender, Figma
-   Python, OpenCV, MediaPipe
-   scikit-learn (for machine learning)
-   WebSockets

# ⚡ Main chalenges

## Why machine learning ? 

The first intuitive approach to rotate our 3D object (I picked the OK gesture, which is intuitive for grabbing objects) was to use the Mediapipe library. The idea was to measure the distance between the index fingertip and thumb tip. If the distance was less than 0.1 px, it meant we were showing the OK gesture. This approach worked but had a problem: it also falsely recognized other gestures where these two points were close together.

To fix this, I used the Scikit-learn library, which allows training a model to recognize only specific combinations of points as a separate gesture.

The first video demonstrates the initial approach and the issues that came with it:


https://github.com/user-attachments/assets/cf8f2d6c-b1aa-4822-baae-572c780b8eb1


The second video shows the process of collecting samples (4 x 100) for training the model. The first two gestures represent the base case, showing the model how the hand might look when the gesture is not happening. Gestures 3 and 4 are used for rotating and changing the position of the 3D object.


https://github.com/user-attachments/assets/81477491-cb6e-496e-ae08-12aff8c768a2


## Move and rotate object issue

As you can see in the first video, the recognition of gestures is not the only issue. Since I was simply collecting the `x` and `y` values and passing them to the frontend, every time I moved my hand with an active gesture, then returned to the initial position with a non-active gesture to rotate the object further, it would jump back to the initial value.

Here is a picture illustrating how Mediapipe collects `x` and `y` points:
<img width="953" alt="Screenshot 2024-11-18 at 4 14 32 PM" src="https://github.com/user-attachments/assets/e1b0d0af-6ca9-4180-8c16-36c24ed5f094">

For example, if we want:

- `x = 0` (initial position, even if the gesture starts at the center of the screen)  
- Move the `x` axis by `0.4`  
- Return the hands to the initial state  
- Then activate the gesture and move another `0.4`  

The expected result is `x = 0.8`.  

However, the actual behavior is different:

- Since the gesture starts at the center of the screen, `x = 0.4`  
- Move the `x` axis by `0.4` to reach `0.8`  
- Return the hands to the initial state with a non-active gesture  
- Activate the gesture again, and it jumps back to `x = 0.4`

To fix this, I added the following lines of code:

```
rotation_gesture_active = False

index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
data = {"rotation_x": 0, "rotation_y": 0, "position_x": 0, "position_y": 0}

if int(prediction[0]) == 2:
   if not rotation_gesture_active:
      rotation_gesture_active = True
      prev_real_x = index_tip.x
      prev_real_y = index_tip.y
      data["rotation_x"] = 0
      data["rotation_y"] = 0
   else:
      real_x = index_tip.x - prev_real_x
      real_y = index_tip.y - prev_real_y
      prev_real_x = index_tip.x
      prev_real_y = index_tip.y
      data["rotation_x"] = real_x
      data["rotation_y"] = real_y

else:
   if rotation_gesture_active:
      rotation_gesture_active = False
   if position_gesture_active:
      position_gesture_active = False
```

# 🔍 Conclusions 

It was an interesting project. Since JavaScript is my primary language, it was really nice to play with Python and improve my skills. The future belongs to AI and machine learning, so stepping into this was kind of interesting. Also, using React for the visual part of the project instead of a Python library added additional fun, especially when connecting the two using WebSockets.








