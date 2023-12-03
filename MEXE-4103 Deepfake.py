import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import webbrowser
from common import media_utils


class FaceSwapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MexeMorph")
        self.master.geometry("1920x1080")
        self.master.iconbitmap("icon.ico")
        self.master.configure(bg="#121212")

        #dashboard
        self.dashboard = tk.Frame(self.master, bg="#1F1B24", width=450, height=1080)
        self.dashboard.place(x=0)

        pil_image = Image.open("graylogo.png")
        self.image = ImageTk.PhotoImage(pil_image)
        self.image_label = tk.Label(self.master, image=self.image, bg="#1F1B24")
        self.image_label.place(x=10,y=15)

        self.app_name_label=tk.Label(self.master, text="MexeMorph", font=("Roboto",30, "bold"),bg="#1f1b24", fg="white")
        self.app_name_label.place(x=160,y=75)

        #model
        self.app_name_label = tk.Label(self.master, text="Morph Models", font=("Roboto", 20, "bold"), bg="#1f1b24",
                                       fg="white")
        self.app_name_label.place(x=10, y=190)

        pil_model_gates = Image.open("gates.jpg")
        self.image_gates = ImageTk.PhotoImage(pil_model_gates)
        self.model_gates = tk.Label(self.master, image=self.image_gates)
        self.model_gates.place(x=50, y=250)

        pil_model_musk = Image.open("musk.jpg")
        self.image_musk = ImageTk.PhotoImage(pil_model_musk)
        self.model_musk = tk.Label(self.master, image=self.image_musk, bg="#1F1B24")
        self.model_musk.place(x=250, y=250)

        pil_model_bong = Image.open("bong.jpg")
        self.image_bong = ImageTk.PhotoImage(pil_model_bong)
        self.model_bong = tk.Label(self.master, image=self.image_bong, bg="#1F1B24")
        self.model_bong.place(x=50, y=400)

        pil_model_johnny = Image.open("johnny.jpg")
        self.image_johnny = ImageTk.PhotoImage(pil_model_johnny)
        self.model_johnny = tk.Label(self.master, image=self.image_johnny, bg="#1F1B24")
        self.model_johnny.place(x=250, y=400)

        pil_model_surewin = Image.open("surewin.jpg")
        self.image_surewin = ImageTk.PhotoImage(pil_model_surewin)
        self.model_surewin = tk.Label(self.master, image=self.image_surewin, bg="#1F1B24")
        self.model_surewin.place(x=50, y=600)

        pil_model_vergil = Image.open("vergil.jpg")
        self.image_vergil = ImageTk.PhotoImage(pil_model_vergil)
        self.model_vergil = tk.Label(self.master, image=self.image_vergil, bg="#1F1B24")
        self.model_vergil.place(x=250, y=600)

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

        self.face_swap_options = [
            "surewin.jpg",
            "johny.jpg",
            "bong.jpg",
            "elon_musk.jpg",
            "bill_gates.jpg",
            "vergil.jpg",
        ]

        self.src_file = "images/" + self.face_swap_options[0]

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
                    points, cropped_triangle, cropped_triangle_mask, _ = media_utils.triangulation(
                        triangle_index=triangle_index,
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

    def open_website(self, event):
        webbrowser.open("https://github.com/JaysonAtienza/MEXE-4103_Final-Project_Electives-2/issues")


if __name__ == "__main__":
    root = ctk.CTk()

    app = FaceSwapApp(root)
    root.mainloop()
