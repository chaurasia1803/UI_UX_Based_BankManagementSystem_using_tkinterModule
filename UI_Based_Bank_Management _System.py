from tkinter import *
from tkinter import messagebox
import random
import mysql.connector 

def connect():
    try:
        return mysql.connector.connect(
            host= "localhost",
            user= "root",
            password= "Bhagya@03",
            database= "accountHolder"
        )
        
    except mysql.connector.Error as e:
        print("DB Error: ", e)
        return None

def admin_login(username, password):
    db= connect()
    cursor= db.cursor()
    cursor.execute("SELECT * FROM admin_user WHERE username=%s AND password=%s", (username, password))
    admin= cursor.fetchone()
    db.close()
    return admin is not None    


def AdminLoginWin():
    clearWindow()
    Label(win, text=" Admin Login", font="arial 25 bold").pack(pady=10)
    Label(win, text="username").pack()
    user=Entry(win)
    user.pack()

    Label(win, text=" Password").pack()
    pwd=Entry(win,  show="*")
    pwd.pack()
    def verify():
        if admin_login(user.get(), pwd.get()):
            AdminDashboard()
        else:
            messagebox.showerror("Error", "Invalid Admin Credentials")

    Button(win, text="Login", width= 20, command=verify).pack(pady=10)

def AdminDashboard():
    

    Label(win, text=" ADMIN DASHBOARD ", font="arial 22 bold").pack(pady=10)

    Button(win, text="VIEW ALL ACCOUNTS", width=30, command=view_accounts).pack(pady=5)
    Button(win, text="DELETE USER ACCOUNT", width=30, command=delete_account).pack(pady=5)
    Button(win, text="DATABASE HEALTH", width=30, command=db_health).pack(pady=5)
    Button(win, text="LOGOUT", width=30, command=MainWindow).pack(pady=10)

def view_accounts():
    db=connect()
    cursor= db.cursor()
    cursor.execute("SELECT acc_num, name, phone, password, balance FROM accounts")
    data= cursor.fetchall()
    db.close()
    
    top= Toplevel(win)
    top.title("User Accounts")

    for i, row in enumerate(data):
        Label(top, text=row, anchor="w").grid(row=i, column=0)




def delete_account():
    top= Toplevel(win)
    top.title("Delete Account")

    Label(win, text=" Enter account no.").pack()
    acc=Entry(top)
    acc.pack()

    def confirm():
        db=connect()
        cursor= db.cursor()
        cursor.execute("DELETE FROM accounts WHERE acc_num=%s", (acc.get(),))
        db.commit()
        db.close()
        messagebox.showinfo("Done", " Account Deleted")

    Button(top, text="Delete Account", command= confirm).pack(pady=5)


def db_health():
    db= connect()
    cursor= db.cursor()
    cursor.execute(" SELECT COUNT(*) FROM accounts")
    total= cursor.fetchone()[0]

    cursor.execute("SHOW TABLE STATUS LIKE 'accounts'")
    status= cursor.fetchone()
    db.close()

    msg= f"""
    Total Accounts: {total}
    Storage Engine: {status[1]}
    Rows          : {status [4]}
    """
    messagebox.showinfo("Database Health", msg)





def MainWindow():
    clearWindow()
    L1 =Label(win, text ="Welcome to Bank", font="arial 25 bold")
    L1.pack()
    B1 = Button(win, text="Create an account", width= 20, command=OpenAccountWindow)
    B1.pack(pady=3)
    B2 = Button(win, text="LOGIN IN", width=20, command=Login)
    B2.pack(pady=3)
    B3 = Button(win, text="Admin Login", width=20, command=AdminLoginWin)
    B3.pack(pady=3)
    B4= Button(win, text="Exit", width=20)
    B4.pack(pady=3)






def Login():
    clearWindow()
    def Verify_Login():
        global acc_num 
        acc_num= E1.get()
        password= E2.get()

        db= connect()
        cursor= db.cursor()

        query= "SELECT * FROM accounts WHERE acc_num =%s AND password=%s"
        cursor.execute(query,(acc_num,password))
        result=cursor.fetchone()
        
        if result:
            Label(win, text="Login Successful!", fg= "green").pack()
            GoToAccount()

        else:
            Label(win, text="Invalid Details", fg= "Red").pack()

        db.close()

    L1 =Label(win, text ="LOGIN IN", font="arial 25 bold")
    L1.pack()
    L2 =Label(win, text="Prior to logging in, please confirm your account.", font="arial 7 italic")
    L2.pack()
    L3= Label(win, text="Enter Account No")
    L3.pack()
    E1=Entry(win, width=20)
    E1.pack()
    L4= Label(win, text="Password")
    L4.pack()
    E2=Entry(win, width=20, show="*")
    E2.pack()
    B5= Button(win, text="LOGIN", width=20, command= Verify_Login)
    B5.pack(pady=3)
    B6= Button(win, text="Back", width=20, command=MainWindow)
    B6.pack(pady=3)

