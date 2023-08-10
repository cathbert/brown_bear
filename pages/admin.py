import tkinter as tk
import time
from . import base
import customtkinter
from tkinter import ttk, IntVar, StringVar
from tkinter import messagebox
from datetime import datetime
from random import randint
from datetime import datetime
import random
import string
from pages.database_engine import DictionaryDatabase, WikipediaDatabase, WorldHistoryDictionaryDatabase
from PIL import Image
import threading
import os
from mutagen.mp3 import MP3
from tkinter import filedialog
import tkinter.messagebox
from ttkthemes import themed_tk as theme_tk
from pygame import mixer

db = DictionaryDatabase()
wikidb = WikipediaDatabase()
whdd = WorldHistoryDictionaryDatabase()

class AdminPage(base.Page):
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)

        # main csp label frame
        main_label_frame = customtkinter.CTkFrame(self)
        main_label_frame.pack(side=tk.TOP, fill="x", anchor=tk.N)

        logo = customtkinter.CTkImage(Image.open("icons/csp_face_logo.png"))

        #lebel in top frame
        title_label = customtkinter.CTkLabel(main_label_frame, text='Admin Page', compound=tk.LEFT, image=logo, font=customtkinter.CTkFont("Maiden Orange", 30, "bold"))
        title_label.pack(expand=True)

        # ---> MAIN WIDGETS FRAME
        main_widgets_frame = customtkinter.CTkFrame(self)
        main_widgets_frame.pack(side=tk.TOP, fill="both", expand=True, anchor=tk.N)

        # ---> PRODUCTS FRAME
        products_frame = customtkinter.CTkFrame(main_widgets_frame,border_width=5)
        products_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # notbook widget tabarent
        tabs_parent = customtkinter.CTkTabview(products_frame, border_color='white')
        tabs_parent.pack(fill="both", expand=True, padx=10, pady=10)
        
        # tab1234 in notbook wigget tab parent
        utilities_tab = tabs_parent.add("  Utilities  ")
        snippets_settings = tabs_parent.add("snippets_settings")
        dictionary_settings = tabs_parent.add("dictionary_settings")
        point_of_sale_settings = tabs_parent.add("point_of_sale_settings")
        diary_settings = tabs_parent.add("diary_settings")

        # -------------------- UTILITIES SECTION BEGINS----------------------------------------------------
         # notbook widget tabarent
        utilities_tabs_parent = customtkinter.CTkTabview(utilities_tab, border_color='white')
        utilities_tabs_parent.pack(fill="both", expand=True, padx=10, pady=10)

        # utilities
        music_player = utilities_tabs_parent.add("music player")
        color_picker = utilities_tabs_parent.add("color picker")
        conversions = utilities_tabs_parent.add("conversions and caculations")
        todo = utilities_tabs_parent.add("todo")

        # -------------------- MUSIC PLAYER BEGINS----------------------------------------------------
        self.paused = False
        self.music_file = ""

        def show_Details(play_it):
            Main_text['text'] = 'Playing.....' + ' ' + os.path.basename(play_it)
            Main_text['anchor'] = 'e'
            file_ext = os.path.splitext(play_it)
            if file_ext[1] == '.mp3':  # To handle mp3 files using mutagen
                audio_lenth = MP3(play_it)
                total_lenth = audio_lenth.info.length
            else:  # to handle .wav,.ogg music file extensions
                a = mixer.Sound(play_it)
                total_lenth = a.get_length()

            m, s = divmod(total_lenth, 60)
            m = round(m)
            s = round(s)

            time_format = '{:02d}:{:02d}'.format(m, s)
            print(f"Show details {time_format}")
            Main_lenth['text'] = 'Duration : '+' '+time_format
            thread1 = threading.Thread(target = rem_count , args=(total_lenth,))
            thread1.start()


        def rem_count(total_lenth):
            curr_secs = 0
            while curr_secs <= total_lenth and mixer.music.get_busy():
                if self.paused:
                    continue
                else:
                    m, s = divmod(curr_secs, 60)
                    m = round(m)
                    s = round(s)
                    m1, s1 = divmod(total_lenth, 60)
                    m1 = round(m1)
                    s1 = round(s1)

                    time_format = '{:02d}:{:02d}'.format(m, s)
                    time_format1 = '{:02d}:{:02d}'.format(m1, s1)
                    current_lenth['text'] = 'Curent Duration : ' + ' ' + time_format
                    time.sleep(1)
                    curr_secs += 1
                    total_lenth -= 1
                    print(f"Rem count details {time_format}")


        def Play_music():
            play_it = ""
            if self.paused:
                mixer.music.unpause()
                # global self.paused = False
                status_bar['text'] = 'Playing Music.....' + ' ' + os.path.basename(self.music_file)
                status_bar['anchor'] = 'w'
                self.paused = False
            else:
                try:
                    Stop_music()
                    time.sleep(1)
                    song = play_list.curselection()
                    print(f"Now playing: {song}")
                    song = int(song[0])
                    play_it = music_list[song]

                    mixer.music.load(play_it)
                    mixer.music.play()
                    status_bar['text'] = 'Playing Music.....' + ' ' + os.path.basename(play_it)
                    status_bar['anchor'] = 'w'
                    show_Details(play_it)
                except Exception as e:
                    tkinter.messagebox.showerror("Error", f"{e} File Not Selected")


        def Stop_music():
            mixer.music.stop()
            status_bar['text'] = 'Music Stopped'
            status_bar['anchor'] = 'e'


        def pause_music():
            self.paused = True
            mixer.music.pause()
            status_bar['text'] = 'Music Paused...'
            status_bar['anchor'] = 'e'


        def rewind_music():
            Play_music()
            status_bar['text'] = 'Music Rewinded...'+' '+os.path.basename(self.music_file)
            status_bar['anchor'] = 'e'


        def close_window_fully():
            Stop_music()
            exit()


        def set_vol(val):
            vol = float(val)/100
            mixer.music.set_volume(vol)


        def about_us():
            tkinter.messagebox.showinfo(
                'Goofy BreezeRock', 'Powered By GoofyCatt')


        def browse_files():
            self.music_file = filedialog.askopenfilename()
            print(self.music_file)
            add_to_listbox(self.music_file)


        music_list = []


        def add_to_listbox(music_file):
            file_name = os.path.basename(music_file)
            index = 0
            play_list.insert(index, file_name)
            music_list.insert(index, music_file)
            play_list.pack()
            index += 1


        def delete_btn():
            song = play_list.curselection()
            song = int(song[0])
            play_list.delete(song)
            music_list.pop(song)


        def mute_music():
            global muted
            if muted:
                mixer.music.set_volume(.7)
                vol_button1.configure(image=pic5)
                scale1.set(70)
                muted = False

            else:
                mixer.music.set_volume(0)
                vol_button1.configure(image=pic4)
                scale1.set(0)
                muted = True


        def close_window_fully1():
            Stop_music()
            exit()


        muted = False


        # music_player = theme_tk.ThemedTk()
        # music_player.get_themes()
        # # themes : 'arc','radiance','breeze','ubuntu' etc
        # music_player.set_theme("breeze")
        # # creating toolbar
        # tool_bar = Menu(music_player)
        # music_player.config(menu=tool_bar)

        status_bar = customtkinter.CTkLabel(music_player, text="GoofyCatt BreezeRock", anchor=tk.W, font=customtkinter.CTkFont('verdana 10 italic'))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # # creating sub menus
        # sub_menu = Menu(tool_bar, tearoff=0)  # to remove dashed line from menu
        # tool_bar.add_cascade(label='File', menu=sub_menu)
        # sub_menu.add_command(label="Open", command=browse_files)
        # sub_menu.add_command(label="Exit", command=close_window_fully1)

        # sub_menu = Menu(tool_bar, tearoff=0)  # to remove dashed line from menu
        # tool_bar.add_cascade(label='Help', menu=sub_menu)
        # sub_menu.add_command(label="About Us ", command=about_us)


        mixer.init()

        # # music_player.geometry("600x300")
        # music_player.title("Rockerz")
        # music_player.iconbitmap("../icons/goofycatt.ico")
        top_frame = customtkinter.CTkFrame(music_player)
        top_frame.pack(fill=tk.X)
        bottom_frame = customtkinter.CTkFrame(music_player)
        bottom_frame.pack(expand=True, fill=tk.BOTH)


        right_frame = customtkinter.CTkFrame(bottom_frame)
        right_frame.pack(side=tk.RIGHT, padx=30, pady=20, fill=tk.Y)
        play_list = tk.Listbox(right_frame, width=100)
        play_list.pack(fill=tk.Y, expand=True)

        add_and_del_frame = customtkinter.CTkFrame(music_player)
        add_and_del_frame.pack(anchor=tk.S)
        add_btn = customtkinter.CTkButton(add_and_del_frame, text='ADD', command=browse_files)
        add_btn.pack(side=tk.LEFT, padx=3)

        del_btn = customtkinter.CTkButton(add_and_del_frame, text='DELETE', command=delete_btn)
        del_btn.pack(side=tk.LEFT)

        left_frame = customtkinter.CTkFrame(bottom_frame)
        left_frame.pack(pady=20, fill=tk.BOTH)

        Main_text = customtkinter.CTkLabel(top_frame, text="Devloped By Robin Singh", font=customtkinter.CTkFont('arial 10 italic'))
        Main_text.pack()

        Main_lenth = customtkinter.CTkLabel(top_frame, text="Length : --:--")
        Main_lenth.pack(pady=5)

        current_lenth = customtkinter.CTkLabel(top_frame, text="Current Duration : --:--")
        current_lenth.pack()

        playlist_box = tk.Listbox(music_player)
        canvas = customtkinter.CTkFrame(left_frame)
        canvas.pack(pady=5)

        pic = customtkinter.CTkImage(Image.open("icons/goofycoder_icon.png"))
        play_button1 = customtkinter.CTkButton(canvas, image=pic, command=Play_music, text="Play")
        play_button1.grid(row=0, column=0, padx=5)

        pic1 = customtkinter.CTkImage(Image.open("icons/goofycoder_icon.png"))
        stop_button1 = customtkinter.CTkButton(canvas, image=pic1, command=Stop_music, text="Stop")
        stop_button1.grid(row=0, column=1, padx=5)

        pic2 = customtkinter.CTkImage(Image.open("icons/goofycoder_icon.png"))
        pause_button1 = customtkinter.CTkButton(canvas, image=pic2, command=pause_music, text="Pause")
        pause_button1.grid(row=0, column=2, padx=5)

        bottom_canvas = customtkinter.CTkFrame(left_frame)
        bottom_canvas.pack(padx=30, pady=30)
        pic3 = customtkinter.CTkImage(Image.open("icons/goofycoder_icon.png"))
        rewind_button1 = customtkinter.CTkButton(bottom_canvas, image=pic3, command=rewind_music, text="Rewind")
        rewind_button1.grid(row=0, column=0, pady=10)

        pic4 = customtkinter.CTkImage(Image.open("icons/goofycoder_icon.png"))
        pic5 = customtkinter.CTkImage(Image.open("icons/goofycoder_icon.png"))
        vol_button1 = customtkinter.CTkButton(bottom_canvas, image=pic5, command=mute_music, text="Volume")
        vol_button1.grid(row=0, column=1)


        scale1 = customtkinter.CTkSlider(bottom_canvas, from_=0, to=100, orientation=tk.HORIZONTAL, command=set_vol)
        scale1.set(50)
        mixer.music.set_volume(.5)
        scale1.grid(row=0, column=3, padx=5, pady=10)

        # For overriding close button
        # music_player.protocol("WM_DELETE_WINDOW", close_window_fully)
        
        # music_player.mainloop()
        # -------------------- MUSIC PLAYER ENDS----------------------------------------------------

        # -------------------- UTILITIES SECTION ENDS------------------------------------------------------

        # -------------------- DICTIONARIES SECTION BEGINS----------------------------------------------------
        def section(e=None):
            status.configure(text_color="lightgrey", text=f"{e} selected")
            if e == "World History Dictionary":
                update(whdd.get_all_words())

        def update(data_list):
            # list_box.delete(0, tk.END)
            items_list.delete(0, tk.END)
            # Add words to listbox
            for word_item in data_list:
                items_list.insert(tk.END, word_item)

        def search(_=None):
            typed_word = title.get()
            if categories.get() == 'Dictionary' and len(typed_word) > 1:
                description.configure(state=tk.NORMAL)
                title.delete(0, "end")
                description.delete(1.0, tk.END)
                description.insert(1.0, typed_word.capitalize() + "\n")
                description.insert(2.0, "\n")
                if len(db.search_word(typed_word)) > 1:
                    description.insert(4.0, db.search_word(typed_word))
                else:
                    description.insert(4.0, 'Word not in Database, perhaps you wish to add it\?')
                    btn = customtkinter.CTkButton(defination_frame, text='Add', font=customtkinter.CTkFont("Century Gothic", 14))
                    description.window_create(4.0, window=btn)
                

            elif categories.get() == 'Wikipedia' and len(typed_word) > 1:
                description.configure(state=tk.NORMAL)
                title.delete(0, "end")
                description.delete(1.0, tk.END)
                #summary = wikipedia.page(typed_word)
                data = wikidb.search_wiki(typed_word)
                if isinstance(data, list):
                    update(data)
                else:
                    description.insert(1.0, data.title)
                    description.insert(2.0,"\n")
                    #result = db.search_wiki(typed_word)
                    description.insert(4.0, data.description)
                    update(wikidb.get_all_wikis())

            elif categories.get() == 'World History Dictionary' and len(typed_word) > 1:
                description.configure(state=tk.NORMAL)
                #title.delete(0, "end")
                description.delete(1.0, tk.END)
                #description.insert(1.0, typed_word.capitalize() + "\n")
                #description.insert(2.0, "\n")
                
                if len(whdd.search_word(typed_word).title) > 0:
                    description.insert(1.0, whdd.search_word(typed_word).description)
                else:
                    description.insert(4.0, 'Word not in Database, perhaps you wish to add it\?')
                    btn = customtkinter.CTkButton(defination_frame, text='Add', font=customtkinter.CTkFont("Century Gothic", 14))
                    description.window_create(4.0, window=btn)
                
            
        def save():
            option = options.get()
            if option == 'Save':
                status.configure(text_color="white")
                _title = title.get()
                _description = description.get('0.0', tk.END)
                category = categories.get()
                if category == "World History Dictionary":
                    check_save = whdd.add_word(_title, _description)
                    if check_save:
                        status.configure(text=f"{_title} saved successfully!", text_color="#50e40f") # SHOW SUCCESS MSG
                        update(whdd.get_all_words())
                        title.delete(0, tk.END)
                        description.delete(1.0, tk.END)
                    else:
                        status.configure(text="Saving failed!", text_color="#da2f25")
            elif option == 'Edit':
                description.configure(state=tk.NORMAL)
                status.configure(text_color="white")
                _title = title.get()
                _description = description.get('0.0', tk.END)
                category = categories.get()
                if category == "World History Dictionary":
                    edit_check = whdd.edit(entry_id.get(), _title, _description)
                    if edit_check:
                        update(whdd.get_all_words())
                        status.configure(text=f"{_title} Edited successfully!", text_color="#50e40f") # SHOW SUCCESS MSG
                        title.delete(0, tk.END)
                        description.delete(1.0, tk.END)
               
            elif option == 'Delete':
                description.configure(state=tk.DISABLED)
                status.configure(text_color="white")
                del_check = whdd.delete(entry_id.get())
                if del_check:
                    update(whdd.get_all_words())
                    status.configure(text=f"{entry_id.get()} deleted successfully!", text_color="#50e40f")
                else:
                    status.configure(text="Deletion failed!", text_color="#da2f25")



        main = customtkinter.CTkFrame(dictionary_settings)
        main.pack(fill=tk.BOTH, expand=True)
        left = customtkinter.CTkFrame(main)
        left.pack(side=tk.LEFT, fill=tk.Y)
        right = customtkinter.CTkFrame(main)
        right.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)

        categories = customtkinter.CTkOptionMenu(left, values=["Dictionary", "Wikipedia","World History Dictionary"], state=tk.NORMAL, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=section)
        categories.pack()

        # notbook widget tabarent
        dictionary_settings_options = customtkinter.CTkTabview(right, border_color='white')
        dictionary_settings_options.pack(fill="both", expand=True, padx=10, pady=10)
        
        # tab1234 in notbook wigget tab parent
        addnew = dictionary_settings_options.add("Add New")
        delete = dictionary_settings_options.add("Delete")
        edit = dictionary_settings_options.add("Edit")

        all_snippets_frame = customtkinter.CTkFrame(left)
        all_snippets_frame.pack(fill=tk.Y, expand=True)

        

        
        def fill_out(_=None):
            # Delete whatever is in the entry box
            title.delete(0, tk.END)
            entry_id.delete(0, tk.END)
            # Add clicked list item to entry box
            title.insert(0, items_list.get("anchor"))
            entry_id.insert(0, whdd.get_id(items_list.get("anchor")))
            search(items_list.get("anchor"))

        

        # SNIPPETS LIST SCROLLBAR
        items_list_scrollbar = customtkinter.CTkScrollbar(all_snippets_frame, orientation='vertical')

        # LIST TO DISPLAY SNIPPETS
        items_list = tk.Listbox(all_snippets_frame, width=40, yscrollcommand=items_list_scrollbar.set, font=("Century Gothic", 10), relief='flat', 
                                    selectmode=tk.BROWSE, selectforeground='black', selectbackground='lightgrey', activestyle='dotbox',  selectborderwidth=0, borderwidth=5)
        items_list.pack(side=tk.LEFT, fill=tk.Y)
        # items_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # PACK AND CONFIGURE SNIPPETS LIST SCROLLBAR
        items_list_scrollbar.pack(side='left', fill='y', expand=True)
        items_list_scrollbar.configure(command=items_list.yview)

        # SNIPPETS LIST BINDS
        items_list.bind("<<ListboxSelect>>", fill_out)
        items_list.bind('<Return>', search)

        controls_frame = customtkinter.CTkFrame(addnew)
        controls_frame.pack(fill=tk.X)
        options = customtkinter.CTkOptionMenu(controls_frame, values=["Save", "Edit","Delete"], state=tk.NORMAL, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"))
        options.pack(side=tk.LEFT)

        entry_id = customtkinter.CTkEntry(controls_frame)
        entry_id.pack(side=tk.LEFT)

        title = customtkinter.CTkEntry(addnew, placeholder_text="Enter title")
        title.pack(fill=tk.X, anchor=tk.N)

        description = customtkinter.CTkTextbox(addnew)
        description.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        save_button = customtkinter.CTkButton(addnew, text="EXECUTE", command=save)
        save_button.pack(fill=tk.X)

        status = customtkinter.CTkLabel(addnew, text='..........')
        status.pack(expand=tk.NO, padx=(10, 0), fill=None, side=tk.LEFT, anchor='sw')

        # -------------------- DICTIONARIES SECTION ENDS----------------------------------------------------
        

