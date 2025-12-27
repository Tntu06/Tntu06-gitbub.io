import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import get_connection
import pyodbc
from popup import Popup


class AdminWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Admin")
        self.win.resizable(False, False)
        self.win.geometry("450x300")
        self.build_ui()

    def build_ui(self):
        self.tree = ttk.Treeview(self.win,columns=("NameProduct", "ID", "Quantity", "Price"),show="headings")
        
        self.tree.heading("NameProduct", text="Tên Sản Phẩm") 
        self.tree.heading("ID", text="Mã SP") 
        self.tree.heading("Quantity", text="Số Lượng") 
        self.tree.heading("Price", text="Giá tiền") 
 
        self.tree.column("NameProduct", width=200, anchor="center") 
        self.tree.column("ID", width=70, anchor="center") 
        self.tree.column("Quantity", width=80, anchor="center")
        self.tree.column("Price", width=110, anchor="center") 

        self.tree.pack()
        self.load_data()

        frame_action = tk.Frame(self.win)
        frame_action.pack(pady=15)

        tk.Button(frame_action, text="Check Hóa Đơn", bg="#7f8c8d", fg="white", font=("Times New Roman", 9, "bold")).pack(side="left", padx=5) 
        tk.Button(frame_action, text="Thêm SP", bg="#7f8c8d", fg="white", font=("Times New Roman", 9, "bold"), command=self.insert_data).pack(side="left", padx=5) 
        tk.Button(frame_action, text="Xóa SP", bg="#7f8c8d", fg="white", font=("Times New Roman", 9, "bold"), command=self.delete_data).pack(side="left", padx=5) 
        tk.Button(frame_action, text="Chỉnh Sửa SP", bg="#7f8c8d", fg="white", font=("Times New Roman", 9, "bold"), command=self.update_data).pack(side="left", padx=5) 
        tk.Button(frame_action, text="Load", bg="#7f8c8d", fg="white", font=("Times New Roman", 9, "bold"), command=self.load_data).pack(side="left", padx=5)
        tk.Button(frame_action, text="Đăng Xuất", bg="red", fg="white", font=("Times New Roman", 9, "bold"),command=self.logout).pack(side="left", padx=5) 

    def logout(self):
        self.win.destroy()
        self.parent.deiconify()
    
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("Select Ten_SP, Ma_SP, So_Luong_Ton, Gia_Ban from dbo.Products")
        row = cursor.fetchall()
        for i in row:
            self.tree.insert("", "end", values=list(i))
        conn.close()

    def delete_data(self):
        self.selection_item = self.tree.selection()
        if self.selection_item:
            self.item_id = self.selection_item[0]
            self.item_info = self.tree.item(self.item_id)
            self.full_data = self.item_info['values']
        self.dlt = self.full_data[1]
        for item in self.selection_item:
            self.tree.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        sql_delete = "Delete from dbo.Products where Ma_Sp = ?"
        cursor.execute(sql_delete, (self.dlt, ))
        conn.commit()
        messagebox.showinfo("Thông báo", "Xóa thành công")
    
    def insert_data(self):
        popup = Popup(self.win)
        self.win.wait_window(popup.win)
        if popup.data:
            get_id, get_name, get_price, get_quantity = popup.data

            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()

                sql_insert = "INSERT INTO dbo.Products(Ma_SP, Ten_SP, Gia_Ban, So_Luong_Ton) Values (?, ?, ?, ?)"
                cursor.execute(sql_insert, (get_id, get_name, get_price, get_quantity))
                conn.commit()
                messagebox.showinfo("Thông báo", "Add thành công, vui lòng Load lại")
            except pyodbc.IntegrityError:
                if conn:
                    conn.rollback()
                    messagebox.showerror("Lỗi", "Mã sp đã tồn tại")
            finally:
                if conn:
                    conn.close()

    def update_data(self):
        select_item = self.tree.selection()
        if not select_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn sản phẩm")
            return
        temp_values = self.tree.item(select_item[0])['values']
        main_id = temp_values[1]
        popup = Popup(self.win, datas=temp_values)
        self.win.wait_window(popup.win)
        if popup.data:
            get_id, get_name, get_price, get_quantity = popup.data

            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()

                sql_update = "Update dbo.Products set Ma_SP=?, Ten_SP=?, Gia_Ban=?, So_Luong_Ton=? where Ma_SP=?"
                cursor.execute(sql_update, (get_id, get_name, get_price, get_quantity, main_id))
                conn.commit()
                messagebox.showinfo("Thông báo", "Chỉnh sửa thành công, vui lòng Load lại")
            except pyodbc.IntegrityError:
                if conn:
                    conn.rollback()
                    messagebox.showerror("Lỗi")
            finally:
                if conn:
                    conn.close()



