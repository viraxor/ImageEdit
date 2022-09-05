import tkinter as tk

class Window():    
    def __init__(self, root, image, modify_percent, point_description):
        super().__init__()
        
        self.modify_percent = modify_percent
    
        self.select_point_window = tk.Toplevel(root)
        self.select_point_window.title(f"Selecting the {point_description} point")
            
        self.select_point_label = tk.Label(self.select_point_window, text=f"Select the {point_description} point:")
        self.select_point_image = tk.Label(self.select_point_window, image=image)
            
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

    def return_selected_point(self):
        if self.selected_point == None:
            messagebox.showerror(message="You must select a point first!", title="Error")
        else:
            self.select_point_window.destroy()
            self.select_point_window.quit()
            return self.selected_point
                
    def return_no_point(self):
        self.select_point_window.destroy()
        self.select_point_window.quit()
        return None
        
    def locate_selected_point(self, event):
        self.show_image_x_point = self.select_point_image.winfo_pointerx() - self.select_point_image.winfo_rootx()
        self.show_image_y_point = self.select_point_image.winfo_pointery() - self.select_point_image.winfo_rooty()
            
        # this might have some inaccuracies
        self.current_image_x_point = round(self.show_image_x_point * self.modify_percent)
        self.current_image_y_point = round(self.show_image_y_point * self.modify_percent)
            
        self.selected_point = (self.current_image_x_point, self.current_image_y_point)
            
        self.select_point_label.configure(text=f"Point located! The location is: {self.selected_point}")
