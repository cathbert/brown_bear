# import required modules
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from tkcalendar import Calendar, DateEntry
from datetime import datetime

import multiprocessing
import customtkinter
from . import base
from .database_engine import DiaryDatabase

# --> Initializing diary database
diary = DiaryDatabase()


class DiaryPage(base.Page):
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)

        # --> Set theme color and font
        theme_color = "#003B4A"
        theme_font = ("helvetica", 12)
        entries_bg_color = "#003B4A"
        entries_fg_color = "#ffff00"

        # --> Frame to hold the page title
        diary_page_title_frame = customtkinter.CTkFrame(self)
        diary_page_title_frame.pack(fill=tk.X, anchor=tk.N)

        calendar_frame = customtkinter.CTkFrame(self)
        calendar_frame.pack(fill=tk.BOTH, expand=True, anchor=tk.N)

        # --> Set page title
        diary_page_title = customtkinter.CTkLabel(diary_page_title_frame, text="Cathbert's Diary", font=theme_font)
        diary_page_title.pack(side="top", fill="both", expand=True)

        # --> This function serves to create a new entry
        def create_entry():
            selected_date = calendarobj.selection_get()
            new_entry_form(selected_date)

        def new_entry_form(date_selected):
            root = customtkinter.CTkToplevel(self)
            root.geometry("800x400")
            root.resizable(False, False)

            # --> Frame to hold the form tiyle
            form_title_frame = tk.Frame(root)
            form_title_frame.pack()
            # --> Set form title
            form_title = customtkinter.CTkLabel(form_title_frame, text="CREATE NEW ENTRY")
            form_title.pack()

            # --> Frame to hold all form widgets
            widgets_frame = customtkinter.CTkFrame(root)
            widgets_frame.pack()

            # --> Set form form
            font = ("Verdana", 12)

            entry_title_label = customtkinter.CTkLabel(widgets_frame, text="Entry title")
            entry_title_label.grid(row=0, column=0, sticky="w")

            # --> entry title entry field
            entry_title = customtkinter.CTkEntry(widgets_frame, font=font, width=50)
            entry_title.grid(row=0, column=1, sticky="w")

            entry_theme_label = customtkinter.CTkLabel(widgets_frame, text="Entry theme")
            entry_theme_label.grid(row=1, column=0, sticky="w")

            # --> entry theme entry field
            entry_theme = customtkinter.CTkEntry(widgets_frame, font=font, width=50)
            entry_theme.grid(row=1, column=1, sticky="w")

            def trace_var(*args):
                if last_value == "59" and min_str.get() == "0":
                    hour_str.set(int(hour_str.get()) + 1 if hour_str.get() != "23" else 0)
                self.last_value = min_str.get()

            entry_time_label = customtkinter.CTkLabel(widgets_frame, text="Time")
            entry_time_label.grid(row=2, column=0, sticky="w")

            # entry time selector field
            time_frame = customtkinter.CTkFrame(widgets_frame)
            time_frame.grid(row=2, column=1, sticky="w")

            # --> Set hour string variable
            hour_str = tk.StringVar(self, '10')

            # --> Hour spinbox
            hour_box = tk.Spinbox(time_frame, from_=0, to=23, wrap=True, textvariable=hour_str, width=2,
                                  state="readonly", font=("Verdana", 12))
            hour_box.grid(row=0, column=0)

            # --> Minute spinbox variable
            min_str = tk.StringVar(self, '30')
            min_str.trace("w", trace_var)
            last_value = ""
            min_box = tk.Spinbox(time_frame, from_=0, to=59, wrap=True, textvariable=min_str, width=2, state="readonly",
                                 font=("Verdana", 12))
            min_box.grid(row=0, column=1)

            entry_information = scrolledtext.ScrolledText(widgets_frame, height=15)
            entry_information.grid(row=3, column=1, sticky="w")

            def save_entry():
                time = datetime.strptime(f"{hour_box.get()}:{min_box.get()}", "%H:%M")
                entry = entry_title.get()
                if len(entry) < 1:
                    messagebox.showwarning("Missing title", "Please set tile in order to create an Event")
                else:
                    calendarobj.calevent_create(date_selected, entry, entry_theme.get())
                    diary.create_an_entry(entry_title.get(), entry_theme.get(), date_selected, time,
                                           entry_information.get(1.0, tk.END))
                    root.destroy()
                    messagebox.showinfo("Success", "entry has been created, congratulations!!")
                reupdate()

            save_entry_button = customtkinter.CTkButton(widgets_frame, text="Save entry", command=save_entry)
            save_entry_button.grid(row=4, column=0, sticky="w")

        def delete_all_today_entries():
            selected_date = calendarobj.selection_get()

            if diary.check_if_entries_are_available(selected_date):
                answer = messagebox.askyesno("Warning", "Do you really want to clear all of this days's entries")
                if answer == 1:
                    entries_id_list = calendarobj.get_calevents(selected_date)
                    for i in entries_id_list:
                        calendarobj.calevent_remove(i)
                    diary.delete_this_day_entries(selected_date)
                    my_tree.delete(*my_tree.get_children())
            else:
                messagebox.showinfo("Empty", "There is no availabale entries to delete on this day")

        def delete_entry(e=None):
            x = my_tree.selection()
            ask = messagebox.askyesno('Deletion', 'Do you wish to proceed with deletion?')
            if ask:
                for e in x:
                    text = my_tree.item(e, 'values')
                    my_tree.delete(e)
                    diary.delete_single_entry(text[0])
                if len(x) == 1:
                    messagebox.showinfo("Deletion successful", f"{len(x)} entry deleted!")
                else:
                    messagebox.showinfo("Deletion successful", f"{len(x)} entries deleted!")
            else:
                pass

        
        calendar_frame = customtkinter.CTkFrame(calendar_frame)
        calendar_frame.pack(fill=tk.BOTH, expand=True, anchor=tk.N)
        calendarobj = Calendar(calendar_frame, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand2", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

        calendarobj.pack(fill="both", expand=True)

        def get_entry_info(e=None):
            selected_date = calendarobj.selection_get()
            # entrys_id_list = calendarobj.get_calevents(date)
            #print(events.get_event_by_date(str(selected_date)))
            update(diary.get_entry_by_date(str(selected_date)))
            # print(events.get_all_events())
            """
            for i in events.get_event_by_date(str(date)):
                t = calendarobj.calevent_cget(i, option="text")
                print(t)
            """

        def load_entries():
            for entry in diary.get_all_entries():
                calendarobj.calevent_create(entry[2], entry, 'Its good')

        load_entries()

        calendarobj.bind("<<CalendarSelected>>", get_entry_info)

        # --> entry widgets frame
        main_widgets_frame = customtkinter.CTkFrame(self)
        main_widgets_frame.pack(fill=tk.X, ipadx=10, pady=10)

        # --> entry form frame
        entry_list = customtkinter.CTkFrame(main_widgets_frame)
        entry_list.pack(side=tk.TOP, fill=tk.X)

        # --> entry navigation panel frame
        entry_navigation_frame = customtkinter.CTkFrame(main_widgets_frame)
        entry_navigation_frame.pack(side=tk.TOP, anchor=tk.N)

        # -------------------------------------DIRECTORY TREEVIEW SECTION-----------------------------------------------

        # --> Add some style to the tree view below
        style = ttk.Style()

        # print(style.theme_names())
        '''winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'''

        # --> Pick a theme
        style.theme_use("clam")

        # --> Configure our treeview colors
        style.configure("Treeview", background='#DDD5C6', foreground="black", rowheight=25, font="#003fcc",
                        fieldbackground='#DDD5C6', rowwidth=200)

        # --> Change selected color
        style.map("Treeview", background=[("selected", "#003fcc")])

        # --> Treeview Scrollbar
        tree_scroll = customtkinter.CTkScrollbar(entry_list)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --> Create Treeview
        my_tree = ttk.Treeview(entry_list, yscrollcommand=tree_scroll.set, selectmode="extended", height=10)
        my_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # --> Configure scrollbar
        tree_scroll.configure(command=my_tree.yview)

        def edit_entry(e=None):
            x = my_tree.selection()
            for f in x:
                data = my_tree.item(f, 'values')
                print(diary.get_selected_entry_id(data[0]))
            print("Editing entry")

        def check_date(date):
            current_date = datetime.now()
            return date > current_date.date()

        def new_entry_form(date_selected, title=None, theme=None):
            if check_date(date_selected):
                root = customtkinter.CTkToplevel(self)
                root.geometry("800x400")
                #root.resizable(False, False)

                # --> Frame to hold the form tiyle
                form_title_frame = customtkinter.CTkFrame(root)
                form_title_frame.pack()
                # --> Set form title
                form_title = customtkinter.CTkLabel(form_title_frame, text="CREATE NEW entry")
                form_title.pack(fill=tk.BOTH)

                # --> Frame to hold all form widgets
                widgets_frame = customtkinter.CTkFrame(root)
                widgets_frame.pack(fill=tk.BOTH)

                # --> Set form form
                font = ("Verdana", 12)

                entry_title_label = customtkinter.CTkLabel(widgets_frame, text="entry title")
                entry_title_label.grid(row=0, column=0, sticky="w")

                # --> entry title entry field
                entry_title = customtkinter.CTkEntry(widgets_frame, font=font, width=50)
                entry_title.grid(row=0, column=1, sticky="w")

                entry_theme_label = customtkinter.CTkLabel(widgets_frame, text="entry theme")
                entry_theme_label.grid(row=1, column=0, sticky="w")

                # --> entry theme entry field
                entry_theme = customtkinter.CTkEntry(widgets_frame, font=font, width=50)
                entry_theme.grid(row=1, column=1, sticky="w")

                def trace_var(*args):
                    if last_value == "59" and min_str.get() == "0":
                        hour_str.set(int(hour_str.get()) + 1 if hour_str.get() != "23" else 0)
                    self.last_value = min_str.get()

                entry_time_label = customtkinter.CTkLabel(widgets_frame, text="Time")
                entry_time_label.grid(row=2, column=0, sticky="w")

                # entry time selector field
                time_frame = customtkinter.CTkFrame(widgets_frame)
                time_frame.grid(row=2, column=1, sticky="w")

                # --> Set hour string variable
                hour_str = tk.StringVar(self, '10')

                # --> Hour spinbox
                hour_box = tk.Spinbox(time_frame, from_=0, to=23, wrap=True, textvariable=hour_str, width=2, state="readonly", font=("Verdana", 12))
                hour_box.grid(row=0, column=0)

                # --> Minute spinbox variable
                min_str = tk.StringVar(self, '30')
                min_str.trace("w", trace_var)
                last_value = ""
                min_box = tk.Spinbox(time_frame, from_=0, to=59, wrap=True, textvariable=min_str, width=2, state="readonly",
                                     font=("Verdana", 12))
                min_box.grid(row=0, column=1)

                entry_information = scrolledtext.ScrolledText(widgets_frame, height=15)
                entry_information.grid(row=3, column=1, sticky="w")

                def save_entry():
                    time = datetime.strptime(f"{hour_box.get()}:{min_box.get()}", "%H:%M")
                    entry_name = entry_title.get()
                    if len(entry_name) < 1:
                        messagebox.showwarning("Missing title", "Please set tile in order to create an entry")
                    else:
                        calendarobj.calevent_create(date_selected, entry_name, entry_theme.get())
                        diary.create_an_entry(entry_title.get(), entry_theme.get(), date_selected, time,
                                               entry_information.get(1.0, tk.END))
                        root.destroy()
                        messagebox.showinfo("Success", "entry has been created, congratulations!!")

                save_entry_button = customtkinter.CTkButton(widgets_frame, text="Save entry", command=save_entry)
                save_entry_button.grid(row=4, column=1, sticky="w")
            else:
                messagebox.showinfo("Date not allowed", "You can't create an entry on this day!")

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Ephitome.com")
        menu.add_command(label="Edit", command=edit_entry)

        menu.add_command(label="Go to entries day on Calendar")
        menu.add_command(label="Paste text")
        menu.add_command(label="Paste image")
        menu.add_command(label="Delete", command=delete_entry)

        def show_popup(entry):
            menu.post(entry.x_root, entry.y_root)

        def OnDoubleClick(entry):
            x = my_tree.selection()
            for e in x:
                text = my_tree.item(e, 'values')
                data = diary.get_selected_entry(text[0])
                messagebox.showinfo(f'{text[0]} info', f'Date: {text[1]}\nTime: {text[2]}\nInfo: {data.entry_info}')
                #print(text)

        my_tree.bind("<Double-1>", OnDoubleClick)

        my_tree.bind("<Button-3>", show_popup)

        # --> Define columns
        my_tree["columns"] = ('Title', 'Date', "Time", 'Code', 'Theme')

        # --> Format tree columns
        my_tree.column("#0", width=0, stretch=tk.NO)
        my_tree.column("Title", anchor=tk.W, width=120)
        my_tree.column("Date", anchor=tk.W, width=120)
        my_tree.column("Time", anchor=tk.CENTER, width=50)
        my_tree.column("Code", anchor=tk.W, width=100)
        my_tree.column("Theme", anchor=tk.W, width=180)

        # --> Create tree Headings
        my_tree.heading("#0", text="", anchor=tk.CENTER)
        my_tree.heading("Title", text="Title", anchor=tk.W)
        my_tree.heading("Date", text="Date", anchor=tk.W)
        my_tree.heading("Time", text="Time", anchor=tk.CENTER)
        my_tree.heading("Code", text="Code", anchor=tk.W)
        my_tree.heading("Theme", text="Theme", anchor=tk.W)

        # --> Create striped row tags
        my_tree.tag_configure("oddrow", background="#DDD5C6")
        my_tree.tag_configure("evenrow", background="#CCBF99")

        set_entry_button = customtkinter.CTkButton(entry_navigation_frame, text="Create entry", command=create_entry)
        set_entry_button.pack(side=tk.LEFT)

        rm_entry_button = customtkinter.CTkButton(entry_navigation_frame, text="Clear entries for this day",
                                     command=delete_all_today_entries)
        rm_entry_button.pack(side=tk.LEFT)

        # get_entry_button = customtkinter.CTkButton(entry_navigation_frame, text="Get entry", command=get_entry_info)
        # get_entry_button.pack(side=tk.LEFT)

        delete_this_entry = customtkinter.CTkButton(entry_navigation_frame, text="Delete entry", command=delete_entry)
        delete_this_entry.pack(side=tk.LEFT)
        '''
        def reupdate():
            def update(database_data):

                # entries_id_list = calendarobj.get_calevents(date)

                my_tree.delete(*my_tree.get_children())

                # -- Iterate through the contacts from the database
                for contact in database_data:

                    # --> Check if counter variable contains an odd number or an even number
                    if self.count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=self.count, text="",
                                       values=(contact[0], contact[2], contact[3], contact[5], contact[1]),
                                       tags=('evenrow',))
                    else:
                        my_tree.insert(parent='', index='end', iid=self.count, text="",
                                       values=(contact[0], contact[2], contact[3], contact[5], contact[1]),
                                       tags=('oddrow',))

            # -- Increment count by 1
            self.count += 1
            # --> Load entries data
            data = diary.get_all_entries()

            # --> Update treeview data
            update(data)
        '''
        

        style = ttk.Style()
        # style.theme_use('clam')  # -> uncomment this line if the styling does not work
        style.configure('my.DateEntry',
                        fieldbackground='light green',
                        background='dark green',
                        foreground='dark blue',
                        arrowcolor='white')
        self.count = 0

        def update(datab = None):

            # entries_id_list = calendarobj.get_calevents(date)

            my_tree.delete(*my_tree.get_children())

            if datab == None:
                # -- Iterate through the contacts from the database
                datab = diary.get_all_entries()
                for contact in datab:

                    # --> Check if counter variable contains an odd number or an even number
                    if self.count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=self.count, text="",
                                    values=(contact[0], contact[2], contact[3], contact[5], contact[1]),
                                    tags=('evenrow',))
                    else:
                        my_tree.insert(parent='', index='end', iid=self.count, text="",
                                    values=(contact[0], contact[2], contact[3], contact[5], contact[1]),
                                    tags=('oddrow',))

                    # -- Increment count by 1
                    self.count += 1
            else:
                for contact in datab:
                    # --> Check if counter variable contains an odd number or an even number
                    if self.count % 2 == 0:
                        my_tree.insert(parent='', index='end', iid=self.count, text="",
                                    values=(contact[0], contact[2], contact[3], contact[5], contact[1]),
                                    tags=('evenrow',))
                    else:
                        my_tree.insert(parent='', index='end', iid=self.count, text="",
                                    values=(contact[0], contact[2], contact[3], contact[5], contact[1]),
                                    tags=('oddrow',))

                    # -- Increment count by 1
                    self.count += 1

        # --> Load events data
        data = diary.get_all_entries()

        # --> Update treeview data
        update(data)

        view_all_entries_button = customtkinter.CTkButton(entry_navigation_frame, text="View all entry", command=update)
        view_all_entries_button.pack(side=tk.LEFT)

        date_entry = DateEntry(entry_navigation_frame, style='my.DateEntry', width=12, background='darkblue',
                               foreground='white', borderwidth=2, year=2010, locale='en_US', date_pattern='dd/MM/yyyy')
        date_entry.pack(padx=10, pady=10)
