
import customtkinter
from PIL import Image
from data_controller import test,retreiveItems,createOrder
font = "Comic Sans MS"
try:
    test()
except:
    raise Exception("Unable to connect to data_controller. Ensure you have the whole project open in your explorer and that you have run launcher.py in order to create orders.db")


class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self,master, **kwargs):
        super().__init__(master,**kwargs)
        self.grid_columnconfigure((0,1,2), weight=1)    
        self.logo = customtkinter.CTkImage(light_image=Image.open("assets/logo.png"), size=(70,70))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text="")
        self.logo_label.grid(row = 0, column = 0, padx = 5, sticky = "w")
        self.title = customtkinter.CTkLabel(self, text="Welcome to Fast Food", font = (font,42))
        self.title.grid(row= 0, column=1 )


class AddOrder(customtkinter.CTkFrame):
    def __init__(self,master,item ,**kwargs):
        super().__init__(master,**kwargs)
        self.quantity = 0
        self.item = item
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        self.price_label = customtkinter.CTkLabel(self, text=("£"+str(self.item[3])), font = (font,32))
        self.price_label.grid(row= 0,column = 0, columnspan = 3, padx = 40, pady = 20, sticky = "new")
        self.add_button = customtkinter.CTkButton(self, text = "Add to order", font = (font,24), fg_color="black" , text_color="white", hover_color="grey20",command=self.addToOrder)
        self.add_button.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = "news")

    def addToOrder(self):
        self.add_button.destroy()
        self.quantity = 1
        self.remove_button = customtkinter.CTkButton(self, text = "-", font = (font,16), fg_color="black", text_color="white", width= 40, hover_color="grey20", command= self.decreaseQuantity)
        self.remove_button.grid(row=1, column = 0)
        self.count_label = customtkinter.CTkLabel(self, text = str(self.quantity), font = (font,16),fg_color="black", text_color="white", corner_radius=5, width= 40)
        self.count_label.grid(row=1, column = 1, padx = 5)
        self.add_button = customtkinter.CTkButton(self, text = "+", font = (font,16),fg_color="black", text_color="white",  hover_color="grey20", width= 40, command= self.increaseQuantity)
        self.add_button.grid(row=1, column = 2)
        app.check_totals()

    def increaseQuantity(self):
        self.quantity +=1
        self.count_label.configure(text = str(self.quantity))
        app.check_totals()

    def decreaseQuantity(self):
        if self.quantity-1 == 0:
            self.remove_button.destroy()
            self.count_label.destroy()
            self.add_button.destroy()
            self.add_button = customtkinter.CTkButton(self, text = "Add to order", font = (font,24), fg_color="black" , text_color="white", hover_color="grey20",command=self.addToOrder)
            self.add_button.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = "news")
            self.quantity = 0
            app.check_totals()
        else:
            self.quantity -= 1
            self.count_label.configure(text = str(self.quantity))
            app.check_totals()

    def getInfo(self):
        return self.item[0],self.quantity


class MenubodyFrame(customtkinter.CTkFrame):
    def __init__(self,master,item, **kwargs):
        super().__init__(master,**kwargs)
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.image_label = customtkinter.CTkLabel(self, text= "Image", fg_color="orange", corner_radius= 5, font = (font, 32))
        self.image_label.grid(row = 0, rowspan = 2, column = 0, ipady = 65, ipadx = 35, padx = 10, pady = 10,sticky = "w")

        self.item_info = customtkinter.CTkFrame(self)
        self.item_info.grid(row = 0, column = 1, pady = 10, sticky = "nsew")
        self.item_info.grid_columnconfigure((0), weight=1)

        self.item_name = customtkinter.CTkLabel(self.item_info,text = item[1], font = (font,42))
        self.item_name.grid(row= 0, column = 0,pady = 10, padx = 5, sticky = "ew")

        self.item_name = customtkinter.CTkLabel(self.item_info,text = item[2], font = (font,24))
        self.item_name.grid(row= 1, column = 0,pady = 30, padx = 5, sticky = "ew")

        self.add_order = AddOrder(self,item ,fg_color = "pink")
        self.add_order.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "nse")


class BodyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self,master, items, **kwargs):
        super().__init__(master,**kwargs)
        #Hold the menu item frames#
        self.bodyFrames = []
        for count in range (len(items)):
            self.grid_columnconfigure((0), weight=1)
            self.menubodyFrame = MenubodyFrame(self, items[count], fg_color = "green")
            self.menubodyFrame.grid(row = count, column = 0, sticky = "ew", pady = 2)  
            self.bodyFrames.append(self.menubodyFrame)
    def return_items(self):
        return self.bodyFrames


class FooterFrame(customtkinter.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.totalPrice = 0
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)

        self.price_label = customtkinter.CTkLabel(self, text=f"Total: £{self.totalPrice}", font = (font,36),)
        self.price_label.grid(row = 0, column = 9, sticky = "nse")

        self.checkout_button = customtkinter.CTkButton(self,text="Pay",font=(font,36), fg_color="black", text_color="white", hover_color="grey20", command= lambda: App.checkout_popup(app))
        self.checkout_button.grid(row = 0, column = 10, padx = 10, pady = 10, sticky = "nse")#


class PaymentNotification(customtkinter.CTkToplevel):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.geometry("300x500")
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)
        self.label = customtkinter.CTkLabel(self,text="Please Pay for your order!", font = (font,24))
        self.label.grid(row = 0, column = 0)
        self.payButton = customtkinter.CTkButton(self,text="Click to pay!", font = (font,30), command= self.on_click)
        self.payButton.grid(row = 1, column = 0, sticky = "NSEW",padx = 20, pady = 20)

        self.transient(master)
        self.lift()
        self.grab_set()
        self.focus_force()

    def on_click(self):
        App.submit_order(app)
        self.destroy()

        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Setup Window
        self.title("Order Kiosk")
        self.geometry("1280x720")
        self._set_appearance_mode("light")

        #Grid Weight
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)

        #Check items to display.
        self.items = retreiveItems()

        #Elements
        self.headerFrame = HeaderFrame(self, fg_color = "red")
        self.headerFrame.grid(row = 0, column = 0, columnspan = 1, sticky= "nsew")

        self.bodyFrame = BodyFrame(self, self.items, fg_color = "blue")
        self.bodyFrame.grid(row = 1, column = 0, rowspan = 2, sticky = "nsew")

        self.footerFrame = FooterFrame(self, fg_color = "yellow")
        self.footerFrame.grid(row = 3, column = 0, sticky = "nsew")

        self.orderConfimation_window = None

    def check_totals(self):
        self.order = []
        for item in self.bodyFrame.return_items():
            item.id, item.quantity = item.add_order.getInfo()
            if item.quantity != 0:
                self.order.append([item.id, item.quantity])

        #calculate Price
        self.totalPrice = 0
        for item in self.order:
            for item2 in self.items:
                if item[0] == item2[0]:
                    self.totalPrice += (item2[3])*item[1]
        self.totalPrice = round(self.totalPrice,2)
        self.footerFrame.price_label.configure(text = "Total: £"+ str(self.totalPrice))

    def checkout_popup(self):
        if self.orderConfimation_window is None or not self.orderConfimation_window.winfo_exists():
            self.orderConfimation_window = PaymentNotification(self)
        else:
            self.orderConfimation_window.focus()

    def submit_order(self):
        self.order = []
        for item in self.bodyFrame.return_items():           
            item.id, item.quantity = item.add_order.getInfo()
            if item.quantity != 0:
                self.order.append([item.id, item.quantity])
        createOrder(self.order)


app = App()
app.mainloop()

