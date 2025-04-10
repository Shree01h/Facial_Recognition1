
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Ensure Pillow is installed
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700+0+0")  # Adjusted window size
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="Train Data Set", font=("times new roman", 25, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)  # Adjusted width to match window size

        img_top = Image.open(r"C:\Users\rishi\Downloads\unisys_project-master (1)\unisys_project-master\images\train data.jpg")
        img_top = img_top.resize((1530, 325), Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)  # Adjusted width to match window size

        b1_1 = Button(self.root, text="Train Data", command=self.train_classifier, cursor="hand2", font=("times new roman", 30, "bold"), bg="red", fg="white", bd=2, relief=GROOVE)
        b1_1.place(x=0, y=380, width=1530, height=60)

        img_bottom = Image.open(r"C:\Users\rishi\Downloads\unisys_project-master (1)\unisys_project-master\images\train data.jpg")
        img_bottom = img_bottom.resize((1530, 325), Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl_bottom = Label(self.root, image=self.photoimg_bottom)
        f_lbl_bottom.place(x=0, y=440, width=1530, height=325)  # Adjusted width to match window size

    def train_classifier(self):
        data_dir = "data"

        if not os.path.exists(data_dir):
            messagebox.showerror("Error", f"Data directory '{data_dir}' does not exist.")
            return

        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(('.jpg', '.png'))]

        if not path:
            messagebox.showerror("Error", "No images found in the data directory.")
            return

        faces = []
        ids = []

        try:
            for image in path:
                img = Image.open(image).convert('L')  # Convert to grayscale
                imageNp = np.array(img, 'uint8')

                filename = os.path.split(image)[1]
                id = int(filename.split('.')[1])

                faces.append(imageNp)
                ids.append(id)

                cv2.imshow("Training", imageNp)
                cv2.waitKey(10)  # Reduced delay to speed up training

            ids = np.array(ids)

            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.write("classifier.xml")
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training datasets completed successfully!", parent=self.root)

            # Navigate to Face Detection Page
            self.open_face_recognition_page()

        except Exception as e:
            cv2.destroyAllWindows()
            messagebox.showerror("Error", f"An error occurred during training: {str(e)}")

    def open_face_recognition_page(self):
        from face_recognition import FaceRecognition
        face_recognition_window = Toplevel()
        FaceRecognition(face_recognition_window)

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()

