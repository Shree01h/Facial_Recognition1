from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from main import Face_Recognition_System  # Import your main application class

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1550x800+0+0")
        
        # Background Image
        self.bg = ImageTk.PhotoImage(file=r"images\login_bg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Login Frame
        frame = Frame(self.root, bg="white")
        frame.place(x=610, y=170, width=340, height=450)
        
        # Title
        title = Label(frame, text="LOGIN HERE", font=("Impact", 35, "bold"), fg="#d77337", bg="white")
        title.place(x=50, y=30)
        
        # Username
        lbl_user = Label(frame, text="Username", font=("Goudy old style", 15, "bold"), fg="gray", bg="white")
        lbl_user.place(x=50, y=120)
        self.txt_user = Entry(frame, font=("times new roman", 15), bg="lightgray")
        self.txt_user.place(x=50, y=150, width=250, height=35)
        
        # Password
        lbl_pass = Label(frame, text="Password", font=("Goudy old style", 15, "bold"), fg="gray", bg="white")
        lbl_pass.place(x=50, y=210)
        self.txt_pass = Entry(frame, font=("times new roman", 15), show="*", bg="lightgray")
        self.txt_pass.place(x=50, y=240, width=250, height=35)
        
        # Login Button
        login_btn = Button(frame, text="Login", command=self.login, 
                         fg="white", bg="#d77337", font=("times new roman", 20))
        login_btn.place(x=50, y=320, width=250, height=40)
        
        # Register Button
        register_btn = Button(frame, text="Register New Account", command=self.register_window,
                            font=("times new roman", 10), bg="white", bd=0, fg="#d77337")
        register_btn.place(x=50, y=380)
        
        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#1heymysql",
            database="face_recog"
        )
        self.cursor = self.conn.cursor()
    
    def login(self):
        username = self.txt_user.get()
        password = self.txt_pass.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            self.cursor.execute(query, (username, password))
            row = self.cursor.fetchone()

            if row:
                messagebox.showinfo("Success", f"Welcome {row[1]}!", parent=self.root)
                self.root.destroy()
                from main import Face_Recognition_System
                root = Tk()
                Face_Recognition_System(root)
                root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}", parent=self.root)
    
    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Register")
        self.new_window.geometry("400x450")
        
        # Registration Form
        frame = Frame(self.new_window, bg="white")
        frame.place(x=50, y=50, width=300, height=350)
        
        title = Label(frame, text="REGISTER", font=("Impact", 25, "bold"), fg="#d77337", bg="white")
        title.place(x=90, y=30)
        
        # Full Name
        lbl_name = Label(frame, text="Full Name", font=("Goudy old style", 15), fg="gray", bg="white")
        lbl_name.place(x=30, y=90)
        self.reg_name = Entry(frame, font=("times new roman", 15), bg="lightgray")
        self.reg_name.place(x=30, y=120, width=240, height=30)
        
        # Username
        lbl_user = Label(frame, text="Username", font=("Goudy old style", 15), fg="gray", bg="white")
        lbl_user.place(x=30, y=160)
        self.reg_user = Entry(frame, font=("times new roman", 15), bg="lightgray")
        self.reg_user.place(x=30, y=190, width=240, height=30)
        
        # Password
        lbl_pass = Label(frame, text="Password", font=("Goudy old style", 15), fg="gray", bg="white")
        lbl_pass.place(x=30, y=230)
        self.reg_pass = Entry(frame, font=("times new roman", 15), show="*", bg="lightgray")
        self.reg_pass.place(x=30, y=260, width=240, height=30)
        
        # Register Button
        btn_register = Button(frame, text="Register", command=self.register,
                            fg="white", bg="#d77337", font=("times new roman", 15))
        btn_register.place(x=30, y=300, width=240, height=35)
    
    def register(self):
        if self.reg_name.get() == "" or self.reg_user.get() == "" or self.reg_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.new_window)
            return

        try:
            query = "SELECT * FROM users WHERE username=%s"
            self.cursor.execute(query, (self.reg_user.get(),))
            row = self.cursor.fetchone()

            if row:
                messagebox.showerror("Error", "Username already exists", parent=self.new_window)
            else:
                query = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)"
                self.cursor.execute(query, (
                    self.reg_name.get(),
                    self.reg_user.get(),
                    self.reg_pass.get()
                ))
                self.conn.commit()  # Ensure the changes are committed to the database
                messagebox.showinfo("Success", "Registration successful", parent=self.new_window)
                self.new_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}", parent=self.new_window)

if __name__ == "__main__":
    # First create the users table if it doesn't exist
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#1heymysql",
            database="face_recog"
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    
    # Run the login system
    root = Tk()
    obj = Login(root)
    root.mainloop()