def GoToAccount():
    clearWindow()

    
    def CheckBalance():
        clearWindow()
        global balance_label
        
        def Balance():
            db= connect()
            cursor= db.cursor()
            query= "SELECT balance FROM accounts WHERE acc_num=%s"
            cursor.execute(query,(acc_num,))
            result= cursor.fetchone()
            db.close()

            if result:
                balance_label.config(text=f"Your balance is ....Rs.{result[0]}")
            else:
                balance_label.config(text="Error fetching balance...")
        
        L1=Label(win, text ="---Checking Your Balance Amount----", font="arial 20")
        L1.pack()
        L2=Label(win, text =f"Logged in as.. {acc_num}", font="arial 15")
        L2.pack()
        balance_label=Label(win, text =" ", font="arial 15", fg="blue")
        balance_label.pack()
        B1= Button(win, text="Show", width=20, command=Balance)
        B1.pack(pady=3)
        B2= Button(win, text="Back", width=20, command=GoToAccount)
        B2.pack(pady=3)

    def Deposit():
        clearWindow()
        def AddAmount():
            amount= int(E1.get())
            db=connect()
            cursor= db.cursor()
            query="UPDATE accounts SET balance =balance+ %s WHERE acc_num=%s"
            cursor.execute(query,(amount,acc_num,))
            db.commit()
            db.close()

            L3.config(text="Deposited Successfully!!...", fg="blue")

        global amount
        
        L1=Label(win, text ="Please deposit money into your account to cover your outstanding balance.", font="arial 7 italic")
        L1.pack()
        L2=Label(win, text ="Amount to be Added", font="arial 25")
        L2.pack()
        E1=Entry(win, width=20)
        E1.pack()
        
        B1= Button(win, text="Deposit", width=20, command= AddAmount)
        B1.pack(pady=3)
        L3=Label(win, text ="", font="arial 25 bold italic")
        L3.pack()
        B2= Button(win, text="Back", width=20, command=GoToAccount)
        B2.pack(pady=3)


    def Withdraw():
        clearWindow()
        def Debit():
            amount= int(E1.get())
            db=connect()
            cursor= db.cursor()
            query="UPDATE accounts SET balance =balance- %s WHERE acc_num=%s"
            cursor.execute(query,(amount,acc_num,))
            db.commit()
            db.close()

            L3.config(text="Debited Amount Successfully!!...", fg="blue")

        global amount

        L1=Label(win, text ="Please process a withdrawal from your account.", font="arial 7 italic")
        L1.pack()
        L2=Label(win, text ="Amount to be withdraw", font="arial 15")
        L2.pack()
        E1=Entry(win, width=20)
        E1.pack()
        B1= Button(win, text="Withdraw", width=20, command= Debit)
        B1.pack(pady=3)
        L3=Label(win, text ="", font="arial 15")
        L3.pack()
        B2= Button(win, text="Back", width=20, command=GoToAccount)
        B2.pack(pady=3)

    def Transfer():
        clearWindow()
        def Transaction():
            db= connect()
            cursor= db.cursor()
            money=int(E3.get())
            sender= E1.get()
            receiver= E2.get()
            try:
                query1= "UPDATE accounts SET balance = balance - %s WHERE acc_num=%s"
                cursor.execute(query1,(money, sender))
                
                query2= "UPDATE accounts SET balance = balance + %s WHERE acc_num=%s"
                cursor.execute(query2,(money, receiver))

                db.commit()
                L5.config(text="Transaction Completed.....", fg= "blue")
            except:
                db.rollback()
                L5.config(text="Transaction Failed.....", fg= "red")
            db.close()


        L1=Label(win, text ="Money Transfer", font="arial 15 bold")
        L1.pack()
        L2=Label(win, text ="Sender's Account No.", font="arial 15")
        L2.pack()
        E1=Entry(win, width=20)
        E1.pack()
        L3=Label(win, text ="Reciever's Account No.", font="arial 15")
        L3.pack()
        E2=Entry(win, width=20)
        E2.pack()
        L4=Label(win, text ="Amount", font="arial 15")
        L4.pack()
        E3=Entry(win, width=20)
        E3.pack()
        L5=Label(win, text="", font=" arial 25 bold")
        L5.pack()
        B1= Button(win, text="Transfer", width=20, command=Transaction)
        B1.pack(pady=3)
        B2= Button(win, text="Back", width=20, command=GoToAccount)
        B2.pack(pady=3)

    def EditProfile():
        clearWindow()
        def PassChange():
            
            def Change():
                db=connect()
                cursor= db.cursor(buffered=True)
                old=E1.get()
                new=E2.get()
                check_query= "SELECT password FROM accounts WHERE acc_num=%s"
                cursor.execute(check_query, (acc_num,))
                result=cursor.fetchone()

                if result and result[0] == old:
                    update_query="UPDATE accounts SET password=%s WHERE acc_num= %s"
                    cursor.execute(update_query,(new,acc_num,))
                    db.commit()
                    L3.config(text="PASSWORD UPDATED!!", fg="blue")
                else:
                    L3.config(text="INCORRECT OLD PASSWORD!!", fg="red")
                
                db.close()
                
            L1=Label(win, text="Old Password", font="arial 15", show="*")
            L1.pack()
            E1= Entry(win, width=20)
            E1.pack()
            L2=Label(win, text="Create New Password", font="arial 15", show="*")
            L2.pack()
            E2=Entry(win, width=20)
            E2.pack()
            L3=Label(win, text="", font="arial 15")
            L3.pack()
            B1= Button(win, text="Create", width=20, command=Change)
            B1.pack()
        
        B1= Button(win, text="Password Change", width=20, command=PassChange)
        B1.pack(pady=3)
        B2= Button(win, text="Back", width=20, command=GoToAccount)
        B2.pack(pady=3)


    L1 =Label(win, text ="LOGIN IN SUCCESSFULLY!", font="arial 13 bold italic", fg="blue" )
    L1.pack(pady=3)
    B1 = Button(win, text="Check Balance", width=20, command=CheckBalance)
    B1.pack(pady=3)
    B2 = Button(win, text="Deposit Amount", width=20, command=Deposit)
    B2.pack(pady=3)
    B3 = Button(win, text="Transfer Amount", width =20, command=Transfer)
    B3.pack(pady=3)
    B4= Button(win, text="Withdraw Amount", width=20, command=Withdraw)
    B4.pack(pady=3)
    B5= Button(win, text="Edit Profile", width=20, command=EditProfile)
    B5.pack(pady=3)
    B6= Button(win, text="Back", width=20, command=MainWindow)
    B6.pack(pady=3)

