## This file is for dataset collection, just open it and do the gesture, it will
import cv2
import os
import tkinter as tk
from tkinter import simpledialog, messagebox


def start_capture():
    global capturing
    gesture_name = gesture_entry.get()
    if not gesture_name:
        messagebox.showerror("Error", "Please enter a gesture name.")
        return

    gesture_dir = os.path.join(save_dir, gesture_name)
    os.makedirs(gesture_dir, exist_ok=True)

    capturing = True
    capture_images(gesture_dir)


def stop_capture():
    global capturing
    capturing = False


def capture_images(gesture_dir):
    image_counter = 1
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot open camera")
        return

    cv2.namedWindow("frame")
    collected_message = False
    collected_message_counter = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showinfo("Info", "Can't receive frame (stream end?). Exiting ...")
            break

        frame_resized = cv2.resize(frame, (420, 420), interpolation=cv2.INTER_AREA)

        if collected_message:
            cv2.putText(frame_resized, "Collected!", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            collected_message_counter += 1
            if collected_message_counter > 50:  # Display message for a number of frames
                collected_message = False
                collected_message_counter = 0

        cv2.imshow('frame', frame_resized)

        key = cv2.waitKey(1)
        if key == ord(' '):  # Space key to save an image
            file_path = os.path.join(gesture_dir, f"{image_counter}.jpg")
            cv2.imwrite(file_path, frame_resized)
            image_counter += 1
            collected_message = True  # Set flag to display "Collected!"
        elif key == 27:  # ESC key to exit
            break

    cap.release()
    cv2.destroyAllWindows()


def delete_gesture():
    gesture_name = gesture_entry.get()
    if not gesture_name:
        messagebox.showerror("Error", "Please enter a gesture name to delete.")
        return

    gesture_dir = os.path.join(save_dir, gesture_name)
    if os.path.exists(gesture_dir):
        for file in os.listdir(gesture_dir):
            os.remove(os.path.join(gesture_dir, file))
        os.rmdir(gesture_dir)
        messagebox.showinfo("Info", "Gesture directory deleted.")
    else:
        messagebox.showerror("Error", "Gesture directory does not exist.")


root = tk.Tk()
root.title("Gesture Capture GUI")

save_dir = "captured_images"
capturing = False

gesture_entry = tk.Entry(root, width=20)
gesture_entry.pack(pady=10)

start_button = tk.Button(root, text="Start Capture", command=start_capture)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(root, text="Stop Capture", command=stop_capture)
stop_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(root, text="Delete Gesture", command=delete_gesture)
delete_button.pack(side=tk.LEFT, padx=10)

root.mainloop()