"""
    Project title: Business Management and Sales program
    Author: Cathbert "GoofyCatt" Mutaurwa
    Project Commenced: 09/11/2021
    Description: This program's main function is to aid a developer to access code in infomation offline
"""

# --> Download required modules
import tkinter as tk
import os
from fontTools.ttLib import TTFont
from datetime import datetime
from pages.home import StartPage
from pages.customers import CustomersPage
from pages.pos import PosPage
from pages.diary import DiaryPage
from pages.snippets import SnippetsPage
from pages.dictionary import DictionaryPage
from pages.database_engine import UserDatabase
from pages.admin import AdminPage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import multiprocessing
import customtkinter
from PIL import Image


# --> Create base folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

userdb = UserDatabase()

# --> Set theme color and font
THEME_COLOR = '#004D54'
THEME_FONT = ("Century Gothic", 11)
entries_bg_color = "#003B4A"
entries_fg_color = "#ffff00"

# --> Loading and installing font
fonts_path = os.path.join(BASE_DIR, 'fonts')
for font in os.listdir(fonts_path):
    this_font = TTFont(os.path.join(fonts_path, font))
    this_font.save(os.path.join(fonts_path, font))


class MainView(customtkinter.CTkFrame):  # --> Main view class to control pages
    def __init__(self, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, *args, **kwargs)

        # --> Available pages
        p1 = StartPage(self)
        p2 = CustomersPage(self)
        p3 = PosPage(self)
        p4 = DiaryPage(self)
        p5 = SnippetsPage(self) 
        p6 = DictionaryPage(self)
        p7 = AdminPage(self)

        # --> Set theme color for the program's main view
        theme_color = ("#003B4A")

        # --> Create a frame that will hold navigation buttons
        button_frame = customtkinter.CTkFrame(self)
        button_frame.pack(side="top", fill="x", pady=5, padx=10, anchor=tk.N)

        # --> Create main container that will contain the pages
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        # --> Place pages in the container
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p7.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # --> Function to iterate through time and configure the time display label
        def clock_it(label):
            def clock():
                label.configure(text=f"{datetime.now().time().strftime('%H:%M:%S')}")
                label.after(1000, clock)

            clock()

        # --> This is the label to display time
        time_display_label = customtkinter.CTkLabel(button_frame, text='This is time', font=customtkinter.CTkFont('Digital-7 Mono', 25, 'bold'))
        time_display_label.pack(side=tk.LEFT, padx=4)
        clock_it(time_display_label)  # --> Now use clock it function to display time to the window
 
        # --> Load images
        customer_list_logo = customtkinter.CTkImage(Image.open("img/customers.png"))  # size=(self.width, self.height)
        pos_logo = customtkinter.CTkImage(Image.open("img/booking_logo.png"))  # size=(self.width, self.height)
        home_logo = customtkinter.CTkImage(Image.open("img/home.png"))  # size=(self.width, self.height)
        goofycoder_logo = customtkinter.CTkImage(Image.open("img/goofycoder_icon.png"))  # size=(self.width, self.height)
        events_logo = customtkinter.CTkImage(Image.open("img/event_logo.png"))  # size=(self.width, self.height)

        # --> Home page button
        home_button = customtkinter.CTkButton(button_frame, width=80, text="Home", image=home_logo, command=p1.show)
        home_button.image = home_logo
        home_button.pack(side="left", padx=2)

        # --> Home page button
        snippets_button = customtkinter.CTkButton(button_frame, width=80, text="Snippets", image=home_logo, command=p5.show)
        snippets_button.image = home_logo
        snippets_button.pack(side="left", padx=2)

         # --> Home page button
        dictionary_button = customtkinter.CTkButton(button_frame, width=80, text="Dictionary", image=home_logo, command=p6.show)
        dictionary_button.image = home_logo
        dictionary_button.pack(side="left", padx=2)

        # --> Customer list page button
        customer_list_button = customtkinter.CTkButton(button_frame, width=80, image=customer_list_logo, text="Customers", command=p2.show)
        customer_list_button.image = customer_list_logo
        customer_list_button.pack(side="left", padx=2)

        # --> pos page button
        pos_button = customtkinter.CTkButton(button_frame, width=80, image=pos_logo, text="POS", command=p3.show)
        pos_button.image = pos_logo
        pos_button.pack(side="left", padx=2)

        # --> Diary page button
        diary_button = customtkinter.CTkButton(button_frame, width=80, image=events_logo, text="Diary", command=p4.show)
        diary_button.image = events_logo
        diary_button.pack(side="left", padx=2)

        # --> Admin page button
        admin_button = customtkinter.CTkButton(button_frame, width=80, image=events_logo, text="Admin", command=p7.show)
        admin_button.image = events_logo
        admin_button.pack(side="left", padx=2)

        # --> Create a frame to hold the program title
        program_title_frame = customtkinter.CTkFrame(button_frame, width=40, bg_color='transparent')
        program_title_frame.pack(side="left")

        # --> Set program title
        program_title = customtkinter.CTkLabel(program_title_frame, text="\u00A9Brown Bear", font=customtkinter.CTkFont("Maiden Orange", 30))
        program_title.pack(padx=(10, 0), pady=(0,5))

        def change_appearance_mode(new_appearance_mode: str):
            customtkinter.set_appearance_mode(new_appearance_mode)

        appearance_mode_label = customtkinter.CTkLabel(button_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.pack(side="right", padx=2, pady=2)
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(button_frame, values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode)
        appearance_mode_optionemenu.pack(side="right", padx=2, pady=2)

        # --> Creator brand logo
        goofycoder_button = customtkinter.CTkButton(button_frame, text="info", image=goofycoder_logo, command=p1.show)
        goofycoder_button.image = goofycoder_logo
        goofycoder_button.pack(side="right", padx=2, pady=2)

        # --> Run first page
        p1.show()

        credits_state = customtkinter.CTkLabel(self, text='\u00A9 @goofycatt', font=customtkinter.CTkFont("Maiden "
                                                                                                          "Orange",
                                                                                                          20,))
        credits_state.pack(anchor='nw', padx=(10, 0), pady=(0,5))

if __name__ == "__main__":

    root = customtkinter.CTk()
    root.iconbitmap('img/icons/brown-bear.ico')
    root.title('\u00A9Brown Bear')

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.update()

    

    '''
    customtkinter.set_appearance_mode("dark") # system, dark, light
    customtkinter.set_default_color_theme("dark-blue") # blue, green, dark-blue

    authentication_frame = customtkinter.CTkFrame(root)
    authentication_frame.pack(pady=150, padx=200, fill='both', expand=True, anchor=tk.CENTER)
    
    def auth():
        # user = authenticate(username=username.get(), password=password.get())
        if True:

            multiprocessing.Process(target=username.destroy).run() 
            multiprocessing.Process(target=password.destroy).run()
            multiprocessing.Process(target=enter.destroy).run()
            multiprocessing.Process(target=authentication_frame.destroy).run()

            main = MainView(root)
            main.pack(side="top", fill="both", expand=True)
            root.update()
        else:
            username.delete(0, tk.END)
            password.delete(0, tk.END)
            msg.configure(text='Wrong Username or Password')

    title = customtkinter.CTkLabel(authentication_frame, text='ORIGAART SYSTEM 0.1', font=("Century Gothic", 35), corner_radius=8)
    title.pack(pady=12,padx=10)

    username = customtkinter.CTkEntry(authentication_frame, justify=tk.CENTER, width=250, placeholder_text = "Username", font=("Century Gothic", 25))
    username.pack(pady=12,padx=10)
    username.bind('<Enter>', lambda e: msg.configure(text=''))
    username.focus_set()
    
    password = customtkinter.CTkEntry(authentication_frame, show='*', justify=tk.CENTER, width=250, placeholder_text = "Password", font=("Century Gothic", 25))
    password.pack(pady=12,padx=10)
    username.bind('<Enter>', lambda e: msg.configure(text=''))

    enter = customtkinter.CTkButton(authentication_frame, text='Login', command=auth, font=("Century Gothic", 25))
    enter.pack(pady=12,padx=10)

    msg = customtkinter.CTkLabel(authentication_frame, text='')
    msg.pack(pady=12,padx=10)
    
    root.wm_geometry("1000x600")
    root.resizable(False, False)
    root.mainloop()
    '''
    root.wm_geometry("1000x600")
    # root.resizable(False, False)
    root.mainloop()
