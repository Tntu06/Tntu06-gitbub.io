import tkinter as tk
from tkinter import messagebox

class Popup:
    def __init__(self, parent, datas = None):
        self.parent = parent
        self.data = None
        self.datas = datas
        self.win = tk.Toplevel(parent)
        self.win.title("Chỉnh sửa sản phẩm" if datas else "Thêm sản phẩm")
        self.win.geometry("300x220")
        self.win.resizable(False, False)

        self.var_name = tk.StringVar()
        self.var_id = tk.StringVar()
        self.var_quantity = tk.StringVar()
        self.var_price = tk.StringVar()
        
        if datas:
            self.var_name.set(datas[0])
            self.var_id.set(datas[1])
            self.var_quantity.set(datas[2])
            self.var_price.set(datas[3])
            

        self.build()
    
    def build(self):
        frame_header = tk.Frame(self.win)
        frame_header.pack(pady=5)
        tk.Label(frame_header, text="Thêm/Sửa thông tin", font=("Times New Roman", 12, "bold")).pack()

        frame_form = tk.Frame(self.win)
        frame_form.pack(padx=10, pady=5)

        tk.Label(frame_form, text="Tên SP", width=8).grid(row=0, column=0, pady=5, sticky="w")
        self.new_product = tk.Entry(frame_form, textvariable=self.var_name)
        self.new_product.grid(row=0, column=1, pady=5)

        tk.Label(frame_form, text="Mã SP", width=8).grid(row=1, column=0, pady=5, sticky="w")
        self.new_id = tk.Entry(frame_form,textvariable=self.var_id)
        self.new_id.grid(row=1, column=1, pady=5)
        if self.datas:
            self.new_id.config(state="disabled")

        tk.Label(frame_form, text="Số Lượng", width=8).grid(row=2, column=0, pady=5, sticky="w")
        self.new_quantity = tk.Entry(frame_form, textvariable=self.var_quantity)
        self.new_quantity.grid(row=2, column=1, pady=5)

        tk.Label(frame_form, text="Đơn giá", width=8).grid(row=3, column=0, pady=5, sticky="w")
        self.new_price = tk.Entry(frame_form, textvariable=self.var_price)
        self.new_price.grid(row=3, column=1, pady=5)

        frame_btn = tk.Frame(self.win)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Save" if self.datas else "Add", bg="gray", command=self.save).pack(side="left")

    def save(self):
        self.data = (self.var_id.get(), self.var_name.get(), self.var_price.get(), self.var_quantity.get())
        self.win.destroy()
