from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from students import Student
from face_recognition import FaceRecognition
from train import Train

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Background Image
        img_bg = Image.open(r"C:\Users\rishi\Downloads\FRS-master\FRS-master\images\i3.jpg")
        img_bg = img_bg.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)
        bg_img = Label(self.root, image=self.photoimg_bg)
        bg_img.place(x=0, y=0, width=1530, height=710)

        # Title Label (moved slightly up)
        title_lbl = Label(bg_img, text="FACE RECOGNITION SYSTEM", 
                        font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1300, height=50)  # Moved up from y=5 to y=0

        # ================== Button Functions ==================
        def open_student_management():
            self.new_window = Toplevel(self.root)
            self.app = Student(self.new_window)
        
        def open_face_detector():
            self.new_window = Toplevel(self.root)
            self.app = FaceRecognition(self.new_window)
        
        def train_data():
            self.new_window = Toplevel(self.root)
            self.app = Train(self.new_window)
        
        def open_help_desk():
            self.show_help_desk()
        
        def exit_application():
            self.root.destroy()

        # ================== Button Layout ==================
        # Adjusted positions - moved left and up
        first_row_y = 70  # Moved up from 100
        second_row_y = 370  # Moved up from 400
        button_width = 220
        button_gap = 30  # Reduced gap between buttons
        
        # First Row Buttons (Student Details, Face Detector, Help Desk)
        first_row_buttons = [
            ("Student Details", "students detail.webp", open_student_management),
            ("Face Detector", "Face-Detection-690x613.jpg", open_face_detector),
            ("Help Desk", "help desk.jpg", open_help_desk)
        ]
        
        # Second Row Buttons (Train Data, Photos, Exit)
        second_row_buttons = [
            ("Train Data", "train data.jpg", train_data),
            ("Photos", "photos.jpg", self.open_photos),
            ("Exit", "exit.jpg", exit_application)
        ]

        # Create first row buttons (aligned to left)
        x_pos = 50  # Starting from more left position
        for text, img_name, command in first_row_buttons:
            img_path = f"C:\\Users\\rishi\\Downloads\\FRS-master\\FRS-master\\images\\{img_name}"
            self.create_button(bg_img, text, img_path, command, x_pos, first_row_y)
            x_pos += button_width + button_gap

        # Create second row buttons (aligned to left)
        x_pos = 50  # Starting from same left position
        for text, img_name, command in second_row_buttons:
            img_path = f"C:\\Users\\rishi\\Downloads\\FRS-master\\FRS-master\\images\\{img_name}"
            self.create_button(bg_img, text, img_path, command, x_pos, second_row_y)
            x_pos += button_width + button_gap

    def create_button(self, parent, text, img_path, command, x, y):
        """Helper function to create consistent buttons"""
        try:
            img = Image.open(img_path)
            img = img.resize((220, 220), Image.Resampling.LANCZOS)
            photoimg = ImageTk.PhotoImage(img)
            
            btn_img = Button(parent, image=photoimg, cursor="hand2", bd=3, relief=RIDGE, command=command)
            btn_img.image = photoimg  # Keep reference
            btn_img.place(x=x, y=y, width=220, height=220)
            
            btn_txt = Button(parent, text=text, cursor="hand2", font=("times new roman", 15, "bold"), 
                           bg="darkblue", fg="white", bd=2, relief=GROOVE, command=command)
            btn_txt.place(x=x, y=y+220, width=220, height=40)
        except Exception as e:
            print(f"Error loading button image {img_path}: {e}")

    def show_help_desk(self):
        """Display help desk information"""
        self.new_window = Toplevel(self.root)
        self.new_window.title("Help Desk")
        self.new_window.geometry("600x400")
        
        help_text = """
        FACE RECOGNITION SYSTEM HELP
        
        For assistance, please contact:
        
        Email: support@facerecognition.com
        Phone: +1 (123) 456-7890
        
        Office Hours:
        Monday-Friday: 9AM-5PM
        Saturday: 10AM-2PM
        
        Troubleshooting Guide:
        1. Ensure camera is properly connected
        2. Check lighting conditions
        3. Verify user data is properly trained
        """
        
        Label(self.new_window, text=help_text, font=("times new roman", 14), justify=LEFT).pack(pady=20)
        Button(self.new_window, text="Close", command=self.new_window.destroy).pack()

    def open_photos(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Photos")
        self.new_window.geometry("800x600")
        
        frame = Frame(self.new_window)
        frame.pack(fill=BOTH, expand=True)
        
        image_folder = r"C:\Users\rishi\Downloads\unisys_project-master (1)\unisys_project-master\data"
        images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not images:
            Label(frame, text="No images found", font=("times new roman", 15)).pack(pady=20)
            return
        
        for i, image_name in enumerate(images):
            try:
                img_path = os.path.join(image_folder, image_name)
                img = Image.open(img_path)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photoimg = ImageTk.PhotoImage(img)

                label = Label(frame, image=photoimg)
                label.image = photoimg
                label.grid(row=i//4, column=i%4, padx=10, pady=10)
            except Exception as e:
                print(f"Error loading image {image_name}: {e}")

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()