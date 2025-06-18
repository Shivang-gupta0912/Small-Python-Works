from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class monthlyClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Head Hoppers Studios")
        self.root.config(bg="white")
        self.root.focus_force()
        
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_SNo = StringVar()
        self.var_month = StringVar()
        self.var_dop = StringVar()
        self.var_item = StringVar()
        self.var_total = StringVar()
        self.var_given = StringVar()
        self.var_remaining = StringVar()

        SearchFrame = LabelFrame(self.root, text="Search Monthly Expense", font=("goudy old style", 12, "bold"), bd=2,
                                 relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                  values=("Select", "Date", "Item Name", "Month"), state="readonly",
                                  justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                           bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search",command=self.search, font=("Times new roman", 15, "bold"),
                            bg="Blue", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        title = Label(self.root, text="Monthly Expenses", font=("Times new roman", 15, "bold"), bg="black",
                      fg="white").place(x=50, y=100, width=1000)

        lbl_dop = Label(self.root, text="Date", font=("goudy old style", 15), bg="white").place(x=100, y=150)
        lbl_month = Label(self.root, text="Month", font=("goudy old style", 15), bg="white").place(x=420, y=150)
        lbl_item_name = Label(self.root, text="Item Name", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        txt_dop = Entry(self.root, textvariable=self.var_dop, font=("goudy old style", 15), bg="light yellow")
        txt_dop.place(x=150, y=150, width=180)
        txt_month = ttk.Combobox(self.root, textvariable=self.var_month,
                                  values=('Select', "January", "February","March","April","May","June","July","August","September","October","November","December"), state="readonly", justify=CENTER,
                                  font=("goudy old style", 15))
        txt_month.place(x=500, y=150, width=180)
        txt_month.current(0)
        txt_itme_name = Entry(self.root, textvariable=self.var_item, font=("goudy old style", 15),
                            bg="light yellow").place(x=850, y=150, width=180)

        lbl_total = Label(self.root, text="Total Amount", font=("goudy old style", 15), bg="white").place(x=730, y=190)
        lbl_given = Label(self.root, text="Given Amount", font=("goudy old style", 15), bg="white").place(x=360, y=190)
        lbl_remaining = Label(self.root, text="Remaining", font=("goudy old style", 15), bg="white").place(x=50, y=190)

        txt_total = Entry(self.root, textvariable=self.var_total, font=("goudy old style", 15),
                         bg="light yellow").place(x=850, y=190, width=180)
        txt_given= Entry(self.root, textvariable=self.var_given, font=("goudy old style", 15),
                        bg="light yellow").place(x=500, y=190, width=180)
        txt_remaining = Entry(self.root, textvariable=self.var_remaining, font=("goudy old style", 15),
                        bg="light yellow").place(x=150, y=190, width=180)

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=250)
        self.txt_desc = Entry(self.root, font=("goudy old style", 15), bg="light yellow")
        self.txt_desc.place(x=150, y=250, width=300, height=60)

        btn_add = Button(self.root, text="Save",command=self.add,font=("Times new roman", 15, "bold"),
                         bg="#2196f3", fg="white", cursor="hand2").place(x=520, y=280, width=110, height=28)
        btn_update = Button(self.root, text="Update",command=self.update, font=("Times new roman", 15, "bold"),
                            bg="green", fg="white", cursor="hand2").place(x=655, y=280, width=110, height=28)
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("Times new roman", 15, "bold"),
                            bg="red", fg="white", cursor="hand2").place(x=785, y=280, width=110, height=28)
        btn_clear = Button(self.root, text="Clear",command=self.clear,font=("Times new roman", 15, "bold"),
                           bg="black", fg="white", cursor="hand2").place(x=920, y=280, width=110, height=28)

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.ExpenseTable = ttk.Treeview(emp_frame, columns=("S_No", "dop", "month", "item", "remaining", "given", "total", "description"),
                                         yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ExpenseTable.xview)
        scrolly.config(command=self.ExpenseTable.yview)
        
        self.ExpenseTable.heading("S_No",text="S.No.")
        self.ExpenseTable.heading("dop",text="D.O.P.")
        self.ExpenseTable.heading("month",text="Month")
        self.ExpenseTable.heading("item", text="Item Name")
        self.ExpenseTable.heading("remaining", text="Remaining Amount")
        self.ExpenseTable.heading("given", text="Given Amount")
        self.ExpenseTable.heading("total", text="Total Amount")
        self.ExpenseTable.heading("description", text="Description")
        
        self.ExpenseTable["show"] = "headings"

        self.ExpenseTable.column("S_No", width=50)
        self.ExpenseTable.column("dop", width=100)
        self.ExpenseTable.column("month", width=100)
        self.ExpenseTable.column("item", width=100)
        self.ExpenseTable.column("remaining", width=100)
        self.ExpenseTable.column("given", width=100)
        self.ExpenseTable.column("total", width=100)
        self.ExpenseTable.column("description", width=150)
        self.ExpenseTable.pack(fill=BOTH, expand=1)
        self.ExpenseTable.bind("<ButtonRelease-1>", self.get_data)

        self.create_table()  # Create table if not exists
        self.clear()

    def create_table(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS monthly (
                        S_No INTEGER PRIMARY KEY AUTOINCREMENT,
                        dop TEXT,
                        month TEXT,
                        item TEXT,
                        remaining TEXT,
                        given TEXT,
                        total TEXT,
                        description TEXT
                    )''')
        con.commit()
        con.close()

    def add(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_item.get() == "":
                messagebox.showerror("Error", "Item Name Required", parent=self.root)
            else:
                cur.execute("INSERT INTO monthly(dop, month, item, remaining, given, total, description) VALUES (?,?,?,?,?,?,?)",(
                                        self.var_dop.get(),
                                        self.var_month.get(),
                                        self.var_item.get(),
                                        self.var_remaining.get(),
                                        self.var_given.get(),
                                        self.var_total.get(),
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
            cur.execute("SELECT * from monthly")
            rows = cur.fetchall()
            self.ExpenseTable.delete(*self.ExpenseTable.get_children())
            for row in rows:
                self.ExpenseTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected_row = self.ExpenseTable.focus()
        content = self.ExpenseTable.item(selected_row)
        row = content['values']
        if row:
            self.var_dop.set(row[1])
            self.var_month.set(row[2])
            self.var_item.set(row[3])
            self.var_remaining.set(row[4])
            self.var_given.set(row[5])
            self.var_total.set(row[6])
            self.txt_desc.delete('0', END)
            self.txt_desc.insert(END, row[7])

    def update(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_dop.get() == "":
                messagebox.showerror("Error", "Date Must be required", parent=self.root)
            else:
                cur.execute("UPDATE monthly SET month=?, item=?, remaining=?, given=?, total=?, description=? WHERE dop=?", (
                    self.var_month.get(),
                    self.var_item.get(),
                    self.var_remaining.get(),
                    self.var_given.get(),
                    self.var_total.get(),
                    self.txt_desc.get(),
                    self.var_dop.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Data Updated Successfully", parent=self.root)
                self.show()  # Update the Treeview display
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_dop.get() == "":
                messagebox.showerror("Error", "Date Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM monthly WHERE dop=?", (self.var_dop.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Date", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM monthly WHERE dop=?", (self.var_dop.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Data Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_dop.set("")
        self.var_month.set("Select")
        self.var_item.set("")
        self.var_remaining.set("") 
        self.var_given.set("")
        self.var_total.set("")
        self.txt_desc.delete('0',END)
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
                    query = "SELECT * FROM monthly WHERE dop LIKE ?"
                elif self.var_searchby.get() == "Item Name":
                    query = "SELECT * FROM monthly WHERE item LIKE ?"
                elif self.var_searchby.get() == "Month":
                    query = "SELECT * FROM monthly WHERE month LIKE ?"
                else:
                    messagebox.showerror("Error", "Invalid search option", parent=self.root)
                    return

                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if rows:
                    self.ExpenseTable.delete(*self.ExpenseTable.get_children())
                    for row in rows:
                        self.ExpenseTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__=="__main__":
    root=Tk()
    obj=monthlyClass(root)
    root.mainloop()
