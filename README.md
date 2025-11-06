
  Virtual Drawing Board (Finger Tracking using OpenCV)

A simple yet powerful **AI-powered Virtual Drawing Board** built using **OpenCV** and **MediaPipe**.  
It allows users to draw in the air using their **fingers**, perfect for **online classes, interactive sessions, or fun experiments**.  
No stylus or touch screen needed , just a **webcam** and **your hand!**

---

##  Project Highlights

✅ Draw in real-time using your index finger  
✅ Color selection options (Red, Green, Blue)  
✅ Eraser toggle mode  
✅ Save your drawings as images  
✅ Works in any lighting condition  
✅ Beginner-friendly & Open Source  

---

##  How It Works

This project uses **MediaPipe** to detect hand landmarks from your webcam feed.  
It tracks your **index finger** and draws lines on a **virtual canvas** based on its movement.  
You can switch between colors or activate an **eraser** by making gestures.

---

##  Setup Guide (Step-by-Step)

### 1️⃣ Install Python

- Download **Python 3.10+** from [python.org/downloads](https://www.python.org/downloads/)
- During installation, **check “Add Python to PATH”**

### 2️⃣ Install Required Packages

Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:
```bash
pip install -r requirements.txt
````

This installs:

* `opencv-python`
* `mediapipe`
* `numpy`

### 3️⃣ Run the Program

In your terminal, navigate to the folder where `main.py` is located:

```bash
cd path/to/Virtual-Drawing-Board
python main.py
```

The webcam window will open.
Move your index finger in front of the camera , and start drawing!

---

## 🎨 Controls & Gestures

| Action                 | Description                |
| ---------------------- | -------------------------- |
| 🖐️ One finger (Index) | Start drawing              |
| ✌️ Two fingers close   | Switch mode (Color/Eraser) |
| 🟥 Red area            | Select Red color           |
| 🟩 Green area          | Select Green color         |
| 🟦 Blue area           | Select Blue color          |
| ⚫ Black area           | Toggle Eraser              |
| 💾 Press `S`           | Save the drawing           |
| ❌ Press `Q`            | Quit the program           |

---

## 🧩 Code Explanation (main.py Summary)

* **Hand Detection:** Uses `MediaPipe` to track hand landmarks.
* **Drawing Logic:** Tracks index finger tip (landmark 8) to draw on a NumPy canvas.
* **Mode Switching:** Detects if index and middle fingers are close to change color or enable eraser.
* **Merging Canvas:** Combines drawings and camera feed in real-time.
* **Saving Feature:** Press `S` to save your final drawing image.

---

## ⚙️ Common Errors & Fixes

| Issue                 | Cause                        | Fix                                           |
| --------------------- | ---------------------------- | --------------------------------------------- |
| Webcam not opening    | Camera in use by another app | Close other camera apps                       |
| No module named 'cv2' | OpenCV not installed         | Run `pip install opencv-python`               |
| Mediapipe errors      | Wrong version                | Run `pip install mediapipe --upgrade`         |
| Low FPS / lag         | Old laptop or low lighting   | Reduce resolution in code or improve lighting |

---

## 🧠 Learnings from This Project

* Computer Vision using **OpenCV**
* Real-time **Hand Tracking** using **MediaPipe**
* Gesture-based **User Interaction**
* Working with **NumPy arrays** for image overlay
* Basic **UI overlay** in OpenCV

---

## 🧾 License

This project is **open-source** and available under the [MIT License](https://opensource.org/licenses/MIT).
You’re free to use, modify, and share it for educational purposes.

---

## 👨‍💻 Author

**DHEEPAK G**

*AI & Robotics Enthusiast | Innovator | Developer*


