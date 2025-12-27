import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import get_connection
import pyodbc

class in_hoa_don:
    def __init__(self, parent, data, user_n):
        #Khởi tạo cửa sổ kèm thuộc tính
        self.parent = parent
        self.data = data
        self.user_n = user_n
        self.win = tk.Toplevel(parent)
        self.win.title("Hóa Đơn")
        self.win.geometry("500x365")
        self.win.resizable(False, False)
        self.build()
    

    def build(self):
        #Xây bảng
        frame_header = tk.Frame(self.win)
        frame_header.pack(pady=5)

        tk.Label(frame_header, text="Hóa Đơn", font=("Times New Roman", 16, "bold"), width=10, fg="white", background="#555555").grid(row=0, column=0)

        tree = ttk.Treeview(self.win, columns=("ID", "NameProduct", "Price", "Quantity", "Total_price"), show="headings")

        tree.heading("ID", text="Mã SP")
        tree.heading("NameProduct", text="Tên sản phẩm")
        tree.heading("Quantity", text="Số Lượng")
        tree.heading("Price", text="Đơn giá")
        tree.heading("Total_price", text="Thành tiền")

        tree.column("ID", width=65, anchor="center")
        tree.column("NameProduct", width=185, anchor="center")
        tree.column("Quantity", width=65, anchor="center")
        tree.column("Price", width=90, anchor="center")
        tree.column("Total_price", width=90, anchor="center")
        tree.pack()
        
        #Load dữ liệu vào hóa đơn
        for i in tree.get_children():
            tree.delete(i)
        for ma_sp, sp in self.data.items():
            ten = sp["Name"]
            gia = sp["Price"]
            sl = sp["Quantity"]
            tree.insert("", "end", values=(ma_sp, ten, gia, sl, gia*sl))
        tong_tien = 0
        for sp in self.data.values():
            tong_tien += sp["Price"] * sp["Quantity"]
        
        #Xây dựng nút bấm các chức năng đi kèm
        frame_total = tk.Frame(self.win)
        frame_total.pack(fill="x", padx=10, pady=5)
        tong_tien_final = tk.StringVar()
        tong_tien_final.set(str(tong_tien)) 
        lock = tk.Entry(frame_total, width=15, font=("Times New Roman", 11, "bold"), textvariable=tong_tien_final)
        lock.pack(side="right")
        lock.config(state="disabled")
        tk.Label(frame_total, text="Tổng tiền", font=("Times New Roman", 11, "bold")).pack(side="right", padx=5)
        frame_button = tk.Frame(self.win)
        frame_button.pack(pady=5)
        tk.Button(frame_button, text="Thanh Toán", width=10, bg="green", fg="white", font=("Times New Roman", 12, "bold"), command=self.pay).pack(side="left", padx=10)
        tk.Button(frame_button, text="Cancel", width=10, bg="red", fg="white", font=("Times New Roman", 12, "bold"), command=self.close_hd).pack(side="left", padx=10)

    def close_hd(self):
        self.data.clear()
        self.win.destroy()
    
    def pay(self):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Ma_KH FROM Customers WHERE Username=?", (self.user_n,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Lỗi", "Không tìm thấy khách hàng")
                return
            ma_kh = row[0]
            cursor.execute("SELECT Ma_DH FROM Orders WHERE Ma_KH=? AND Trang_Thai=N'CHƯA THANH TOÁN'",(ma_kh,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Lỗi", "Không có đơn hàng đang tạo")
                return
            ma_dh = row[0]
            for ma_sp, sp in self.data.items():
                so_luong = sp["Quantity"]
                don_gia = sp["Price"]
                tong_tien = so_luong * don_gia
                cursor.execute("INSERT INTO OrderDetails(Ma_DH, Ma_SP, So_Luong, Gia_Ban_Hien_Tai, Tong_Tien)VALUES (?, ?, ?, ?, ?)", (ma_dh, ma_sp, so_luong, don_gia, tong_tien))
            cursor.execute("UPDATE Orders SET Trang_Thai=N'Đã thanh toán' WHERE Ma_DH=?", (ma_dh, ))
            conn.commit()
            messagebox.showinfo("Thanh Toán", "Thanh toán thành công")
            self.close_hd()
        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn:
                conn.close()
