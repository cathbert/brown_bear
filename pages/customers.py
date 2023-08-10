# --> Load required modules
import os
import tkinter as tk
from . import base
import tkinter.ttk as ttk
from pages.database_engine import CustomerDatabase
from tkinter import messagebox, StringVar, filedialog
import customtkinter

# --> Initialize customers database
customers = CustomerDatabase()


class CustomersPage(base.Page):  # --> Customer Page inheriting from base module
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)  # --> Initialize base Page

        # --> Set theme color and font
        theme_color = "#003B4A"
        theme_font = ("helvetica", 12)
        entries_bg_color = "#003B4A"
        entries_fg_color = "#ffff00"

        # --> Frame to hold the page title
        customer_page_title_frame = customtkinter.CTkFrame(self)
        customer_page_title_frame.pack(fill=tk.BOTH)

        # --> Set page title
        customer_page_title = customtkinter.CTkLabel(customer_page_title_frame, text="Customer Database", font=customtkinter.CTkFont("helvetica", 12))
        customer_page_title.pack(side="top", fill="both", expand=True)

        # --> Create main frame that will hold all the widgets
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(side='top', fill='both', expand=True)

        # --> This frame will hold the list of all the customers
        customer_list_frame = customtkinter.CTkFrame(main_frame)
        customer_list_frame.pack(side='top', fill='both', expand=True)

        # --> This frame will contain all widgets to manipulate the customers database
        customer_controls_frame = customtkinter.CTkFrame(main_frame)
        customer_controls_frame.pack(side='top', fill='both', expand=True, anchor=tk.N)

        # -------------------------------------DIRECTORY TREEVIEW SECTION-----------------------------------------------

        # --> Add some style to the tree view below
        style = ttk.Style()

        # print(style.theme_names())
        '''winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'''

        # --> Pick a theme
        style.theme_use("clam")

        # --> Configure our treeview colors
        style.configure("Treeview", background='#DDD5C6', foreground="black", rowheight=25, font=customtkinter.CTkFont("helvetica", 12),
                        fieldbackground='#DDD5C6', rowwidth=200)

        # --> Change selected color
        style.map("Treeview", background=[("selected", theme_color)])

        # --> Treeview Scrollbar
        tree_scroll = tk.Scrollbar(customer_list_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --> Create Treeview
        my_tree = ttk.Treeview(customer_list_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # --> Configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # --> Define columns
        my_tree["columns"] = ('Id','First Name', 'Last Name', "Cell Number", 'Email', 'Home Address 1', 'Home Address 2', 'Home Address 3')

        # --> Format tree columns
        my_tree.column("#0", width=0, stretch=tk.NO)
        my_tree.column("Id", anchor=tk.CENTER, width=6)
        my_tree.column("First Name", anchor=tk.W, width=100)
        my_tree.column("Last Name", anchor=tk.W, width=100)
        my_tree.column("Cell Number", anchor=tk.CENTER, width=10)
        my_tree.column("Email", anchor=tk.W, width=40)
        my_tree.column("Home Address 1", anchor=tk.W, width=255)
        my_tree.column("Home Address 2", anchor=tk.W, width=255)
        my_tree.column("Home Address 3", anchor=tk.W, width=255)

        # --> Create tree Headings
        my_tree.heading("#0", text="", anchor=tk.CENTER)
        my_tree.heading("Id", text="ID", anchor=tk.CENTER)
        my_tree.heading("First Name", text="First Name", anchor=tk.W)
        my_tree.heading("Last Name", text="Last Name", anchor=tk.W)
        my_tree.heading("Cell Number", text="Cell Number", anchor=tk.CENTER)
        my_tree.heading("Email", text="Email", anchor=tk.W)
        my_tree.heading("Home Address 1", text="Address_line_1", anchor=tk.W)
        my_tree.heading("Home Address 2", text="Address_line_2", anchor=tk.W)
        my_tree.heading("Home Address 3", text="Address_line_3", anchor=tk.W)

        # --> Create striped row tags
        my_tree.tag_configure("oddrow", background="#DDD5C6")
        my_tree.tag_configure("evenrow", background="#CCBF99")

        # --> This function is for updating treeview
        self.count = 0

        def update(database_data):
            # --> Select everything in treeview
            # x = my_tree.selection()
            # --> Clear everything from tree
            my_tree.delete(*my_tree.get_children())

            # -- Iterate through the contacts from the database
            for contact in database_data:

                # --> Check if counter variable contains an odd number or an even number
                if self.count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=self.count, text="",
                                   values=(contact[0], contact[1], contact[2], "0" + str(contact[3]), contact[4], contact[5], contact[6], contact[7]),
                                   tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=self.count, text="",
                                   values=(contact[0], contact[1], contact[2], "0" + str(contact[3]), contact[4], contact[5], contact[6], contact[7]),
                                   tags=('oddrow',))

                # -- Increment count by 1
                self.count += 1

        # --> Load customers data
        data = customers.get_all_customers()

        # --> Update treeview data
        update(data)

        # --> Remove one customer
        ''''
        def delete_customer():
            x = my_tree.selection()[0]
            text = my_tree.item(x, 'values')
            deletion_info = customers.delete_customer(text[0])
            # print(text)
            # print(deletion_info)

            if deletion_info:
                messagebox.showinfo("Contact deleted!", f"Successfully deleted {text[0]}")
                my_tree.delete(x)
            else:
                messagebox.showerror("Deletion failed!", f"Failed to delete contact {text[0]}")
        '''

        def delete_multiple():
            x = my_tree.selection()
            for e in x:
                text = my_tree.item(e, 'values')
                my_tree.delete(e)
                customers.delete_customer(text[0])
            messagebox.showinfo("Deletion successful", f"{len(x)} contacts deleted!")

        def fill_out(_):
            x = my_tree.selection()[0]
            text = my_tree.item(x, 'values')

            clear_entries()

            customer_id_display.insert(tk.END, text[0])
            firstname_entry_update.insert(tk.END, text[1])
            lastname_entry_update.insert(tk.END, text[2])
            phone_entry_update.insert(tk.END, text[3])
            email_entry_update.insert(tk.END, text[4])
            home_address1_entry.insert(tk.END, text[5])
            home_address2_entry.insert(tk.END, text[6])
            home_address3_entry.insert(tk.END, text[7])

        def check(_):
            # --> grab what is typed
            typed = str(search_customer.get())

            if typed == "":
                customers_data = customers.get_all_customers()
            else:
                customers_data = []
                for item in customers.get_all_customers():
                    if typed.lower() in item[1].lower():
                        customers_data.append(item)

            # --> Clear everything from tree
            my_tree.delete(*my_tree.get_children())

            update(customers_data)

        def add_new_customer():
            f_name = firstname_entry_update.get()
            l_name = lastname_entry_update.get()
            phone = phone_entry_update.get()
            email = email_entry_update.get()
            address1 = home_address1_entry.get()
            address2 = home_address2_entry.get()
            address3 = home_address3_entry.get()

            customers.new_customer(f_name.capitalize(), l_name.capitalize(), phone, email, address1,address2,address3)
            clear_entries()
            update(customers.get_all_customers())

        def edit_customer_info():
            f_name = firstname_entry_update.get()
            l_name = lastname_entry_update.get()
            phone = phone_entry_update.get()
            email = email_entry_update.get()
            address1 = home_address1_entry.get()
            address2 = home_address2_entry.get()
            address3 = home_address3_entry.get()

            add = customers.edit_customer(customer_id_display.get(), f_name, l_name, phone, email, address1, address2, address3)
            if add:
                clear_entries()
                # --> Select everything in treeview
                x = my_tree.selection()

                # --> Iterate through all the rows and clear everything
                for _ in x:
                    my_tree.delete(x)
                update(customers.get_all_customers())
                messagebox.showinfo("Success", "customer information updated")
            else:
                messagebox.showerror("Failure", "Select customer to update")

        def clear_entries():
            firstname_entry_update.delete(0, tk.END)
            lastname_entry_update.delete(0, tk.END)
            phone_entry_update.delete(0, tk.END)
            email_entry_update.delete(0, tk.END)
            home_address1_entry.delete(0, tk.END)
            home_address2_entry.delete(0, tk.END)
            home_address3_entry.delete(0, tk.END)
            customer_id_display.delete(0, tk.END)

        # --> This frame hold the firstname and lastname entries
        names_phone_email_entry_frame = customtkinter.CTkFrame(customer_controls_frame)
        names_phone_email_entry_frame.pack(fill='x', side=tk.TOP, anchor=tk.N)

        # This frame holds home address entry
        home_address_entry_frame = customtkinter.CTkFrame(customer_controls_frame)
        home_address_entry_frame.pack(fill='x', side=tk.TOP, anchor=tk.N)

        # --> First name entry
        firstname_entry_update = customtkinter.CTkEntry(names_phone_email_entry_frame, width=25, placeholder_text="first",
                                          font=("helvetica", 12, "bold"))
        firstname_entry_update.pack(side='left', padx=2, anchor=tk.N, expand=True, fill=tk.X)

        # --> Last name entry
        lastname_entry_update = customtkinter.CTkEntry(names_phone_email_entry_frame, width=30, placeholder_text="last name",
                                         font=("helvetica", 12, "bold"))
        lastname_entry_update.pack(side='left', padx=2, expand=True, fill=tk.X)

        # --> Phone number entry
        phone_entry_update = customtkinter.CTkEntry(names_phone_email_entry_frame, placeholder_text="phone",
                                      font=("helvetica", 12, "bold"))
        phone_entry_update.pack(side='left', padx=2, expand=True, fill=tk.X)

        # --> Email entry
        email_entry_update = customtkinter.CTkEntry(names_phone_email_entry_frame, width=35, placeholder_text="email",
                                      font=("helvetica", 12, "bold"))
        email_entry_update.pack(side='left', padx=2, expand=True, fill=tk.X)

        # --> Home address entry
        home_address1_entry = customtkinter.CTkEntry(home_address_entry_frame, width=35, placeholder_text="address",
                                      font=("helvetica", 12, "bold"))
        home_address1_entry.pack(side='left', padx=2, expand=True, fill=tk.X)
        home_address2_entry = customtkinter.CTkEntry(home_address_entry_frame, width=35, placeholder_text="address",
                                      font=("helvetica", 12, "bold"))
        home_address2_entry.pack(side='left', padx=2, expand=True, fill=tk.X)
        home_address3_entry = customtkinter.CTkEntry(home_address_entry_frame, width=35, placeholder_text="address",
                                      font=("helvetica", 12, "bold"))
        home_address3_entry.pack(side='left', padx=2, expand=True, fill=tk.X)

        # --> customer list database control panel frame
        button_panel_frame = customtkinter.CTkFrame(customer_controls_frame)
        button_panel_frame.pack(fill='x')

        new_customer_button = customtkinter.CTkButton(button_panel_frame, text='New customer',command=add_new_customer, font=customtkinter.CTkFont("helvetica", 12))
        new_customer_button.pack(side='left')

        # delete_customer_button = customtkinter.CTkButton(button_panel_frame, text='Delete Customer', relief='groove', bg='red',
        #                                 command=delete_customer, font=customtkinter.CTkFont("helvetica", 12))
        # delete_customer_button.pack(side='left')

        edit_customer = customtkinter.CTkButton(button_panel_frame, text='Update Customer',command=edit_customer_info, font=customtkinter.CTkFont("helvetica", 12))
        edit_customer.pack(side='left')

        delete_multiple = customtkinter.CTkButton(button_panel_frame, text='Delete Customer/s',font=customtkinter.CTkFont("helvetica", 12), command=delete_multiple)
        delete_multiple.pack(side='left')

        clear_entry_fields = customtkinter.CTkButton(button_panel_frame, text='Clear entry fields',font=customtkinter.CTkFont("helvetica", 12), command=clear_entries)
        clear_entry_fields.pack(side='left')

        search_customer = customtkinter.CTkEntry(button_panel_frame, font=customtkinter.CTkFont("helvetica", 12), width=40)
        search_customer.insert(0, "Search Customer")
        search_customer.pack(side='left', padx=10)

        search_customer.bind('<Button-1>', lambda e: search_customer.delete(0, tk.END))
        search_customer.bind('<KeyRelease>', check)

        my_tree.bind("<<TreeviewSelect>>", fill_out)

        customer_id_display = customtkinter.CTkEntry(button_panel_frame, font=customtkinter.CTkFont("helvetica", 12))
        customer_id_display.pack(side='left', padx=10)

        section_demarkater = customtkinter.CTkLabel(customer_controls_frame, text="_" * 400)
        section_demarkater.pack()

        output_frame = customtkinter.CTkFrame(customer_controls_frame)
        output_frame.pack(fill='x', padx=10, side=tk.TOP, anchor=tk.N)

        def change_functionality():
            # myLabel = Label(root, text=myCombo.get()).pack()
            customers_data = customers.get_all_customers()
            import csv
            if combo_option_menu.get() == 'txt':
                file_path = filedialog.asksaveasfilename()

                if os.path.exists(file_path + ".txt"):
                    messagebox.showinfo("Info", "File already exists")
                else:
                    with open(file_path + ".txt", "w") as f:
                        for line in customers_data:
                            f.write(f"{line[0]},{line[1]},{line[2]},{line[3]},{line[4], line[5]}\n")
            if combo_option_menu.get() == 'csv':
                print("Csv")
                spreadsheet = csv.writer(open('data.csv', 'w', newline=''))
                for line in customers_data:
                    spreadsheet.writerow([line[0], line[1], line[2], line[3], line[4], line[5]])
                # customers.get_all_customers()
            elif combo_option_menu.get() == "pdf":
                print("Pdf")
                from pdf_creator import PdfEngine
                t = PdfEngine()
                t.generate_customers_list()

            elif combo_option_menu.get() == 'json':
                from json_creator import create_customers_json
                create_customers_json()
            else:
                pass
                # myLabel = customtkinter.CTkLabel(output_frame, text=myCombo.get()).pack()

        options = [
            "Select output format",
            ".TXT",
            ".PDF",
            ".CSV",
            ".DOCX",
            ".JSON",
        ]

        combo_label = customtkinter.CTkLabel(output_frame, text="Mode:")
        combo_label.pack(side=tk.LEFT)
        combo_option_menu = customtkinter.CTkOptionMenu(output_frame, values=options, command=change_functionality)
        combo_option_menu.pack(side=tk.LEFT)

        clicked = StringVar()
        clicked.set(options[0])
        '''
        my_combo = ttk.Combobox(output_frame, value=options, font=('Verdana', 11), width=16)
        my_combo.current(0)
        # my_combo.bind("<<ComboboxSelected>>", combo_click)
        my_combo.pack(side=tk.LEFT)
       
        my_button = tk.Button(output_frame, text="Output to file", command=change_functionality)
        my_button.pack(side=tk.LEFT)
        '''
