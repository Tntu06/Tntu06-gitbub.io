import tkinter as tk
from tkinter import messagebox
from database import get_connection
import pyodbc

class Signup:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Sign Up")
        self.win.geometry("300x250")
        self.build_ui()

    def build_ui(self):
        frame_header = tk.Frame(self.win)
        frame_header.pack(pady=10)
        tk.Label(frame_header, text="Create New Account", font=("Times New Roman", 12, "bold")).pack()

        frame_form = tk.Frame(self.win)
        frame_form.pack(padx=5)
        tk.Label(frame_form, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.new_user = tk.Entry(frame_form, width=20)
        self.new_user.grid(row=0, column=1, pady=5)

        tk.Label(frame_form, text="Password").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.new_pass = tk.Entry(frame_form, show="*", width=20)
        self.new_pass.grid(row=1, column=1, pady=2)

        tk.Label(frame_form, text="Password again").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.again_pass = tk.Entry(frame_form, show="*", width=20)
        self.again_pass.grid(row=2, column=1, pady=2)

        tk.Label(frame_form, text="Full Name").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.full_name = tk.Entry(frame_form, width=20)
        self.full_name.grid(row=3, column=1, pady=2)

        tk.Label(frame_form, text="Address").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.adr = tk.Entry(frame_form, width=20)
        self.adr.grid(row=4, column=1, pady=2)

        tk.Label(frame_form, text="TelePhone").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.telephone = tk.Entry(frame_form, width=20)
        self.telephone.grid(row=5, column=1, pady=2)

        frame_action = tk.Frame(self.win)
        frame_action.pack()
        tk.Button(frame_action, text="Create", command=self.insert_data, bg="gray", width=10).pack(side="left", padx=10, pady=5)
        tk.Button(frame_action, text="Cancel", command=self.cancel, bg="red", width=10).pack(side="left", padx=10, pady=5)

    
    def insert_data(self):
        self.username = self.new_user.get()
        self.password = self.new_pass.get()
        self.password_again = self.again_pass.get()
        self.fname = self.full_name.get()
        self.address = self.adr.get()
        self.phone = self.telephone.get()
     
        if not self.username or not self.password or not self.password_again or not self.fname or not self.address or not self.phone:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đủ thông tin")
            return
        if self.password_again != self.password:
            messagebox.showwarning("Lỗi", "Password nhập lại bị sai")
            return

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql_user = "INSERT INTO DBO.Users(Username, Pass, Roles) VALUES (?, ?, 1)"
            cursor.execute(sql_user, (self.username, self.password))

            sql_cust = "INSERT INTO Customers (Ten_KH, SDT, Dia_Chi, Username) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_cust, ( self.fname, self.phone, self.address, self.username))

            conn.commit()
            messagebox.showinfo("Thành công", "Tạo tài khoản thành công!")
            self.win.destroy()
            self.parent.deiconify()

        except pyodbc.IntegrityError:
            if conn:
                conn.rollback()
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại hoặc lỗi dữ liệu!")
        except Exception as e:
            if conn: 
                conn.rollback()
            messagebox.showerror("Lỗi hệ thống", f"Chi tiết : {e}")
        finally:
            if conn: 
                conn.close()

    def cancel(self):
        self.win.destroy()
        self.parent.deiconify()

