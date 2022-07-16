from PIL import Image, ImageTk, ImageStat
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
import effects
from inspect import getmembers, isfunction

class App():
    def __init__(self):
        super().__init__()
        
        self.root = tk.Tk()
        self.root.title("ImageEdit v1.0")
        
        self.root.resizable(False, False)
        
        self.menubar = tk.Menu(self.root)
        
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menubar)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Resize", command=self.resize_menu)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Stats", command=self.image_stats)

        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        
        self.root.config(menu=self.menubar)
        
        self.image_frame = tk.Frame(self.root, bg="gray38", width=800, height=800)
        self.image_frame.grid(row=0, column=0)

        self.show_image = None

        self.image_label = tk.Label(self.image_frame, image=self.show_image)
        self.image_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.button_bg_frame = tk.Frame(self.root, bg="gray67", width=800 + 20, height=200 + 20)
        self.button_canvas = tk.Canvas(self.button_bg_frame)
        self.button_frame = tk.Frame(self.button_canvas)
        
        self.button_scrollbar = tk.Scrollbar(self.button_bg_frame, orient="horizontal", command=self.button_canvas.xview)
        
        self.button_canvas.configure(xscrollcommand=self.button_scrollbar.set)
        
        self.button_scrollbar.grid(row=1, column=0, columnspan=7)
        
        self.effects = getmembers(effects, isfunction)
        self.buttons = []
        
        self.current_image = filedialog.askopenfilename()
        if self.current_image:
            self.current_image = Image.open(self.current_image)
            
        self.resize_image()
        
        self.add_buttons()
        
        self.button_bg_frame.grid(row=1, column=0)
        self.button_canvas.grid(row=0, column=0)
        self.button_frame.grid(row=0, column=0)
        
        self.button_frame.bind("<Configure>", self.scroll)
        
        self.button_canvas.create_window((0,0), window=self.button_frame, anchor='nw')
        
        self.root.mainloop()

    def undo(self):
        image = self.current_image
        self.current_image = self.last_image
        self.last_image = image
        self.resize_image()
        self.render_image()
        
    def keep_aspect_ratio(self, entry1, entry2):
        try:
            self.resize_dimension_1 = int(entry1.get())
            self.resize_dimension_2 = int(entry2.get())
        except ValueError:
            if entry1.get() != "" and entry2.get() != "":
                messagebox.showerror(message="You must enter an integer!", title="Error")
                entry1.set("")
                entry2.set("")
        else:
            if self.keep_aspect_ratio_var.get() == 1:
                if entry1 == self.width_sv:
                    self.modify_percent = self.resize_dimension_1 / self.current_image.width
                    self.resize_dimension_2 *= self.modify_percent
                    entry2.set(str(round(self.resize_dimension_2)))
                else:
                    self.modify_percent = self.resize_dimension_2 / self.current_image.height
                    self.resize_dimension_1 *= self.modify_percent
                    entry1.set(str(round(self.resize_dimension_1)))
                
    def resize(self):
        self.current_image = self.current_image.resize((int(self.width_entry.get()), int(self.height_entry.get())))
        
        self.resize_window.destroy()
        
        self.resize_image()
        self.render_image()

    def resize_menu(self):
        self.resize_window = tk.Toplevel(self.root)
        
        self.resolution_frame = tk.Frame(self.resize_window)
        
        self.width_sv = tk.StringVar()
        self.height_sv = tk.StringVar()
        self.width_entry = tk.Entry(self.resolution_frame, textvariable=self.width_sv)
        self.height_entry = tk.Entry(self.resolution_frame, textvariable=self.height_sv)
        
        self.x_label = tk.Label(self.resolution_frame, text="x")
        
        self.checkbutton_frame = tk.Frame(self.resize_window)
        
        self.keep_aspect_ratio_var = tk.IntVar()
        self.keep_aspect_ratio_checkbutton = tk.Checkbutton(self.checkbutton_frame, onvalue=1, offvalue=0, variable=self.keep_aspect_ratio_var)
        self.keep_aspect_ratio_label = tk.Label(self.checkbutton_frame, text="Keep aspect ratio (doesn't work)")
        
        self.width_sv.trace("w", lambda *args: self.keep_aspect_ratio(self.width_sv, self.height_sv))
        self.height_sv.trace("w", lambda *args: self.keep_aspect_ratio(self.height_sv, self.width_sv))
        
        self.resize_button_frame = tk.Frame(self.resize_window)
        
        self.resize_ok = tk.Button(self.resize_button_frame, text="OK", command=self.resize)
        self.resize_cancel = tk.Button(self.resize_button_frame, text="Cancel", command=self.resize_window.destroy)
        
        self.resize_label = tk.Label(self.resize_window, text="Enter the new size of the image:")
        self.resize_label.grid(row=0, column=0)
        
        self.width_entry.grid(row=0, column=0)
        self.height_entry.grid(row=0, column=2)
        self.x_label.grid(row=0, column=1)
        
        self.resolution_frame.grid(row=1, column=0)
        
        self.keep_aspect_ratio_checkbutton.grid(row=0, column=0)
        self.keep_aspect_ratio_label.grid(row=0, column=1)
        
        self.resize_ok.grid(row=0, column=0)
        self.resize_cancel.grid(row=0, column=1)
        
        self.resize_button_frame.grid(row=3, column=0)
        
        self.checkbutton_frame.grid(row=2, column=0)
        
    def image_stats(self):
        self.stat = ImageStat.Stat(self.current_image)
        
        self.stat_window = tk.Toplevel(self.root)
        self.stat_label = tk.Label(self.stat_window, text=f"Extrema: {self.stat.extrema}\nTotal pixels: {self.stat.count}\nSum of all pixels: {self.stat.sum}\nSquared sum of all pixels: {self.stat.sum2}\nAverage (mean) pixel level: {self.stat.mean}\nMedian pixel level: {self.stat.median}\nRMS: {self.stat.rms}\nVariance: {self.stat.var}\nStandard deviation: {self.stat.stddev}")
        
        self.stat_ok = tk.Button(self.stat_window, text="OK", command=self.stat_window.destroy)
        
        self.stat_label.grid(row=0, column=0)
        self.stat_ok.grid(row=1, column=0)
        
    def scroll(self, e):
        self.button_canvas.configure(scrollregion=self.button_canvas.bbox("all"), width=self.new_width, height=80)
        
    def open_image(self):
        self.current_image = filedialog.askopenfilename()
        if self.current_image:
            self.current_image = Image.open(self.current_image)
            
        self.resize_image()
        
    def save_image(self):
        self.save_image = filedialog.asksaveasfilename()
        if self.save_image:
            self.current_image.save(self.save_image)
        
    def render_image(self):
        self.image_label.config(image=self.show_image)
        
    def resize_image(self):
        """makes the image fit the boundaries (800x800, sorry 4k users, but I have a 4:3 monitor)."""
    
        self.original_width = self.current_image.width
        self.original_height = self.current_image.height
        
        self.modify_percent = 1 # value * 1 does nothing. it is faster than checking if this value is False and blah blah blah
        # TODO: make the boundaries changeable by user
        if self.original_width > 800:
            self.modify_percent = self.original_width / 800 # how much times is original larger than
        elif self.original_height > 800:
            self.modify_percent = self.original_height / 800
            
        # division because modify_percent is always 1 or larger
        self.new_width = round(self.original_width / self.modify_percent)
        self.new_height = round(self.original_height / self.modify_percent)
        
        # this could happen on very thin images (like 4000px height 1px width), but nobody will edit them...
        if self.new_width == 0: self.new_width = 1
        if self.new_height == 0: self.new_height = 1
        
        # self.current_image = self.current_image.convert("RGBA")
        
        self.show_image = self.current_image.resize((self.new_width, self.new_height))
        self.show_image = ImageTk.PhotoImage(self.show_image)
        
        self.render_image()
        
    def add_buttons(self):
        i = 0
        for name, value in self.effects:
            if not name.startswith("_"): # __init__, _limit, etc
                self.buttons.append(tk.Button(self.button_frame, text=name, command=lambda c=i: self.button_onclick(c), width=10, height=5))
                i += 1
                
        button_column = 0
        for button in self.buttons:
            button.grid(row=0, column=button_column)
            button_column += 1
            
    def reset_buttons(self):
        i = 0
        for name, value in self.effects:
            if not name.startswith("_"): # __init__, _limit, etc
                self.buttons[i].configure(text=name, command=lambda c=i: self.button_onclick(c))
                i += 1
            
    def button_onclick(self, number):
        self.clicked_button = self.buttons[number]
        
        for name, value in self.effects:
            if name == self.clicked_button["text"]:
                self.clicked_button_val = value
                
                self.last_image = self.current_image
                self.current_image = value(self.current_image) # image changes here
                break
                
        self.clicked_button_text = self.clicked_button["text"]

        self.resize_image()
        self.render_image()
                
        self.reset_buttons()

        if len(self.clicked_button_val.__code__.co_varnames) != 1:
            self.clicked_button.configure(text="options", command=self.button_options)

    def apply_options(self):
        self.args = ""

        for slider in self.sliders:
            self.args += f"{slider.get()},"

        self.args = self.args[:len(self.args) - 1]
        self.current_image = eval(f"self.clicked_button_val(self.last_image, {self.args})")

        self.resize_image()
        self.render_image()
        
    def turn_off_options(self):
        self.current_image = self.last_image
        self.options_window.destroy()
        
        self.resize_image()
        self.render_image()
        
    def apply_and_close_options(self):
        self.apply_options()
        self.options_window.destroy()
        
    def button_options(self):
        params = self.clicked_button_val.__code__.co_varnames # gets all the parameters (arguments) that the function wants
        
        self.options_window = tk.Toplevel(self.root)
        
        self.sliders = []
        self.labels = []
        for param in params:
            if not param.startswith("image"):
                self.sliders.append(tk.Scale(self.options_window, from_=0, to=effects._limit(self.clicked_button_text, param), orient="horizontal"))
                self.labels.append(tk.Label(self.options_window, text=param))
                
        slider_row = 1
        for slider, label in zip(self.sliders, self.labels):
            label.grid(row=slider_row - 1, column=0)
            slider.grid(row=slider_row, column=0)
            slider_row += 2
        
        self.options_button_frame = tk.Frame(self.options_window)
        self.options_button_frame.grid(row=slider_row + 1, column=0)
        
        self.options_ok = tk.Button(self.options_button_frame, text="OK", command=self.apply_options)
        self.options_ok_and_close = tk.Button(self.options_button_frame, text="OK & Close", command=self.apply_and_close_options)
        self.options_cancel = tk.Button(self.options_button_frame, text="Cancel", command=self.turn_off_options)
        self.options_ok.grid(row=0, column=0)
        self.options_ok_and_close.grid(row=0, column=1)
        self.options_cancel.grid(row=0, column=2)
        
if __name__ == "__main__":
    App()
