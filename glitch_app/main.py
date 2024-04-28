from model.nets import Generator

from tkinter import *
# To override the basic Tk widgets, the import should follow the Tk import
from tkinter import filedialog, font
from tkinter import ttk
from PIL import Image, ImageTk
import torch
import torchvision.transforms as tt

def get_generated(x, g, f=tt.ToPILImage(), origin_size=[256, 256] ):
    generated = g(transforms(x)[None, :])
    with torch.no_grad():
        gsize = generated.size()
        generated = generated.cpu().view(3, gsize[2], gsize[3])*0.5+0.5 
    return f(generated).resize(origin_size)
    
mean = (0.5, 0.5, 0.5)
std = (0.5, 0.5, 0.5)
transforms = tt.Compose( [
                          #tt.Resize([256, 256]),
                          tt.ToTensor(),
                          tt.Normalize(mean=mean, std=std)
 ] )
Generator_x = Generator()
    
root = Tk()      
root.resizable(False, False)
root.iconbitmap('images/icon.ico')
root.title('GlithMaker')
WIDTH = 800
HEIGHT = 450
canvas = Canvas(root, width = WIDTH, height = HEIGHT, bg='white')      
canvas.pack()     


modes_places = iter([(35, 350), (35, 390), (135, 350), (135, 390)])
selected_mode = StringVar()
s = ttk.Style()
s.configure('TRadiobutton', font=('Helvetica', 12),  background='white')

for mode in [ 'Light', 'Medium', 'Hard', 'Art']:
    mode_button =  ttk.Radiobutton(root, text=mode, variable=selected_mode, value=mode)
    if mode == 'Light':
        mode_button.invoke()
    place = next(modes_places)
    mode_button.place(x=place[0], y=place[1])


def save_output_1() -> None:
    '''Function for save_output button'''
    filename = filedialog.asksaveasfile(mode='wb', defaultextension=".png")
    if not filename:
        return
    img1_out_raw.save(filename)

def open_img_1() -> None:
    '''Function for open_image button'''
    global img1, img1_out, img1_out_raw, btn_img1_save
    try:
        btn_img1_save.place_forget()
    except NameError:
        pass
    try:
        btn_img1.place_forget()
        btn_img1_out.place_forget()
    except UnboundLocalError:
        pass
    
    input1 = filedialog.askopenfilename(title='choose a photo')
    
    img1 = Image.open(input1).convert('RGB')
    origin_size = img1.size
    
    mode = selected_mode.get()
    checkpoint = torch.load(f'model/Generator_{mode.lower()}_params.pth', map_location=torch.device('cpu'))
    Generator_x.load_state_dict(checkpoint)
    Generator_x.eval()
    
    img1_out_raw = get_generated(img1, Generator_x, origin_size=origin_size)
    if origin_size[0] >= origin_size[1]:
        button_size = (256, int(origin_size[1]*256/origin_size[0]))
        img1 = img1.resize(button_size) 
    else:
        button_size = (int(origin_size[0]*256/origin_size[1]), 256)
        img1 = img1.resize(button_size) 
    img1_out = ImageTk.PhotoImage(get_generated(img1, Generator_x, origin_size=button_size), master=root)
    img1 = ImageTk.PhotoImage(img1, master=root) 
    canvas.image = img1
    canvas.image = img1_out
    btn1.place_forget()
    
    btn_img1_save = Button(root, text='Save output', command=save_output_1)
    btn_img1_save.place(x=WIDTH - WIDTH//5 -25, y=HEIGHT-100)
    
    btn_img1 = Button(root, image=img1, command=open_img_1)
    btn_img1_out = Button(root, image=img1_out, command=ignore)
    btn_img1.place(x=25, y=50)
    btn_img1_out.place(x=WIDTH - WIDTH//5-256/2, y=50)
    canvas.pack()
    
    
button_img = Image.open("images/Button_sample.png").resize( (256, 256))
button_img = ImageTk.PhotoImage(button_img, master=root) 
out_img = Image.open("images/Button_sample.png").resize( (256, 256))
out_img = ImageTk.PhotoImage(out_img, master=root) 
btn1 = Button(root, image=button_img, command=open_img_1)

def ignore(): pass
output = Button(root, image=out_img, command=ignore)

btn1.place(x=25, y=50)
output.place(x=WIDTH - WIDTH//5-256/2, y=50)


img3 = Image.open("images/Arrow.png")
img3 = img3.rotate(-90, fillcolor='white', expand=True).resize( (WIDTH//4, HEIGHT//4) )
img3 = ImageTk.PhotoImage(img3, master=root) 


canvas.create_text((WIDTH - WIDTH//5, 30), text='Your output here', font=font.Font(family='Helvetica',size=16))
canvas.create_text((WIDTH//5, 30), text='Glitch photo', font=font.Font(family='Helvetica',size=16))

def Open():
    top = Toplevel()
    # Add a label to the TopLevel, just like you would the root window
    Instruction_img = ImageTk.PhotoImage(Image.open("images/Instruction.png"), master=root) 
    canvas.image = Instruction_img
    lbl = Label(top, image=Instruction_img)
    lbl.pack()
Instruction_btn = Button(root, text="?", font=font.Font(family='Helvetica',size=16), command=Open)
Instruction_btn.place(x=WIDTH/2, y=HEIGHT-50)

canvas.create_image(WIDTH//2.07, HEIGHT/2.5, image=img3)            

root.mainloop()

