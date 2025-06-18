from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class storeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Head Hoppers Studios")
        self.root.config(bg="white")
        self.root.focus_force()
        
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_SNo = StringVar()
        self.var_asset = StringVar()
        self.var_qnt = StringVar()

        # Call method to create table
        self.create_table()

        SearchFrame = LabelFrame(self.root, text="Search Assets", font=("goudy old style", 12, "bold"), bd=2,
                                 relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                  values=("Select", "Asset Name"), state="readonly",
                                  justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                           bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("Times new roman", 15, "bold"),
                            bg="Blue", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        title = Label(self.root, text="Assets In Store", font=("Times new roman", 15, "bold"), bg="black",
                      fg="white").place(x=50, y=100, width=1000)

        lbl_asset = Label(self.root, text="Asset Name", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_qnt= Label(self.root, text="Quantity", font=("goudy old style", 15), bg="white").place(x=55, y=220)

        txt_asset = Entry(self.root, textvariable=self.var_asset, font=("goudy old style", 15), bg="light yellow")
        txt_asset.place(x=160, y=150, width=180)
        txt_qnt = Entry(self.root, textvariable=self.var_qnt, font=("goudy old style", 15), bg="light yellow")
        txt_qnt.place(x=160, y=220, width=180)
        

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=285)
        self.txt_desc = Entry(self.root, font=("goudy old style", 15), bg="light yellow")
        self.txt_desc.place(x=160, y=285, width=300, height=100)

        btn_add = Button(self.root, text="Save", command=self.add, font=("Times new roman", 15, "bold"),
                         bg="#2196f3", fg="white", cursor="hand2").place(x=60, y=430, width=90, height=28)
        btn_update = Button(self.root, text="Update", command=self.update, font=("Times new roman", 15, "bold"),
                            bg="green", fg="white", cursor="hand2").place(x=170, y=430, width=90, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Times new roman", 15, "bold"),
                            bg="red", fg="white", cursor="hand2").place(x=280, y=430, width=90, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Times new roman", 15, "bold"),
                           bg="black", fg="white", cursor="hand2").place(x=390, y=430, width=90, height=28)

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=500, y=140, width=550, height=325)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.assetTable = ttk.Treeview(emp_frame, columns=("S_No", "asset", "qnt", "description"),
                                       yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.assetTable.xview)
        scrolly.config(command=self.assetTable.yview)

        self.assetTable.heading("S_No", text="S.No.")
        self.assetTable.heading("asset", text="Assets")
        self.assetTable.heading("qnt", text="Quantity")
        self.assetTable.heading("description", text="Description")
        
        self.assetTable["show"] = "headings"

        self.assetTable.column("S_No", width=90)
        self.assetTable.column("asset", width=100)
        self.assetTable.column("qnt", width=100)
        self.assetTable.column("description", width=100)
        self.assetTable.pack(fill=BOTH, expand=1)
        self.assetTable.bind("<ButtonRelease-1>", self.get_data)
        self.assetTable.bind('<<TreeviewSelect>>', self.get_data)
        self.clear()

    def create_table(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS store (
                            S_No INTEGER PRIMARY KEY AUTOINCREMENT,
                            asset TEXT,
                            quantity TEXT,
                            description TEXT
                        )''')
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def add(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_asset.get() == "":
                messagebox.showerror("Error", "Asset Name Required", parent=self.root)
            else:
                cur.execute("INSERT INTO store(asset, quantity, description) VALUES (?,?,?)",(
                                        self.var_asset.get(),
                                        self.var_qnt.get(),
                                        self.txt_desc.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Asset Added Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * from store")
            rows = cur.fetchall()
            self.assetTable.delete(*self.assetTable.get_children())
            for row in rows:
                self.assetTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected_row = self.assetTable.selection()
        if selected_row:
            content = self.assetTable.item(selected_row)
            row = content['values']
            self.var_asset.set(row[1])
            self.var_qnt.set(row[2])
            self.txt_desc.delete('0', END)
            self.txt_desc.insert(END, row[3])

    def update(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_asset.get() == "":
                messagebox.showerror("Error", "Asset Name Must be required", parent=self.root)
            else:
                cur.execute("UPDATE store SET quantity=?, description=? WHERE asset=?", (
                    self.var_qnt.get(),
                    self.txt_desc.get(),
                    self.var_asset.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Asset Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_asset.get() == "":
                messagebox.showerror("Error", "Asset Name Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM store WHERE asset=?", (self.var_asset.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Asset", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM store WHERE asset=?", (self.var_asset.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Asset Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_asset.set("")
        self.var_qnt.set("")
        self.txt_desc.delete('0', END)
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
        
    def search(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                if self.var_searchby.get() == "Asset Name":
                    query = "SELECT * FROM store WHERE asset LIKE ?"
                else:
                    messagebox.showerror("Error", "Invalid search option", parent=self.root)
                    return

                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.assetTable.delete(*self.assetTable.get_children())
                    for row in rows:
                        self.assetTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = storeClass(root)
    root.mainloop()
