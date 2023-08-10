import tkinter as tk
from . import base
import pyglet
import tkinter.ttk as ttk
from pages.database_engine import DictionaryDatabase, WikipediaDatabase, WorldHistoryDictionaryDatabase
from tkinter import messagebox
import os
from tkinter import IntVar
import customtkinter
from PIL import Image
import wikipedia
from functools import lru_cache
#import pyttsx3
import threading

db = DictionaryDatabase()
wikidb = WikipediaDatabase()
whdd = WorldHistoryDictionaryDatabase()
# ----- Create base folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pyglet.font.add_file('fonts/Base 02.ttf')
pyglet.font.add_file('fonts/Blacksword.otf')
pyglet.font.add_file('fonts/Lcd.ttf')
pyglet.font.add_file('fonts/europa_.TTF')
pyglet.font.add_file('fonts/SF Espresso Shack Bold Italic.ttf')

pyglet.font.load('Digital-7 Mono')
blacksword = pyglet.font.load('Blacksword')


THEME_COLOR = '#004D54'
TITLE_FONT = ("Century Gothic", 22)
TEXT_ENTRY_FONT = ("Century Gothic", 11)

class Voice:
    pass
#     def com_voice(self, text):
#         engine = pyttsx3.init()
#         rate = engine.getProperty('rate')
#         engine.setProperty('rate', rate - 20)
#         voices = engine.getProperty('voices')
#         engine.setProperty('voice', voices[2].id)
#         engine.say(text)
#         engine.runAndWait()

# AUDIO_ENGINE = pyttsx3.init()

