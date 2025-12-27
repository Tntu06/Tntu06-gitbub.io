import tkinter as tk
from tkinter import messagebox
from database import get_connection
from signup import Signup
from admin_view import AdminWindow
from user_view import Users

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x180")
        self.root.resizable(False, False)
        self.build_form()
    
    def build_form(self):
        frame_header = tk.Frame(self.root)
        frame_header.pack(pady=10)
        tk.Label(frame_header, text="Quản Lý Bán Hàng", font=("Times New Roman", 12, "bold")).pack()

        frame_form = tk.Frame(self.root)
        frame_form.pack(padx=20, pady=10)
        tk.Label(frame_form, text="Username").grid(row=0, column=0, sticky="w", pady=5)
        self.user = tk.Entry(frame_form, width=20)
        self.user.grid(row=0, column=1, pady=5)
        tk.Label(frame_form, text="Password").grid(row=1, column=0, sticky="w", pady=5)
        self.password = tk.Entry(frame_form, show="*", width=20)
        self.password.grid(row=1, column=1, pady=5)

        frame_action = tk.Frame(self.root)
        frame_action.pack(pady=10)
        tk.Button(frame_action, text="Sign Up", command=self.open_signup).pack(side="left", padx=5)
        tk.Button(frame_action, text="Login", command=self.check).pack(side="left", padx=5)

    def check(self):
        conn = get_connection()
        cursor = conn.cursor()
        user_name = self.user.get()
        cursor.execute("SELECT Roles FROM Users WHERE Username=? AND Pass=?",(self.user.get(), self.password.get()))

        data = cursor.fetchone()
        conn.close()

        if not data:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")
            return

        if data[0] == 0:
            self.root.withdraw()
            AdminWindow(self.root)
        else:
            self.root.withdraw()
            Users(self.root, user_name)

    def open_signup(self):
        self.root.withdraw()
        Signup(self.root)