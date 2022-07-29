from PIL import Image, ImageFilter
import tkinter as tk
from tkinter import filedialog, messagebox

class App():
    def __init__(self, root):
        super().__init__()
    
        self.root = tk.Toplevel(root)
        self.root.title("ImageEdit Kernel Creator v1.0")
        
        self.menubar = tk.Menu(self.root)
        
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label="Open", command=self.open_kernel)
        self.file_menu.add_command(label="Save", command=self.save_kernel)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        self.root.config(menu=self.menubar)
        
        self.buttons = []
        self.button_vars = []
        self.button_canvas = tk.Canvas(self.root)
        
        self.create_buttons(3)
        
        self.button_canvas.grid(row=0, column=0)
        
        self.separate_label = tk.Label(self.root, text=" ", width=1)
        self.separate_label.grid(row=1, column=0)
        
        self.size_button_frame = tk.Frame(self.root)
        
        self.size_button_3x3 = tk.Button(self.size_button_frame, text="3x3", command=lambda: self.create_buttons(3))
        self.size_button_5x5 = tk.Button(self.size_button_frame, text="5x5", command=lambda: self.create_buttons(5))
        
        self.size_button_3x3.grid(row=0, column=0)
        self.size_button_5x5.grid(row=0, column=1)
        
        self.size_button_frame.grid(row=2, column=0)
        
        self.root.mainloop()
        
    def open_kernel(self):
        self.open_kernel_dialog = filedialog.askopenfilename(defaultextension=".iek", filetypes=(("ImageEdit Kernel", "*.iek"), ("All Files", "*.*")))
        if self.open_kernel_dialog:
            try:
                f = open(self.current_macro_dialog, "r")
            except FileNotFoundError:
                messagebox.showerror(title="Error", message="File not found.")
            else:
                self.kernel_instructions = f.readlines()
                f.close()
                
                self.kernel_values = self.kernel_instructions[0].split(" ")
                for value, var in zip(self.kernel_values, self.button_vars):
                    var.set(int(value))
                
    def save_kernel(self):
        self.save_kernel_dialog = filedialog.asksaveasfilename(defaultextension=".iek", filetypes=(("ImageEdit Kernel", "*.iek"), ("All Files", "*.*")))
        if self.save_kernel_dialog:
            with open(self.save_kernel_dialog, "w") as f:
                write_to_file = ""
                for var in self.button_vars:
                    write_to_file += f"{var.get()} "
                write_to_file = write_to_file[:-1]
                    
                f.write(write_to_file)
                
    def create_buttons(self, w):
        for i in self.buttons:
            i.grid_forget()
    
        self.buttons = []
        self.button_vars = []

        k = 0
        for i in range(w):
            for j in range(w):
                button_var = tk.IntVar()
                button_var.set(0)
                self.button_vars.append(button_var)
                
                button = tk.Button(self.button_canvas, textvariable=self.button_vars[k], command=lambda c=k: self.button_vars[c].set(self.button_vars[c].get() + 1), width=5, height=3)
                
                button.bind("<Button-2>", lambda e, c=k: self.button_vars[c].set(self.button_vars[c].get() - 1))
                button.bind("<Button-3>", lambda e, c=k: self.button_vars[c].set(self.button_vars[c].get() - 1))
                button.grid(row=i, column=j)
                
                self.buttons.append(button)

                k += 1
                
def execute(root):
    App(root)
    
def do_kernel(image, filename):
    with open(f"./kernels/{filename}.iek", "r") as f:
        kernel_values = tuple([int(x) for x in f.read().split(" ")])
        if len(kernel_values) == 9: kernel_size = (3, 3)
        else: kernel_size = (5, 5)
    
    return image.filter(ImageFilter.Kernel(kernel_size, kernel_values))