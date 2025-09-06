from data_controller import test,fetch_orders,get_name,update_status,fetch_status,move_order_complete
import customtkinter
from PIL import Image
font = "Comic Sans MS"

try:
    test()
except:
    raise Exception("Unable to connect to data_controller. Ensure you have the whole project open in your explorer and that you have run launcher.py in order to create orders.db")

class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)    
        self.logo = customtkinter.CTkImage(light_image=Image.open("assets/logo.png"), size=(70,70))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text="")
        self.logo_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.title = customtkinter.CTkLabel(self, text="Order Fufillment", font = (font,42))
        self.title.grid(row= 0, column=1 )


class BodyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, orders,**kwargs):
        super().__init__(master, **kwargs)
        self.orders = orders
        self.grid_columnconfigure(0, weight=1)
        for count in range (len(self.orders)):
            self.orderFrame = OrderFrame(self,orders[count], fg_color = "green")
            self.orderFrame.grid(row = count, column = 0, padx = 2, pady = 2, sticky = "EW")   


class OrderFrame(customtkinter.CTkFrame):
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
        for count in range (len(self.order_noID)):
            self.item_frame = ItemFrame(self,self.order_noID[count],self.items,fg_color = "transparent")
            self.item_frame.grid(row = count+1, column = 0, padx = 5, pady = 5 ,sticky = "NSEW")
            self.items.append(self.item_frame)
            if self.item_frame.item_made_checkbox.get() == "notdone":
                self.done = False
        if self.done == True:
            self.send_button.configure(state = "normal")
            




    def send_event(self):
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
            update_status(self.master.order[0],self.item[0],"made")
        if self.item_made_checkbox.get() == "notdone":
            update_status(self.master.order[0],self.item[0],"received")
        
        
        for frame in self.items:
            if frame.item_made_checkbox.get() == "notdone":
                self.done = False
        if self.done == True:
            self.master.send_button.configure(state = "normal")
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

        def refresh_body(self):
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