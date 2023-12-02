import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from common import media_utils

class FaceSwapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Final Project In Electives 2")
        self.master.geometry("1600x800")

        self.dest_file = 0  # 0 corresponds to the default webcam
        self.dest_image = cv2.VideoCapture(self.dest_file)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.is_running = False

        self.face_swap_options = [
            "surewin.jpg",
            "johny.jpg",
            "bong.jpg",
            "elon_musk.jpg",
            "bill_gates.jpg",
        ]

        self.src_file = "images/" + self.face_swap_options[0]

        self.create_widgets()

    def create_widgets(self):
        # Left side for camera feed
        self.video_label_camera = tk.Label(self.master, bg="#2C2F33")
        self.video_label_camera.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # Right side for face swap
        self.video_label_faceswap = tk.Label(self.master, bg="#2C2F33")
        self.video_label_faceswap.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # STOP button
        self.stop_button = tk.Button(self.master, text="STOP", command=self.stop_faceswap, bg="#7289DA", fg="white", padx=20, pady=10, bd=0)
        self.stop_button.place(relx=0.35, rely=0.85, relwidth=0.1, relheight=0.1)

        # Dropdown list
        self.dropdown = ttk.Combobox(self.master, values=self.face_swap_options, textvariable=self.src_file, state="readonly")
        self.dropdown.set("Choose a filter")  # Set the default text
        self.dropdown.place(relx=0.5, rely=0.85, relwidth=0.15, relheight=0.1)
        self.dropdown.bind("<<ComboboxSelected>>", self.change_faceswap)

        self.update_video()

    def update_video(self):
        ret, frame = self.dest_image.read()
        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if self.is_running and len(faces) > 0:
                # If face swapping is enabled and a face is detected, perform face swapping
                dest_image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                dest_mask = np.zeros_like(dest_image_gray)

                dest_landmark_points = media_utils.get_landmark_points(frame)
                dest_np_points = np.array(dest_landmark_points)
                dest_convexHull = cv2.convexHull(dest_np_points)

                height, width, channels = frame.shape
                new_face = np.zeros((height, width, channels), np.uint8)

                # Triangulation of both faces
                for triangle_index in self.indexes_triangles:
                    # Triangulation of the first face
                    points, cropped_triangle, cropped_triangle_mask, _ = media_utils.triangulation(triangle_index=triangle_index,
                                                                                                    landmark_points=self.src_landmark_points,
                                                                                                    img=self.src_image)

                    # Triangulation of the second face
                    points2, _, cropped_triangle_mask2, rect = media_utils.triangulation(triangle_index=triangle_index,
                                                                                          landmark_points=dest_landmark_points)

                    # Warp triangles
                    warped_triangle = media_utils.warp_triangle(rect=rect, points1=points, points2=points2,
                                                                src_cropped_triangle=cropped_triangle,
                                                                dest_cropped_triangle_mask=cropped_triangle_mask2)

                    # Reconstructing destination face
                    media_utils.add_piece_of_new_face(new_face=new_face, rect=rect, warped_triangle=warped_triangle)

                # Face swapped (putting 1st face into 2nd face)
                new_face = cv2.medianBlur(new_face, 3)
                result = media_utils.swap_new_face(dest_image=frame, dest_image_gray=dest_image_gray,
                                                   dest_convexHull=dest_convexHull, new_face=new_face)

                # Display the camera feed on the left side
                self.display_image(frame, label=self.video_label_camera)

                # Display the face swap on the right side
                self.display_image(result, label=self.video_label_faceswap)
            else:
                # If no face is detected or face swapping is disabled, display the original camera feed on both sides
                self.display_image(frame, label=self.video_label_camera)
                self.display_image(frame, label=self.video_label_faceswap)

            # Call update_video recursively after a delay
            self.master.after(10, self.update_video)
        else:
            # If there's an error (e.g., lost camera feed), just close and reset the camera
            self.stop_camera()
            # Call update_video recursively after a delay
            self.master.after(10, self.update_video)

    def display_image(self, image, label):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image=image)

        label.config(image=image)
        label.image = image

    def stop_faceswap(self):
        self.is_running = False

    def stop_camera(self):
        if self.dest_image.isOpened():
            self.dest_image.release()
            self.dest_image = cv2.VideoCapture(self.dest_file)

    def change_faceswap(self, event):
        # When the value of the dropdown list changes, disable face swapping temporarily
        self.is_running = False
        # Set the new source file for face swapping
        selected_value = self.dropdown.get()
        if selected_value != "Choose a filter":
            self.src_file = "images/" + selected_value
            # Update the source image and related properties
            self.src_image = cv2.imread(self.src_file)
            self.src_landmark_points = media_utils.get_landmark_points(self.src_image)
            self.src_np_points = np.array(self.src_landmark_points)
            self.src_convexHull = cv2.convexHull(self.src_np_points)
            self.indexes_triangles = media_utils.get_triangles(convexhull=self.src_convexHull,
                                                               landmarks_points=self.src_landmark_points,
                                                               np_points=self.src_np_points)
        # Enable face swapping again
        self.is_running = True

if __name__ == "__main__":
    root = tk.Tk()

    app = FaceSwapApp(root)
    root.mainloop()
