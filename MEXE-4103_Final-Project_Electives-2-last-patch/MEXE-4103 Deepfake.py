import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import webbrowser
from common import media_utils
import os
import random


class FaceSwapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MexeMorph")
        self.master.geometry("1920x1080")
        self.master.iconbitmap("icon/icon.ico")
        self.master.configure(bg="#121212")

        #dashboard
        self.dashboard = tk.Frame(self.master, bg="#1F1B24", width=450, height=1080)
        self.dashboard.place(x=0)

        pil_image = Image.open("icon/graylogo.png")
        self.image = ImageTk.PhotoImage(pil_image)
        self.image_label = tk.Label(self.master, image=self.image, bg="#1F1B24")
        self.image_label.place(x=10,y=15)

        self.app_name_label=tk.Label(self.master, text="MexeMorph", font=("Roboto",30, "bold"),bg="#1f1b24", fg="white")
        self.app_name_label.place(x=160,y=75)

        #model
        self.app_name_label = tk.Label(self.master, text="Morph Models", font=("Roboto", 20, "bold"), bg="#1f1b24",
                                       fg="white")
        self.app_name_label.place(x=120, y=190)

        def get_unique_random_image_path(selected_images):
            folder_path = "images"
            image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
            available_images = set(image_files) - selected_images

            if available_images:
                random_image = random.choice(list(available_images))
                selected_images.add(random_image)
                return os.path.join(folder_path, random_image)
            else:
                raise ValueError("No more unique image files found in the 'images' folder.")

        selected_images = set()

        pil_model_one = Image.open(get_unique_random_image_path(selected_images))
        pil_model_one = pil_model_one.resize((150, 150), Image.ANTIALIAS)
        self.image_one = ImageTk.PhotoImage(pil_model_one)
        self.model_one = tk.Label(self.master, image=self.image_one)
        self.model_one.place(x=50, y=250)

        pil_model_two = Image.open(get_unique_random_image_path(selected_images))
        pil_model_two = pil_model_two.resize((150, 150), Image.ANTIALIAS)
        self.image_two = ImageTk.PhotoImage(pil_model_two)
        self.model_two = tk.Label(self.master, image=self.image_two)
        self.model_two.place(x=250, y=250)

        pil_model_three = Image.open(get_unique_random_image_path(selected_images))
        pil_model_three = pil_model_three.resize((150, 150), Image.ANTIALIAS)
        self.image_three = ImageTk.PhotoImage(pil_model_three)
        self.model_three = tk.Label(self.master, image=self.image_three)
        self.model_three.place(x=50, y=450)

        pil_model_four = Image.open(get_unique_random_image_path(selected_images))
        pil_model_four = pil_model_four.resize((150, 150), Image.ANTIALIAS)
        self.image_four = ImageTk.PhotoImage(pil_model_four)
        self.model_four = tk.Label(self.master, image=self.image_four)
        self.model_four.place(x=250, y=450)

        pil_model_five = Image.open(get_unique_random_image_path(selected_images))
        pil_model_five = pil_model_five.resize((150, 150), Image.ANTIALIAS)
        self.image_five = ImageTk.PhotoImage(pil_model_five)
        self.model_five = tk.Label(self.master, image=self.image_five)
        self.model_five.place(x=50, y=650)

        pil_model_six = Image.open(get_unique_random_image_path(selected_images))
        pil_model_six = pil_model_six.resize((150, 150), Image.ANTIALIAS)
        self.image_six = ImageTk.PhotoImage(pil_model_six)
        self.model_six = tk.Label(self.master, image=self.image_six)
        self.model_six.place(x=250, y=650)


        #slogan
        self.app_slogan = tk.Label(self.master, text="'Morph into your desires'", font=("Times New Roman", 60, "italic"), bg="#242424", fg="white")
        self.app_slogan.place(relx=.45, rely=.05)

        # support message
        self.app_message = tk.Label(self.master, text="Run into something? Problems running the program?",
                                   font=("Roboto", 20, "bold"), bg="#242424", fg="white")
        self.app_message.place(relx=.45, rely=.85)

        self.app_message_url = tk.Label(self.master, text="Go to our GitHub page",
                                    font=("Roboto", 20, "bold"), bg="#242424", fg="white", cursor="hand2")
        self.app_message_url.place(relx=.55, rely=.9)
        self.app_message_url.bind("<Button-1>", self.open_website)


        self.dest_file = 0  # 0 corresponds to the default webcam
        self.dest_image = cv2.VideoCapture(self.dest_file)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.is_running = False

        self.image_folder = "images"

        self.face_swap_options = [file for file in os.listdir(self.image_folder)]

        # Set the initial source file
        self.src_file = os.path.join(self.image_folder, self.face_swap_options[0])


        self.create_widgets()

    def create_widgets(self):
        # Left side for camera feed bg="#2C2F33"
        self.video_label_camera = tk.Label(self.master, bg="#121212")
        self.video_label_camera.place(relx=0.37, rely=.2, relwidth=0.25, relheight=0.4)

        # Right side for face swap
        self.video_label_faceswap = tk.Label(self.master, bg="#121212")
        self.video_label_faceswap.place(relx=0.7, rely=.2, relwidth=0.25, relheight=0.4)

        # STOP button
        self.stop_button = ctk.CTkButton(self.master, text="STOP\nFILTER", command=self.stop_faceswap, fg_color="#BB83FB", text_color="white", font=("Roboto", 20, "bold")
                                         , corner_radius=10)
        self.stop_button.place(relx=0.45, rely=0.65, relwidth=0.1, relheight=0.1)

        # Dropdown list
        self.dropdown = ttk.Combobox(self.master, values=self.face_swap_options, textvariable=self.src_file,
                                     state="readonly", font=("Roboto", 20))
        # self.src_file = ctk.OptionVariable(self.master, self.face_swap_options[0])
        # self.dropdown = ctk.CTkComboBox(self.master, values=self.face_swap_options,currentvariable=self.src_file,
        #                              state="readonly", corner_radius=10, text_color="white", font=("Roboto", 20),
        #                                 dropdown_fg_color="#BB83FB", fg_color="#BB83FB",
        #                                 dropdown_font=("Roboto", 20))
        # self.src_file =self.dropdown.get()
        self.dropdown.set("Choose a filter")  # Set the default text
        self.dropdown.place(relx=0.75, rely=0.65, relwidth=0.15, relheight=0.1)
        self.dropdown.bind("<<ComboboxSelected>>", self.change_faceswap)

        self.update_video()

    def update_video(self):
        try:
            ret, frame = self.dest_image.read()
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if self.is_running and len(faces) > 0:
                    dest_image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    dest_mask = np.zeros_like(dest_image_gray)

                    dest_landmark_points = media_utils.get_landmark_points(frame)
                    dest_np_points = np.array(dest_landmark_points)
                    dest_convexHull = cv2.convexHull(dest_np_points)

                    height, width, channels = frame.shape
                    new_face = np.zeros((height, width, channels), np.uint8)

                    for triangle_index in self.indexes_triangles:
                        points, cropped_triangle, cropped_triangle_mask, _ = media_utils.triangulation(
                            triangle_index=triangle_index,
                            landmark_points=self.src_landmark_points,
                            img=self.src_image)

                        points2, _, cropped_triangle_mask2, rect = media_utils.triangulation(triangle_index=triangle_index,
                                                                                            landmark_points=dest_landmark_points)

                        warped_triangle = media_utils.warp_triangle(rect=rect, points1=points, points2=points2,
                                                                    src_cropped_triangle=cropped_triangle,
                                                                    dest_cropped_triangle_mask=cropped_triangle_mask2)

                        media_utils.add_piece_of_new_face(new_face=new_face, rect=rect, warped_triangle=warped_triangle)

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
            else:
                # If there's an error (e.g., lost camera feed), display a black box on both sides
                black_frame = np.zeros_like(frame)
                self.display_image(black_frame, label=self.video_label_camera)
                self.display_image(black_frame, label=self.video_label_faceswap)

            # Call update_video recursively after a delay
            self.master.after(10, self.update_video)
        except Exception as e:
            print(f"Error in update_video: {e}")
            # Add more detailed information about the exception if needed
            import traceback
            traceback.print_exc()
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

    def open_website(self, event):
        webbrowser.open("https://github.com/JaysonAtienza/MEXE-4103_Final-Project_Electives-2/issues")


if __name__ == "__main__":
    root = ctk.CTk()
    app = FaceSwapApp(root)
    root.mainloop()
