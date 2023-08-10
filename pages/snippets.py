# IMPORT ALL REQUIRED MODULES AND LIBRARIES
import tkinter as tk
import pyglet
import tkinter.ttk as ttk
from .database_engine import SnippetsDatabase, SnippetCategoryDatabase
from tkinter import messagebox
import os
import customtkinter
from . import base
from PIL import Image
from tkinter import filedialog
import threading

# INITIALIZE DATABASES
db = SnippetsDatabase()
sn_db = SnippetCategoryDatabase()

# LOAD FONTS
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

# MAIN CLASS
class SnippetsPage(base.Page):
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)
        
        def cut_text():
            copy_text()
            delete_text()

        def copy_text():
            selection = snippets_display_screen.tag_ranges(tk.SEL)
            if selection:
                self.clipboard_clear()
                self.clipboard_append(snippets_display_screen.get(*selection))

        def paste_text(): snippets_display_screen.insert(tk.INSERT, self.clipboard_get())

        def paste_image():
            global img
            try:
                img = tk.PhotoImage(file=self.clipboard_get())
                position = snippets_display_screen.index(tk.INSERT)
                snippets_display_screen.image_create(position, image=img)
            except tk.TclError: pass

        def delete_text():
            selection = snippets_display_screen.tag_ranges(tk.SEL)
            if selection: snippets_display_screen.delete(*selection)

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Ephitome.com")
        menu.add_command(label="Cut", command=cut_text)

        menu.add_command(label="Copy", command=copy_text)
        menu.add_command(label="Paste", command=paste_text)
        menu.add_command(label="Paste image", command=paste_image)
        menu.add_command(label="Delete", command=delete_text)

        def show_popup(event): menu.post(event.x_root, event.y_root)
 
        menu_info = tk.Menu(self, tearoff=0)
        menu_info.add_command(label="Ephitome.com")
        menu_info.add_command(label="Add new Category")

        def show_popup_info_enter(event): menu_info.post(event.x_root, event.y_root)

        def show_popup_info_leave(event): menu_info.destroy
            

        # THIS FUCTION SERVES TO GET THE FILE FROM THE PATH AND NAME OF THE FILE
        def new_file():
            status.configure(text_color="white")
            # GET FILE PATH
            file = filedialog.askopenfilename()

            # IF THE LENGTH OF THE FILENAME IS EQUAL TO ZERO THE TAKE NO ACTION
            if len(file) == 0: pass
            else:
                # ELSE CHECK IF THE PATH OR FILENAME HAS THE REQUIRED EXTENSION
                if file.endswith('.py') or file.endswith('.md') or file.endswith('.txt') or file.endswith('.yaml') or file.endswith('.kv'):
                    # THIS FUCTION CALL WILL CLEAR ALL POPULATED FIELDS
                    clear_fields()
                    # OPEN FILE IN READ MODE
                    with open(file, 'r') as f:
                        try:
                            # SPLIT FILE ABSOLUTE PATH TO GET THE NAME OF THE FILE
                            title = os.path.split(file)[1].split('.')[0]
                            # INSERT FILENAME INTO SEARCH ENTRY
                            search.insert(0, title)
                            # READ THE FILE
                            code = f.read()
                            # INSERT THE CONTENTS OF THE FILE INTO THE TEXT AREA
                            snippets_display_screen.insert(tk.END, code)
                            # FINALLY RETURN A TURPLE WITH FILENAME AND CONTENTS, IN THIS CASE, CODE
                            return title, code
                        except UnicodeDecodeError: status.configure(text="File Error, system cannot decode file!", text_color="#da2f25")
                else: messagebox.showerror("None type", "You are trying to load a file that does not have .py extension!")

        # THIS FUNCTION CALL WILL POPULATE THE SEARCH AND SCREEN(TEXT) AREA
        def fill_out(_=None):
            status.configure(text_color="white")
            search.delete(0, tk.END)
            # ADD CLICKED/SELECTED LIST ITEM TO ENTRY(SEARCH) BOX
            search.insert(0, snippets_list.get("anchor"))
            
            try:
                # SEARCH SNIPPET IN DATABASE USING THE TITLE PULLED FROM THE LISTBOX, IN THIS CASE SNIPPETS LIST
                snippet = db.search_snippet(snippets_list.get("anchor"))
                # GET SNIPPET ID FROM THE DATA PULLED FROM THE DATABASE
                iid = snippet[0]
                # print(type(iid))
                # GET SNIPPET TITLE FROM THE DATA PULLED FROM THE DATABASE
                title = snippet[1]
                # GET SNIPPET CODE FROM THE DATA PULLED FROM THE DATABASE
                code = snippet[2]
                # GET SNIPPET CATEGORY FROM THE DATA PULLED FROM THE DATABASE
                category = snippet[3]
                
                # INSERT THE CODE INTO THE TEXT(SCREEN) AREA TO DISPLAY IT
                snippets_display_screen.delete('0.0', tk.END)
                snippets_display_screen.insert(tk.END, code)

                # DISPLAY SNIPPET ID IN THE ENTRY AREA IN THIS CASE, SNIPPET ID AREA
                snippet_id.configure(state=tk.NORMAL) # CHANGE ENTRY STATE TO BE ABLE TO WRITE TO IT
                snippet_id.delete(0, tk.END)
                snippet_id.insert(0, iid)
                snippet_id.configure(state=tk.DISABLED) # CHANGE ENTRY STATE TO BLOCK WRITING

                status.configure(text=f"{title} snippet on display")

            except IndexError as e:
                snippets_display_screen.delete('0.0', tk.END)
                status.configure(text=f"Query for snippet failed with exception{str(e)}", text_color="#da2f25")
                # messagebox.showinfo('Match failed', 'It seems there is no matching title in the Database\nPlease do check database or contact Admin.')
                # status.configure(text="No matching query in the database, Please do check database or contact Admin.!", text_color="#da2f25")

            

        # CHECK REQUIRED FIELDS FOR DATA IN ORDER TO ACTIVATE THE 'SAVE' BUTTON
        def check_fields_for_save(e=None):
            status.configure(text="")
            status.configure(text_color="white")
            snippet_pk = snippet_id.get()
            title = search.get().lower() # GET TITLE FROM SEARCH ENTRY
            #print(snippet_pk, ' ', len(snippet_pk), ' ', type(snippet_pk))
            #print(snippet_pk in db.list_snippets_ids_by_category(sn_db.get_category_object(categories.get())))
            code = snippets_display_screen.get('0.0', tk.END).strip() # GET CODE FROM TEXT(SCREEN) AREA

            # THIS STATEMENT WILL CHECK IF THE LENGTH OF BOTH TITLE & CODE AS WELL AS IF SNIPPET IS ALREADY AVAILABLE
            if len(title) != 0 and len(code) != 0 and title not in db.list_snippets_by_category(sn_db.get_category_object(categories.get())) and snippet_pk not in db.list_snippets_ids_by_category(sn_db.get_category_object(categories.get())):
                save_snippet_button.configure(state=tk.NORMAL, text_color='lime', font=customtkinter.CTkFont("Century Gothic",12,'bold')) # ACTIVATE BUTTON

            # DISABLE BUTTON IN THE ENTRES DONT MATCH THE CRITERIA
            elif title in db.list_snippets_by_category(sn_db.get_category_object(categories.get())):
                status.configure(text=f"{title} already in database!", text_color="turquoise")
            else: 
                save_snippet_button.configure(state=tk.DISABLED, text_color='red', font=customtkinter.CTkFont("Century Gothic",12))
                
                
        
        # THIS FUNCTION WILL LISTEN TO EVENTS AND EXECUTE ACCORDINGLY
        def listen_to_events(e=None):
            def start():
                t1 = threading.Thread(target=check_fields_for_save())
                t2 = threading.Thread(target=on_content_changed())
                
                t1.start()
                t2.start()
               
                t1.join()
                t2.join()
                
                self.after(500, start)
            start()
 
        # THIS FUNCTION WILL SAVE A NEW SNIPPET TO DATABASE
        def save_snippet():
            status.configure(text_color="white")
            title = search.get().replace('-', ' ')
            title = search.get().replace('_', ' ') # GET SNIPPET TITLE FROM SEARCH(ENTRY) AREA
            category = categories.get() # GET CATEGORY TITLE FROM CATEGORIES LIST(OPTIONMENU) AREA
            code = snippets_display_screen.get('0.0', tk.END).strip() # GET CODE FROM THE SCREEN(TEXT) AREA

            # DATA CLEANUP
            if '-' in title.split(): title.replace('-', ' ')
            elif '_' in title.split(): title.replace('_', ' ')
            
            database_insert_status = '' # INITIALIZE STATUS
            # CHECK IF THE SNIPPET IS ALREADY SAVED OR NOT
            if title in db.list_snippets_by_category(sn_db.get_category_object(categories.get())): database_insert_status = False  
            else: # IF NOT SAVED THEN PROCEED TO EXECUTE HERE
                ask = messagebox.askyesno('Alert', 'Are you sure you selected the right Category') # ASK USER TO CHECK CATEGORY
                if ask: 
                    database_insert_status = db.new_snippet(title, code.strip(), category) # IF YES THEN PROCEED HERE
                else: database_insert_status = 'cancel' # IF NOT, DO HERE

            # CHECK STATUS AND EXECUTE ALL REQUIRED STATEMENT
            if database_insert_status == 'saved':
                snippets_display_screen.insert(tk.END, code) # WITH SUCCESS INSERT/DISPLAY CODE TO SCREEN
                clear_fields() # CLEAR ALL THE POPULATED FIELDS
                status.configure(text=f"{title} succesfully saved!", text_color="#50e40f")# SHOW SUCCESS MSG TO USER
                
                # UPDATE THE SNIPPETS LIST WITH NEW DATABASE CONTENTS, ADDING THE NEW SNIPPET TO SNIPPETS LIST
                update(db.list_snippets_by_category(sn_db.get_category_object(categories.get())))
                # SHOW AVAILABLE SNIPPETS IN THIS CATEGORY
                snippets_count_label.configure(text=f'All available snippets in {categories.get().capitalize()}: {db.count_all_snippets_by_category(sn_db.get_category_object(categories.get()))}')
            elif database_insert_status == "cancel": # IF ITS CANCEL THEN EXECUTE HERE
                update(db.list_snippets_by_category(sn_db.get_category_object(categories.get())))
                status.configure(text=f"Cancelled!", text_color="#e1f105")
                

            elif database_insert_status == "exist": # IF ITS CANCEL THEN EXECUTE HERE
                update(db.list_snippets_by_category(sn_db.get_category_object(categories.get())))
                status.configure(text=f"{title} already in the database!", text_color="#9191ff")
                
        

        # THIS FUNCTION SOLEY CHECK WHATS BEING TYPED IN THE SEARCH(ENTRY) AREA AND COMPARE WITH THE DATABASE CONTENTS TO GET THE MATCHING ITEMS
        def check(_):
            typed = search.get() # GRAB WHAT IS TYPED IN THE SEARCH(ENTRY) IN REALTIME
            if typed == "": # IF TYPED IS NOTHING, IN THIS CASE SEARCH AREA EMPTY
                clear_fields()
                data = db.list_snippets_by_category(sn_db.get_category_object(categories.get())) # FILL LIST(LISTBOX) AREA WITH ALL SNIPPETS
            else:
                data = []
                # ITERATE ALL THE SNIPPETS IN DATABASE AND COMPARE WITH WHATS BEING TYPED AND UPDATE DATA
                for item in db.list_snippets_by_category(sn_db.get_category_object(categories.get())):
                    if typed.lower() in item.lower():
                        data.append(item) # APPEND ALL MATCHING SNIPPETS 

            update(data) # UPDATE SNIPPETS LIST

        # THIS FUNCTION GETS DATA AND UPDATE THE SNIPPETS LIST
        def update(snippets):
            snippets_list.delete(0, tk.END) # CLEAR SNIPPETS LIST(LISTBOX)
            for snippet in snippets: # ITERATE AND INSERT SNIPPETS INTO LIST
                snippets_list.insert(tk.END, snippet)
            
        # SEARCH DATABASE FOR AN INDIVIDUAL SNIPPET
        def search_snippet(_=None):
            status.configure(text_color="white")
            try:
                title = search.get() # GET WHATEVER NAME/TITLE DISPLAYED IN THE SEARCH/TEXT AREA
                snippet = db.search_snippet(title) # SEARCH DATABASE FOR THE REQUIRED SNIPPET USING THE TITLE
                sid = snippet[0] # SLICE THE DATA TURPLE AND GET THE ID
                code = snippet[2] # SLICE THE DATA TURPLE AND GET THE CODE
                clear_fields() # CLEAR ALL POPULATED FIELDS
                snippets_display_screen.insert(tk.END, code.strip()) # INSERT THE CODE/CONTENTS OF THE SNIPPET INTO THE SCREEN/TEXT AREA
                snippet_id.configure(state=tk.NORMAL) # CHANGE ENTRY STATE TO BE ABLE TO WRITE TO IT
                snippet_id.insert(0, iid)
                snippet_id.configure(state=tk.DISABLED) # CHANGE ENTRY STATE TO BLOCK WRITING
                update(db.list_snippets_by_category(sn_db.get_category_object(categories.get()))) # UPDATE SNIPPETS LIST
            except TypeError: # IF THE FIELD IS EMPTY OR NONE TYPE, EXECUTE THIS CODE
                status.configure(text="You are trying to search for an empty field!!", text_color="#da2f25")

        # DELETE SELECTED SNIPPET
        def delete_snippet():
            status.configure(text_color="white")
            title = snippets_list.get("anchor") # GET SELECTED SNIPPET
            if len(title) < 1: # CHECK IF THERE IS SOMETHING IN VARIABLE TITLE
                messagebox.showerror("Error", "No title selected, Please select Snippet to delete!") # ALERT USER IF THERE IS NO ITEM SELECTED
            else:
                ask = messagebox.askyesno("Alert", "Do you wish to proceed deleting this Snippet?") # GET CONFIRMATION FROM THE USER TO PROCEED 
                if ask: # IF YES, THE DELETE
                    deletion_status = db.delete_snippet(title) # DELETE FROM DATABASE AND RETURN DELETIONVSTATUS
                    if deletion_status: # IF DELETION STATUS IS SUCCESS
                        clear_fields() # CLEAR ALL POPULATED FIELDS
                        update(db.list_snippets_by_category(sn_db.get_category_object(categories.get()))) # UPDATE LIST WITH NEW SNIPPETS LIST
                        snippets_count_label.configure(text=f'All available snippets in {categories.get().capitalize()}: {db.count_all_snippets_by_category(sn_db.get_category_object(categories.get()))}')
                        status.configure(text="Snippet deletion successful!", text_color="#50e40f") # SHOW SUCCESS MSG
                    else: status.configure(text="Snippet deletion unsuccessful!", text_color="#da2f25")# ELSE SHOW ERROR MSG

        # UPDATE A SINGLE SNIPPET
        def update_db():
            status.configure(text_color="white")
            title = search.get() # GET WHATEVER IS IN THE SEARCH/ENTRY AREA
            code = snippets_display_screen.get('0.0', tk.END) # GET WHATEVER IS IN THE TEXT/SCREEN AREA
            # ----- Call database method and update changes made in title and code and return update status
            snippet_id.configure(state=tk.NORMAL) # CHANGE ENTRY STATE TO BE ABLE TO WRITE TO IT
            update_status = db.edit_snippet(snippet_id.get(), title, code.strip()) # EDIT DATABASE ENTRY
            snippet_id.configure(state=tk.DISABLED) # CHANGE ENTRY STATE TO BLOCK WRITING
            if update_status: # CHECK STATUS MSG IF ITS TRUE THEN PROCEED TO UPDATE THE SNIPPETS LIST
                update(db.list_snippets_by_category(sn_db.get_category_object(categories.get()))) # UPDATE LIST WITH NEW SNIPPETS LIST
                status.configure(text="Snippet update successful!", text_color="#50e40f") # SHOW SUCCESS MSG
            else:
                messagebox.showwarning("Failure", "Snippet update unsuccessful!") # ELSE SHOW ERROR MSG

        def run(): # RUN CODE/SNIPPET IN THE SCREEN/TEXT AREA
            status.configure(text_color="white")
            code = snippets_display_screen.get('0.1', tk.END)  # GET WHATEVER IS IN THE SCREEN/TEXT AREA
            if len(code) > 1:  # CHECK IF THERE IS SOMETHING IN VARIABLE CODE    
                with open("test_code.py", 'w') as f: # ----- Open a file with a .py extension and write mode
                    f.write(code) # ----- Write code/text from the textarea/screen to the .py file
                os.startfile("test_code.py") # ----- Now use os module to execute the file
            else:
                status.configure(text="Failed to run snippet!", text_color="#da2f25") # ELSE SHOW ERROR MSG

        # CLEAR ALL FIELDS
        def clear_fields():
            search.delete(0, tk.END)
            snippets_display_screen.delete('0.0', tk.END)
            snippet_id.configure(state=tk.NORMAL)
            snippet_id.delete(0, tk.END)
            snippet_id.configure(state=tk.DISABLED)
            update(db.list_snippets_by_category(sn_db.get_category_object(categories.get())))

        # LOAD ALL IMAGES
        SAVE_IMAGE = customtkinter.CTkImage(Image.open("img/icons/safe.png"))
        UPDATE_IMAGE = customtkinter.CTkImage(Image.open("img/icons/compose.png"))
        DELETION_IMAGE = customtkinter.CTkImage(Image.open("img/icons/delete.png"))
        RUN_IMAGE = customtkinter.CTkImage(Image.open("img/icons/play.png"))
        CLEAR_IMAGE = customtkinter.CTkImage(Image.open("img/icons/broom.png"))
        SEARCH_IMAGE = customtkinter.CTkImage(Image.open("img/icons/import.png"))

        # SEARCH AREA FRAME
        search_frame = customtkinter.CTkFrame(self)
        search_frame.pack(fill=tk.X, padx=5)

        # DELETE SNIPPET BUTTON
        delete_snippet_button = customtkinter.CTkButton(search_frame, width=80, text='DELETE', image=DELETION_IMAGE,command=delete_snippet)
        delete_snippet_button.image = DELETION_IMAGE
        delete_snippet_button.pack(side='left', padx=1)

        # -SAVE SNIPPET BUTTON
        save_snippet_button = customtkinter.CTkButton(search_frame, width=80, text='SAVE', font=customtkinter.CTkFont("Century Gothic",12), text_color='crimson', state=tk.DISABLED, image=SAVE_IMAGE, command=save_snippet)
        save_snippet_button.image = SAVE_IMAGE
        save_snippet_button.pack(side='left', padx=1)

        # UPDATE SNIPPET BUTTON
        update_snippet_button = customtkinter.CTkButton(search_frame, width=80, text='UPDATE', image=UPDATE_IMAGE,command=update_db)
        update_snippet_button.image = UPDATE_IMAGE
        update_snippet_button.pack(side='left', padx=1)

        # RUN SNIPPET BUTTON
        run_code_button = customtkinter.CTkButton(search_frame, width=80, text='RUN', image=RUN_IMAGE,command=run)
        run_code_button.image = RUN_IMAGE
        run_code_button.pack(side='left', padx=1)

        # CLEAR SNIPPET BUTTON
        clear_code_button = customtkinter.CTkButton(search_frame, width=80, text='CLEAR', image=CLEAR_IMAGE,command=clear_fields)
        clear_code_button.image = CLEAR_IMAGE
        clear_code_button.pack(side='left', padx=1)

        def show_readme():
            snippets_display_screen.delete('0.0', tk.END)
            data = db.get_readme_file(search.get())
            if data == None:
                snippets_display_screen.insert(tk.END, "README file unavailable!")
            else:
                snippets_display_screen.insert(tk.END, data.code)

            status.configure(text=f"{search.get()} README file on display")
        
        def show_snippet():
            snippets_display_screen.delete('0.0', tk.END)
            snippets_display_screen.insert(tk.END, db.get_snippet_info_by_name(search.get())["code"])
            status.configure(text=f"{search.get()} snippet on display")

        # THIS IS THE MAIN SEARCH AREA
        search = customtkinter.CTkEntry(search_frame, font = customtkinter.CTkFont("Century Gothic", 12))
        search.pack(expand=True, side='left', padx=5, fill=tk.X)
        search.focus_set()

        # SEARCH BUTTON BINDS
        search.bind("<KeyRelease>", check)
        search.bind("<<Motion>>", check_fields_for_save)
        search.bind('<Return>', search_snippet)
        search.bind('<Enter>', check_fields_for_save)
        
        # NEW SNIPPET FROM SCRIPTS BUTTON
        get_new_snippet_button = customtkinter.CTkButton(search_frame, width=80, text= 'Load Script',image=SEARCH_IMAGE, command=new_file)
        get_new_snippet_button.image = SEARCH_IMAGE
        get_new_snippet_button.pack(side='left', padx=5)

        # ALL BINDINGS
        '''
        delete_snippet_button.bind("<Enter>", lambda x: main_label.configure(text="delete snippet"))
        delete_snippet_button.bind("<Leave>", lambda x: main_label.configure(text="Snippets"))

        save_snippet_button.bind("<Enter>", lambda x: main_label.configure(text="save snippet"))
        save_snippet_button.bind("<Leave>", lambda x: main_label.configure(text="Snippets"))

        search_snippet_button.bind("<Enter>", lambda x: main_label.configure(text="search snippet"))
        search_snippet_button.bind("<Leave>", lambda x: main_label.configure(text="Snippets"))

        update_snippet_button.bind("<Enter>", lambda x: main_label.configure(text="update snippet"))
        update_snippet_button.bind("<Leave>", lambda x: main_label.configure(text="Snippets"))

        get_new_snippet_button.bind("<Enter>", lambda x: main_label.configure(text="get new snippet from file"))
        get_new_snippet_button.bind("<Leave>", lambda x: main_label.configure(text="Snippets"))

        run_code_button.bind("<Enter>", lambda x: main_label.configure(text="test run snippet"))
        run_code_button.bind("<Leave>", lambda x: main_label.configure(text="Snippets"))

        clear_code_button.bind("<Enter>", lambda x: main_label.configure(text="clear everything in text area"))
        clear_code_button.bind("<Leave>", lambda x: main_label.configure(text="Snippets"))
        '''

        # MAIN FRAME TO HOLD LISTBOX AND TEXT(SCREEN)
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(fill='both', expand=True, padx=7, pady=7)
        
        # THIS IS THE FRAME ON THE FAR LEFT CONTAINING SNIPPETS LIST
        snippets_list_and_recents_frame = customtkinter.CTkFrame(main_frame)
        snippets_list_and_recents_frame.pack(side='left', fill=tk.Y)

        # THIS IS THE FRAME ON THE FAR RIGHT CONTAINING CATEGORIS, AVAILBLE SNIPPETS LABLE AND ID
        category_and_available_snippets_frame = customtkinter.CTkFrame(main_frame)
        category_and_available_snippets_frame.pack(side='top', anchor=tk.N, pady=5, fill=tk.X)

        # SNIPPETS SCREEN FRAME
        snippets_screen_frame = customtkinter.CTkFrame(main_frame)
        snippets_screen_frame.pack(side='top', fill=tk.BOTH, expand=True)

        status_frame = customtkinter.CTkFrame(main_frame)
        status_frame.pack(side='bottom', anchor=tk.N, pady=5, fill=tk.X)

         # SNIPPETS ID FRAME
        snippet_id_frame = customtkinter.CTkFrame(category_and_available_snippets_frame)
        snippet_id_frame.pack(side='right', anchor=tk.E)

        # SNIPPET ID LABEL
        snippet_id_label = customtkinter.CTkLabel(snippet_id_frame, text="Snippet ID: ", font=customtkinter.CTkFont("Century Gothic", 12, 'bold'))
        snippet_id_label.pack(side='left')

        # SNIPPET ID
        snippet_id = customtkinter.CTkEntry(snippet_id_frame, font=customtkinter.CTkFont("Century Gothic", 12, 'bold'))
        snippet_id.pack(side='left')

        # THIS FUNCTION UPDATES THE CATEGORY OPTION MENU
        def update_list_category(cat=None):
            search.delete(0, tk.END)
            snippets_display_screen.delete('0.0', tk.END)
            update(db.list_snippets_by_category(sn_db.get_category_object(cat)))
            if categories.get() != 'python':
                snip.forget()
                readme.forget()
            else:
                snip.pack(side=tk.LEFT, padx=5)
                readme.pack(side=tk.LEFT, padx=5)
            snippets_count_label.configure(text=f'All available snippets in {cat.capitalize()}: {db.count_all_snippets_by_category(sn_db.get_category_object(categories.get()))}')
                              
        # CATEGORIES LIST OPTION MENU
        categories = customtkinter.CTkOptionMenu(category_and_available_snippets_frame, values=sn_db.get_all_categories(), command=update_list_category)
        categories.pack(side=tk.LEFT)
        categories.bind('<Enter>', lambda e: categories.configure(values=sn_db.get_all_categories()))

         # ADD NEW CATEGORY BUTTON
        snip = customtkinter.CTkButton(category_and_available_snippets_frame, text='<snippet', text_color='lime', width=1, command=show_snippet)
        #snip.pack(side=tk.LEFT, padx=5)
        
        readme = customtkinter.CTkButton(category_and_available_snippets_frame, text='readme>', text_color='lime', width=1, command=show_readme)
        #readme.pack(side=tk.LEFT, padx=5)
        # add_new_category.bind('<Enter>', show_popup_info_enter)
        readme.bind('<Enter>', lambda e: status.configure(text="Check README"))
        readme.bind('<Leave>', lambda e: status.configure(text=""))

        # SNIPPETS COUNT LABEL
        snippets_count_label = customtkinter.CTkLabel(category_and_available_snippets_frame, text=f'All available snippets in {categories.get().capitalize()}: {db.count_all_snippets_by_category(sn_db.get_category_object(categories.get()))}',
                                        font=("Century Gothic", 14, 'bold'))
        snippets_count_label.pack(side=tk.LEFT) 

        # 
        all_snippets_frame = customtkinter.CTkFrame(snippets_list_and_recents_frame)
        all_snippets_frame.pack(fill=tk.Y, expand=True)

        # SNIPPETS LIST SCROLLBAR
        snippets_list_scrollbar = customtkinter.CTkScrollbar(all_snippets_frame, orientation='vertical')

        # LIST TO DISPLAY SNIPPETS
        snippets_list = tk.Listbox(all_snippets_frame, width=40, yscrollcommand=snippets_list_scrollbar.set, font=("Century Gothic", 10), relief='flat', 
                                    selectmode=tk.BROWSE, selectforeground='black', selectbackground='lightgrey', activestyle='dotbox',  selectborderwidth=0, borderwidth=5)
        snippets_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # PACK AND CONFIGURE SNIPPETS LIST SCROLLBAR
        snippets_list_scrollbar.pack(side='left', fill='y', expand=True)
        snippets_list_scrollbar.configure(command=snippets_list.yview)

        # SNIPPETS LIST BINDS
        snippets_list.bind("<<ListboxSelect>>", fill_out)
        snippets_list.bind('<Return>', search_snippet)
        
        # UPDATE THE LIST WITH DATA FROM THE DATABASE BY CATEGORY
        update(db.list_snippets_by_category(sn_db.get_category_object(categories.get())))

        def on_content_changed(event=None):
            update_line_numbers()

        def get_line_numbers():
            output = ''
            row, col = snippets_display_screen.index("end").split('.')

            for i in range(1, int(row)):
                output += str(i)+ '\n'
            return output

        def update_line_numbers(event = None):
            line_numbers = get_line_numbers()
            line_number_bar.configure(state='normal')
            line_number_bar.delete('0.0', 'end')
            line_number_bar.insert('0.0', line_numbers)
            line_number_bar.configure(state='disabled')

        shortcut_bar = customtkinter.CTkFrame(snippets_screen_frame, height=25, bg_color='light seagreen')
        shortcut_bar.pack(expand='no', fill='y', side='left')

        line_number_bar = customtkinter.CTkTextbox(shortcut_bar, border_color=None, activate_scrollbars=False, width=4, font=customtkinter.CTkFont("Courier New", 16), border_width=1, takefocus=0, border_spacing=0, state='disabled', wrap='none')
        line_number_bar.pack(fill=tk.Y, anchor='center', expand=True, ipady=2, ipadx=8)

        # Main screen to view snippet contents
        snippets_display_screen = customtkinter.CTkTextbox(snippets_screen_frame, wrap='word', font=customtkinter.CTkFont("Courier New", 16), border_width=1)
        snippets_display_screen.pack(side='left', fill=tk.BOTH, expand=True)

        # SNIPPETS DISPLAY SCREEN BINDS
        snippets_display_screen.bind("<Button-3>", show_popup)
        #snippets_display_screen.bind('<Any-KeyPress>', on_content_changed)

        def on_content_changed(event=None):
            update_line_numbers()
            update_cursor_info_bar()

        show_cursor_info_checked = True
        def show_cursor_info_bar():
            
            if show_cursor_info_checked:
                cursor_info_bar.pack(expand='no', fill=None, side='right',anchor='se')
            else:
                cursor_info_bar.pack_forget()

        def update_cursor_info_bar(event=None):
            row, col = snippets_display_screen.index(tk.INSERT).split('.')
            line_num, col_num = str(int(row)), str(int(col)+1) # col starts at 0
            infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
            cursor_info_bar.configure(text=infotext)

        status = customtkinter.CTkLabel(status_frame, text='..........')
        status.pack(expand=tk.NO, padx=(10, 0), fill=None, side=tk.LEFT, anchor='sw')

        cursor_info_bar = customtkinter.CTkLabel(status_frame, text='Line: 1 | Column: 1')
        cursor_info_bar.pack(expand=tk.NO, fill=None, side=tk.RIGHT, anchor='se')

        # EVENTS SECTION
        listen_to_events()
        
