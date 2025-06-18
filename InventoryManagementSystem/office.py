from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class officeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Head Hoppers Studios")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_SNo = StringVar()
        self.var_date = StringVar()
        self.var_item = StringVar()
        self.var_expense = StringVar()
        
        # Call method to create table
        self.create_table()

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Office Expenses", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Date", "Item Name"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("Times new roman", 15, "bold"), bg="Blue", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        # Title
        title = Label(self.root, text="Office Expenses", font=("Times new roman", 15, "bold"), bg="black", fg="white").place(x=50, y=100, width=1000)

        # Labels and Entries
        lbl_date = Label(self.root, text="Date", font=("goudy old style", 15), bg="white").place(x=100, y=150)
        lbl_item_name = Label(self.root, text="Item Name", font=("goudy old style", 15), bg="white").place(x=55, y=220)
        lbl_expense = Label(self.root, text="Expense", font=("goudy old style", 15), bg="white").place(x=70, y=280)

        txt_date = Entry(self.root, textvariable=self.var_date, font=("goudy old style", 15), bg="light yellow")
        txt_date.place(x=160, y=150, width=180)
        txt_item_name = Entry(self.root, textvariable=self.var_item, font=("goudy old style", 15), bg="light yellow")
        txt_item_name.place(x=160, y=220, width=180)
        txt_expense = Entry(self.root, textvariable=self.var_expense, font=("goudy old style", 15), bg="light yellow")
        txt_expense.place(x=160, y=285, width=180)

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=345)
        self.txt_desc = Entry(self.root, font=("goudy old style", 15), bg="light yellow")
        self.txt_desc.place(x=160, y=350, width=300, height=60)

        # Buttons
        btn_add = Button(self.root, text="Save", command=self.add, font=("Times new roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2").place(x=60, y=440, width=90, height=28)
        btn_update = Button(self.root, text="Update", command=self.update, font=("Times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2").place(x=170, y=440, width=90, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Times new roman", 15, "bold"), bg="red", fg="white", cursor="hand2").place(x=280, y=440, width=90, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Times new roman", 15, "bold"), bg="black", fg="white", cursor="hand2").place(x=390, y=440, width=90, height=28)

        # Treeview
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=500, y=140, width=550, height=325)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.officeTable = ttk.Treeview(emp_frame, columns=("S_No", "date", "item", "expense", "description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.officeTable.xview)
        scrolly.config(command=self.officeTable.yview)

        self.officeTable.heading("S_No", text="S.No.")
        self.officeTable.heading("date", text="Date")
        self.officeTable.heading("item", text="Item Name")
        self.officeTable.heading("expense", text="Expenses")
        self.officeTable.heading("description", text="Description")
        
        self.officeTable["show"] = "headings"

        self.officeTable.column("S_No", width=90)
        self.officeTable.column("date", width=100)
        self.officeTable.column("item", width=100)
        self.officeTable.column("expense", width=100)
        self.officeTable.column("description", width=100)
        self.officeTable.pack(fill=BOTH, expand=1)
        
        self.officeTable.bind("<ButtonRelease-1>", self.get_data)
        self.officeTable.bind('<<TreeviewSelect>>', self.get_data)
        
        self.clear()

    def create_table(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS office (
                            S_No INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT,
                            item TEXT,
                            expense TEXT,
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
            if self.var_item.get() == "":
                messagebox.showerror("Error", "Item Name Required", parent=self.root)
            else:
                cur.execute("INSERT INTO office(date, item, expense, description) VALUES (?,?,?,?)", (
                    self.var_date.get(),
                    self.var_item.get(),
                    self.var_expense.get(),
                    self.txt_desc.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Data Added Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * from office")
            rows = cur.fetchall()
            self.officeTable.delete(*self.officeTable.get_children())
            for row in rows:
                self.officeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected_row = self.officeTable.selection()
        if selected_row:
            content = self.officeTable.item(selected_row)
            row = content['values']
            self.var_date.set(row[1])
            self.var_item.set(row[2])
            self.var_expense.set(row[3])
            self.txt_desc.delete('0', END)
            self.txt_desc.insert(END, row[4])

    def update(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_date.get() == "":
                messagebox.showerror("Error", "Date Must be required", parent=self.root)
            else:
                cur.execute("UPDATE office SET item=?, expense=?, description=? WHERE date=?", (
                    self.var_item.get(),
                    self.var_expense.get(),
                    self.txt_desc.get(),
                    self.var_date.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Data Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_date.get() == "":
                messagebox.showerror("Error", "Date Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM office WHERE date=?", (self.var_date.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Date", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM office WHERE date=?", (self.var_date.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Data Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_date.set("")
        self.var_item.set("")
        self.var_expense.set("")
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
                if self.var_searchby.get() == "Date":
                    query = "SELECT * FROM office WHERE date LIKE ?"
                elif self.var_searchby.get() == "Item Name":
                    query = "SELECT * FROM office WHERE item LIKE ?"
                else:
                    messagebox.showerror("Error", "Invalid search option", parent=self.root)
                    return

                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.officeTable.delete(*self.officeTable.get_children())
                    for row in rows:
                        self.officeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = officeClass(root)
    root.mainloop()
