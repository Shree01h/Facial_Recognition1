from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Ensure Pillow is installed
import mysql.connector 
import cv2
import os

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700+0+0")  # Adjusted window size
        self.root.title("Student Management System")

        # Variables
        self.var_Department = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_Student_id = StringVar()
        self.var_Name = StringVar()
        self.var_roll = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_photosample = StringVar(value="No")  # Default value for no photo sample
        self.var_dob = StringVar()  # Date of Birth
        self.var_gender = StringVar()  # Gender

        # Load images
        self.load_images()

        # Title label
        title_lbl = Label(self.bg_img, text="Student Management System", font=("times new roman", 25, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1200, height=40)

        # Main frame
        main_frame = Frame(self.bg_img, bd=2)
        main_frame.place(x=5, y=50, width=1180, height=540)

        # Left Frame (Student Details)
        left_frame = LabelFrame(main_frame, bg="white", bd=2, relief=RIDGE, text="Student Details", font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=580, height=520)

        # Current course
        self.create_current_course_frame(left_frame)

        # Student Information
        self.create_student_info_frame(left_frame)

        # Right Frame
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Information", font=("times new roman", 12, "bold"))
        right_frame.place(x=600, y=10, width=570, height=520)

        # Search System Frame
        self.create_search_system_frame(right_frame)

        # Table Frame for Student Data
        self.create_table_frame(right_frame)

        # Fetch data to populate the table
        self.fetch_data()

    def load_images(self):
        # Load images
        img = Image.open(r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\student details 2nd.jpg")
        img = img.resize((400, 100), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=400, height=100)

        img1 = Image.open(r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\student details 2nd.jpg")
        img1 = img1.resize((400, 100), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=400, y=0, width=400, height=100)

        img2 = Image.open(r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\student details 2nd.jpg")
        img2 = img2.resize((400, 100), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=800, y=0, width=400, height=100)

        img_bg = Image.open(r"C:\Users\Yashwini Raghavendra\OneDrive\Desktop\face_recognition\images\i1.jpg")
        img_bg = img_bg.resize((1200, 600), Image.Resampling.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)
        self.bg_img = Label(self.root, image=self.photoimg_bg)
        self.bg_img.place(x=0, y=100, width=1200, height=600)

    def create_current_course_frame(self, left_frame):
        current_course_frame = LabelFrame(left_frame, bg="white", bd=2, relief=RIDGE, text="Current Course", font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=10, width=560, height=130)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 12, "bold"))
        dep_label.grid(row=0, column=0)
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_Department, font=("times new roman", 12, "bold"), state="readonly")
        dep_combo["values"] = ("Select Department", "Computer", "IT", "Civil", "Mechanical")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Course
        course_label = Label(current_course_frame, text="Course", font=("times new roman", 12, "bold"))
        course_label.grid(row=0, column=2)
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=("times new roman", 12, "bold"), state="readonly")
        course_combo["values"] = ("Select Course", "B.Tech", "M.Tech", "B.Sc", "M.Sc")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # Year
        year_label = Label(current_course_frame, text="Year", font=("times new roman", 12, "bold"))
        year_label.grid(row=1, column=0)
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("times new roman", 12, "bold"), state="readonly")
        year_combo["values"] = ("Select Year", "First", "Second", "Third", "Fourth")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester
        sem_label = Label(current_course_frame, text="Semester", font=("times new roman", 12, "bold"))
        sem_label.grid(row=1, column=2)
        sem_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("times new roman", 12, "bold"), state="readonly")
        sem_combo["values"] = ("Select Semester", "Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7", "Sem 8")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

    def create_student_info_frame(self, left_frame):
        class_student_frame = LabelFrame(left_frame, bg="white", bd=2, relief=RIDGE, text="Class Student Info", font=("times new roman", 12, "bold"))
        class_student_frame.place(x=5, y=140, width=560, height=300)

        # Row 0: Student ID and Phone No
        studentID_label = Label(class_student_frame, text="Student ID:", font=("times new roman", 13, "bold"))
        studentID_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        studentID_entry = ttk.Entry(class_student_frame, textvariable=self.var_Student_id, width=10, font=("times new roman", 13, "bold"))
        studentID_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        phone_label = Label(class_student_frame, text="Phone No:", font=("times new roman", 13, "bold"))
        phone_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        phone_entry = ttk.Entry(class_student_frame, textvariable=self.var_phone, width=10, font=("times new roman", 13, "bold"))
        phone_entry.grid(row=0, column=3, padx=5, pady=5, sticky=W, columnspan=2)

        # Row 1: Student Name and Address
        studentName_label = Label(class_student_frame, text="Student Name:", font=("times new roman", 13, "bold"))
        studentName_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        studentName_entry = ttk.Entry(class_student_frame, textvariable=self.var_Name, width=10, font=("times new roman", 13, "bold"))
        studentName_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        address_label = Label(class_student_frame, text="Address:", font=("times new roman", 13, "bold"))
        address_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        address_entry = ttk.Entry(class_student_frame, textvariable=self.var_address, width=10, font=("times new roman", 13, "bold"))
        address_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W, columnspan=2)

        # Row 2: Roll No and Email
        rollNo_label = Label(class_student_frame, text="Roll No:", font=("times new roman", 13, "bold"))
        rollNo_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        rollNo_entry = ttk.Entry(class_student_frame, textvariable=self.var_roll, width=10, font=("times new roman", 13, "bold"))
        rollNo_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        email_label = Label(class_student_frame, text="Email:", font=("times new roman", 13, "bold"))
        email_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        email_entry = ttk.Entry(class_student_frame, textvariable=self.var_email, width=10, font=("times new roman", 13, "bold"))
        email_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W, columnspan=2)

        # Row 3: Date of Birth and Gender
        dob_label = Label(class_student_frame, text="Date of Birth:", font=("times new roman", 13, "bold"))
        dob_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        dob_entry = ttk.Entry(class_student_frame, textvariable=self.var_dob, width=10, font=("times new roman", 13, "bold"))
        dob_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        gender_label = Label(class_student_frame, text="Gender:", font=("times new roman", 13, "bold"))
        gender_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, font=("times new roman", 12, "bold"), state="readonly", width=10)
        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Row 4: Photo Sample Radio Buttons
        radiobtn1 = ttk.Radiobutton(class_student_frame, variable=self.var_photosample, text="Take Photo Sample", value="Yes")
        radiobtn1.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        radiobtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_photosample, text="No Photo Sample", value="No")
        radiobtn2.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # Take Photo and Update Photo Buttons
        take_photo_btn = Button(class_student_frame, command=self.generate_dataset, text="Take Photo", width=15, font=("times new roman", 12), bg="blue", fg="white")
        take_photo_btn.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        update_photo_btn = Button(class_student_frame, text="Update Photo", width=15, font=("times new roman", 12), bg="blue", fg="white")
        update_photo_btn.grid(row=5, column=1, padx=5, pady=5, sticky=W)

        # Button Frame
        btn_frame = Frame(class_student_frame, bg="white", bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=220, width=550, height=50)

        save_btn = Button(btn_frame, text="Save", command=self.add_data, width=12, font=("times new roman", 12), bg="blue", fg="white")
        save_btn.grid(row=0, column=0, padx=5, pady=5)

        update_btn = Button(btn_frame, text="Update", command=self.update_data, width=12, font=("times new roman", 12), bg="blue", fg="white")
        update_btn.grid(row=0, column=1, padx=5, pady=5)

        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, width=12, font=("times new roman", 12), bg="blue", fg="white")
        delete_btn.grid(row=0, column=2, padx=5, pady=5)

        reset_btn = Button(btn_frame, text="Reset", command=self.reset_fields, width=12, font=("times new roman", 12), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3, padx=5, pady=5)

    def create_search_system_frame(self, right_frame):
        search_frame = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE, text="Search System", font=("times new roman", 12, "bold"))
        search_frame.place(x=5, y=10, width=550, height=70)

        # Search Label
        search_label = Label(search_frame, text="Search By:", font=("times new roman", 13, "bold"), bg="yellow", fg="black")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        # Search Dropdown
        search_combo = ttk.Combobox(search_frame, font=("times new roman", 12, "bold"), state="readonly", width=15)
        search_combo["values"] = ("Select", "Roll No", "Phone No", "Student ID")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Search Entry Field
        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman", 13, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        # Search and Show All Buttons
        search_btn = Button(search_frame, text="Search", width=12, font=("times new roman", 12), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=5, pady=5)

        showAll_btn = Button(search_frame, text="Show All", width=12, font=("times new roman", 12), bg="blue", fg="white")
        showAll_btn.grid(row=0, column=4, padx=5, pady=5)

    def create_table_frame(self, right_frame):
        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=90, width=550, height=300)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # Student Table
        self.student_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Dep", "Course", "Year", "Sem", "Roll No", "email", "Phone", "Address", "Photo Sample", "DOB", "Gender"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        # Configure Scrollbars
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Pack Scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Table Headings
        self.student_table.heading("Dep", text="Department")
        self.student_table.heading("Course", text="Course")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("Sem", text="Semester")
        self.student_table.heading("ID", text="Student ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Roll No", text="Roll No")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("Address", text="Address")
        self.student_table.heading("Phone", text="Phone No")
        self.student_table.heading("Photo Sample", text="Photo Sample")
        self.student_table.heading("DOB", text="Date of Birth")
        self.student_table.heading("Gender", text="Gender")

        # Column Widths
        column_width = 80
        for col in ("ID", "Name", "Dep", "Course", "Year", "Sem", "Roll No", "email", "Phone", "Address", "Photo Sample", "DOB", "Gender"):
            self.student_table.column(col, width=column_width)

        # Pack Table after Scrollbars
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="yashwinir@2005",
                database="face_recog"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student")
            rows = cursor.fetchall()
            if len(rows) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert('', 'end', values=row)
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

    def add_data(self):
        if self.var_Student_id.get() == "" or self.var_Name.get() == "" or self.var_email.get() == "" or self.var_dob.get() == "" or self.var_gender.get() == "Select Gender":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="yashwinir@2005",
                database="face_recog"
            )
            cursor = conn.cursor()

            query = "INSERT INTO student (Student_id, Name, Department, course, year, semester, roll, phone, email, address, photosample, dob, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
                self.var_Student_id.get(),
                self.var_Name.get(),
                self.var_Department.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_roll.get(),
                self.var_phone.get(),
                self.var_email.get(),
                self.var_address.get(),
                self.var_photosample.get(),
                self.var_dob.get(),
                self.var_gender.get()
            )
            cursor.execute(query, values)
            conn.commit()
            self.fetch_data()  # Refresh the table data
            self.reset_fields()  # Reset fields after adding data
            conn.close()

            messagebox.showinfo("Success", "Student details have been added successfully", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        self.var_Student_id.set(data[0])
        self.var_Name.set(data[1])
        self.var_Department.set(data[2])
        self.var_course.set(data[3])
        self.var_year.set(data[4])
        self.var_semester.set(data[5])
        self.var_roll.set(data[6])
        self.var_phone.set(data[7])
        self.var_email.set(data[8])
        self.var_address.set(data[9])
        self.var_photosample.set(data[10])
        self.var_dob.set(data[11])
        self.var_gender.set(data[12])

    def update_data(self):
        if self.var_Department.get() == "Select Department" or self.var_course.get() == "" or self.var_Student_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        current_data = content["values"]

        if (self.var_Student_id.get() == current_data[0] and
            self.var_Name.get() == current_data[1] and
            self.var_Department.get() == current_data[2] and
            self.var_course.get() == current_data[3] and
            self.var_year.get() == current_data[4] and
            self.var_semester.get() == current_data[5] and
            self.var_roll.get() == current_data[6] and
            self.var_phone.get() == current_data[7] and
            self.var_email.get() == current_data[8] and
            self.var_address.get() == current_data[9] and
            self.var_photosample.get() == current_data[10] and
            self.var_dob.get() == current_data[11] and
            self.var_gender.get() == current_data[12]):
            
            messagebox.showinfo("Info", "No changes made to update.", parent=self.root)
            return

        update = messagebox.askyesno("Update", "Do you want to update this student details?", parent=self.root)
        if update:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="yashwinir@2005",
                    database="face_recog"
                )
                cursor = conn.cursor()
                cursor.execute("UPDATE student SET Department=%s, course=%s, roll=%s, email=%s, phone=%s, address=%s, year=%s, semester=%s, photosample=%s, dob=%s, gender=%s WHERE Student_id=%s",
                               (
                                   self.var_Department.get(),
                                   self.var_course.get(),
                                   self.var_roll.get(),
                                   self.var_email.get(),
                                   self.var_phone.get(),
                                   self.var_address.get(),
                                   self.var_year.get(),
                                   self.var_semester.get(),
                                   self.var_photosample.get(),
                                   self.var_dob.get(),
                                   self.var_gender.get(),
                                   self.var_Student_id.get()
                               ))
                conn.commit()
                self.fetch_data()  # Refresh the table data
                self.reset_fields()  # Reset fields after updating data
                conn.close()
                messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

    def delete_data(self):
        if self.var_Student_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required", parent=self.root)
            return

        delete = messagebox.askyesno("Delete", "Do you want to delete this student record?", parent=self.root)
        if delete:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="yashwinir@2005",
                    database="face_recog"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM student WHERE Student_id=%s", (self.var_Student_id.get(),))
                conn.commit()
                self.fetch_data()  # Refresh the table data
                self.reset_fields()  # Reset fields after deleting data
                conn.close()
                messagebox.showinfo("Success", "Student record deleted successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

    def reset_fields(self):
        self.var_Department.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_Student_id.set("")
        self.var_Name.set("")
        self.var_roll.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_photosample.set("No")
        self.var_dob.set("")
        self.var_gender.set("Select Gender")

    def generate_dataset(self):
        if self.var_Department.get() == "Select Department" or self.var_course.get() == "" or self.var_Student_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="yashwinir@2005",
                database="face_recog"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * from student")
            myresult = cursor.fetchall()
            id = len(myresult) + 1  # Get the next ID for the new student

            # Start capturing images
            cap = cv2.VideoCapture(0)
            img_id = 0

            while True:
                ret, my_frame = cap.read()
                if self.face_cropped(my_frame) is not None:
                    img_id += 1
                    face = cv2.resize(self.face_cropped(my_frame), (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"data/user.{id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face) 
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2) 
                    cv2.imshow("Cropped Face", face)

                if cv2.waitKey(1) == 13 or int(img_id) == 100:
                    break      

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Generating data sets completed!!")

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    @staticmethod
    def face_cropped(img):
        face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_cropped = img[y:y+h, x:x+w]
            return face_cropped

if __name__ == "__main__":  # This should be outside the class
    root = Tk()
    obj = Student(root)
    root.mainloop()
