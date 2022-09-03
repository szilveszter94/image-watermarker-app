from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageFont, ImageDraw
import csv

# ------------------------------------------------- SET SCREEN ---------------------------------------------------- #
screen = Tk()
screen.config(padx=50, pady=30, bg='#323232')
screen.title('Watermarker')
COLOR = '#EFFFFD'

# ------------------------------------------------- SET VARIABLES ------------------------------------------------- #

# read all fonts from fonts.csv
fonts = []
with open('fonts.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        fonts.append(row)

# create font type array
font_type_list = []
for values in fonts[0]:
    font_type_list.append(values)

# create fontsize_values array
fontsize_value = ['Default']
for i in range(0, 501):
    fontsize_value.append(i)

# set the opacity values array
opacity_value = ['Default']
for i in range(0, 256):
    opacity_value.append(i)

# set the color array
color_list = ['Default', 'Write Hex color here']

# set the x coordinate default value
xcoord_value = ['Default']

# set the y coordinate default value
ycoord_value = ['Default']


# --------------------------------------------------- SET FUNCTIONS ------------------------------------------------ #

# get the font size from the input
def get_fontsize():
    size = font_size_value.get()
    if size == 'Default (40)':
        size = 40
    else:
        size = int(size)
    return size


# get the font type from the input
def get_font_type():
    font = font_type_input.get()
    if font == 'Default (arial)':
        font = 'arial'
    return font


# get the opacity value from the input
def get_opacity_value():
    opacity_val = opacity.get()
    if opacity_val == 'Default (128)':
        opacity_val = 128
    else:
        opacity_val = int(opacity_val)
    return opacity_val


# this function convert hex colors to rgb
def color_manager():
    list_rgb = []
    opacity_v = get_opacity_value()
    hex_color = color_input.get()
    if hex_color == 'Default (white)':
        list_rgb = [255, 255, 255, opacity_v]
    else:
        h = hex_color.lstrip('#')
        rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        for i in rgb:
            list_rgb.append(i)
        list_rgb.append(opacity_v)
    return tuple(list_rgb)


# select image file type
def select_file():
    filetypes = (
        ('JPEG', '*.jpeg'),
        ('JPEG', '*.jpg'),
        ('PNG', '*.png'),
        ('GIF', '*.gif'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    with Image.open(filename).convert("RGBA") as base:
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        # get a font
        font = get_font_type()
        size = get_fontsize()
        fnt = ImageFont.truetype(font, size)
        # get a drawing context
        d = ImageDraw.Draw(txt)
        # draw text, half opacity
        text = watermark_text.get()
        color = color_manager()
        # get the text coordinates
        xcor = xcoord.get()
        ycor = ycoord.get()
        if xcor == 'Default':
            xcor = base.size[0]
        if ycor == 'Default':
            ycor = base.size[1]
            # set default text position
            d.text((60, ycor - 60 - size), text, font=fnt, fill=color)
        else:
            # else set user's text coordinates
            d.text((int(xcor), int(ycor)), text, font=fnt, fill=color)
        # return the image with the text
        out = Image.alpha_composite(base, txt)
        image_size_value.config(text=f'{base.size[0]} x {base.size[1]} px')
        # show the final image
        out.show()


# --------------------------------------------------- SET UI ------------------------------------------------------- #

# set the text color label
color_label = Label(text="Color:", font=("Montserrat", 12, "bold"),
                    highlightthickness=0, bg='#323232', fg='#F76E11')
color_label.grid(column=0, row=5, pady=5)

# set the color input entry
color_input = ttk.Combobox(screen, values=color_list)
color_input.set("Default (white)")
color_input.grid(column=1, row=5, pady=5)

# set the font type label
font_type_label = Label(text="Choose font:", font=("Montserrat", 12, "bold"),
                        highlightthickness=0, bg='#323232', fg='#F76E11')
font_type_label.grid(column=2, row=3, padx=15, pady=5)

# set the font type entry combo box
font_type_input = ttk.Combobox(screen, values=font_type_list)
font_type_input.set("Default (arial)")
font_type_input.grid(column=3, row=3, pady=5)

# set the font size label
font_size_label = Label(text="Font size:", font=("Montserrat", 12, "bold"),
                        highlightthickness=0, bg='#323232', fg='#F76E11')
font_size_label.grid(column=0, row=3, pady=5)

# set the font size entry
font_size_value = ttk.Combobox(screen, values=fontsize_value)
font_size_value.set("Default (40)")
font_size_value.grid(column=1, row=3, pady=5)

# set the image size label
image_size_label = Label(text="Your image size:", font=("Montserrat", 12, "bold"),
                         highlightthickness=0, bg='#323232', fg='#F76E11')
image_size_label.grid(column=2, row=6, pady=5)

# set the image size value
image_size_value = Label(text="0 x 0 px", font=("Montserrat", 12, "bold"),
                         highlightthickness=0, bg='#323232', fg='#F76E11')
image_size_value.grid(column=3, row=6, pady=5)

# set the opacity label
opacity_label = Label(text="Opacity:", font=("Montserrat", 12, "bold"),
                      highlightthickness=0, bg='#323232', fg='#F76E11')
opacity_label.grid(column=0, row=4, pady=5)

# set the opacity entry
opacity = ttk.Combobox(screen, values=opacity_value)
opacity.set("Default (128)")
opacity.grid(column=1, row=4, pady=5)

# set title
title_label = Label(text="Image Watermarker", font=("Arvo", 26, "bold"), highlightthickness=0, fg='#F76E11')
title_label.config(bg='#323232')
title_label.grid(column=0, row=1, pady=30, columnspan=4)

# image upload label
upload_text = Label(text="Upload your photo:", font=("Montserrat", 12, "bold"),
                    highlightthickness=0, bg='#323232', fg='#F76E11')
upload_text.grid(column=0, row=6, pady=5)

# upload button
upload_button = Button(text="Open a file", width=10, height=1, font=("Montserrat", 11, "bold"),
                       bg='#FFBC80', fg='#F76E11', highlightthickness=0, command=select_file)
upload_button.grid(column=1, row=6, pady=10)

# set the watermark text label
watermark_label = Label(text="Watermark text:", font=("Montserrat", 15, "bold"),
                        highlightthickness=0, bg='#323232', fg='#F76E11')
watermark_label.grid(column=1, row=2, pady=15, padx=10)
# set the entry for get the text
watermark_text = Entry(font=("Montserrat", 12, "normal"), bg='#EEEDDE', fg='#141E27')
watermark_text.insert(END, 'Anonymus')
watermark_text.grid(column=2, row=2, pady=15)

# set the x coordinates label
xcoord_label = Label(text="Horizontal position of text (px):", font=("Montserrat", 12, "bold"),
                     highlightthickness=0, bg='#323232', fg='#F76E11')
xcoord_label.grid(column=2, row=4, padx=15, pady=5)

# set the x coordinate entry
xcoord = ttk.Combobox(screen, values=xcoord_value)
xcoord.set("Default")
xcoord.grid(column=3, row=4, pady=5)

# set the y coordinate label
ycoord_label = Label(text="Vertical position of text (px):", font=("Montserrat", 12, "bold"),
                     highlightthickness=0, bg='#323232', fg='#F76E11')
ycoord_label.grid(column=2, row=5, pady=5)

# set the y coordinate entry
ycoord = ttk.Combobox(screen, values=ycoord_value)
ycoord.set("Default")
ycoord.grid(column=3, row=5, pady=5)

# infinite loop for refresh the screen
screen.mainloop()
