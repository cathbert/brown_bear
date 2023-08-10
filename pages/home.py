from . import base
import customtkinter
import tkintermapview
import os
from .database_engine import KnowledgeDatabase
from .database_engine import accounts
import threading

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    import tkinter as tk
    from tkinter import ttk

know_db = KnowledgeDatabase()

class StartPage(base.Page):
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)

        # ============ create two CTkFrames ============
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        contro_panel_frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=5, fg_color=None, border_width=1)
        contro_panel_frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        major_widgets_frame = customtkinter.CTkFrame(master=self, corner_radius=5, border_width=1)
        major_widgets_frame.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ major_widgets_frame ============

        major_widgets_frame.grid_rowconfigure(1, weight=1)
        major_widgets_frame.grid_rowconfigure(0, weight=0)
        major_widgets_frame.grid_columnconfigure(0, weight=1)
        major_widgets_frame.grid_columnconfigure(1, weight=0)
        major_widgets_frame.grid_columnconfigure(2, weight=1)

        def search_info(_ = None):
            try:
                data = know_db.search(search.get())
                update_recents(know_db.search(search.get()))
            except AttributeError:
                update_recents(['No results!'])
                


        # THIS FUNCTION GETS DATA AND UPDATE THE RECENTS LIST
        def update_recents(recents):
            list_all_searches.delete(0, tk.END) # CLEAR SNIPPETS LIST(LISTBOX)
            list_of_recents = []
            for recent in recents: # ITERATE AND INSERT SNIPPETS INTO LIST
                list_of_recents.append((recent.id, recent.title))
                list_all_searches.insert(tk.END, f'\u231B {recent.visited.strftime("%m/%d/%Y, %H:%M:%S")} 🗳 {recent.title.upper()}  - {recent.info[0:130]} ..........')
                list_all_searches.selection_set(0)

        def options(_ = None):
            if option_choices.get() == 'Save':
                title = search.get().lower().strip() # GET TITLE TITLE FROM SEARCH(ENTRY) AREA
                section = section_option_menu.get().lower().strip() # GET SECTION TITLE FROM CATEGORIES LIST(OPTIONMENU) AREA
                thematic = thematic_mode_optionemenu.get().lower().strip()
                info = display_screen.get('0.0', tk.END).strip() # GET INFO FROM THE SCREEN(TEXT) AREA
                
                try: 
                    save = know_db.add_new_knowledge(know_db.get_section_object_by_title(section) , know_db.get_thematic_object_by_title(thematic), title, info)
                    if save:
                        data = know_db.get_all_thematics_by_section(know_db.get_section_object_by_title(section_option_menu.get()))
                        thematic_mode_optionemenu.configure(values=data)
                        status.configure(text=f"{title} succesfully saved!", text_color="#50e40f")
                        # UPDATE THE LIST WITH DATA FROM THE DATABASE BY RECENTS
                        update_recents(know_db.get_five_recently_added())
                        search.delete(0, tk.END)
                        display_screen.delete('0.0', tk.END)
                        know_code.delete(0, tk.END)
                    else:
                        pass
                except accounts.models.KnowledgeThematic.DoesNotExist: status.configure(text='Please do check your thematic selection!', text_color="#da2f25")
                except accounts.models.KnowledgeSection.DoesNotExist: status.configure(text='Please do check your section selection!', text_color="#da2f25")
                except Exception as e: status.configure(text=f'{str(e)}', text_color="#da2f25")
                

            elif option_choices.get() == 'Search':
                try:
                    data = know_db.search(search.get())
                    update_recents(know_db.search(search.get()))
                except AttributeError:
                    update_recents(['No results!'])
            elif option_choices.get() == 'Update':
                edit_knowledge()

        def edit_knowledge():
            status.configure(text_color="white")
            try:
                title = search.get().lower().strip() # GET TITLE TITLE FROM SEARCH(ENTRY) AREA
                section = section_option_menu.get().lower().strip() # GET SECTION TITLE FROM CATEGORIES LIST(OPTIONMENU) AREA
                thematic = thematic_mode_optionemenu.get().lower().strip()
                info = display_screen.get('0.0', tk.END).strip() # GET INFO FROM THE SCREEN(TEXT) AREA
                know_db.update_knowledge(know_code.get(), know_db.get_section_object_by_title(section), know_db.get_thematic_object_by_title(thematic), title, info)
                status.configure(text=f"{title} succesfully updated!", text_color="#50e40f")
            except Exception as e:
                status.configure(text=f"{e} failed to update!", text_color="#e1f105")



        def check_section_and_update_thematic(event=None):
            if event is not None:
                data = know_db.get_all_thematics_by_section(know_db.get_section_object_by_title(event))
                thematic_mode_optionemenu.configure(values=data)
            else:
                data = know_db.get_all_thematics_by_section(know_db.get_section_object_by_title(section_option_menu.get()))
                thematic_mode_optionemenu.configure(values=data)

        def display(e=None):
            text = list_all_searches.get("anchor").split('🗳')[1].split('  ')[0].lower()
            data = know_db.get_single_selected_knowledge(text.strip())
            search.delete(0, tk.END)
            search.insert(0, data.title)
            display_screen.delete('0.0', tk.END)
            display_screen.insert(tk.END, data.info.strip())
            status.configure(text=f"{data.knowledge_section.title}: {data.knowledge_thematic.title}")
            # UPDATE THE LIST WITH DATA FROM THE DATABASE BY RECENTS
            update_recents(know_db.get_five_recently_added())
            know_code.delete(0, tk.END)
            know_code.insert(tk.END, data.id)


        def listen_to_events(e=None):
            def start():
                self.after(500, start)
            start()

        def clear():
            search.delete(0, tk.END)
            display_screen.delete('0.0', tk.END)
            know_code.delete(0, tk.END)
            status.configure(text="Status .....")

        def check(_):
            display_screen.delete('0.0', tk.END)
        
        # ============ contro_panel_frame_left ============
        contro_panel_frame_left.grid_rowconfigure(2, weight=1)

        button_1 = customtkinter.CTkButton(master=contro_panel_frame_left,text="Mark search")
        button_1.grid(pady=(10, 0), padx=(10, 10), row=0, column=0)

        button_2 = customtkinter.CTkButton(master=contro_panel_frame_left, text="Clear Markers")
        button_2.grid(pady=(10, 0), padx=(10, 10), row=1, column=0)

        section_label = customtkinter.CTkLabel(contro_panel_frame_left, text="Section", anchor="w")
        section_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        section_option_menu = customtkinter.CTkOptionMenu(contro_panel_frame_left, values=know_db.get_all_sections(), command = check_section_and_update_thematic)
        section_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        appearance_mode_label = customtkinter.CTkLabel(contro_panel_frame_left, text="Thematic:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))

        thematic_mode_optionemenu = customtkinter.CTkOptionMenu(contro_panel_frame_left, values=['Thematic'])
        thematic_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        search = customtkinter.CTkEntry(master=major_widgets_frame,placeholder_text="Type to search")
        search.grid(row=0, column=0, sticky="we", padx=(5, 0), pady=(12,0))
        search.focus_set()
        search.bind("<Return>", search_info)
        search.bind("<KeyRelease>", check)

        option_choices = customtkinter.CTkOptionMenu(master=major_widgets_frame,values=['Search', 'Save', 'Update'], width=90)
        option_choices.grid(row=0, column=1, sticky="w", padx=(5, 0), pady=(12,0))

        know_code = customtkinter.CTkEntry(master=major_widgets_frame, width=90)
        know_code.grid(row=0, column=2, sticky="w", padx=(0, 0), pady=(12,0))

        search_save_button = customtkinter.CTkButton(master=major_widgets_frame,text="Execute", width=90, command=options)
        search_save_button.grid(row=0, column=3, sticky="w", padx=(5, 0), pady=(12,0))

        clear_button = customtkinter.CTkButton(master=major_widgets_frame,text="X",width=2, hover_color='lightgrey', fg_color='transparent', text_color='red', font=customtkinter.CTkFont("Century Gothic", 15,'bold'), command=clear)
        clear_button.grid(row=0, column=4, sticky="w", padx=(0, 10), pady=(12,0))

        MAJOR_FRAME = customtkinter.CTkFrame(master=major_widgets_frame)
        MAJOR_FRAME.grid(row=1, column=0, columnspan=5, sticky="news", padx=(5, 5), pady=(5, 5))

        SEARCH_DISPLAY = customtkinter.CTkFrame(master=self)
        SEARCH_DISPLAY.grid(row=1, column=0, columnspan=5, sticky="news", padx=(5, 5), pady=(5, 5))

        # SNIPPETS LIST SCROLLBAR
        list_all_searches_scrlbar = customtkinter.CTkScrollbar(SEARCH_DISPLAY, orientation='vertical')
        list_all_searches = tk.Listbox(SEARCH_DISPLAY, yscrollcommand=list_all_searches_scrlbar.set, font=("Century Gothic", 10),
                                                        foreground='blue', relief=tk.FLAT, selectmode=tk.BROWSE, selectforeground='purple', 
                                                        selectbackground='lightgrey', activestyle='none',  selectborderwidth=0, borderwidth=8,
                                                        highlightthickness=5)
        list_all_searches.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # PACK AND CONFIGURE SNIPPETS LIST SCROLLBAR
        list_all_searches_scrlbar.pack(side=tk.LEFT, fill=tk.Y)
        list_all_searches_scrlbar.configure(command=list_all_searches.yview)
        list_all_searches.bind('<Double-1>', display)

        # Main screen to view text contents
        display_screen = customtkinter.CTkTextbox(MAJOR_FRAME, wrap='word', font=customtkinter.CTkFont("Courier New", 16), border_width=1)
        display_screen.pack(fill=tk.BOTH, expand=True)
        
        status = customtkinter.CTkLabel(MAJOR_FRAME, text="Status")
        status.pack(fill=tk.X)

        # UPDATE THE LIST WITH DATA FROM THE DATABASE BY RECENTS
        update_recents(know_db.get_five_recently_added())   

        #listen_to_events()
        
    def search_event(event=None): pass

    def set_marker_event(): pass

    def clear_marker_event(): pass

    def change_appearance_mode(new_appearance_mode: str): pass

    def change_map(new_map: str): pass
        
    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()
