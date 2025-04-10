

from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import mysql.connector
import os
import pandas as pd
import cv2

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700+0+0")
        self.root.title("Student Management System")

        # Initialize bg_img first with a default value
        self.bg_img = Label(self.root, bg="lightgray")
        self.bg_img.place(x=0, y=100, width=1200, height=600)

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
        self.var_photosample = StringVar(value="No")
        self.var_dob = StringVar()
        self.var_gender = StringVar()

        # Load images (with error handling)
        self.load_images()

        # Title label
        title_lbl = Label(self.bg_img, text="Student Management System", 
                          font=("times new roman", 25, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1200, height=40)

        # Main frame
        main_frame = Frame(self.bg_img, bd=2)
        main_frame.place(x=5, y=50, width=1180, height=540)

        # Left Frame (Student Details)
        left_frame = LabelFrame(main_frame, bg="white", bd=2, relief=RIDGE, 
                                text="Student Details", font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=580, height=520)

        # Current course
        self.create_current_course_frame(left_frame)

        # Student Information
        self.create_student_info_frame(left_frame)

        # Right Frame
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, 
                                 text="Student Information", font=("times new roman", 12, "bold"))
        right_frame.place(x=600, y=10, width=570, height=520)

        # Search System Frame
        self.create_search_system_frame(right_frame)

        # Table Frame for Student Data
        self.create_table_frame(right_frame)

        # Fetch data to populate the table
        self.fetch_data()

    def load_images(self):
        # Create images directory if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")
        
        # Create default images if they don't exist
        default_images = {
            "student_details.jpg": (400, 100),
            "background.jpg": (1200, 600)
        }
        
        for img_name, size in default_images.items():
            img_path = os.path.join("images", img_name)
            if not os.path.exists(img_path):
                # Create a simple colored image
                img = Image.new("RGB", size, (70, 130, 180))  # Steel blue color
                draw = ImageDraw.Draw(img)
                draw.text((10, 10), img_name, fill=(255, 255, 255))
                img.save(img_path)
        
        try:
            # Load header images
            img = Image.open("images/student_details.jpg")
            img = img.resize((400, 100), Image.Resampling.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            f_lbl = Label(self.root, image=self.photoimg)
            f_lbl.place(x=0, y=0, width=400, height=100)

            img1 = Image.open("images/student_details.jpg")
            img1 = img1.resize((400, 100), Image.Resampling.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img1)
            f_lbl = Label(self.root, image=self.photoimg1)
            f_lbl.place(x=400, y=0, width=400, height=100)

            img2 = Image.open("images/student_details.jpg")
            img2 = img2.resize((400, 100), Image.Resampling.LANCZOS)
            self.photoimg2 = ImageTk.PhotoImage(img2)
            f_lbl = Label(self.root, image=self.photoimg2)
            f_lbl.place(x=800, y=0, width=400, height=100)

            # Load background image
            img_bg = Image.open("images/background.jpg")
            img_bg = img_bg.resize((1200, 600), Image.Resampling.LANCZOS)
            self.photoimg_bg = ImageTk.PhotoImage(img_bg)
            self.bg_img.config(image=self.photoimg_bg)
            
        except Exception as e:
            print(f"Error loading images: {e}")
            # Use default background color if image loading fails
            self.bg_img.config(bg="lightgray")

    def create_current_course_frame(self, left_frame):
        current_course_frame = LabelFrame(left_frame, bg="white", bd=2, relief=RIDGE, 
                                           text="Current Course", font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=10, width=560, height=130)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 12, "bold"))
        dep_label.grid(row=0, column=0)
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_Department, 
                                  font=("times new roman", 12, "bold"), state="readonly")
        dep_combo["values"] = ("Select Department", "Computer", "IT", "Civil", "Mechanical")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Course
        course_label = Label(current_course_frame, text="Course", font=("times new roman", 12, "bold"))
        course_label.grid(row=0, column=2)
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, 
                                     font=("times new roman", 12, "bold"), state="readonly")
        course_combo["values"] = ("Select Course", "B.Tech", "M.Tech", "B.Sc", "M.Sc")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # Year
        year_label = Label(current_course_frame, text="Year", font=("times new roman", 12, "bold"))
        year_label.grid(row=1, column=0)
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, 
                                   font=("times new roman", 12, "bold"), state="readonly")
        year_combo["values"] = ("Select Year", "First", "Second", "Third", "Fourth")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester
        sem_label = Label(current_course_frame, text="Semester", font=("times new roman", 12, "bold"))
        sem_label.grid(row=1, column=2)
        sem_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, 
                                 font=("times new roman", 12, "bold"), state="readonly")
        sem_combo["values"] = ("Select Semester", "Sem 1", "Sem 2", "Sem 3", "Sem 4", 
                               "Sem 5", "Sem 6", "Sem 7", "Sem 8")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

    def create_student_info_frame(self, left_frame):
        class_student_frame = LabelFrame(left_frame, bg="white", bd=2, relief=RIDGE, 
                                          text="Class Student Info", font=("times new roman", 12, "bold"))
        class_student_frame.place(x=5, y=140, width=560, height=300)

        # Student ID
        studentID_label = Label(class_student_frame, text="Student ID:", 
                                 font=("times new roman", 13, "bold"))
        studentID_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        studentID_entry = ttk.Entry(class_student_frame, textvariable=self.var_Student_id, 
                                     width=10, font=("times new roman", 13, "bold"))
        studentID_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Phone No
        phone_label = Label(class_student_frame, text="Phone No:", 
                            font=("times new roman", 13, "bold"))
        phone_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        phone_entry = ttk.Entry(class_student_frame, textvariable=self.var_phone, 
                                 width=10, font=("times new roman", 13, "bold"))
        phone_entry.grid(row=0, column=3, padx=5, pady=5, sticky=W, columnspan=2)

        # Student Name
        studentName_label = Label(class_student_frame, text="Student Name:", 
                                   font=("times new roman", 13, "bold"))
        studentName_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        studentName_entry = ttk.Entry(class_student_frame, textvariable=self.var_Name, 
                                       width=10, font=("times new roman", 13, "bold"))
        studentName_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Address
        address_label = Label(class_student_frame, text="Address:", 
                              font=("times new roman", 13, "bold"))
        address_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        address_entry = ttk.Entry(class_student_frame, textvariable=self.var_address, 
                                   width=10, font=("times new roman", 13, "bold"))
        address_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W, columnspan=2)

        # Roll
        roll_label = Label(class_student_frame, text="Roll:", 
                           font=("times new roman", 13, "bold"))
        roll_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        roll_entry = ttk.Entry(class_student_frame, textvariable=self.var_roll, 
                               width=10, font=("times new roman", 13, "bold"))
        roll_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Email
        email_label = Label(class_student_frame, text="Email:", 
                            font=("times new roman", 13, "bold"))
        email_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        email_entry = ttk.Entry(class_student_frame, textvariable=self.var_email, 
                                 width=10, font=("times new roman", 13, "bold"))
        email_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W, columnspan=2)

        # Date of Birth
        dob_label = Label(class_student_frame, text="Date of Birth:", 
                          font=("times new roman", 13, "bold"))
        dob_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        dob_entry = ttk.Entry(class_student_frame, textvariable=self.var_dob, 
                              width=10, font=("times new roman", 13, "bold"))
        dob_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Gender
        gender_label = Label(class_student_frame, text="Gender:", 
                             font=("times new roman", 13, "bold"))
        gender_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, 
                                     font=("times new roman", 12, "bold"), state="readonly", width=10)
        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Photo Sample Radio Buttons
        radiobtn1 = ttk.Radiobutton(class_student_frame, variable=self.var_photosample, 
                                     text="Take Photo Sample", value="Yes")
        radiobtn1.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        radiobtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_photosample, 
                                     text="No Photo Sample", value="No")
        radiobtn2.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # Buttons
        take_photo_btn = Button(class_student_frame, text="Take Photo", width=15, 
                                font=("times new roman", 12), bg="blue", fg="white", 
                                command=self.generate_dataset)
        take_photo_btn.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        update_photo_btn = Button(class_student_frame, text="Upload Photo", width=15, 
                                  font=("times new roman", 12), bg="blue", fg="white", 
                                  command=self.upload_photo)
        update_photo_btn.grid(row=5, column=1, padx=5, pady=5, sticky=W)

        upload_csv_btn = Button(class_student_frame, text="Upload CSV", width=15, 
                                font=("times new roman", 12), bg="blue", fg="white", 
                                command=self.upload_csv)
        upload_csv_btn.grid(row=5, column=2, padx=5, pady=5, sticky=W)

        # Button Frame
        btn_frame = Frame(class_student_frame, bg="white", bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=220, width=550, height=50)

        save_btn = Button(btn_frame, text="Save", command=self.add_data, width=12, 
                          font=("times new roman", 12), bg="blue", fg="white")
        save_btn.grid(row=0, column=0, padx=5, pady=5)

        update_btn = Button(btn_frame, text="Update", command=self.update_data, width=12, 
                            font=("times new roman", 12), bg="blue", fg="white")
        update_btn.grid(row=0, column=1, padx=5, pady=5)

        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, width=12, 
                            font=("times new roman", 12), bg="blue", fg="white")
        delete_btn.grid(row=0, column=2, padx=5, pady=5)

        reset_btn = Button(btn_frame, text="Reset", command=self.reset_fields, width=12, 
                           font=("times new roman", 12), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3, padx=5, pady=5)

    def upload_photo(self):
        if self.var_Student_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required to upload a photo", parent=self.root)
            return

        file_path = filedialog.askopenfilename(title="Select an Image", 
                                                filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), 
                                                           ("All Files", "*.*")))
        
        if file_path:
            try:
                if not os.path.exists("data"):
                    os.makedirs("data")

                student_id = self.var_Student_id.get()
                # Remove existing single photo if it exists
                single_photo_path = f"data/user.{student_id}.jpg"
                if os.path.exists(single_photo_path):
                    os.remove(single_photo_path)
                
                # Save new photo
                img = Image.open(file_path)
                img = img.resize((450, 450), Image.Resampling.LANCZOS)
                img.save(single_photo_path)
                
                # Update photosample status
                self.var_photosample.set("Yes")
                self.update_data()
                
                messagebox.showinfo("Success", "Photo uploaded successfully!", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload photo: {str(e)}", parent=self.root)

    def create_search_system_frame(self, right_frame):
        search_frame = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE, 
                                  text="Search System", font=("times new roman", 12, "bold"))
        search_frame.place(x=5, y=10, width=550, height=70)

        # Search Label
        search_label = Label(search_frame, text="Search By:", 
                             font=("times new roman", 13, "bold"), bg="yellow", fg="black")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        # Search Dropdown
        search_combo = ttk.Combobox(search_frame, font=("times new roman", 12, "bold"), 
                                     state="readonly", width=15)
        search_combo["values"] = ("Select", "Roll", "Phone No", "Student ID")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Search Entry Field
        search_entry = ttk.Entry(search_frame, width=15, 
                                  font=("times new roman", 13, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        # Search and Show All Buttons
        search_btn = Button(search_frame, text="Search", width=12, 
                            font=("times new roman", 12), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=5, pady=5)

        showAll_btn = Button(search_frame, text="Show All", width=12, 
                             font=("times new roman", 12), bg="blue", fg="white", 
                             command=self.fetch_data)
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
            columns=("ID", "Name", "Dep", "Course", "Year", "Sem", "Roll", "Email", 
                     "Phone", "Address", "Photo Sample", "DOB", "Gender"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.student_table.heading("ID", text="Student ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Dep", text="Department")
        self.student_table.heading("Course", text="Course")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("Sem", text="Semester")
        self.student_table.heading("Roll", text="Roll")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("Phone", text="Phone No")
        self.student_table.heading("Address", text="Address")
        self.student_table.heading("Photo Sample", text="Photo Sample")
        self.student_table.heading("DOB", text="Date of Birth")
        self.student_table.heading("Gender", text="Gender")

        self.student_table["show"] = "headings"
        
        column_width = 80
        for col in ("ID", "Name", "Dep", "Course", "Year", "Sem", "Roll", "Email", 
                    "Phone", "Address", "Photo Sample", "DOB", "Gender"):
            self.student_table.column(col, width=column_width)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="#1heymysql",
                database="face_recog")
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
                port=3307,
                user="root",
                password="#1heymysql",
                database="face_recog"
            )
            cursor = conn.cursor()

            # Check if student ID already exists
            cursor.execute("SELECT * FROM student WHERE Student_id=%s", (self.var_Student_id.get(),))
            existing = cursor.fetchone()
            
            if existing:
                messagebox.showerror("Error", "Student ID already exists", parent=self.root)
                return

            query = """
            INSERT INTO student 
            (Student_id, Name, Department, course, year, semester, Roll, phone, email, address, photosample, dob, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
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
            self.fetch_data()
            self.reset_fields()
            conn.close()

            messagebox.showinfo("Success", "Student details have been added successfully", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        
        if data:
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
        
        try:
            update = messagebox.askyesno("Update", "Do you want to update this student details?", parent=self.root)
            if update:
                conn = mysql.connector.connect(
                    host="localhost",
                    port=3307,
                    user="root",
                    password="#1heymysql",
                    database="face_recog"
                )
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE student SET 
                    Department=%s, course=%s, year=%s, semester=%s, 
                    Roll=%s, phone=%s, email=%s, address=%s, 
                    photosample=%s, dob=%s, gender=%s, Name=%s 
                    WHERE Student_id=%s
                    """, (
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
                        self.var_gender.get(),
                        self.var_Name.get(),
                        self.var_Student_id.get()
                    ))
                conn.commit()
                self.fetch_data()
                self.reset_fields()
                conn.close()
                messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)

    def delete_data(self):
        if self.var_Student_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required", parent=self.root)
            return

        try:
            delete = messagebox.askyesno("Delete", "Do you want to delete this student record?", parent=self.root)
            if delete:
                conn = mysql.connector.connect(
                    host="localhost",
                    port=3307,
                    user="root",
                    password="#1heymysql",
                    database="face_recog"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM student WHERE Student_id=%s", (self.var_Student_id.get(),))
                conn.commit()
                self.fetch_data()
                self.reset_fields()
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
            student_id = self.var_Student_id.get()
            
            # Create data directory if it doesn't exist
            if not os.path.exists("data"):
                os.makedirs("data")
                
            # Remove existing images for this student to prevent duplicates
            for filename in os.listdir("data"):
                if filename.startswith(f"user.{student_id}."):
                    os.remove(os.path.join("data", filename))

            cap = cv2.VideoCapture(0)
            img_id = 0
            face_detected = False

            while True:
                ret, my_frame = cap.read()
                cropped_face = self.face_cropped(my_frame)
                
                if cropped_face is not None:
                    face_detected = True
                    img_id += 1
                    face = cv2.resize(cropped_face, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"data/user.{student_id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Cropped Face", face)

                if cv2.waitKey(1) == 13 or int(img_id) == 100:  # 13 is Enter Key, stop after 100 images
                    break

            cap.release()
            cv2.destroyAllWindows()
            
            if face_detected:
                # Update photosample status in database
                self.var_photosample.set("Yes")
                self.update_data()  # Save the photosample status
                messagebox.showinfo("Result", f"Generated {img_id} images for student ID {student_id}")

                # Navigate to Train Page
                go_to_train = messagebox.askyesno("Navigate to Train Page", "Do you want to go to the Train Page now?", parent=self.root)
                if go_to_train:
                    self.root.destroy()  # Close the current Students Page
                    from train import Train
                    train_window = Toplevel()  # Use Toplevel for the new window
                    Train(train_window)  # Initialize the Train class
            else:
                messagebox.showerror("Error", "No face detected during the session", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    @staticmethod
    def face_cropped(img):
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_cropped = img[y:y+h, x:x+w]
            return face_cropped

    def upload_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

        if not file_path:
            return

        try:
            # Read CSV file
            data = pd.read_csv(file_path)
            
            # Standardize column names
            data.columns = data.columns.str.strip().str.lower().str.replace(' ', '')
            
            # Column name mapping
            column_mapping = {
                'student_id': ['studentid', 'id', 'student_id'],
                'name': ['studentname', 'name'],
                'department': ['dept', 'department'],
                'course': ['program', 'course'],
                'year': ['studyyear', 'year'],
                'semester': ['sem', 'semester'],
                'roll': ['rollno', 'rollnumber', 'roll'],
                'phone': ['phoneno', 'mobile', 'phone'],
                'email': ['emailid', 'email'],
                'address': ['addr', 'address'],
                'photosample': ['photo', 'photosample'],
                'dob': ['dateofbirth', 'birthdate', 'dob'],
                'gender': ['sex', 'gender']
            }
            
            # Rename columns to standard names
            for standard_name, possible_names in column_mapping.items():
                for name in possible_names:
                    if name in data.columns:
                        data.rename(columns={name: standard_name}, inplace=True)
                        break
            
            # Check for required columns
            required_columns = ['student_id', 'name', 'department', 'course', 'year',
                                'semester', 'roll', 'phone', 'email', 'address',
                                'photosample', 'dob', 'gender']
            
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                messagebox.showerror(
                    "Error",
                    f"Missing required columns: {', '.join(missing_columns)}\n"
                    f"Available columns: {', '.join(data.columns)}",
                    parent=self.root)
                return

            # Connect to database
            conn = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="#1heymysql",
                database="face_recog"
            )
            cursor = conn.cursor()

            # Get existing student IDs
            cursor.execute("SELECT Student_id FROM student")
            existing_ids = {str(row[0]) for row in cursor.fetchall()}
            
            # Process data
            new_rows = []
            duplicate_in_csv = set()
            duplicate_in_db = set()
            
            # Check for duplicates in CSV first
            seen_in_csv = set()
            for index, row in data.iterrows():
                student_id = str(row['student_id'])
                if student_id in seen_in_csv:
                    duplicate_in_csv.add(student_id)
                seen_in_csv.add(student_id)
            
            if duplicate_in_csv:
                messagebox.showwarning(
                    "Warning",
                    f"Found {len(duplicate_in_csv)} duplicate Student IDs in CSV: "
                    f"{', '.join(sorted(duplicate_in_csv)[:5])}"
                    f"{'...' if len(duplicate_in_csv) > 5 else ''}",
                    parent=self.root)
                return

            # Process valid rows
            for index, row in data.iterrows():
                student_id = str(row['student_id'])
                
                if student_id in existing_ids:
                    duplicate_in_db.add(student_id)
                    continue
                
                new_rows.append((
                    student_id,
                    str(row['name']),
                    str(row['department']),
                    str(row['course']),
                    str(row['year']),
                    str(row['semester']),
                    str(row['roll']),
                    str(row['phone']),
                    str(row['email']),
                    str(row['address']),
                    str(row.get('photosample', 'No')),
                    str(row['dob']),
                    str(row['gender'])
                ))

            # Handle duplicates
            if duplicate_in_db:
                response = messagebox.askyesno(
                    "Duplicate Entries",
                    f"Found {len(duplicate_in_db)} existing Student IDs in database. "
                    "Would you like to update these records instead?",
                    parent=self.root)
                
                if response:  # User wants to update
                    update_count = 0
                    for index, row in data[data['student_id'].astype(str).isin(duplicate_in_db)].iterrows():
                        try:
                            cursor.execute("""
                                UPDATE student SET 
                                Name=%s, Department=%s, course=%s, year=%s, semester=%s,
                                Roll=%s, phone=%s, email=%s, address=%s,
                                photosample=%s, dob=%s, gender=%s
                                WHERE Student_id=%s
                                """, (
                                str(row['name']),
                                str(row['department']),
                                str(row['course']),
                                str(row['year']),
                                str(row['semester']),
                                str(row['roll']),
                                str(row['phone']),
                                str(row['email']),
                                str(row['address']),
                                str(row.get('photosample', 'No')),
                                str(row['dob']),
                                str(row['gender']),
                                str(row['student_id'])
                            ))
                            update_count += 1
                        except Exception as e:
                            print(f"Error updating record {row['student_id']}: {e}")
                    
                    conn.commit()
                    messagebox.showinfo(
                        "Update Complete",
                        f"Updated {update_count} existing records",
                        parent=self.root)

            # Insert new records
            if new_rows:
                try:
                    cursor.executemany("""
                        INSERT INTO student 
                        (Student_id, Name, Department, course, year, semester, 
                        Roll, phone, email, address, photosample, dob, gender) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, new_rows)
                    conn.commit()
                    messagebox.showinfo(
                        "Success",
                        f"Added {len(new_rows)} new student records",
                        parent=self.root)
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror(
                        "Insert Error",
                        f"Failed to insert new records: {str(e)}",
                        parent=self.root)

            # Refresh data
            self.fetch_data()
            conn.close()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to process CSV: {str(e)}",
                parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()

