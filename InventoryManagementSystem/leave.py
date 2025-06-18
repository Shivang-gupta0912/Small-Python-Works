from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class leaveClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Head Hoppers Studios")
        self.root.config(bg="white")
        self.root.focus_force()
        
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_SNo = StringVar()
        self.var_emp = StringVar()
        self.var_ttl = StringVar()
        self.var_taken = StringVar()
        self.var_rmn = StringVar()
        
        # Create the table if it doesn't exist
        self.create_table()

        SearchFrame = LabelFrame(self.root, text="Search Emp", font=("goudy old style", 12, "bold"), bd=2,
                                 relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                  values=("Emp"), state="readonly",
                                  justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                           bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("Times new roman", 15, "bold"),
                            bg="Blue", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        title = Label(self.root, text="Leave Details", font=("Times new roman", 15, "bold"), bg="black",
                      fg="white").place(x=50, y=100, width=1000)

        lbl_emp = Label(self.root, text="Employee", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_ttl = Label(self.root, text="Total Leaves Alloted", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_taken = Label(self.root, text="Leaves taken", font=("goudy old style", 15), bg="white").place(x=50, y=227)
        lbl_rmn = Label(self.root, text="Leaves Remaining", font=("goudy old style", 15), bg="white").place(x=50, y=265)

        txt_emp = Entry(self.root, textvariable=self.var_emp, font=("goudy old style", 15), bg="light yellow")
        txt_emp.place(x=160, y=150, width=180)
        txt_ttl = Entry(self.root, textvariable=self.var_ttl, font=("goudy old style", 15), bg="light yellow")
        txt_ttl.place(x=220, y=190, width=180)
        txt_taken = Entry(self.root, textvariable=self.var_taken, font=("goudy old style", 15), bg="light yellow")
        txt_taken.place(x=160, y=230, width=180)
        txt_rmn = Entry(self.root, textvariable=self.var_rmn, font=("goudy old style", 15), bg="light yellow")
        txt_rmn.place(x=200, y=270, width=180)

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=310)
        self.txt_desc = Entry(self.root, font=("goudy old style", 15), bg="light yellow")
        self.txt_desc.place(x=160, y=315, width=300, height=100)

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

        self.leaveTable = ttk.Treeview(emp_frame, columns=("S_No", "emp", "total", "taken", "remaining", "description"),
                                       yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.leaveTable.xview)
        scrolly.config(command=self.leaveTable.yview)

        self.leaveTable.heading("S_No", text="S.No.")
        self.leaveTable.heading("emp", text="Emp")
        self.leaveTable.heading("total", text="Total")
        self.leaveTable.heading("taken", text="Taken")
        self.leaveTable.heading("remaining", text="Remaining")
        self.leaveTable.heading("description", text="Description")
        
        self.leaveTable["show"] = "headings"

        self.leaveTable.column("S_No", width=90)
        self.leaveTable.column("emp", width=100)
        self.leaveTable.column("total", width=100)
        self.leaveTable.column("taken", width=100)
        self.leaveTable.column("remaining", width=100)
        self.leaveTable.column("description", width=100)
        self.leaveTable.pack(fill=BOTH, expand=1)
        self.leaveTable.bind("<ButtonRelease-1>", self.get_data)
        self.leaveTable.bind('<<TreeviewSelect>>', self.get_data)
        self.clear()

    def create_table(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS leave (
                            S_No INTEGER PRIMARY KEY AUTOINCREMENT,
                            emp TEXT,
                            total TEXT,
                            taken TEXT,
                            remaining TEXT,
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
            if self.var_emp.get() == "":
                messagebox.showerror("Error", "Emp Required", parent=self.root)
            else:
                cur.execute("INSERT INTO leave(emp,total,taken,remaining,description) VALUES (?,?,?,?,?)", (
                    self.var_emp.get(),
                    self.var_ttl.get(),
                    self.var_taken.get(),
                    self.var_rmn.get(),
                    self.txt_desc.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Leave Added Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * from leave")
            rows = cur.fetchall()
            self.leaveTable.delete(*self.leaveTable.get_children())
            for row in rows:
                self.leaveTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected_row = self.leaveTable.selection()
        if selected_row:
            content = self.leaveTable.item(selected_row)
            row = content['values']
            self.var_emp.set(row[1])
            self.var_ttl.set(row[2])
            self.var_taken.set(row[3])
            self.var_rmn.set(row[4])
            self.txt_desc.delete('0', END)
            self.txt_desc.insert(END, row[5])

    def update(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_emp.get() == "":
                messagebox.showerror("Error", "Emp Must be required", parent=self.root)
            else:
                cur.execute("UPDATE leave SET total=?, taken=?, remaining=?, description=? WHERE emp=?", (
                    self.var_ttl.get(),
                    self.var_taken.get(),
                    self.var_rmn.get(),
                    self.txt_desc.get(),
                    self.var_emp.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Leave Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_emp.get() == "":
                messagebox.showerror("Error", "Emp Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM leave WHERE emp=?", (self.var_emp.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM leave WHERE emp=?", (self.var_emp.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Details Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_emp.set("")
        self.var_ttl.set("")
        self.var_taken.set("")
        self.var_rmn.set("")
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
                messagebox.showerror("Error", "Search input must be required", parent=self.root)
            else:
                if self.var_searchby.get() == "Emp":
                    query = "SELECT * FROM leave WHERE emp LIKE ?"
                else:
                    messagebox.showerror("Error", "Invalid search option", parent=self.root)
                    return

                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.leaveTable.delete(*self.leaveTable.get_children())
                    for row in rows:
                        self.leaveTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = leaveClass(root)
    root.mainloop()