def OpenAccountWindow():
    clearWindow()

    
    def is_phone_unique(phone):
        db=connect()
        cursor= db.cursor()


        cursor.execute("SELECT phone FROM accounts WHERE phone=%s ",(phone,))
        result= cursor.fetchone()
        db.close()
        return result is None
    

    def generate_acc():
        while True:
            acc_num= str(random.randint(10_000_000,99_999_999))
            db=connect()
            cursor= db.cursor()
            cursor.execute("SELECT acc_num FROM accounts WHERE acc_num=%s",(acc_num,))
            if cursor.fetchone() is None:
                db.close()
                return acc_num
            
            db.close()

    def create_acc(name, phone, password, balance):
        if not is_phone_unique(phone):
            return "Phone no. already registered..."
        
        acc_num= generate_acc()
        db=connect()
        cursor=db.cursor()

        cursor.execute("""
            INSERT INTO accounts (acc_num, name, phone, password, balance)
            VALUES(%s, %s,%s,%s,%s)
        """,(acc_num, name, phone, password, balance,))

        db.commit()
        db.close()
    
        return f"Account created Successfully! Your Account No.: {acc_num}"

    def submit():
        
        phone= E1.get()
        name= E2.get()
        password= E3.get()
        balance= E4.get()
        
        result= create_acc(name, phone, password, balance)
        messagebox.showinfo("Status", result)

    


    L1= Label(win, text="Open Account", font="arial 24 bold")
    L1.pack()
    L2= Label(win, text="Enter Phone No")
    L2.pack()
    E1=Entry(win, width=20)
    E1.pack()
    L3= Label(win, text="Enter Name")
    L3.pack()
    E2=Entry(win, width=20)
    E2.pack()
    L4= Label(win, text="create a password ")
    L4.pack()
    E3=Entry(win, width=20, show="*")
    E3.pack()
    L5= Label(win, text="Enter your Opening balannce ")
    L5.pack()
    E4=Entry(win, width=20)
    E4.pack()
    L6= Label(win, text="",font="arial 15 bold")
    L6.pack()
    B1= Button(win, text="Create", width=20, command=submit)
    B1.pack(pady=3)
    B2= Button(win, text="Back", width=20, command=MainWindow)
    B2.pack(pady=3)
        


def clearWindow():
    for item in win.winfo_children():
        item.destroy()


    



win=Tk()
win.geometry("300x400")
win.title("BankApp")
MainWindow()
win.mainloop()