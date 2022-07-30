import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
import effects
from inspect import getmembers, isfunction

class App():
    def __init__(self, root):
        super().__init__()
        
        self.root = tk.Toplevel(root)
        self.root.title("ImageEdit Macro Creator v1.0.1")
        
        self.last_effect_listbox = 1
        
        self.effects = getmembers(effects, isfunction)
        self.make_effects_list()
        
        self.effects_listbox = tk.Listbox(self.root)
        self.effects_listbox.grid(row=0, column=0)
        
        self.button_frame = tk.Frame(self.root)
        
        self.open_macro_button = tk.Button(self.button_frame, text="Open", command=self.open_macro, width=10)
        self.save_macro_button = tk.Button(self.button_frame, text="Save", command=self.save_macro, width=10)
        self.add_macro_button = tk.Button(self.button_frame, text="Add", command=self.add_macro, width=10)
        self.remove_macro_button = tk.Button(self.button_frame, text="Remove", command=self.remove_macro, width=10)
        self.clear_macro_button = tk.Button(self.button_frame, text="Clear", command=self.clear_macro, width=10)
        
        self.open_macro_button.grid(row=0, column=0)
        self.save_macro_button.grid(row=1, column=0)
        self.add_macro_button.grid(row=2, column=0)
        self.remove_macro_button.grid(row=3, column=0)
        self.clear_macro_button.grid(row=4, column=0)
        
        self.button_frame.grid(row=0, column=1)
        
        self.root.mainloop()
        
    def make_effects_list(self):
        self.effects_list = []
        for name, value in self.effects:
            if not name.startswith("_"): # __init__, _limit, etc
                self.effects_list.append(name)
        
    def open_macro(self):
        self.current_macro_dialog = filedialog.askopenfilename(defaultextension=".iem", filetypes=[("ImageEdit Macro", "*.iem"), ("All Files", "*.*")])
        if self.current_macro_dialog:
            try:
                f = open(self.current_macro_dialog, "r")
            except FileNotFoundError:
                messagebox.showerror(title="Error", message="File not found.")
            else:
                self.macro_instructions = f.readlines()
                f.close()
                
                self.last_effect_listbox = len(self.macro_instructions)
                self.effects_listbox.insert(*self.macro_instructions)
    
    def save_macro(self):
        self.save_macro_dialog = filedialog.asksaveasfilename(defaultextension=".iem", filetypes=[("ImageEdit Macro", "*.iem"), ("All Files", "*.*")])
        if self.save_macro_dialog:
            with open(self.save_macro_dialog, "w") as f:
                write_to_f = ""
                for i in range(self.last_effect_listbox):
                    write_to_f += f"{self.effects_listbox.get(i)}\n"
                write_to_f = write_to_f[:-1]
                
                f.write(write_to_f)
        
    def add_macro_to_listbox(self):
        insert_str = self.add_macro_variable.get()
        for slider in self.sliders:
            insert_str += f" {slider.get()}"
    
        self.effects_listbox.insert(self.last_effect_listbox, insert_str)
        self.last_effect_listbox += 1
        
    def remove_macro(self):
        for i in self.effects_listbox.curselection():
            self.effects_listbox.delete(i)
            self.last_effect_listbox -= 1

    def exit_add_macro(self):
        self.add_macro_window.destroy()
        self.add_macro_window.quit()
        
    def sliders_add_macro(self, a, b, c):
        macro_name = self.add_macro_variable.get()
        params = eval(f"effects.{macro_name}.__code__.co_varnames") # gets all the parameters (arguments) that the function wants
    
        self.slider_frame.grid_forget()
    
        self.sliders = []
        self.labels = []
        self.slider_frame = tk.Frame(self.add_macro_window)
        
        for param in params:
            if not param.startswith("image"):
                self.sliders.append(tk.Scale(self.slider_frame, from_=0, to=effects._limit(macro_name, param), orient="horizontal"))
                self.labels.append(tk.Label(self.slider_frame, text=param))
                
        slider_row = 1
        for slider, label in zip(self.sliders, self.labels):
            label.grid(row=slider_row - 1, column=0)
            slider.grid(row=slider_row, column=0)
            slider_row += 2
            
        self.slider_frame.grid(row=2, column=0)
        
    def add_macro(self):
        self.add_macro_window = tk.Toplevel()
        
        self.slider_frame = tk.Frame(self.add_macro_window)
        
        self.add_macro_label = tk.Label(self.add_macro_window, text="Add macro:")
        
        self.add_macro_variable = tk.StringVar()
        self.add_macro_option_menu = tk.OptionMenu(self.add_macro_window, self.add_macro_variable, *self.effects_list)
        
        self.add_macro_variable.trace("w", self.sliders_add_macro)
        
        self.add_macro_buttons = tk.Frame(self.add_macro_window)
        
        self.add_macro_ok = tk.Button(self.add_macro_buttons, text="OK", command=self.add_macro_to_listbox)
        self.add_macro_cancel = tk.Button(self.add_macro_buttons, text="Cancel", command=self.exit_add_macro)
        
        self.add_macro_label.grid(row=0, column=0)
        self.add_macro_option_menu.grid(row=1, column=0)
        
        self.add_macro_ok.grid(row=0, column=0)
        self.add_macro_cancel.grid(row=0, column=1)
        
        self.add_macro_buttons.grid(row=3, column=0)
        
        self.add_macro_window.mainloop()
        
    def clear_macro(self):
        self.effects_listbox.delete(0, tk.END)
        
def execute(root):
    App(root)

def do_macro(image, filename):
    with open(f"./macros/{filename}.iem", "r") as f:
        instructions = f.readlines()
        
    for instr in instructions:
        if " " in instr:
            image_perform = f"effects.{instr.split(' ')[0]}"
            image_perform_args = [int(x) for x in instr.split(" ")[1:]]
            image = eval(f"effects.{instr.split(' ')[0]}")(image, *image_perform_args)
        else:
            image = eval(f"effects.{instr}")(image)
    return image
