import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import get_connection
from hoadon import in_hoa_don
import pyodbc

class Users:
    def __init__(self, parent, user_login):
        self.hoa_don = {}
        self.user_login = user_login
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("User")
        self.win.geometry("550x300")
        self.win.resizable(False, False)
        self.build_ui()

    def build_ui(self):
        frame_searchbox = tk.Frame(self.win)
        frame_searchbox.pack(pady=5)
        self.search_bar = tk.Entry(frame_searchbox, width=50)
        self.search_bar.grid(row=0, column=0, padx=5)
        tk.Button(frame_searchbox, text="Search", bg="gray", command=self.search).grid(row=0, column=1)

        self.tree = ttk.Treeview(self.win, columns=("NameProduct", "ID", "SoLuongTon", "Price", "Quantity"), show="headings")
        self.tree.heading("NameProduct", text="Tên sản phẩm")
        self.tree.heading("ID", text="Mã Sản Phẩm")
        self.tree.heading("SoLuongTon", text="Tồn kho")
        self.tree.heading("Quantity", text="Số Lượng")
        self.tree.heading("Price", text="Đơn giá")

        self.tree.column("NameProduct", width=185, anchor="center")
        self.tree.column("ID", width=95, anchor="center")
        self.tree.column("SoLuongTon", width=75, anchor="center")
        self.tree.column("Price", width=120, anchor="center")
        self.tree.column("Quantity", width=75, anchor="center")

        self.tree.pack()
        self.load_data()

        frame_button = tk.Frame(self.win)
        frame_button.pack(pady=5)
        tk.Button(frame_button, text="+", width=10, bg="#7f8c8d", fg="white", font=("Times New Roman", 9, "bold"), command=self.mua_Sp).pack(side="left", padx=10)
        self.sub = tk.Button(frame_button, text="-", width=10, bg="#7f8c8d", fg="white", font=("Times New Roman", 9, "bold"), command=self.khong_mua)
        self.sub.pack(side="left", padx=10)
        tk.Button(frame_button, text="Mua", width=10, bg="#27ae60", fg="white", font=("Times New Roman", 9, "bold"), command=self.mua).pack(side="left", padx=10)
        tk.Button(frame_button, text="Xuất Hóa Đơn", width=10, bg="#555555", fg="white", font=("Times New Roman", 9, "bold"), command=self.xuat_hd).pack(side="left", padx=10)
        tk.Button(frame_button, text="Đăng Xuất", width=10, bg="red", fg="white", font=("Times New Roman", 9, "bold"), command=self.logout).pack(side="left", padx=10)
        # tk.Button(frame_button, text="LOAD", width=9, bg="red", fg="white", font=("Times New Roman", 8, "bold"), command=self.load_data).pack(side="left", padx=10)


    def load_data(self, request=None):
        conn = get_connection()
        cursor = conn.cursor()
        for i in self.tree.get_children():
            self.tree.delete(i)
        cursor.execute("Select Ten_SP, Ma_SP, So_Luong_Ton, Gia_Ban from dbo.Products")
        rows = cursor.fetchall()
        for i in rows:
            self.tree.insert("", "end", values=(*i, 0))

    def logout(self):
        self.win.destroy()
        self.parent.deiconify()

    def check(self, request=None):
        select = self.tree.selection()
        temp_data = int(self.tree.set(select[0], "Quantity"))
        if temp_data <= 0:
            self.sub.config(state="disabled")
        else:
            self.sub.config(state="normal")

    def mua_Sp(self):
        select = self.tree.selection()
        if not select:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm")
            return
        data = select[0]
        temp_data = self.tree.set(data, "Quantity")
        new_data = int(temp_data) + 1
        self.tree.set(data, "Quantity", new_data)
        self.check()
        full_data = self.tree.item(data)['values']
        ten_sp = full_data[0]
        ma_sp = full_data[1]
        don_gia = full_data[3]
        if ma_sp in self.hoa_don:
            self.hoa_don[ma_sp]["Quantity"] += 1
        else:
            self.hoa_don[ma_sp] = {
                "Name" : ten_sp,
                "Price" : don_gia,
                "Quantity" : 1
            }
    
    def khong_mua(self):
        select = self.tree.selection()
        if not select:
            messagebox.showerror("Lỗi", "vui lòng chọn sản phẩm")
            return
        data = select[0]
        temp_data = self.tree.set(data, "Quantity")
        new_data = int(temp_data) - 1
        if new_data >= 0:
            self.tree.set(data, "Quantity", new_data)
        self.check()
        full_data = self.tree.item(data)['values']
        ma_sp = full_data[1]
        if ma_sp in self.hoa_don:
            self.hoa_don[ma_sp]["Quantity"] -= 1
            if self.hoa_don[ma_sp]["Quantity"] <= 0:
                del self.hoa_don[ma_sp]

    def search(self):
        conn = get_connection()
        cursor = conn.cursor()
        for i in self.tree.get_children():
            self.tree.delete(i)
        sql_search = "Select Ten_SP, Ma_SP, So_Luong_Ton, Gia_Ban from dbo.Products Where Ten_SP like N'?%'"
        cursor.execute(sql_search.replace('?', self.search_bar.get()))
        rows = cursor.fetchall()
        for i in rows:
            self.tree.insert("", "end", values=(*i, 0))

    def mua(self):
        if not self.hoa_don:
            messagebox.showerror("Lỗi", "Chưa có sản phẩm nào trong hóa đơn")
        else:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                for ma_sp , sp in self.hoa_don.items():
                    so_luong = sp["Quantity"]
                    sql_update = "UPDATE Products SET So_Luong_Ton = So_Luong_Ton - ? WHERE Ma_SP = ? AND So_Luong_Ton >= ?"
                    cursor.execute(sql_update, (so_luong, ma_sp, so_luong))
                    if cursor.rowcount == 0:
                        conn.rollback()
                        messagebox.showerror("Lỗi", "Số lượng tồn kho không đủ")
                        self.hoa_don.clear()
                        self.load_data()
                        return    

                SQL_ID = "Select Ma_KH from Customers where Username=?"
                cursor.execute(SQL_ID, (self.user_login, ))
                row = cursor.fetchone()
                if not row:
                    messagebox.showerror("Lỗi", "Không tìm thấy khách hàng")
                    return
                ma_kh = row[0]
                sql_oder = "INSERT INTO DBO.Orders(Ma_KH) VALUES (?)" 
                cursor.execute(sql_oder, (ma_kh, )) 
                conn.commit()
                messagebox.showinfo("Thanh Toán", "Vui lòng xuất hóa đơn để thanh toán")
            except pyodbc.IntegrityError:
                if conn:
                    conn.rollback()
                    messagebox.showerror("Lỗi")
            finally:
                if conn: 
                    conn.close()
        self.load_data()       


    def xuat_hd(self):
        if not self.hoa_don:
            messagebox.showwarning("Thông báo", "Chưa có sản phẩm nào để xuất hóa đơn!")
            return
        in_hoa_don(self.win, data=self.hoa_don, user_n=self.user_login)
        self.load_data()
        self.sub.config("Disabled")