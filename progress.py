try:
    from data_controller import test,fetch_kitchen_ids,fetch_sent_ids,order_collected
except ImportError or ModuleNotFoundError:
    sys.exit("Unable to connect to data_controller. Ensure you have the whole project open in your explorer.")

import customtkinter
import sys
font = "Comic Sans MS"

try:
    test()
except FileNotFoundError as e:
    sys.exit(e)

class CookingItem(customtkinter.CTkFrame): #A frame that contains the order number of an item that is in the kitchen
    def __init__(self,master, id, **kwargs):
        super().__init__(master, **kwargs)#
        self.grid_columnconfigure(0, weight=1)
        self.id_label = customtkinter.CTkLabel(self, text=id, font = (font, 56))
        self.id_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "NEWS")


class CookedItem(customtkinter.CTkFrame): #A frame that contains the ID of an item that has been cooked
    def __init__(self,master, id, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.id = id
        self.id_label = customtkinter.CTkButton(self, text=self.id, font = (font, 56), fg_color="white", text_color="black", border_color= "white", hover_color="grey90", command= self.on_click)
        self.id_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "NEWS")

    def on_click(self): #This is effectivly the user collecting their order
        self.id_label.configure(text = "Collected",font = (font,42), state = "disabled")
        order_collected(self.id)


class CookingItemsFrame(customtkinter.CTkScrollableFrame): #This frame is a layout for all of the ID's that are being cooked.
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
 
        orders = fetch_kitchen_ids()
        print(orders)
        for count in range (len(orders)):
            print(count)
            itemFrame = CookingItem(self,id = orders[count][0] ,fg_color = "white")
            row = int((count/2))
            column = count-(2*row)
            itemFrame.grid(row = row, column = column, padx = 5, pady = 5, sticky= "NEWS")


class CookedItemsFrame(customtkinter.CTkScrollableFrame): #This frame is a layour for all of the ID's that are cooked.
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
 
        orders = fetch_sent_ids()
        print(orders)
        for count in range (len(orders)):
            print(count)
            itemFrame = CookedItem(self,id = orders[count][0] ,fg_color = "white")
            row = int((count/2))
            column = count-(2*row)
            itemFrame.grid(row = row, column = column, padx = 5, pady = 5, sticky= "NEWS")


class CookingFrame(customtkinter.CTkFrame): #Label at top of cooking frame
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)  

        self.label = customtkinter.CTkLabel(self,text="Please Wait", text_color="white", font = (font, 72))
        self.label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "NEW")
        self.itemsFrame = CookingItemsFrame(self, fg_color = "grey20")
        self.itemsFrame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "NSEW")


class CookedFrame(customtkinter.CTkFrame): #Label at the top of the cooked frame
    def __init__(self,master,**kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)

        self.label = customtkinter.CTkLabel(self,text="Please Collect", text_color="white", font = (font, 72))
        self.label.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "NEW")
        self.itemsFrame = CookedItemsFrame(self, fg_color = "grey20")
        self.itemsFrame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "NSEW")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Setup Window
        self.title("Fufillment")
        self.geometry("1280x720")
        self._set_appearance_mode("light")

        #Grid Weight
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        def refresh_body(self): #This refreshes the data every 10 seconds. It is not regualar as it is noticable when it updates so I decided it better not to do it regually.
            self.cookingFrame.destroy()
            self.cookedFrame.destroy()
            self.cookingFrame = CookingFrame(self, border_color = "white", fg_color = "grey20")
            self.cookingFrame.grid(row = 0, column = 0, sticky = "NEWS")
            self.cookedFrame = CookedFrame(self, border_color = "white", fg_color = "grey20")
            self.cookedFrame.grid(row = 0, column = 1, sticky = "NEWS")
            self.after(10000, lambda: refresh_body(self))


        #Elements
        self.cookingFrame = CookingFrame(self, border_color = "white", fg_color = "grey20")
        self.cookingFrame.grid(row = 0, column = 0, sticky = "NEWS")
        self.cookedFrame = CookedFrame(self, border_color = "white", fg_color = "grey20")
        self.cookedFrame.grid(row = 0, column = 1, sticky = "NEWS")
        refresh_body(self)


app = App()
app.mainloop()