class DictionaryPage(base.Page):
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)

        # Frame for main title label and logo
        mainlabel_frame = customtkinter.CTkFrame(self)
        mainlabel_frame.pack(anchor=tk.N, fill=tk.X)

        title_label = customtkinter.CTkLabel(mainlabel_frame, text="@goofycatt's Websters English Dictionary", font=customtkinter.CTkFont("Maiden Orange", 20, 'bold'))
        title_label.pack()

        def search(_=None):
            typed_word = search_entry.get()
            if functionality_option_menu.get() == 'Dictionary' and len(typed_word) > 1:
                defination_box.configure(state=tk.NORMAL)
                search_entry.delete(0, "end")
                defination_box.delete(1.0, tk.END)
                defination_box.insert(1.0, typed_word.capitalize() + "\n")
                defination_box.insert(2.0, "\n")
                if len(db.search_word(typed_word)) > 1:
                    defination_box.insert(4.0, db.search_word(typed_word))
                else:
                    defination_box.insert(4.0, 'Word not in Database, perhaps you wish to add it\?')
                    btn = customtkinter.CTkButton(defination_frame, text='Add', font=customtkinter.CTkFont("Century Gothic", 14))
                    defination_box.window_create(4.0, window=btn)
                defination_box.configure(state=tk.DISABLED)

            elif functionality_option_menu.get() == 'Wikipedia' and len(typed_word) > 1:
                defination_box.configure(state=tk.NORMAL)
                search_entry.delete(0, "end")
                defination_box.delete(1.0, tk.END)
                #summary = wikipedia.page(typed_word)
                data = wikidb.search_wiki(typed_word)
                if isinstance(data, list):
                    update(data)
                else:
                    defination_box.insert(1.0, data.title)
                    defination_box.insert(2.0,"\n")
                    #result = db.search_wiki(typed_word)
                    defination_box.insert(4.0, data.description)
                    update(wikidb.get_all_wikis())

            elif functionality_option_menu.get() == 'World History Dictionary' and len(typed_word) > 1:
                defination_box.configure(state=tk.NORMAL)
                search_entry.delete(0, "end")
                defination_box.delete(1.0, tk.END)
                defination_box.insert(1.0, typed_word.capitalize() + "\n")
                defination_box.insert(2.0, "\n")
                
                if len(whdd.search_word(typed_word).title) > 0:
                    defination_box.insert(4.0, whdd.search_word(typed_word).description)
                else:
                    defination_box.insert(4.0, 'Word not in Database, perhaps you wish to add it\?')
                    btn = customtkinter.CTkButton(defination_frame, text='Add', font=customtkinter.CTkFont("Century Gothic", 14))
                    defination_box.window_create(4.0, window=btn)
                defination_box.configure(state=tk.DISABLED)

        
        def update(data_list):
            # list_box.delete(0, tk.END)
            words_list_box.delete(0, tk.END)
            # Add words to listbox
            for word_item in data_list:
                words_list_box.insert(tk.END, word_item)

        def what_selected(typed_from_keyboard):
            if functionality_option_menu.get() == 'Dictionary':
                if typed_from_keyboard == "":
                    data = []
                else:
                    data = []
                    for item in db.search_all_matching(typed_from_keyboard):
                        data.append(item)
                    update(data)

            elif functionality_option_menu.get() == 'Wikipedia':
                if typed_from_keyboard == "":
                    data = []
                else:
                    data = []
                    for item in wikidb.search_all_matching_wikis(typed_from_keyboard):
                        data.append(item)
                    update(data)

            elif functionality_option_menu.get() == 'World History Dictionary':
                if typed_from_keyboard == "":
                    data = []
                else:
                    data = []
                    for item in whdd.search_all_matching_words(typed_from_keyboard):
                        data.append(item)
                    update(data)

        def check(_=None):
            # grab what is typed
            typed = search_entry.get()
            what_selected(typed)
            # self.update()

        def fill_out(_=None):
            # Delete whatever is in the entry box
            search_entry.delete(0, tk.END)

            # Add clicked list item to entry box
            search_entry.insert(0, words_list_box.get("anchor"))
            search(words_list_box.get("anchor"))

        def check_me():
            pass

        def cut_text():
            copy_text()
            delete_text()

        def copy_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                self.clipboard_clear()
                self.clipboard_append(defination_box.get(*selection))

        def paste_text():
            defination_box.insert(tk.INSERT, self.clipboard_get())

        def paste_image():
            global img
            try:
                img = customtkinter.CTkImage(Image.open(self.clipboard_get()))
                position = defination_box.index(tk.INSERT)
                defination_box.image_create(position, image=img)
            except tk.TclError:
                pass

        def delete_text():
            selection = defination_box.tag_ranges(tk.SEL)
            if selection:
                defination_box.delete(*selection)

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="@goofycatt")
        menu.add_command(label="Cut", command=cut_text)

        menu.add_command(label="Copy", command=copy_text)
        menu.add_command(label="Paste", command=paste_text)
        menu.add_command(label="Paste", command=paste_image)
        menu.add_command(label="Delete", command=delete_text)

        def show_popup(event):
            menu.post(event.x_root, event.y_root)

        search_widget_frame = customtkinter.CTkFrame(self)
        search_widget_frame.pack(fill=tk.X, anchor=tk.N, padx=100, pady=10)
        '''
        dictionary_var = IntVar()
        dictionary_check = customtkinter.CTkCheckBox(search_widget_frame,variable=dictionary_var, onvalue=1, offvalue=0,text="Dictionary", command=check_me)
        dictionary_check.pack(side=tk.LEFT)
        dictionary_check.select()
        '''
        def change_functionality(new_mode: str):
            if new_mode == 'Wikipedia':
                update(wikidb.get_all_wikis())
            if new_mode == 'Dictionary':
                update(db.get_all_words())
            if new_mode == 'World History Dictionary':
                update(whdd.get_all_words())

        def read_text():
            try:
                #AUDIO_ENGINE.stop()
                AUDIO_ENGINE.say(defination_box.get(1.0, tk.END))
                AUDIO_ENGINE.runAndWait()
            except RuntimeError as e:
                pass
            
            

        read_btn = customtkinter.CTkButton(search_widget_frame, text='Read', command=read_text)
        read_btn.pack(side=tk.LEFT)

        functionality_label = customtkinter.CTkLabel(search_widget_frame, text="Mode:")
        functionality_label.pack(side=tk.LEFT)
        functionality_option_menu = customtkinter.CTkOptionMenu(search_widget_frame, values=["Dictionary", "Wikipedia", "World History Dictionary"], command=change_functionality)
        functionality_option_menu.pack(side=tk.LEFT)

        search_text = customtkinter.CTkLabel(search_widget_frame, text="Search ", font=customtkinter.CTkFont("Century Gothic", 14))
        search_text.pack(side=tk.LEFT)

        search_entry = customtkinter.CTkEntry(search_widget_frame, font=customtkinter.CTkFont("Century Gothic", 14))
        search_entry.pack(pady=10, side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.focus_set()
        search_entry.bind("<KeyRelease>", check)

        search_img = customtkinter.CTkImage(Image.open('icons/search.png'))
        search_btn = customtkinter.CTkButton(search_widget_frame, image=search_img, width=80, command=search)
        search_btn.image = search_img
        search_btn.pack(side=tk.LEFT, padx=5)

        defination_frame = customtkinter.CTkFrame(self)
        defination_frame.pack(fill=tk.BOTH, expand=True)

        defination_box = customtkinter.CTkTextbox(defination_frame, width=40,height=20, font=customtkinter.CTkFont("Century Gothic", 14))
        defination_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        words_listbox_scrbar = customtkinter.CTkScrollbar(defination_frame, orientation='vertical')
        words_list_box = tk.Listbox(defination_frame, font=customtkinter.CTkFont("Century Gothic", 14), yscrollcommand=words_listbox_scrbar.set, 
                                                      relief='flat', selectmode=tk.BROWSE, selectforeground='black', 
                                                      selectbackground='lightgrey', activestyle='dotbox',  selectborderwidth=0, borderwidth=5)
        words_list_box.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.pack(side=tk.LEFT, fill=tk.Y)
        words_listbox_scrbar.configure(command=words_list_box.yview)

        self.bind("<Return>", search)
        words_list_box.bind("<<ListboxSelect>>", fill_out)
        defination_box.bind("<Button-3>", show_popup)

        update(db.get_all_words())