# import required modules
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from . import base
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from pages.database_engine import EventsDatabase
import multiprocessing

# --> Initializing events database
events = EventsDatabase()


class EventsPage(base.Page):
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)

        # --> Set theme color and font
        theme_color = "#003B4A"
        theme_font = ("helvetica", 12)
        entries_bg_color = "#003B4A"
        entries_fg_color = "#ffff00"

        self.config(bg=theme_color)

        # --> Frame to hold the page title
        events_page_title_frame = tk.Frame(self, bg=theme_color, padx=7)
        events_page_title_frame.pack(fill=tk.BOTH)

        # --> Set page title
        events_page_title = tk.Label(events_page_title_frame, text="Events Database", font=theme_font, relief=tk.RAISED,
                                     bg=theme_color, fg="#ffff00", bd=2)
        events_page_title.pack(side="top", fill="both", expand=True)

        # --> This function serves to create a new event
        def create_event():
            selected_date = cal.selection_get()
            new_event_form(selected_date)

        def new_event_form(date_selected):
            root = tk.Toplevel(self)
            root.geometry("800x400")
            root.resizable(False, False)

            # --> Frame to hold the form tiyle
            form_title_frame = tk.Frame(root)
            form_title_frame.pack()
            # --> Set form title
            form_title = tk.Label(form_title_frame, text="CREATE NEW EVENT")
            form_title.pack()

            # --> Frame to hold all form widgets
            widgets_frame = tk.Frame(root)
            widgets_frame.pack()

            # --> Set form form
            font = ("Verdana", 12)

            event_title_label = tk.Label(widgets_frame, text="Event title")
            event_title_label.grid(row=0, column=0, sticky="w")

            # --> Event title entry field
            event_title = tk.Entry(widgets_frame, font=font, width=50)
            event_title.grid(row=0, column=1, sticky="w")

            event_theme_label = tk.Label(widgets_frame, text="Event theme")
            event_theme_label.grid(row=1, column=0, sticky="w")

            # --> Event theme entry field
            event_theme = tk.Entry(widgets_frame, font=font, width=50)
            event_theme.grid(row=1, column=1, sticky="w")

            def trace_var(*args):
                if last_value == "59" and min_str.get() == "0":
                    hour_str.set(int(hour_str.get()) + 1 if hour_str.get() != "23" else 0)
                self.last_value = min_str.get()

            event_time_label = tk.Label(widgets_frame, text="Time")
            event_time_label.grid(row=2, column=0, sticky="w")

            # Event time selector field
            time_frame = tk.Frame(widgets_frame)
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

            event_information = scrolledtext.ScrolledText(widgets_frame, height=15)
            event_information.grid(row=3, column=1, sticky="w")

            def save_event():
                time = datetime.strptime(f"{hour_box.get()}:{min_box.get()}", "%H:%M")
                event = event_title.get()
                if len(event) < 1:
                    messagebox.showwarning("Missing title", "Please set tile in order to create an Event")
                else:
                    cal.calevent_create(date_selected, event, event_theme.get())
                    events.create_an_event(event_title.get(), event_theme.get(), date_selected, time,
                                           event_information.get(1.0, tk.END))
                    root.destroy()
                    messagebox.showinfo("Success", "Event has been created, congratulations!!")
                reupdate()

            save_event_button = ttk.Button(widgets_frame, text="Save Event", command=save_event)
            save_event_button.grid(row=4, column=0, sticky="w")

        def delete_all_today_events():
            selected_date = cal.selection_get()

            if events.check_if_events_are_available(selected_date):
                answer = messagebox.askyesno("Warning", "Do you really want to clear all of this days's events")
                if answer == 1:
                    events_id_list = cal.get_calevents(selected_date)
                    for i in events_id_list:
                        cal.calevent_remove(i)
                    events.delete_this_day_events(selected_date)
                    my_tree.delete(*my_tree.get_children())
            else:
                messagebox.showinfo("Empty", "There is no availabale events to delete on this day")

        def delete_event():
            x = my_tree.selection()
            for e in x:
                text = my_tree.item(e, 'values')
                my_tree.delete(e)
                events.delete_single_event(text[0])
            if len(x) == 1:
                messagebox.showinfo("Deletion successful", f"{len(x)} event deleted!")
            else:
                messagebox.showinfo("Deletion successful", f"{len(x)} events deleted!")

        calendar_frame = tk.Frame(self, padx=10, bg=theme_color)
        calendar_frame.pack(fill=tk.X)
        cal = Calendar(calendar_frame, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand2", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

        cal.pack(fill="both", expand=True)

        def get_event_info(e=None):
            selected_date = cal.selection_get()
            # events_id_list = cal.get_calevents(date)
            #print(events.get_event_by_date(str(selected_date)))
            update(events.get_event_by_date(str(selected_date)))
            # print(events.get_all_events())
            """
            for i in events.get_event_by_date(str(date)):
                t = cal.calevent_cget(i, option="text")
                print(t)
            """

        def load_events():
            for event in events.get_all_events():
                cal.calevent_create(event[2], event, 'Its good')

        load_events()

        cal.bind("<<CalendarSelected>>", get_event_info)

        # --> Event widgets frame
        main_widgets_frame = tk.Frame(self, padx=10, bg=theme_color)
        main_widgets_frame.pack(fill=tk.X)

        # --> Event form frame
        event_list = tk.Frame(main_widgets_frame, pady=5, bg=theme_color)
        event_list.pack(side=tk.TOP, fill=tk.X)

        # --> Event navigation panel frame
        event_navigation_frame = tk.Frame(main_widgets_frame, bg=theme_color)
        event_navigation_frame.pack(side=tk.TOP)

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
        tree_scroll = tk.Scrollbar(event_list)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --> Create Treeview
        my_tree = ttk.Treeview(event_list, yscrollcommand=tree_scroll.set, selectmode="extended", height=5)
        my_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # --> Configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        def edit_event():
            x = my_tree.selection()
            print(len(x))
            print("Editing event")

        def check_date(date):
            current_date = datetime.now()
            return date > current_date.date()

        def new_event_form(date_selected):
            if check_date(date_selected):
                root = tk.Toplevel(self)
                root.geometry("800x400")
                root.resizable(False, False)

                # --> Frame to hold the form tiyle
                form_title_frame = tk.Frame(root)
                form_title_frame.pack()
                # --> Set form title
                form_title = tk.Label(form_title_frame, text="CREATE NEW EVENT")
                form_title.pack()

                # --> Frame to hold all form widgets
                widgets_frame = tk.Frame(root)
                widgets_frame.pack()

                # --> Set form form
                font = ("Verdana", 12)

                event_title_label = tk.Label(widgets_frame, text="Event title")
                event_title_label.grid(row=0, column=0, sticky="w")

                # --> Event title entry field
                event_title = tk.Entry(widgets_frame, font=font, width=50)
                event_title.grid(row=0, column=1, sticky="w")

                event_theme_label = tk.Label(widgets_frame, text="Event theme")
                event_theme_label.grid(row=1, column=0, sticky="w")

                # --> Event theme entry field
                event_theme = tk.Entry(widgets_frame, font=font, width=50)
                event_theme.grid(row=1, column=1, sticky="w")

                def trace_var(*args):
                    if last_value == "59" and min_str.get() == "0":
                        hour_str.set(int(hour_str.get()) + 1 if hour_str.get() != "23" else 0)
                    self.last_value = min_str.get()

                event_time_label = tk.Label(widgets_frame, text="Time")
                event_time_label.grid(row=2, column=0, sticky="w")

                # Event time selector field
                time_frame = tk.Frame(widgets_frame)
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

                event_information = scrolledtext.ScrolledText(widgets_frame, height=15)
                event_information.grid(row=3, column=1, sticky="w")

                def save_event():
                    time = datetime.strptime(f"{hour_box.get()}:{min_box.get()}", "%H:%M")
                    event = event_title.get()
                    if len(event) < 1:
                        messagebox.showwarning("Missing title", "Please set tile in order to create an Event")
                    else:
                        cal.calevent_create(date_selected, event, event_theme.get())
                        events.create_an_event(event_title.get(), event_theme.get(), date_selected, time,
                                               event_information.get(1.0, tk.END))
                        root.destroy()
                        messagebox.showinfo("Success", "Event has been created, congratulations!!")

                save_event_button = ttk.Button(widgets_frame, text="Save Event", command=save_event)
                save_event_button.grid(row=4, column=0, sticky="w")
            else:
                messagebox.showinfo("Date not allowed", "You can't create an event on this day!")

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="GoofyCoder.com")
        menu.add_command(label="Edit", command=edit_event)

        menu.add_command(label="Go to events day on Calendar")
        menu.add_command(label="Paste text")
        menu.add_command(label="Paste image")
        menu.add_command(label="Delete")

        def show_popup(event):
            menu.post(event.x_root, event.y_root)

        def OnDoubleClick(event):
            x = my_tree.selection()
            for e in x:
                text = my_tree.item(e, 'values')
                print(text)

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

        set_event_button = ttk.Button(event_navigation_frame, text="Create Event", command=create_event)
        set_event_button.pack(side=tk.LEFT)

        rm_event_button = ttk.Button(event_navigation_frame, text="Clear Events for this day",
                                     command=delete_all_today_events)
        rm_event_button.pack(side=tk.LEFT)

        # get_event_button = ttk.Button(event_navigation_frame, text="Get Event", command=get_event_info)
        # get_event_button.pack(side=tk.LEFT)

        delete_this_event = ttk.Button(event_navigation_frame, text="Delete Event", command=delete_event)
        delete_this_event.pack(side=tk.LEFT)

        def reupdate():
            def update(database_data):

                # events_id_list = cal.get_calevents(date)

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
            # --> Load events data
            data = events.get_all_events()

            # --> Update treeview data
            update(data)

        view_all_events_button = ttk.Button(event_navigation_frame, text="View all Event", command=reupdate)
        view_all_events_button.pack(side=tk.LEFT)

        style = ttk.Style()
        # style.theme_use('clam')  # -> uncomment this line if the styling does not work
        style.configure('my.DateEntry',
                        fieldbackground='light green',
                        background='dark green',
                        foreground='dark blue',
                        arrowcolor='white')
        self.count = 0

        def update(database_data):

            # events_id_list = cal.get_calevents(date)

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

        # --> Load events data
        data = events.get_all_events()

        # --> Update treeview data
        update(data)

        date_entry = DateEntry(event_navigation_frame, style='my.DateEntry', width=12, background='darkblue',
                               foreground='white', borderwidth=2, year=2010, locale='en_US', date_pattern='dd/MM/yyyy')
        date_entry.pack(padx=10, pady=10)
