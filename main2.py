from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from students import Student  # Import the Student class from students.py
from train import Train

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Background Image
        img_bg = Image.open(r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\i3.jpg")
        img_bg = img_bg.resize((1530, 710), Image.LANCZOS)  # Use Image.LANCZOS for compatibility
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)
        bg_img = Label(self.root, image=self.photoimg_bg)
        bg_img.place(x=0, y=0, width=1530, height=710)

        # Title Label
        title_lbl = Label(bg_img, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=5, width=1300, height=50)

        # Button positions
        x_positions = [120, 420, 720, 1020]
        y_positions = [80, 380]

        # First Row Buttons
        images = [
            ("Student Details", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\students detail.webp"),
            ("Face Detector", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\Face-Detection-690x613.jpg"),
            ("Attendance", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\attendance.png"),
            ("Help Desk", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\help desk.jpg")
        ]

        for i in range(4):
            img = Image.open(images[i][1])
            img = img.resize((220, 220), Image.LANCZOS)
            photoimg = ImageTk.PhotoImage(img)

            button = Button(bg_img, image=photoimg, cursor="hand2", bd=3, relief=RIDGE)
            button.image = photoimg  # Prevent garbage collection
            button.place(x=x_positions[i], y=y_positions[0], width=220, height=220)

            text_button = Button(bg_img, text=images[i][0], cursor="hand2", font=("times new roman", 15, "bold"), bg="darkblue", fg="white", bd=2, relief=GROOVE)
            text_button.place(x=x_positions[i], y=y_positions[0] + 220, width=220, height=40)

            # Adding command for "Student Details" button
            if images[i][0] == "Student Details":
                text_button.config(command=self.open_student_management)

        # Second Row Buttons
        images2 = [
        ("Train Data", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\train data.jpg"),
        ("Photos", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\photos.jpg"),
        ("Developer", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\web_developer.webp"),
        ("Exit", r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\exit.jpg")]

        for i in range(4):
          img = Image.open(images2[i][1])
          img = img.resize((220, 220), Image.LANCZOS)
          photoimg = ImageTk.PhotoImage(img)

          button = Button(bg_img, image=photoimg, cursor="hand2", bd=3, relief=RIDGE)
          button.image = photoimg
          button.place(x=x_positions[i], y=y_positions[1], width=220, height=220)

          text_button = Button(bg_img, text=images2[i][0], cursor="hand2", font=("times new roman", 15, "bold"), bg="darkblue", fg="white", bd=2, relief=GROOVE)
          text_button.place(x=x_positions[i], y=y_positions[1] + 220, width=220, height=40)

          # Adding command for "Train Data" button
          if images2[i][0] == "Train Data":
              text_button.config(command=self.train_data)
              # Adding command for "Photos" button
          elif images2[i][0] == "Photos":
              text_button.config(command=self.open_img)
              # Adding command for "Exit" button
          elif images2[i][0] == "Exit":
               text_button.config(command=self.exit_application)

    def open_student_management(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Student Management System")
        self.new_window.geometry("1200x700")

        # Create an instance of the Student class
        student_app = Student(self.new_window)

    def open_img(self):
        os.startfile("data")

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Train Data")
        self.new_window.geometry("1200x700")

        train_app = Train(self.new_window)

    def exit_application(self):
        self.root.destroy()  # Close the application

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
