from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog,filedialog, Tk, Button, Label
import cv2
import numpy as np
import math

load_image1 = None
size = 720, 720
space = 15
width = (2*size[0]+3*space)
dimensions=str(width)+'x800'

def on_click1():
    # Step 1.5
    global path_image1
    global load_image1
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    path_image1 = filedialog.askopenfilename()
    # load the image using the path
    load_image1 = Image.open(path_image1)
    # set the image into the GUI using the thumbnail function from tkinter
    load_image1.thumbnail(size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image1)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    img.place(x=20, y=50)

def on_click2(path_image2):
    # Step 1.5
    global load_image2
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    # load the image using the path
    load_image2 = Image.open(path_image2)
    load_image2 = load_image2.resize(size, Image.ANTIALIAS)
    # set the image into the GUI using the thumbnail function from tkinter
    load_image2.thumbnail(size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image2)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    img.place(x=size[0]+2*space, y=50)

MAX_COLOR_VALUE = 256
MAX_BIT_VALUE = 8
n_bits = 2

def make_image(data, resolution):
    image = Image.new("RGB", resolution)
    image.putdata(data)
    return np.array(image)


def get_n_least_significant_bits(value, n):
    value = value << (MAX_BIT_VALUE - n)
    value = value % MAX_COLOR_VALUE
    return value >> (MAX_BIT_VALUE - n)

def shift_n_bits_to_8(value, n):
    return value << (MAX_BIT_VALUE - n)

def decode(enrypted_image):

    global n_bits
    #enrypted_image = Image.open(path1)
    #enrypted_image_in = Image.open(path2)
    width, height = enrypted_image.size

    image_data = enrypted_image.load()
    '''
    The Encoded image & decoded one (as a result of it) is not carrying as much information as the original files and is somehow compressed
    the reason is the image size defined at the beginning of the code
    '''
    data = []

    for y in range(height):
        for x in range(width):

            r_hiden, g_hiden, b_hiden = image_data[x,y][0],image_data[x,y][1],image_data[x,y][2]

            r_hiden = get_n_least_significant_bits(r_hiden, n_bits)
            g_hiden = get_n_least_significant_bits(g_hiden, n_bits)
            b_hiden = get_n_least_significant_bits(b_hiden, n_bits)

            r_hiden = shift_n_bits_to_8(r_hiden, n_bits)
            g_hiden = shift_n_bits_to_8(g_hiden, n_bits)
            b_hiden = shift_n_bits_to_8(b_hiden, n_bits)

            data.append((b_hiden, 
                         g_hiden,
                         r_hiden))

    img = make_image(data, enrypted_image.size)
    # Step 6
    # Write the encrypted image into a new file
    path_to_save=filedialog.asksaveasfilename(defaultextension=".png",filetypes=(("png file", "*.png"),("jpg file", "*.jpg"),("All Files", "*.*")))
    cv2.imwrite(path_to_save, img)
    
    # Display the success label.
    # success_label = Label(app, text="Decryption Successful",
    #             bg='lavender', font=("Cascadia Code", 20))
    # success_label.place(x=(width/2), y=0)
    show_label = Label(app, text="Decryption Successful! - Decrypted Image",
                bg='lavender', font=("Cascadia Code", 20))
    show_label.place(x=(width/2)+430, y=0)
    on_click2(path_to_save)

# Step 1
# Defined the TKinter object app with background lavender, title Encrypt, and app size 600*600 pixels.
app = Tk()
app.configure(background='lavender')
app.title("Decrypt")
app.geometry(dimensions)
# create a button for calling the function on_click
on_click_button1 = Button(app, text="Select Encryted Image", bg='white', fg='black', command=on_click1)
on_click_button1.place(x=space+5, y=10)
# add a text box using tkinter's Text function and place it at (340,55). The text box is of height 165pixels.

encrypt_button = Button(app, text="DECRYPT", bg='white', fg='black', command=lambda : decode(load_image1))
encrypt_button.place(x=space+150, y=10)
app.mainloop()

