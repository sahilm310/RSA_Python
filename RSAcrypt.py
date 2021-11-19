from tkinter import * 
import numpy as np
import random

# generates an array of prime numbers
# from a specified range
def primeGen(lower=300, upper=500):
    primeArr= []
    for num in range(lower, upper):
        if num > 1:
            # changed num to int(num**0.5)+1
            # to dramatically sped up computation 
            # a lot faster with larger numbers
            for i in range(2, int(num**0.5)+1):
                if (num % i) == 0:
                    break
            else:
                primeArr.append(num)
    return primeArr

# the following block of code is for Modular Inverse and was referenced from:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Modular_inverse
# By WikiBooks - Last accessed(23/03/2021)
# using the Extended Euclidean algorithm
# common denominator
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g,y,x = egcd(b % a, a)# recursive
        return g, x - (b // a) * y, y
# modular inverse
def modInv(e, r):
    g,x,y = egcd(e, r)
    if g != 1:
        raise Exception('g != 1, try generating new keys')
    else:
        return x%r

# main function for key generation
def keyGen():
    # generating a list of primes
    primes = primeGen(300,600)
    # randomly choosing  from list of primes
    p = random.choice(primes)
    q = random.choice(primes)
    print("≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠")
    print('p: {}       q: {}'.format(p,q))
    # calculating e and N with p and q
    n = p*q
    r = (p-1) * (q-1)
    print('N: {}    r: {}'.format(n,r))
    # generating a list of primes for 1<e<r
    ePrimes = primeGen(1,r-1)
    # choosing random prime from list
    e = random.choice(ePrimes)
    print('e: {}'.format(e))
    # modular inverse of (e.r)
    d = modInv(e,r)
    print('d: {}'.format(d))
    # display new keys in the ui
    display.insert(0.0,displayKeys(str(n),str(e),str(d)))
    # setting the ui fields automatically 
    # with calculated values
    new_n.set(n)
    new_e.set(e)
    new_d.set(d)


def encrypt(_plain, _e, _n):
    # the encryption calculation
    def encrypt_calc(ch_uni, _e, _n):
        calc = (ch_uni**_e)%_n
        return calc
    # ord return unicode integer
    # unicode of each character passed to function
    # (ch^e)mod n calculation is performed and returned
    # each output is joined together as a large string
    # separated by commas
    cipherT = ','.join(str(encrypt_calc(ord(ch), _e, _n)) for ch in _plain)
    # displaying final cipher text on the UI
    cipherText.set(cipherT)
    # print to console
    print("≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠")
    print("Encrypted message: ", cipherT)


def decrypt(_cipher, _d, _n):
    # empty decrypted text
    decrypted=''
    # decryption calculation
    # c^d mod n
    def decrypt_calc(ch_c, _d, _n):
        calc = ((ch_c**_d)%_n)
        # return as a character
        return chr(calc)
    # seperate and store cipher text as list
    ciph = list(_cipher.split(','))
    # loop through all the values in cipher
    for ch in ciph:
        # add result of each calculation (character)
        # to decryption text
        decrypted+=decrypt_calc(int(ch), _d, _n)
    # Display decrypted plain text on UI
    plainText.set(decrypted)
    print("≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠")
    print("Decrypted message: ",decrypted)

# root holds the main tkinter frame
root = Tk()
# set window title
root.title("RSA encrytion")
# set window size
root.geometry("600x500")

# function to display keys as a message
def displayKeys(n,e,d):
    return str("\n Private key(d,n):\n ({},{})\n\n Public key(e,n):\n ({},{})\n\n\n\n".format(d,n,e,n))
# text area to display keys
# user is able to copy from this area
display = Text(root,height=7,width=25,bg='black', fg="white", font=('Courier', 14))
# default text for display
display.insert(1.0,displayKeys('n','e','d'))
display.place(x = 390, y = 100)

# variables to connect the UI element values to the code
new_n = IntVar()
new_e = IntVar()
new_d = IntVar()
cipherText = StringVar()
plainText = StringVar()
# main gui function to hold most of the UI
def gui(root):
    # main function tying other function together
    def init():
        create_widgets()
        create_labels()

    # functions for creating each type of 
    # widget from a 'template'
    def createL(root,_text, _f, _fS, _fB, _x,_y):
        tempL = Label(root, text=_text, font=(_f, _fS, _fB)).place(x = _x, y = _y)
        return tempL
    # entry fields template
    def createE(root, _var, _w, _b, _x, _y):
        tempE = Entry(root,textvariable = _var, width=str(_w), border=str(_b), 
        bg='Lightgrey').place(x = _x, y = _y)
        return tempE
    # buttons template
    def createB(root,_text, _w, _h, _command, _x, _y):
        tempB = Button(root,text=_text, width=str(_w), height=str(_h), command=_command).place(x = _x, y = _y)
        return tempB

    # function for widgets, entrys and buttons
    def create_widgets():
        # entry for values
        n_entry = createE(root, new_n, 22, 3, 50, 100)
        e_entry = createE(root, new_e, 22, 3, 50, 150)
        d_entry = createE(root, new_d, 22, 3, 50, 200)
        #key gen button
        key_gen = createB(root, "Generate\nNew Key", 7, 7, keyGen, 270, 100)
        # entry for text
        plain_entry = createE(root, plainText, 40, 3, 30, 290)
        cipher_entry = createE(root, cipherText, 40, 3, 30, 410)
        # encrypt and decrypt buttons
        encrypt_button = createB(root,"ENCRYPT",14,3,lambda:encrypt(plainText.get(),new_e.get(),new_n.get()),420,260)
        decrypt_button = createB(root,"DECRYPT",14,3,lambda:decrypt(cipherText.get(), new_d.get(), new_n.get()),420,380)
        # quit button
        quit = Button(root, text="QUIT", fg="red", command=root.destroy).place(x=520,y=20)
        
    # function for static text on UI
    def create_labels():
        # heading
        heading = createL(root, "RSA Encryption\nand Decryption", 'Helvetica', 25, 'bold', 200, 10)
        # labels for entry fields
        n_l = createL(root, "N:", 'Courier', 18, 'bold', 10, 100)
        e_l = createL(root, "e:", 'Courier', 18, 'bold', 10, 150)
        d_l = createL(root, "d:", 'Courier', 18, 'bold', 10, 200)
        plain_l = createL(root, "Plain text to encrypt:", 'Courier', 16, 'bold', 30, 260)
        cipherT_l = createL(root, "Cipher text to decrypt:", 'Courier', 16, 'bold', 30, 380)
        
    # run the functions
    init()
# calling gui function
gui(root)
# end of tk UI
# call mainloop, runs until application window is closed
root.mainloop()
