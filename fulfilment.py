try:
    from data_controller import test,fetch_orders,get_name,update_status,fetch_status,move_order_complete
except ImportError or ModuleNotFoundError:
    sys.exit("Unable to connect to data_controller. Ensure you have the whole project open in your explorer.")

import customtkinter
import sys
from PIL import Image
font = "Comic Sans MS"

try:
    test()
except FileNotFoundError as e:
    sys.exit(e)

class HeaderFrame(customtkinter.CTkFrame): 
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)    
        self.logo = customtkinter.CTkImage(light_image=Image.open("assets/logo.png"), size=(70,70))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text="")
        self.logo_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.title = customtkinter.CTkLabel(self, text="Order Fufillment", font = (font,42))
        self.title.grid(row= 0, column=1 )


class BodyFrame(customtkinter.CTkScrollableFrame): #Main body frame that holds all of the order that need to be fufilled
    def __init__(self, master, orders,**kwargs):
        super().__init__(master, **kwargs)
        self.orders = orders
        self.grid_columnconfigure(0, weight=1)
        for count in range (len(self.orders)):
            self.orderFrame = OrderFrame(self,orders[count], fg_color = "green")
            self.orderFrame.grid(row = count, column = 0, padx = 2, pady = 2, sticky = "EW")   


class OrderFrame(customtkinter.CTkFrame): #This is the order frame, this contains all of the parts of the order and allows the kitchen staff to tick off parts of orders as they get compleated
    def __init__(self,master,order,**kwargs):
        super().__init__(master,**kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        self.order = order
        self.items = []

        self.order_id_label = customtkinter.CTkLabel(self, text=("ID: "+str(self.order[0])), font = (font, 42))
        self.order_id_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "NW")
        self.order_noID = self.order[1:]

        self.send_button = customtkinter.CTkButton(self, text  = "Send Out Order", state= "disabled", fg_color="yellow", font = (font,24), text_color= "black", command= self.send_event)
        self.send_button.grid(row = len(self.order_noID)+2, column = 0, padx = 10, pady = 10, sticky = "NEWS")
        self.done = True
        for count in range (len(self.order_noID)): #Add all of the order items to the frame
            self.item_frame = ItemFrame(self,self.order_noID[count],self.items,fg_color = "transparent")
            self.item_frame.grid(row = count+1, column = 0, padx = 5, pady = 5 ,sticky = "NSEW")
            self.items.append(self.item_frame)
            if self.item_frame.item_made_checkbox.get() == "notdone":
                self.done = False
        if self.done == True: #Unlocks the send out order button when all checkboxes are clicked.
            self.send_button.configure(state = "normal")
            

    def send_event(self): #Sends out the order and disables everything possible untill next refresh
        self.order_id_label.configure(text = "SENT OUT", text_color = "grey")
        self.send_button.configure(text = "SENT OUT", state = "disabled")
        for itemFrame in self.items:
            itemFrame.item_made_checkbox.configure(state = customtkinter.DISABLED)
        move_order_complete(self.order[0])
        
        
class ItemFrame(customtkinter.CTkFrame):
    def __init__(self,master,item,items,**kwargs):
        super().__init__(master, **kwargs)
        self.item = item
        name = get_name(str(self.item[0]))
        name = name[0][0]
        self.items = items
        self.item_made_checkbox = customtkinter.CTkCheckBox(self, text = (name+"            "+self.item[1]), font = (font, 28), onvalue="done", offvalue= "notdone", command= self.checkbox_event )
        self.item_made_checkbox.grid(row = 0, column = 0, padx = 5, pady = 5)
        if fetch_status(self.master.order[0], self.item[0])[0][0] == "made":
            self.item_made_checkbox.select()  #This allows the program to continue from last state after crash or program stop.


    def checkbox_event(self):
        self.done = True
        if self.item_made_checkbox.get() == "done":
            update_status(self.master.order[0],self.item[0],"made") #Updates each item in the database as it is checked off
        if self.item_made_checkbox.get() == "notdone":
            update_status(self.master.order[0],self.item[0],"received")
        
        
        for frame in self.items:
            if frame.item_made_checkbox.get() == "notdone":
                self.done = False
        if self.done == True:
            self.master.send_button.configure(state = "normal") #Every checkbopx event it makes sure all the checkboxes are filled, if they are the button activates.
        if self.done == False:
            self.master.send_button.configure(state = "disabled")
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.orders = fetch_orders()

        #Setup Window
        self.title("Order Progress")
        self.geometry("1280x720")
        self._set_appearance_mode("light")

        #Grid Weight
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1), weight=1)

        #Elements
        def refresh_body(self): #This refreshes the data every 10 seconds. It is not regualar as it is noticable when it updates so I decided it better not to do it regually.
            self.bodyFrame.destroy()
            self.orders = fetch_orders()
            self.bodyFrame = BodyFrame(self,self.orders ,fg_color = "blue")
            self.bodyFrame.grid(row = 1, column = 0, sticky = "NEWS")
            self.after(10000, lambda: refresh_body(self))
        
        self.headerFrame = HeaderFrame(self, fg_color = "red")
        self.headerFrame.grid(row = 0, column = 0, sticky = "NEW")

        self.bodyFrame = BodyFrame(self,self.orders ,fg_color = "blue")
        self.bodyFrame.grid(row = 1, column = 0, sticky = "NEWS")
        refresh_body(self)


app = App()
app.mainloop()