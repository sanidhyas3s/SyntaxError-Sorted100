from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Button, Label
import cv2
import numpy as np
import math

load_image1 = None
load_image2 = None
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
    load_image1 = load_image1.resize(size, Image.ANTIALIAS)
    # set the image into the GUI using the thumbnail function from tkinter
    load_image1.thumbnail(size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image1)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    img.place(x=space, y=50)

def on_click2():
    # Step 1.5
    global path_image2
    global load_image2
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    path_image2 = filedialog.askopenfilename()
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

def remove_n_least_significant_bits(value, n):
    value = value >> n 
    return value << n

def get_n_least_significant_bits(value, n):
    value = value << (MAX_BIT_VALUE - n)
    value = value % MAX_COLOR_VALUE
    return value >> (MAX_BIT_VALUE - n)

def get_n_most_significant_bits(value, n):
    return value >> (MAX_BIT_VALUE - n)

def shift_n_bits_to_8(value, n):
    return value << (MAX_BIT_VALUE - n)

def encode(image_to_hide, image_to_hide_in):

    global n_bits
    #image_to_hide = Image.open(path1)
    #image_to_hide_in = Image.open(path2)
    width, height = image_to_hide.size

    hide_image = image_to_hide.load()
    hide_in_image = image_to_hide_in.load()

    data = []

    for y in range(height):
        for x in range(width):

            # (107, 3, 10)
            # most sig bits
            r_hide, g_hide, b_hide = hide_image[x,y][0],hide_image[x,y][1],hide_image[x,y][2]

            r_hide = get_n_most_significant_bits(r_hide, n_bits)
            g_hide = get_n_most_significant_bits(g_hide, n_bits)
            b_hide = get_n_most_significant_bits(b_hide, n_bits)

            # remove lest n sig bits
            r_hide_in, g_hide_in, b_hide_in = hide_in_image[x,y][0],hide_in_image[x,y][1],hide_in_image[x,y][2]

            r_hide_in = remove_n_least_significant_bits(r_hide_in, n_bits)
            g_hide_in = remove_n_least_significant_bits(g_hide_in, n_bits)
            b_hide_in = remove_n_least_significant_bits(b_hide_in, n_bits)
            #print("p2",r_hide_in+r_hide,g_hide_in+g_hide,b_hide_in+b_hide)
            data.append((b_hide + b_hide_in, 
                         g_hide + g_hide_in,
                         r_hide + r_hide_in))

    img = make_image(data, image_to_hide.size)
    # Step 6
    # Write the encrypted image into a new file
    path_to_save=filedialog.asksaveasfilename(defaultextension=".png",filetypes=(("png file", "*.png"),("jpg file", "*.jpg"),("All Files", "*.*")))
    # path_to_save=path_to_save if '.jpg' in path_to_save else path_to_save + '.jpg'
    cv2.imwrite(path_to_save, img)
    # Display the success label.
    success_label = Label(app, text="Encryption Successful!",
                bg='lavender', font=("Cascadia Code", 20))
    success_label.place(x=(width/2)+200, y=0)

# Step 1
# Defined the TKinter object app with background lavender, title Encrypt, and app size 600*600 pixels.
app = Tk()
app.configure(background='lavender')
app.title("Encrypt")
# app.attributes('-fullscreen',True)
app.geometry(dimensions)
# create a button for calling the function on_click
on_click_button1 = Button(app, text="Select image to hide", bg='white', fg='black', command=on_click1)
on_click_button1.place(x=space, y=10)
on_click_button2 = Button(app, text="Select image to hide in", bg='white', fg='black', command=on_click2)
on_click_button2.place(x=space+135, y=10)
# add a text box using tkinter's Text function and place it at (340,55). The text box is of height 165pixels.

encrypt_button = Button(app, text="ENCRYPT", bg='white', fg='black', width=15, command=lambda : encode(load_image1,load_image2))
encrypt_button.place(x=width-130, y=10)#20 is the button width
app.mainloop()

