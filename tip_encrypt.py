from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math

global path_image

space = 15
image_display_size = 720, 720

def on_click():
    # Step 1.5
    global path_image
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    path_image = filedialog.askopenfilename()
    # load the image using the path
    load_image = Image.open(path_image)
    # set the image into the GUI using the thumbnail function from tkinter
    load_image.thumbnail(image_display_size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    img.place(x=20, y=50)

def encrypt_data_into_image():
    # Step 2
    global path_image
    data = txt.get(1.0, "end-1c")
    # load the image
    img = cv2.imread(path_image)
    # break the image into its character level. Represent the characyers in ASCII.
    data = [format(ord(i), '08b') for i in data]
    _, width, _ = img.shape
    # algorithm to encode the image
    PixReq = len(data) * 3

    RowReq = PixReq/width
    RowReq = math.ceil(RowReq)

    count = 0
    charCount = 0
    # Step 3
    for i in range(RowReq + 1):
        # Step 4
        while(count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            # Step 5
            for index_k, k in enumerate(char):
                if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if(index_k % 3 == 2):
                    count += 1
                if(index_k == 7):
                    if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if(charCount*3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0
    # Step 6
    # Write the encrypted image into a new file
    path_to_save=filedialog.asksaveasfilename(defaultextension=".png",filetypes=(("png file", "*.png"),("jpg file", "*.jpg"),("All Files", "*.*")))
    # path_to_save=path_to_save if '.jpg' in path_to_save else path_to_save + '.jpg'
    cv2.imwrite(path_to_save, img)
    # Display the success label.
    success_label = Label(app, text="Encryption Successful!",
                bg='lavender', font=("Cascadia Code", 20))
    success_label.place(x=image_display_size[0]+200, y=450)

# Step 1
# Defined the TKinter object app with background lavender, title Encrypt, and app size 600*600 pixels.
app = Tk()
app.configure(background='lavender')
app.title("Encrypt Text into Image")
app.geometry('1485x800')
# create a button for calling the function on_click
on_click_button = Button(app, text="Select Image to hide Text into", bg='white', fg='black', command=on_click)
on_click_button.place(x=2*space-8, y=10, height = 25)
# add a text box using tkinter's Text function and place it at (340,55). The text box is of height 165pixels.
txt = Text(app, wrap=WORD, width=75, font=("Cascadia Code", 12))
txt.place(x=image_display_size[0]+3*space, y=50, height=300)

encrypt_button = Button(app, text="Encrypt and Save", bg='white', fg='black', command=encrypt_data_into_image)
encrypt_button.place(x=image_display_size[0]+310, y=360)

text_prompt_label = Label(app, text="Enter Text:",
            bg='lavender', font=("Cascadia Code", 15))
text_prompt_label.place(x=image_display_size[0]+3*space, y=12)
app.mainloop()

''' 
1.Load the image and write the text in the text box provided below
2.Convert the message into an array representation of the ASCII letters.
3.Compute the number of pixels required, which is equal to the 3 times the length of the array of ASCII letters
4.Number of rows required = number of pixels required / width of the image
5.Traversing the image row-wise, we will check for the following conditions:
    -Check the number of pixels traversed. If the bit is 1 and the pixel value is an even number, make it an odd number by subtracting 1. Similarly, if the bit is 0 and the pixel value is an odd number, make it an even number by subtracting 1.
    -Keep a count of the number of letters using the count variable.
    -If the index is 7, check if the next character exists. If yes, mark the EOF bit as 0 and continue. Else, mark as 1 and end.
6.We have successfully encrypted the image into the file.
'''