from tkinter import * 
# modinverse using the Extended Euclidean algorithm
# common denominator
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g,y,x = egcd(b % a, a)
        return g, x - (b // a) * y, y
# modular inverse
def modInv(e, r):
    g,x,y = egcd(e, r)
    if g != 1:
        raise Exception('g != 1, try generating new keys')
    else:
        return x%r
# displaying the keys
def displayKeys(n,e,d):
    text = str("\n Private key(d,n):\n ({},{})\n\n Public key(e,n):\n ({},{})\n\n\n\n".format(d,n,e,n))
    return text
# calculates the possible factors of a number n
# if the modulo of a number and n == 0 
# the number is a factor of n and is stored in the array
def factors(n):
    factors = []
    for i in range(2, n):
        if n % i == 0:
            factors.append(i)
    return factors[0],factors[1]
# main key crack function 
def crackKey(_e,_n):
    # use factor function to find p and q
    # as n = p*q
    p, q = factors(_n)
    # finding r value from q and q
    r = (p-1)*(q-1)
    # finally finding the private d value 
    # from modular inverse of (e,r)
    d = modInv(_e,r)
    # displaying the private key
    # that was just cracked
    display.insert(1.0,displayKeys(_n,_e,d))
    print("≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠")
    print("Private d value: ", d)

# root holds the main tkinter frame
root = Tk()
# set window title
root.title("RSA Key Crack")
# set window size
root.geometry("400x350")
# variables from ui
n_val = IntVar()
e_val = IntVar()
# text area to display keys
# user is able to copy from this area
display = Text(root,height=7,width=42,bg='black', fg="white", font=('Courier', 14))
# default text for display
display.insert(1.0,displayKeys('n','e','d'))
display.place(x = 20, y = 200)

# main gui function to hold most of the UI
def gui(root):
    # main function tying other function together
    def init():
        create_widgets()
        create_labels()
    # function for widgets, entrys and buttons
    def create_widgets():
        # entry fields for values
        n_entry = Entry(root,textvariable = n_val, width='22', border='3', bg='Lightgrey').place(x = 50, y = 100)
        e_entry = Entry(root,textvariable = e_val, width='22', border='3', bg='Lightgrey').place(x = 50, y = 150)
        key_crack = Button(root,text="Calculate\nPrivate Key",width='7', height='4', 
                command=lambda:crackKey(e_val.get(),n_val.get())).place(x = 270, y = 100)
    # function for static text on UI
    def create_labels():
        # heading
        heading = Label(root, text="RSA Key Crack", 
                    font=('Helvetica', 25, 'bold')).place(x = 110, y = 10)
        # labels for entry fields
        n_l = Label(root, text="N:", font=('Helvetica', 18, 'bold')).place(x = 20, y = 100)
        e_l = Label(root, text="e:", font=('Helvetica', 18, 'bold')).place(x = 20, y = 150)
    # run the functions
    init()
# calling gui function
gui(root)
# end of tk UI
# call mainloop, runs until application window is closed
root.mainloop()