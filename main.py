from PIL import Image, ImageTk, ImageStat, UnidentifiedImageError
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog, ttk
import effects, macrocreator, kernelcreator
from inspect import getmembers, isfunction
import glob

class App():
    def __init__(self):
        super().__init__()
        
        self.max_image_pixels_number = Image.MAX_IMAGE_PIXELS

        self.version = "v1.2"
        
        self.root = tk.Tk()
        self.root.title(f"ImageEdit {self.version}")

        self.read_settings()
        
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
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Resize", command=self.resize_menu)
        self.edit_menu.add_command(label="Crop", command=self.crop_menu)
        self.edit_menu.add_command(label="Tile", command=self.tile_menu)
        self.edit_menu.add_command(label="Repeat", command=self.repeat_menu)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Settings", command=self.settings_menu)

        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        
        self.view_menu = tk.Menu(self.menubar)
        self.view_menu.add_command(label="Stats", command=self.image_stats)
        self.view_menu.add_command(label="ImageEdit Macro Creator", command=lambda: macrocreator.execute(self.root))
        self.view_menu.add_command(label="ImageEdit Kernel Creator", command=lambda: kernelcreator.execute(self.root))
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Reload buttons", command=self.reload_buttons)
        
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        
        self.root.config(menu=self.menubar)
        
        self.image_frame = tk.Frame(self.root, bg="gray38", width=800, height=800)
        self.image_frame.grid(row=0, column=0)

        self.show_image_default = True
        self.show_image = Image.new("RGB", (200, 200))

        self.image_label = tk.Label(self.image_frame, image=ImageTk.PhotoImage(self.show_image))
        self.image_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.macros_buttons = [] 
        self.effects_buttons = []
        self.kernels_buttons = []

        self.sliders = []
        self.labels = []
        
        self.effects = getmembers(effects, isfunction)
        self.macros = glob.glob("./macros/*.iem")
        self.kernels = glob.glob("./kernels/*.iek")

        self.make_effects_list()
        self.make_macros_list()
        self.make_kernels_list()
        
        self.button_notebook = ttk.Notebook(self.root, height=100)
        
        self.current_image_dialog_response = self.open_image()
        if self.show_image_default:
            self.current_image = self.show_image

            self.resize_image()
            self.render_image()
        
        self.effects_button_bg_frame = tk.Frame(self.button_notebook, bg="gray67", width=820, height=220)
        self.effects_button_canvas = tk.Canvas(self.effects_button_bg_frame)
        self.effects_button_frame = tk.Frame(self.effects_button_canvas)
        
        self.effects_button_scrollbar = tk.Scrollbar(self.effects_button_bg_frame, orient="horizontal", command=self.effects_button_canvas.xview)
        
        self.effects_button_canvas.configure(xscrollcommand=self.effects_button_scrollbar.set)
        
        self.effects_button_scrollbar.grid(row=1, column=0)
        
        self.macros_button_bg_frame = tk.Frame(self.button_notebook, bg="gray67", width=820, height=220)
        self.macros_button_canvas = tk.Canvas(self.macros_button_bg_frame)
        self.macros_button_frame = tk.Frame(self.macros_button_canvas)
        
        self.macros_button_scrollbar = tk.Scrollbar(self.macros_button_bg_frame, orient="horizontal", command=self.macros_button_canvas.xview)
        
        self.macros_button_canvas.configure(xscrollcommand=self.macros_button_scrollbar.set)
        
        self.macros_button_scrollbar.grid(row=1, column=0)
        
        self.kernels_button_bg_frame = tk.Frame(self.button_notebook, bg="gray67", width=820, height=220)
        self.kernels_button_canvas = tk.Canvas(self.kernels_button_bg_frame)
        self.kernels_button_frame = tk.Frame(self.kernels_button_canvas)
        
        self.kernels_button_scrollbar = tk.Scrollbar(self.kernels_button_bg_frame, orient="horizontal", command=self.kernels_button_canvas.xview)
        
        self.kernels_button_canvas.configure(xscrollcommand=self.kernels_button_scrollbar.set)
        
        self.kernels_button_scrollbar.grid(row=1, column=0)
        
        self.add_effects_buttons()
        
        self.effects_button_canvas.grid(row=0, column=0)
        self.effects_button_frame.grid(row=0, column=0)
        
        self.effects_button_frame.bind("<Configure>", self.scroll_effects)
        
        self.effects_button_canvas.create_window((0, 0), window=self.effects_button_frame, anchor='nw')
            
        self.add_macros_buttons()
            
        self.macros_button_canvas.grid(row=0, column=0)
        self.macros_button_frame.grid(row=0, column=0)
        
        self.macros_button_frame.bind("<Configure>", self.scroll_macros)
        
        self.macros_button_canvas.create_window((0, 0), window=self.macros_button_frame, anchor='nw')
        
        self.add_kernels_buttons()
        
        self.kernels_button_canvas.grid(row=0, column=0)
        self.kernels_button_frame.grid(row=0, column=0)
        
        self.kernels_button_frame.bind("<Configure>", self.scroll_kernels)
        
        self.kernels_button_canvas.create_window((0, 0), window=self.kernels_button_frame, anchor='nw')
            
        self.button_notebook.add(self.effects_button_bg_frame, text="Effects")
        self.button_notebook.add(self.macros_button_bg_frame, text="Macros")
        self.button_notebook.add(self.kernels_button_bg_frame, text="Kernels")
            
        self.button_notebook.grid(row=1, column=0)
        
        self.root.mainloop()

    def make_effects_list(self):
        self.effects_list = []
        for name, value in self.effects:
            if not name.startswith("_"): # __init__, _limit, etc
                self.effects_list.append(name)

    def make_macros_list(self):
        self.macros_list = []
        for name in self.macros:
            if "\\" in name:
                self.macros_list.append(name.split("\\")[-1][:-4])
            else:
                self.macros_list.append(name.split("/")[-1][:-4])

        self.macros_list = sorted(self.macros_list) # too lazy to implement sorting

    def make_kernels_list(self):
        self.kernels_list = []
        for name in self.kernels:
            if "\\" in name:
                self.kernels_list.append(name.split("\\")[-1][:-4])
            else:
                self.kernels_list.append(name.split("/")[-1][:-4])

        self.kernels_list = sorted(self.kernels_list) # too lazy to implement sorting

    def repeat_menu_change_list(self, *args):
        self.choose_repeat_actual.grid_forget()
        self.choose_repeat_actual = eval(f"self.choose_repeat_{self.choose_repeat_type_var.get()}s_optionmenu") # avoid ifs or something, idk
        self.choose_repeat_actual.grid(row=0, column=2)

    def repeat_menu_add_options(self, *args):
        for slider, label in zip(self.sliders, self.labels):
            slider.grid_forget()
            label.grid_forget()
            
        if self.choose_repeat_type_var.get() == "effect":
            params = eval(f"effects.{self.choose_repeat_actual_var.get()}").__code__.co_varnames # gets all the parameters (arguments) that the function wants

            self.sliders = []
            self.labels = []
            for param in params:
                if not param.startswith("image"):
                    self.sliders.append(tk.Scale(self.choose_repeat_options, from_=0, to=effects._limit(self.choose_repeat_actual_var.get(), param), orient="horizontal"))
                    self.labels.append(tk.Label(self.choose_repeat_options, text=param))
                
            slider_row = 1
            for slider, label in zip(self.sliders, self.labels):
                label.grid(row=slider_row - 1, column=0)
                slider.grid(row=slider_row, column=0)
                slider_row += 2

    def repeat_menu_quit(self):
        self.current_image = self.last_image

        self.repeat_menu_window.destroy()
        self.repeat_menu_window.quit()

    def repeat_effect(self):
        self.last_image = self.current_image

        if self.choose_repeat_type_var.get() == "effect":
            for i in range(self.choose_repeat_times.get()):
                self.clicked_button_val = eval(f"effects.{self.choose_repeat_actual_var.get()}")
                self.apply_options()
        elif self.choose_repeat_type_var.get() == "macro":
            for i in range(self.choose_repeat_times.get()):
                self.current_image = macrocreator.do_macro(self.current_image, self.choose_repeat_actual_var.get())
        elif self.choose_repeat_type_var.get() == "kernel":
            for i in range(self.choose_repeat_times.get()):
                self.current_image = kernelcreator.do_kernel(self.current_image, self.choose_repeat_actual_var.get())

        self.resize_image()
        self.render_image()

        self.repeat_menu_window.destroy()
        self.repeat_menu_window.quit()

    def repeat_menu(self):
        self.repeat_menu_window = tk.Toplevel(self.root)
        self.repeat_menu_window.title("Repeat...")

        self.choose_repeat_frame = tk.Frame(self.repeat_menu_window)

        self.choose_repeat_label = tk.Label(self.choose_repeat_frame, text="Repeat")

        self.choose_repeat_type_var = tk.StringVar()
        self.choose_repeat_type = tk.OptionMenu(self.choose_repeat_frame, self.choose_repeat_type_var, *["effect", "macro", "kernel"]) # type of stuff to repeat

        self.choose_repeat_type_var.trace("w", self.repeat_menu_change_list)

        self.choose_repeat_actual_var = tk.StringVar()

        self.choose_repeat_effects_optionmenu = tk.OptionMenu(self.choose_repeat_frame, self.choose_repeat_actual_var, *self.effects_list)
        self.choose_repeat_macros_optionmenu = tk.OptionMenu(self.choose_repeat_frame, self.choose_repeat_actual_var, *self.macros_list)
        self.choose_repeat_kernels_optionmenu = tk.OptionMenu(self.choose_repeat_frame, self.choose_repeat_actual_var, *self.kernels_list)

        self.choose_repeat_actual = self.choose_repeat_effects_optionmenu

        self.choose_repeat_actual_var.trace("w", self.repeat_menu_add_options)

        self.choose_repeat_label.grid(row=0, column=0)
        self.choose_repeat_type.grid(row=0, column=1)
        self.choose_repeat_actual.grid(row=0, column=2)

        self.choose_repeat_options = tk.Frame(self.repeat_menu_window) # used for effect options, that's why is it empty
        self.choose_repeat_options.grid(row=2, column=0)

        self.choose_repeat_times_frame = tk.Frame(self.repeat_menu_window)
        self.choose_repeat_times_label = tk.Label(self.choose_repeat_times_frame, text="How much times?")
        self.choose_repeat_times = tk.Scale(self.choose_repeat_times_frame, from_=0, to=100, orient="horizontal")

        self.choose_repeat_times_label.grid(row=0, column=0)
        self.choose_repeat_times.grid(row=1, column=0)

        self.choose_repeat_button_frame = tk.Frame(self.repeat_menu_window)

        self.choose_repeat_ok = tk.Button(self.choose_repeat_button_frame, text="OK", command=self.repeat_effect)
        self.choose_repeat_cancel = tk.Button(self.choose_repeat_button_frame, text="Cancel", command=self.repeat_menu_quit)

        self.choose_repeat_ok.grid(row=0, column=0)
        self.choose_repeat_cancel.grid(row=0, column=1)

        self.choose_repeat_frame.grid(row=0, column=0)
        self.choose_repeat_times_frame.grid(row=1, column=0)
        self.choose_repeat_button_frame.grid(row=3, column=0)

        self.repeat_menu_window.mainloop()
        
    def reload_buttons(self):
        self.effects_buttons = []
        self.macros_buttons = []
        self.kernels_buttons = []
        
        import effects
        self.macros = glob.glob("./macros/*.iem")
        self.kernels = glob.glob("./kernels/*.iek")
        
        self.add_effects_buttons()
        self.add_macros_buttons()
        self.add_kernels_buttons()
        
    def show_image_tab(self):
        if self.last_tab_frame != None: self.last_tab_frame.grid_forget()
    
        self.image_tab_frame = tk.Frame(self.settings_window)
        
        self.max_image_pixels_number_frame = tk.Frame(self.image_tab_frame)
        self.max_image_pixels_number_entry = tk.Entry(self.max_image_pixels_number_frame)
        self.max_image_pixels_number_entry.insert(0, f"{self.max_image_pixels_number}")
        self.max_image_pixels_number_label = tk.Label(self.max_image_pixels_number_frame, text="Maximum pixels in an image: ")
        
        self.max_image_pixels_number_entry.grid(row=0, column=1)
        self.max_image_pixels_number_label.grid(row=0, column=0)
        
        self.max_image_pixels_number_frame.grid(row=0, column=0)
        
        self.image_tab_frame.grid(row=0, column=1)
        
        self.last_tab_frame = self.image_tab_frame
        
    def show_display_tab(self):
        if self.last_tab_frame != None: self.last_tab_frame.grid_forget()
    
        self.display_tab_frame = tk.Frame(self.settings_window)
        
        self.resize_image_max_width_frame = tk.Frame(self.display_tab_frame)
        self.resize_image_max_width_entry = tk.Entry(self.resize_image_max_width_frame)
        self.resize_image_max_width_entry.insert(0, f"{self.resize_image_max_width}")
        self.resize_image_max_width_label = tk.Label(self.resize_image_max_width_frame, text=f"Maximum width when showing image: ")
        
        self.resize_image_max_height_frame = tk.Frame(self.display_tab_frame)
        self.resize_image_max_height_entry = tk.Entry(self.resize_image_max_height_frame)
        self.resize_image_max_height_entry.insert(0, f"{self.resize_image_max_height}")
        self.resize_image_max_height_label = tk.Label(self.resize_image_max_height_frame, text=f"Maximum height when showing image: ")
        
        self.resize_image_min_width_frame = tk.Frame(self.display_tab_frame)
        self.resize_image_min_width_entry = tk.Entry(self.resize_image_min_width_frame)
        self.resize_image_min_width_entry.insert(0, f"{self.resize_image_min_width}")
        self.resize_image_min_width_label = tk.Label(self.resize_image_min_width_frame, text=f"Minimum width when showing image: ")
        
        self.resize_image_min_height_frame = tk.Frame(self.display_tab_frame)
        self.resize_image_min_height_entry = tk.Entry(self.resize_image_min_height_frame)
        self.resize_image_min_height_entry.insert(0, f"{self.resize_image_min_height}")
        self.resize_image_min_height_label = tk.Label(self.resize_image_min_height_frame, text=f"Minimum height when showing image: ")
        
        self.resize_image_max_width_entry.grid(row=0, column=1)
        self.resize_image_max_width_label.grid(row=0, column=0)
        
        self.resize_image_max_height_entry.grid(row=0, column=1)
        self.resize_image_max_height_label.grid(row=0, column=0)
        
        self.resize_image_min_width_entry.grid(row=0, column=1)
        self.resize_image_min_width_label.grid(row=0, column=0)
        
        self.resize_image_min_height_entry.grid(row=0, column=1)
        self.resize_image_min_height_label.grid(row=0, column=0)
        
        self.resize_image_max_width_frame.grid(row=0, column=0)
        self.resize_image_max_height_frame.grid(row=1, column=0)
        self.resize_image_min_width_frame.grid(row=2, column=0)
        self.resize_image_min_height_frame.grid(row=3, column=0)
        
        self.display_tab_frame.grid(row=0, column=1)
        
        self.last_tab_frame = self.display_tab_frame
        
    def show_other_tab(self):
        if self.last_tab_frame != None: self.last_tab_frame.grid_forget()
        
        self.other_tab_frame = tk.Frame(self.settings_window)
        
        self.show_full_image_path_frame = tk.Frame(self.other_tab_frame)
        self.show_full_image_path_var = tk.IntVar()
        self.show_full_image_path_checkbutton = tk.Checkbutton(self.show_full_image_path_frame, onvalue=1, offvalue=0, variable=self.show_full_image_path_var)
        self.show_full_image_path_label = tk.Label(self.show_full_image_path_frame, text="Show full image path")
        
        self.show_full_image_path_checkbutton.grid(row=0, column=0)
        self.show_full_image_path_label.grid(row=0, column=1)
        
        self.show_full_image_path_frame.grid(row=0, column=0)
        
        self.other_tab_frame.grid(row=0, column=1)
        
        self.last_tab_frame = self.other_tab_frame
        
    def apply_settings(self):
        try:
            self.resize_image_max_width = int(self.resize_image_max_width_entry.get())
        except:
            messagebox.showerror(title="Settings error", message="You entered the value for resize_image_max_width incorrectly.")
        try:
            self.resize_image_max_height = int(self.resize_image_max_height_entry.get())
        except:
            messagebox.showerror(title="Settings error", message="You entered the value for resize_image_max_height incorrectly.")
        try:
            self.resize_image_min_width = int(self.resize_image_min_width_entry.get())
        except:
            messagebox.showerror(title="Settings error", message="You entered the value for resize_image_min_width incorrectly.")
        try:
            self.resize_image_min_height = int(self.resize_image_min_height_entry.get())
        except:
            messagebox.showerror(title="Settings error", message="You entered the value for resize_image_min_height incorrectly.")
        try:
            self.max_image_pixels_number = Image.MAX_IMAGE_PIXELS = int(self.max_image_pixels_number_entry.get())
        except:
            messagebox.showerror(title="Settings error", message="You entered the value for Image.MAX_IMAGE_PIXELS incorrectly.")
        self.show_full_image_path = self.show_full_image_path_var.get()
            
        with open("./settings.txt", "w") as f:
            f.write(f"{self.resize_image_max_width}\n{self.resize_image_max_height}\n{self.resize_image_min_width}\n{self.resize_image_min_height}\n{self.max_image_pixels_number}\n{self.show_full_image_path}")
            
        self.settings_window.destroy()
        self.settings_window.quit()
        
    def turn_off_settings(self):
        self.settings_window.destroy()
        self.settings_window.quit()
        
    def settings_menu(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("ImageEdit Settings")
        
        self.settings_window_tab_frame = tk.Frame(self.settings_window)
        
        self.settings_window_image_button = tk.Button(self.settings_window_tab_frame, text="image", width=10, height=5, command=self.show_image_tab)
        self.settings_window_display_button = tk.Button(self.settings_window_tab_frame, text="display", width=10, height=5, command=self.show_display_tab)
        self.settings_window_other_button = tk.Button(self.settings_window_tab_frame, text="other", width=10, height=5, command=self.show_other_tab)
        
        self.settings_window_buttons = tk.Frame(self.settings_window)
        
        self.settings_window_apply = tk.Button(self.settings_window_buttons, text="Apply", command=self.apply_settings)
        self.settings_window_cancel = tk.Button(self.settings_window_buttons, text="Cancel", command=self.turn_off_settings)
        
        self.settings_window_image_button.grid(row=0, column=0)
        self.settings_window_display_button.grid(row=1, column=0)
        self.settings_window_other_button.grid(row=2, column=0)
        
        self.settings_window_apply.grid(row=0, column=0)
        self.settings_window_cancel.grid(row=0, column=1)
        
        self.settings_window_tab_frame.grid(row=0, column=0)
        self.settings_window_buttons.grid(row=1, column=1)
        
        self.last_tab_frame = None
        
        # loading all entries and tabs
        self.show_other_tab()
        self.show_image_tab()
        self.show_display_tab()
        
        self.settings_window.mainloop()
        
    def read_settings(self):
        try:
            with open("./settings.txt", "r") as f:
                self.settings_list = f.readlines()
        except:
            with open("./settings.txt", "w") as f:
                f.write("800\n800\n200\n200\n80000000\n0")
            self.resize_image_max_width = 800
            self.resize_image_max_height = 800
            self.resize_image_min_width = 200
            self.resize_image_min_height = 200
            self.max_image_pixels_number = Image.MAX_IMAGE_PIXELS = 80000000
            self.show_full_image_path = False
        else:
            try:
                self.resize_image_max_width = int(self.settings_list[0])
            except:
                self.resize_image_max_width = 800
                messagebox.showwarning(title="Settings error", message="There's an error with max_resize_image_width setting. The default value, 800, will be taken for this setting.")
            try:
                self.resize_image_max_height = int(self.settings_list[1])
            except:
                self.resize_image_max_height = 800
                messagebox.showwarning(title="Settings error", message="There's an error with max_resize_image_height setting. The default value, 800, will be taken for this setting.")
            try:
                self.resize_image_min_width = int(self.settings_list[2])
            except:
                self.resize_image_min_width = 200
                messagebox.showwarning(title="Settings error", message="There's an error with min_resize_image_width setting. The default value, 200, will be taken for this setting.")
            try:
                self.resize_image_min_height = int(self.settings_list[3])
            except:
                self.resize_image_min_height = 200
                messagebox.showwarning(title="Settings error", message="There's an error with min_resize_image_height setting. The default value, 200, will be taken for this setting.")
            try:
                self.max_image_pixels_number = Image.MAX_IMAGE_PIXELS = int(self.settings_list[4])
            except:
                self.max_image_pixels_number = Image.MAX_IMAGE_PIXELS = 80000000
                messagebox.showwarning(title="Settings error", message="There's an error with MAX_IMAGE_PIXELS setting. The value passed by PIL.Image will be used.")
            try:
                self.show_full_image_path = bool(self.settings_list[5])
            except:
                self.show_full_image_path = False
                messagebox.showwarning(title="Settings error", message="There's an error with show_full_image_path setting. The default value, False, will be used.")
            
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
                messagebox.showerror(message="You must enter an integer in both fields!", title="Error")
                entry1.set("")
                entry2.set("")
        else:
            if self.keep_aspect_ratio_var.get() == 1:
                if entry1 == self.width_sv:
                    self.aspect_ratio_modify_percent = self.current_image.width / self.resize_dimension_1 
                    self.resize_dimension_2 = self.current_image.height / self.aspect_ratio_modify_percent
                    entry2.set(str(round(self.resize_dimension_2)))
                else:
                    self.aspect_ratio_modify_percent = self.current_image.height / self.resize_dimension_2 
                    self.resize_dimension_1 = self.current_image.width / self.aspect_ratio_modify_percent
                    entry1.set(str(round(self.resize_dimension_1)))
                
    def resize(self):
        self.current_image = self.current_image.resize((int(self.width_entry.get()), int(self.height_entry.get())))
        
        self.resize_window.destroy()
        self.resize_window.quit()
        
        self.resize_image()
        self.render_image()
        
    def resize_window_quit(self):
        self.resize_window.destroy()
        self.resize_window.quit()

    def resize_menu(self):
        self.resize_window = tk.Toplevel(self.root)
        self.resize_window.title(f"Resize Image")
        
        self.resolution_frame = tk.Frame(self.resize_window)
        
        self.width_sv = tk.StringVar()
        self.height_sv = tk.StringVar()
        
        self.width_sv.set(self.current_image.width)
        self.height_sv.set(self.current_image.height)
        
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
        self.resize_cancel = tk.Button(self.resize_button_frame, text="Cancel", command=self.resize_window_quit)
        
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
        
        self.resize_window.mainloop()
        
    def return_selected_point(self):
        if self.selected_point == None:
            messagebox.showerror(message="You must select a point first!", title="Error")
        else:
            self.select_point_window.destroy()
            self.select_point_window.quit()
            
    def return_no_point(self):
        self.selected_point = None
        self.select_point_window.destroy()
        self.select_point_window.quit()
    
    def locate_selected_point(self, event):
        self.show_image_x_point = self.select_point_image.winfo_pointerx() - self.select_point_image.winfo_rootx()
        self.show_image_y_point = self.select_point_image.winfo_pointery() - self.select_point_image.winfo_rooty()
        
        # this might have some inaccuracies
        self.current_image_x_point = round(self.show_image_x_point * self.modify_percent)
        self.current_image_y_point = round(self.show_image_y_point * self.modify_percent)
        
        self.selected_point = (self.current_image_x_point, self.current_image_y_point)
        
        self.select_point_label.configure(text=f"Point located! The location is: {self.selected_point}")
        
    def select_point(self, point_description):
        self.select_point_window = tk.Toplevel(self.root)
        self.select_point_window.title(f"Selecting the {point_description} point")
        
        self.select_point_label = tk.Label(self.select_point_window, text=f"Select the {point_description} point:")
        self.select_point_image = tk.Label(self.select_point_window, image=self.show_image)
        
        self.select_point_buttons = tk.Frame(self.select_point_window)
        
        self.select_point_button_ok = tk.Button(self.select_point_buttons, text="OK", command=self.return_selected_point)
        self.select_point_button_cancel = tk.Button(self.select_point_buttons, text="Cancel", command=self.return_no_point)
        
        self.select_point_button_ok.grid(row=0, column=0)
        self.select_point_button_cancel.grid(row=0, column=1)
        
        self.select_point_label.grid(row=0, column=0)
        self.select_point_image.grid(row=1, column=0)
        
        self.select_point_buttons.grid(row=2, column=0)
        
        self.selected_point = None
        
        self.select_point_image.bind("<Button-1>", self.locate_selected_point)
        
        self.select_point_window.mainloop()
        
    def crop_menu(self):
        self.select_point("top left")
        self.topleft_point = self.selected_point
        if self.topleft_point == None:
            return None
            
        self.select_point("bottom right")
        self.bottomright_point = self.selected_point
        if self.bottomright_point == None:
            return None
        
        self.current_image = self.current_image.crop((self.topleft_point[0], self.topleft_point[1], self.bottomright_point[0], self.bottomright_point[1]))
        self.resize_image()
        self.render_image()
        
    def tile_window_quit(self):
        self.tile_window.destroy()
        self.tile_window.quit()
        
    def tile_image(self):
        try:
            self.tile_x = int(self.tile_entry_x.get())
            self.tile_y = int(self.tile_entry_y.get())
        except ValueError:
            messagebox.showerror(message="You must enter an integer in both fields!", title="Error")
            self.tile_entry_x.set("")
            self.tile_entry_y.set("")
        else:
            self.last_image = self.current_image
            self.current_image = Image.new("RGB", (self.tile_x, self.tile_y))
            for x in range(self.tile_x // self.last_image.width + 1):
                for y in range(self.tile_y // self.last_image.height + 1):
                    self.current_image.paste(self.last_image, (x * self.last_image.width, y * self.last_image.height))
            self.resize_image()
            self.render_image()
            
            self.tile_window.destroy()
            self.tile_window.quit()
        
    def tile_menu(self):
        self.tile_window = tk.Toplevel(self.root)
        self.tile_window.title("Tile Image")
        
        self.tile_label_x = tk.Label(self.tile_window, text="X: ")
        self.tile_entry_x = tk.Entry(self.tile_window)
        self.tile_label_y = tk.Label(self.tile_window, text="Y: ")
        self.tile_entry_y = tk.Entry(self.tile_window)
        
        self.tile_button_frame = tk.Frame(self.tile_window)
        
        self.tile_button_ok = tk.Button(self.tile_button_frame, text="OK", command=self.tile_image)
        self.tile_button_cancel = tk.Button(self.tile_button_frame, text="Cancel", command=self.tile_window_quit)
        
        self.tile_button_ok.grid(row=0, column=0)
        self.tile_button_cancel.grid(row=0, column=1)
        
        self.tile_label_x.grid(row=0, column=0)
        self.tile_entry_x.grid(row=0, column=1)
        self.tile_label_y.grid(row=1, column=0)
        self.tile_entry_y.grid(row=1, column=1)
        
        self.tile_button_frame.grid(row=2, column=0)
        
        self.tile_window.mainloop()
        
    def image_stats(self):
        self.stat = ImageStat.Stat(self.current_image)
        
        self.stat_window = tk.Toplevel(self.root)
        self.stat_window.title("Image Stats")
        self.stat_label = tk.Label(self.stat_window, text=f"Extrema: {self.stat.extrema}\nTotal pixels: {self.stat.count}\nSum of all pixels: {self.stat.sum}\nSquared sum of all pixels: {self.stat.sum2}\nAverage (mean) pixel level: {self.stat.mean}\nMedian pixel level: {self.stat.median}\nRMS: {self.stat.rms}\nVariance: {self.stat.var}\nStandard deviation: {self.stat.stddev}")
        
        self.stat_ok = tk.Button(self.stat_window, text="OK", command=self.stat_window.destroy)
        
        self.stat_label.grid(row=0, column=0)
        self.stat_ok.grid(row=1, column=0)
        
    def scroll_effects(self, e):
        self.effects_button_canvas.configure(scrollregion=self.effects_button_canvas.bbox("all"), width=self.new_width, height=80)
        
    def scroll_macros(self, e):
        self.macros_button_canvas.configure(scrollregion=self.macros_button_canvas.bbox("all"), width=self.new_width, height=80)
        
    def scroll_kernels(self, e):
        self.kernels_button_canvas.configure(scrollregion=self.kernels_button_canvas.bbox("all"), width=self.new_width, height=80)
        
    def open_image(self):
        Image.MAX_IMAGE_PIXELS = self.max_image_pixels_number
        self.current_image_dialog = filedialog.askopenfilename()
        
        if self.current_image_dialog:
            try:
                self.current_image = Image.open(self.current_image_dialog)
            except FileNotFoundError:
                messagebox.showerror(title="Error", message="File not found.")
            except UnidentifiedImageError:
                messagebox.showerror(title="Error", message="This image is invalid (or the image type isn't supported).")
            except Image.DecompressionBombWarning:
                if messagebox.askyesno(title="Decompression Bomb Warning", message=f"The image that you're opening exceeds {Image.MAX_IMAGE_PIXELS} pixels. Are you sure you want to continue?"):
                    Image.MAX_IMAGE_PIXELS = 0
                    self.current_image = Image.open(self.current_image)
                    messagebox.showwarning(title="Warning", message="The program might be unstable because of the image size. Be aware that the program isn't tested with such gigantic images. If any damage is done to the system, the program is not responsible for it.")
                    self.last_image = self.current_image
            except Image.DecompressionBombError:
                messagebox.showerror(title="Decompression Bomb Error", message=f"The image that you're opening has over twice as many pixels than the limit, {Image.MAX_IMAGE_PIXELS}. When opened, this image could cause crashes and disruption in the system by using too much memory.")
            else:
                self.show_image_default = False
                if self.show_full_image_path:
                    self.root.title(f"ImageEdit {self.version} - {self.current_image_dialog}")
                else:
                    self.root.title(f"ImageEdit {self.version} - {self.current_image_dialog.split('/')[-1]}")
                self.resize_image()
                self.last_image = self.current_image

        return self.current_image_dialog
        
    def save_image(self):
        self.save_image_dialog = filedialog.asksaveasfilename()
        if self.save_image_dialog:
            self.current_image.save(self.save_image_dialog)
        
    def render_image(self):
        self.image_label.config(image=self.show_image)
        
    def resize_image(self):
        self.original_width = self.current_image.width
        self.original_height = self.current_image.height
        
        self.modify_percent = 1 # value * 1 does nothing. it is faster than checking if this value is False and blah blah blah
        if self.original_width > self.resize_image_max_width:
            self.modify_percent = self.original_width / self.resize_image_max_width # how much times is original larger than
        elif self.original_height > self.resize_image_max_height:
            self.modify_percent = self.original_height / self.resize_image_max_height
        elif self.original_width < self.resize_image_min_width:
            self.modify_percent = self.original_width / self.resize_image_min_width
        elif self.original_height < self.resize_image_min_height:
            self.modify_percent = self.original_height / self.resize_image_min_height
            
        # division because modify_percent is always 1 or larger
        self.new_width = round(self.original_width / self.modify_percent)
        self.new_height = round(self.original_height / self.modify_percent)
        
        # this could happen on very thin images (like 4000px height 1px width), but nobody will edit them...
        if self.new_width == 0: self.new_width = 1
        if self.new_height == 0: self.new_height = 1
        
        self.button_notebook.configure(width=self.new_width)
        
        self.current_image = self.current_image.convert("RGB")
        
        self.show_image = self.current_image.resize((self.new_width, self.new_height))
        self.show_image = ImageTk.PhotoImage(self.show_image)
        
        self.render_image()
        
    def add_effects_buttons(self):
        i = 0
        for name, value in self.effects: # don't do effects_list here, because no value
            if not name.startswith("_"):
                self.effects_buttons.append(tk.Button(self.effects_button_frame, text=name, command=lambda c=i: self.effects_button_onclick(c), width=10, height=5))
                i += 1
                
        button_column = 0
        for button in self.effects_buttons:
            button.grid(row=0, column=button_column)
            button_column += 1
            
    def add_macros_buttons(self):
        i = 0
        for name in self.macros_list:
            self.macros_buttons.append(tk.Button(self.macros_button_frame, text=name, command=lambda c=i: self.macros_button_onclick(c), width=10, height=5))
            i += 1
                
        button_column = 0
        for button in self.macros_buttons:
            button.grid(row=0, column=button_column)
            button_column += 1

    def add_kernels_buttons(self):
        i = 0
        for name in self.kernels_list:
            self.kernels_buttons.append(tk.Button(self.kernels_button_frame, text=name, command=lambda c=i: self.kernels_button_onclick(c), width=10, height=5))
            i += 1
                
        button_column = 0
        for button in self.kernels_buttons:
            button.grid(row=0, column=button_column)
            button_column += 1
 
    def reset_buttons(self):
        i = 0
        for name, value in self.effects:
            if not name.startswith("_"): # __init__, _limit, etc
                self.effects_buttons[i].configure(text=name, command=lambda c=i: self.effects_button_onclick(c))
                i += 1
            
    def effects_button_onclick(self, number):
        self.effects_clicked_button = self.effects_buttons[number]
                
        self.clicked_button_text = self.effects_clicked_button["text"]
        self.clicked_button_val = eval(f"effects.{self.clicked_button_text}")
        
        self.last_image = self.current_image
        self.current_image = self.clicked_button_val(self.current_image)

        self.resize_image()
        self.render_image()
                
        self.reset_buttons()

        if len(self.clicked_button_val.__code__.co_varnames) != 1:
            self.effects_clicked_button.configure(text="options", command=self.button_options)
            
    def macros_button_onclick(self, number):
        self.macros_clicked_button = self.macros_buttons[number]
        
        self.last_image = self.current_image
        self.current_image = macrocreator.do_macro(self.current_image, self.macros_clicked_button["text"])
        
        self.resize_image()
        self.render_image()
        
    def kernels_button_onclick(self, number):
        self.kernels_clicked_button = self.kernels_buttons[number]
        
        self.last_image = self.current_image
        self.current_image = kernelcreator.do_kernel(self.current_image, self.kernels_clicked_button["text"])
        
        self.resize_image()
        self.render_image()

    def apply_options(self):
        self.args = ""

        for slider in self.sliders:
            self.args += f"{slider.get()},"

        self.args = self.args[:-1]
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
