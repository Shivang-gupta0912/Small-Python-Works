from tkinter import*
import sqlite3
from PIL import Image,ImageTk
from employee import employeeClass
from monthly import monthlyClass
from office import officeClass
from store import storeClass
import time
from leave import leaveClass
from tkinter import messagebox
import os

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("IMS")
        self.root.config(bg="white")
        
    
        self.icon_title=PhotoImage(file="InventoryManagementSystem/images/yo.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",48,"bold"),bg="black",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=2,height=70)
        
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
        
        self.lbl_clock=Label(self.root,text="Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",13),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=3,y=70,relwidth=1,height=30)
        
        self.MenuLogo=Image.open("InventoryManagementSystem/images/images.png")
        self.MenuLogo=self.MenuLogo.resize((200,200))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)
        
        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)
        
        self.icon_side=PhotoImage(file="InventoryManagementSystem/images/side.png")
        
        
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_mexp=Button(LeftMenu,text="Monthly Exp",command=self.monthly,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",18,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_oexp=Button(LeftMenu,text="Office Exp",command=self.office,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_store=Button(LeftMenu,text="Store",command=self.store,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_leave=Button(LeftMenu,text="Attendance",command=self.leave,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",command=self.exit_page,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #self.lbl_employee=Label(self.root,text="Total Employee\n[0]",bd=5,relief=RIDGE,bg="black",fg="white",font=("goudy old style",20,"bold"))
        #self.lbl_employee.place(x=300,y=180,height=150,width=300)
        
        lbl_footer=Label(self.root,text="IMS-Inventory Management System",font=("times new roman",14),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_date_time()
    
    def logout(self):
     confirmed = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
     if confirmed:
       self.root.destroy()

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    
    def monthly(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=monthlyClass(self.new_win)

    def office(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=officeClass(self.new_win)
        
    def store(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=storeClass(self.new_win)
    
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Inventory Management System\t\t {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)
        
    def leave(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=leaveClass(self.new_win)
    
    def exit_page(self):
        self.new_win.destroy()
        
        
class Signup:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("450x200+0+0")
        self.root.resizable(False, False)

        self.username = StringVar()
        self.password = StringVar()

        Label(root, text="Username:", font=("Arial", 14)).place(x=50, y=50)
        Entry(root, textvariable=self.username, font=("Arial", 14)).place(x=180, y=50)

        Label(root, text="Password:", font=("Arial", 14)).place(x=50, y=100)
        Entry(root, textvariable=self.password, show="*", font=("Arial", 14)).place(x=180, y=100)

        Button(root, text="Sign Up", command=self.signup, font=("Arial", 14)).place(x=180, y=150)

    def signup(self):
        # Get the username and password entered by the user
        username = self.username.get()
        password = self.password.get()

        # Store the new user's credentials in a text file
        with open("user_credentials.txt", "a") as file:
            file.write(f"{username},{password}\n")

        messagebox.showinfo("Sign Up Successful", "Your account has been created successfully!")
        self.root.destroy()

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome To Inventory Management System")
        
        self.root.geometry("450x200+0+0".format(
            int((self.root.winfo_screenwidth() - 450) / 2),
            int((self.root.winfo_screenheight() - 200) / 2)
        ))
        self.root.resizable(False, False)

        self.username = StringVar()
        self.password = StringVar()

        Label(root, text="Username:", font=("Arial", 14)).place(x=50, y=50)
        Entry(root, textvariable=self.username, font=("Arial", 14)).place(x=180, y=50)

        Label(root, text="Password:", font=("Arial", 14)).place(x=50, y=100)
        Entry(root, textvariable=self.password, show="*", font=("Arial", 14)).place(x=180, y=100)

        Button(root, text="Login", command=self.login, font=("Arial", 14)).place(x=180, y=150)

        Button(root, text="Sign Up", command=self.open_signup, font=("Arial", 14)).place(x=280, y=150)

    def login(self):
        # Get the username and password entered by the user
        username = self.username.get()
        password = self.password.get()

        # Check if the credentials match the stored credentials
        if os.path.exists("user_credentials.txt"):
            with open("user_credentials.txt", "r") as file:
                existing_users = file.readlines()
                for user in existing_users:
                    stored_username, stored_password = user.strip().split(',')
                    if username == stored_username and password == stored_password:
                        messagebox.showinfo("Login Successful", "Welcome, Admin!")
                        self.root.destroy()
                        root = Tk()
                        obj = IMS(root)
                        root.mainloop()
                        return

        messagebox.showerror("Login Failed", "Invalid username or password")

    def open_signup(self):
        signup_window = Toplevel(self.root)
        signup = Signup(signup_window)

if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
