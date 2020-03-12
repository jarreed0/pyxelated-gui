#NOTE: I almost never use python so ignore the bugs/disorganization/bad ethics :)

import os
import tkinter as tk
from pyxelate import Pyxelate
from skimage import io
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfile 
import argparse
import sys
import pathlib
from numpy import uint8
from skimage import transform
from PIL import ImageTk,Image

root = tk.Tk()
filename = None
scaling = 5
outfile = tk.StringVar()
canvas = tk.Canvas(root, width = 300, height = 300)  
saveas = None
color = tk.IntVar()
factor = tk.IntVar()
color.set(6)
factor.set(14)
cl = tk.Label(root, text = 'Color')
fl = tk.Label(root, text = 'Factor')
cent = tk.Entry(root,textvariable = color)
fent = tk.Entry(root,textvariable = factor)
opened = tk.StringVar()
opened.set("Pixelated\nPython class that downsamples images to pixel art.\n\nCreated by sedtth\nGUI by jarreed0\n\nhttps://github.com/sedthh/pyxelate")

def open_file(): 
    global filename
    global fn
    global canvas
    global outfile
    global saveas
    global cl
    global fl
    global cent
    global fent
    global factor
    global color
    global opened
    file=askopenfile(mode='r',filetypes=[("Image File",'.jpg')])
    if file is not None: 
        cl.pack()
        cent.pack()
        fl.pack()
        fent.pack()
        filename=file.name
        outfile.set("pyxed-" + os.path.splitext(os.path.basename(filename))[0] + ".png")
        opened.set(filename)
        fimg3 = Image.open(filename)
        fimg2 = fimg3.resize((300,300), resample=0)
        fimg = ImageTk.PhotoImage(fimg2)
        canvas.create_image(20,20, anchor=tk.NW, image=fimg)
        canvas.image = fimg
        canvas.pack(pady = 3)
        root.geometry('370x610')
        saveas = tk.StringVar()
        saveas.set(outfile.get())
        sent = tk.Entry(root,textvariable = saveas)
        px = tk.Button(root, text="Pyxelate", command=pyx_class)
        sb = tk.Button(root, text="Save As", command=save_class)
        px.pack(pady = 3)
        sb.pack(pady = 3)
        sent.pack(pady = 3)
        gen = tk.Button(root, text="Compare", command=get_class)
        gen.pack(pady = 3)

def get_class():
    global filename
    global outfile
    img = io.imread(filename)
    height, width, _ = img.shape
    p = Pyxelate(height // factor.get(), width // factor.get(), color.get(), 0)
    img_small = p.convert(img)
    _, axes = plt.subplots(1, 2, figsize=(16, 16))
    axes[0].imshow(img)
    axes[1].imshow(img_small)
    plt.show()


def save_class():
    global filename
    global scaling
    global outfile
    global canvas
    global saveas
    outfile.set(saveas.get())
    p = Pyxelate(1, 1, color.get(), 1, 1, 0)
    image = io.imread(filename)
    height, width, _ = image.shape
    p.height = height // factor.get()
    p.width = width // factor.get()
    pyxelated = p.convert(image)
    if scaling > 1:
        pyxelated = transform.resize(pyxelated, ((height // factor.get()) * scaling, (width // factor.get()) * scaling), anti_aliasing=False, mode='edge', preserve_range=True, order=0)
    io.imsave(outfile.get(), pyxelated.astype(uint8))
    fimg3 = Image.open(outfile.get())
    fimg2 = fimg3.resize((300,300), resample=0)
    fimg = ImageTk.PhotoImage(fimg2)
    canvas.create_image(20,20, anchor=tk.NW, image=fimg)
    canvas.image = fimg
    canvas.pack(pady = 3)
    fn = tk.Label(root, text = "Saved to " + outfile.get())
    fn.pack(pady = 3)

def pyx_class():
    global filename
    global scaling
    global outfile
    global canvas
    global saveas
    outfile.set("tmp-pyx.png")
    p = Pyxelate(1, 1, color.get(), 1, 1, 0)
    image = io.imread(filename)
    height, width, _ = image.shape
    p.height = height // factor.get()
    p.width = width // factor.get()
    pyxelated = p.convert(image)
    if scaling > 1:
        pyxelated = transform.resize(pyxelated, ((height // factor.get()) * scaling, (width // factor.get()) * scaling), anti_aliasing=False, mode='edge', preserve_range=True, order=0)
    io.imsave(outfile.get(), pyxelated.astype(uint8))
    fimg3 = Image.open(outfile.get())
    fimg2 = fimg3.resize((300,300), resample=0)
    fimg = ImageTk.PhotoImage(fimg2)
    canvas.create_image(20,20, anchor=tk.NW, image=fimg)
    canvas.image = fimg
    canvas.pack(pady = 3)
    os.remove(outfile.get())


root.geometry('370x175')
root.title('Pyxelate GUI')

btn = tk.Button(root, text ='Open', command = lambda:open_file()) 
btn.pack(side = tk.TOP, pady = 10)

desc = tk.Label(root, textvariable = opened)
desc.pack()

root.mainloop()
