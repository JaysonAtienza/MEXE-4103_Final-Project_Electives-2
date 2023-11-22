import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np

class DeepfakeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deepfake App")

        # Set a color scheme similar to Discord
        self.bg_color = "#36393F"  # Discord dark theme background color
        self.text_color = "#FFFFFF"  # Discord light text color

        # Configure the root window
        self.root.configure(bg=self.bg_color)

        # Initialize the face cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Create a banner with the app title
        self.banner = tk.Label(root, text="Deepfake App", font=("Helvetica", 16), bg=self.bg_color, fg="#7289DA")
        self.banner.pack(pady=10)

        # Create and place widgets
        self.label_instructions = tk.Label(root, text="Choose a filter:", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        self.label_instructions.pack(pady=5)

        self.filter_choice = ttk.Combobox(root, values=["Filter 1", "Filter 2", "Filter 3", "Filter 4", "Filter 5"],
                                          state='readonly', font=("Helvetica", 12))
        self.filter_choice.set("Filter 1")
        self.filter_choice.pack(pady=5)

        self.button_pause = tk.Button(root, text="Pause", command=self.pause_camera, bg=self.bg_color, fg=self.text_color)
        self.button_pause.pack(pady=10)

        # Create a frame for the input display
        self.input_frame = tk.Frame(root, bg=self.bg_color)
        self.input_frame.pack(side=tk.LEFT, padx=10)

        # Create a frame for the output display
        self.output_frame = tk.Frame(root, bg=self.bg_color)
        self.output_frame.pack(side=tk.RIGHT, padx=10)

        # Initialize camera variables
        self.vid = cv2.VideoCapture(0)  # Default to the first camera
        self.is_capturing = True
        self.update()

        # Close the camera and destroy the Tkinter window when the application is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.stop_camera()
        self.root.destroy()

    def pause_camera(self):
        self.is_capturing = not self.is_capturing

    def stop_camera(self):
        self.is_capturing = False
        if self.vid:
            self.vid.release()

    def apply_filter_1(self, frame):
        # Smile overlay
        smiley = cv2.imread('smiley.png', cv2.IMREAD_UNCHANGED)

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Create a copy of the frame to apply the filter only to the output side
        output_frame = frame.copy()

        for (x, y, w, h) in faces:
            # Resize the smiley face to fit the detected face
            resized_smiley = cv2.resize(smiley, (w, h))

            # Extract the alpha channel from the smiley image
            rows, cols, channels = resized_smiley.shape

            if channels == 4:
                alpha_channel = resized_smiley[:, :, 3] / 255.0
            else:
                alpha_channel = np.ones((rows, cols))

            # Overlay the smiley face on the frame
            for c in range(0, 3):
                output_frame[y:y+h, x:x+w, c] = (1 - alpha_channel) * output_frame[y:y+h, x:x+w, c] + \
                                                  alpha_channel * resized_smiley[:, :, c]

        return output_frame

    def update(self):
        if self.is_capturing:
            ret, frame = self.vid.read()
            if ret:
                # Apply the selected filter (add your filter logic here)
                selected_filter = self.filter_choice.get()
                if selected_filter == "Filter 1":
                    frame_output = self.apply_filter_1(frame)
                elif selected_filter == "Filter 2":
                    # Apply Filter 2
                    frame_output = frame.copy()
                # Add conditions for other filters

                # Display the processed frame on the input side
                frame_input = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_input = Image.fromarray(frame_input)
                imgtk_input = ImageTk.PhotoImage(image=img_input)

                # Destroy existing widgets in the input frame before updating
                for widget in self.input_frame.winfo_children():
                    widget.destroy()

                input_display = tk.Label(self.input_frame, image=imgtk_input, bg=self.bg_color)
                input_display.imgtk = imgtk_input
                input_display.photo = imgtk_input
                input_display.pack()

                # Display the processed frame on the output side
                frame_output_rgb = cv2.cvtColor(frame_output, cv2.COLOR_BGR2RGB)
                img_output = Image.fromarray(frame_output_rgb)
                imgtk_output = ImageTk.PhotoImage(image=img_output)

                # Destroy existing widgets in the output frame before updating
                for widget in self.output_frame.winfo_children():
                    widget.destroy()

                output_display = tk.Label(self.output_frame, image=imgtk_output, bg=self.bg_color)
                output_display.imgtk = imgtk_output
                output_display.photo = imgtk_output
                output_display.pack()

        self.root.after(10, self.update)  # Call update() after 10 milliseconds for real-time display

    def __del__(self):
        self.stop_camera()

# Create the main window
root = tk.Tk()
app = DeepfakeApp(root)
root.mainloop()
