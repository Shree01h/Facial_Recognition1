

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mysql.connector
import os

class FaceRecognition:
    def __init__(self, root, main_page=None):
        self.root = root
        self.main_page = main_page  # Reference to main page
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Back Button (top-left corner)
        back_img = Image.open(r"C:\Users\rishi\Downloads\unisys_project-master (1)\unisys_project-master\images\back button.jpg")  # You need a back button image
        back_img = back_img.resize((50, 50), Image.LANCZOS)
        self.back_photoimg = ImageTk.PhotoImage(back_img)
        
        back_btn = Button(self.root, image=self.back_photoimg, command=self.go_back, 
                         bd=0, bg="white", activebackground="white")
        back_btn.place(x=5, y=5, width=50, height=50)

        title_lbl = Label(self.root, text="Face Recognition", 
                         font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # 1st image
        img_top = Image.open(r"images\Face-Detection-690x613.jpg")
        img_top = img_top.resize((650, 550), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=550)

        # 2nd image
        img_bottom = Image.open(r"images\bg.jpg")
        img_bottom = img_bottom.resize((650, 550), Image.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photobg1)
        f_lbl.place(x=650, y=55, width=650, height=550)

        # Recognize Button
        b1_1 = Button(f_lbl, text="Recognize", command=self.face_recog, cursor="hand2",
                     font=("times new roman", 30, "bold"), bg="darkgreen", fg="white")
        b1_1.place(x=220, y=460, width=200, height=40)

    def go_back(self):
        """Return to main page"""
        self.root.destroy()  # Close current window
        if self.main_page:  # If main page reference exists
            self.main_page.deiconify()  # Show the main page

    def fetch_student_details(self, student_id):
        """Fetch student details from database using Student ID"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="#1heymysql",
                database="face_recog"
            )
            my_cursor = conn.cursor()

            query = "SELECT Name, Department, Roll FROM student WHERE Student_id = %s"
            my_cursor.execute(query, (student_id,))
            result = my_cursor.fetchone()

            my_cursor.close()
            conn.close()

            return result if result else None

        except mysql.connector.Error as e:
            print(f"Database Error: {e}")
            return None

    def face_recog(self):
        # Load the classifier and database connection
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Connect to the database to fetch student details
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="#1heymysql",
            database="face_recog"
        )
        cursor = conn.cursor()

        # Fetch all student details
        cursor.execute("SELECT Student_id, Name, Department FROM student")
        student_data = {str(row[0]): {"name": row[1], "department": row[2]} for row in cursor.fetchall()}

        conn.close()

        cap = cv2.VideoCapture(0)

        while True:
            ret, img = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                id_, confidence = clf.predict(roi_gray)

                if confidence < 50:  # Confidence threshold
                    student_id = str(id_)
                    confidence_text = f"{round(100 - confidence)}%"

                    # Fetch student details from the database
                    student_name = student_data.get(student_id, {}).get("name", "Unknown")
                    department = student_data.get(student_id, {}).get("department", "Unknown")

                    # Draw a green rectangle around the face
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Display ID, Name, Department, and Confidence
                    cv2.putText(img, f"ID: {student_id}", (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(img, f"Name: {student_name}", (x, y-35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(img, f"Dept: {department}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(img, f"Confidence: {confidence_text}", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    # Draw a red rectangle for unknown faces
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1) == 13:  # Enter key to stop
                break

        cap.release()
        cv2.destroyAllWindows()

    def open_main_page(self):
        from main import Face_Recognition_System
        main_window = Toplevel()
        Face_Recognition_System(main_window)

if __name__ == "__main__":
    root = Tk()
    app = FaceRecognition(root)
    root.mainloop()




