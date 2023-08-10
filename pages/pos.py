import tkinter as tk

from . import base
import customtkinter
from tkinter import ttk, IntVar, StringVar
from tkinter import messagebox
from datetime import datetime
from random import randint
from datetime import datetime
import random
import string
from pages.database_engine import CustomerDatabase, JobDatabase
from PIL import Image

customers = CustomerDatabase()
order_db = JobDatabase()

class PosPage(base.Page):
    def __init__(self, *args, **kwargs):
        base.Page.__init__(self, *args, **kwargs)

        def view_order(e=None):
            order_number.configure(state=tk.NORMAL)
            order_screen.configure(state=tk.NORMAL)
            order_screen.delete('1.0', tk.END)
            order_screen.insert(1.0, order_db.get_selected_order(order_number=order_list.get("anchor")))
            print(order_db.get_selected_order(order_number=order_list.get("anchor")))
            order_screen.configure(state=tk.DISABLED)
            order_number.configure(state=tk.DISABLED)

        
        def edit_order(e=None):
            order_number.configure(state=tk.NORMAL)
            order_number.delete(0,tk.END)
            order_number.insert(0, order_list.get("anchor"))
            order_number.configure(state=tk.DISABLED)
            print(order_db.get_selected_order(order_list.get("anchor")).split('\n'))

        style = ttk.Style()

        def cut_text():
            copy_text()
            delete_text()

        def copy_text():
            selection = snippets_display_screen.tag_ranges(tk.SEL)
            if selection:
                self.clipboard_clear()
                self.clipboard_append(snippets_display_screen.get(*selection))

        def paste_text():
            snippets_display_screen.insert(tk.INSERT, self.clipboard_get())

        def paste_image():
            global img
            try:
                img = tk.PhotoImage(file=self.clipboard_get())
                position = snippets_display_screen.index(tk.INSERT)
                snippets_display_screen.image_create(position, image=img)
            except tk.TclError:
                pass

        def delete_text():
            selection = snippets_display_screen.tag_ranges(tk.SEL)
            if selection:
                snippets_display_screen.delete(*selection)

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="ephitome.com")
        menu.add_command(label="Open", command=view_order)

        menu.add_command(label="Edit", command=edit_order)
        #menu.add_command(label="Paste text", command=paste_text)
        #menu.add_command(label="Paste image", command=paste_image)
        #menu.add_command(label="Delete", command=delete_text)

        def show_popup(event):
            menu.post(event.x_root, event.y_root)

        # main csp label frame
        main_label_frame = customtkinter.CTkFrame(self)
        main_label_frame.pack(side=tk.TOP, fill="x", anchor=tk.N)

        logo = customtkinter.CTkImage(Image.open("icons/csp_face_logo.png"))

        #lebel in top frame
        title_label = customtkinter.CTkLabel(main_label_frame, text='csp point of sale', compound=tk.LEFT, image=logo, font=("Allstar", 30, "bold"))
        title_label.pack(expand=True)

        # ---> MAIN WIDGETS FRAME
        main_widgets_frame = customtkinter.CTkFrame(self)
        main_widgets_frame.pack(side=tk.TOP, fill="both", expand=True, anchor=tk.N)

        # ---> PRODUCTS FRAME
        products_frame = customtkinter.CTkFrame(main_widgets_frame,border_width=5)
        products_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        order_list_frame = customtkinter.CTkFrame(main_widgets_frame,border_width=5, corner_radius=5, width=20)
        order_list_frame.pack(side=tk.LEFT, anchor=tk.N)

        def update_orders_list(orders):
            # ----- First delete the snippets list
            order_list.delete(0, tk.END)
            # ----- Now iterate and insert snippets into the list
            for order in orders:
                order_list.insert(tk.END, order)

        def filter_view(e=None):
            if e == 'Pending':
                update_orders_list(order_db.get_pending_orders())
            elif e == 'Completed':
                update_orders_list(order_db.get_completed_orders())
            elif e == 'All':
                update_orders_list(order_db.get_all_orders())


        # Orders label
        orders_list_label = customtkinter.CTkLabel(order_list_frame, text='ORDERS', font=("Century Gothic", 14, 'bold'), bg_color='transparent')
        orders_list_label.pack()

        list_frame = customtkinter.CTkFrame(order_list_frame)
        list_frame.pack(expand=True, padx=5, anchor=tk.N)

        orders_listbox_scrbar = customtkinter.CTkScrollbar(list_frame, orientation='vertical')
        order_list = tk.Listbox(list_frame, font=customtkinter.CTkFont("Century Gothic", 14, 'bold'), relief='flat', selectmode=tk.BROWSE, selectforeground='black', height=20, 
                                                                    selectbackground='lightgrey', activestyle='dotbox',  selectborderwidth=0, borderwidth=10, 
                                                                    yscrollcommand=orders_listbox_scrbar.set)
        order_list.pack(side=tk.LEFT, expand=True)
        orders_listbox_scrbar.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.S)
        orders_listbox_scrbar.configure(command=order_list.yview)

        order_list.bind('<Double-1>', view_order)
        order_list.bind('<Button-3>', show_popup)

        update_orders_list(order_db.get_all_orders())

        # ---> ORDERS FILTERING FRAME
        orders_filter_frame = customtkinter.CTkFrame(order_list_frame,border_width=2, corner_radius=40, fg_color='black', bg_color='transparent')
        orders_filter_frame.pack(fill=tk.BOTH, expand=True)

        # ---> FILTER LABEL
        filter_label = customtkinter.CTkLabel(orders_filter_frame, text='Filter Orders', text_color='lime', font=customtkinter.CTkFont("Century Gothic", 14, 'bold'))
        filter_label.pack(padx=5, pady=8)

        # ---> FILTERING OPTIONS
        filter_toggle_button = customtkinter.CTkOptionMenu(orders_filter_frame, values=['All', 'Pending','Completed'], command=filter_view)
        filter_toggle_button.pack()

        #bottom frame for buttons
        screen_frame = customtkinter.CTkFrame(main_widgets_frame)
        screen_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # notbook widget tabarent
        tabs_parent = customtkinter.CTkTabview(products_frame, border_color='white')
        tabs_parent.pack(fill="both", expand=True, padx=10, pady=10)
        
        # tab1234 in notbook wigget tab parent
        tab1 = tabs_parent.add("Product")
        tab2 = tabs_parent.add("Additional Requirements")
        tab3 = tabs_parent.add("Others")
        tab4 = tabs_parent.add("Deals")

        def activate_products_fields(e=None):
            if e != 'Select Customer':
                option_1_product.configure(state=tk.NORMAL)
                option_2_product.configure(state=tk.NORMAL)
                option_3_product.configure(state=tk.NORMAL)
                option_4_product.configure(state=tk.NORMAL)
                option_5_product.configure(state=tk.NORMAL)
                option_6_product.configure(state=tk.NORMAL)
                option_7_product.configure(state=tk.NORMAL)
                option_8_product.configure(state=tk.NORMAL)
                option_9_product.configure(state=tk.NORMAL)
                option_10_product.configure(state=tk.NORMAL)

        def activate_option_1_product_extras(e=None):
            if e != '':
                option_1_product_print_type.configure(state=tk.NORMAL)
                option_1_product_size.configure(state=tk.NORMAL)
                option_1_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_1_product_print_type.configure(state=tk.DISABLED)
                option_1_product_size.configure(state=tk.DISABLED)
                option_1_product_qty.configure(state=tk.DISABLED)
                

        def activate_option_2_product_extras(e=None):
            if e != '':
                option_2_product_print_type.configure(state=tk.NORMAL)
                option_2_product_size.configure(state=tk.NORMAL)
                option_2_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_2_product_print_type.configure(state=tk.DISABLED)
                option_2_product_size.configure(state=tk.DISABLED)
                option_2_product_qty.configure(state=tk.DISABLED)
                

        def activate_option_3_product_extras(e=None):
            if e != '':
                option_3_product_print_type.configure(state=tk.NORMAL)
                option_3_product_size.configure(state=tk.NORMAL)
                option_3_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_3_product_print_type.configure(state=tk.DISABLED)
                option_3_product_size.configure(state=tk.DISABLED)
                option_3_product_qty.configure(state=tk.DISABLED)

        def activate_option_4_product_extras(e=None):
            if e != '':
                option_4_product_print_type.configure(state=tk.NORMAL)
                option_4_product_size.configure(state=tk.NORMAL)
                option_4_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_4_product_print_type.configure(state=tk.DISABLED)
                option_4_product_size.configure(state=tk.DISABLED)
                option_4_product_qty.configure(state=tk.DISABLED)

        def activate_option_5_product_extras(e=None):
            if e != '':
                option_5_product_print_type.configure(state=tk.NORMAL)
                option_5_product_size.configure(state=tk.NORMAL)
                option_5_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_5_product_print_type.configure(state=tk.DISABLED)
                option_5_product_size.configure(state=tk.DISABLED)
                option_5_product_qty.configure(state=tk.DISABLED)

        def activate_option_6_product_extras(e=None):
            if e != '':
                option_6_product_print_type.configure(state=tk.NORMAL)
                option_6_product_size.configure(state=tk.NORMAL)
                option_6_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_6_product_print_type.configure(state=tk.DISABLED)
                option_6_product_size.configure(state=tk.DISABLED)
                option_6_product_qty.configure(state=tk.DISABLED)

        def activate_option_7_product_extras(e=None):
            if e != '':
                option_7_product_print_type.configure(state=tk.NORMAL)
                option_7_product_size.configure(state=tk.NORMAL)
                option_7_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_7_product_print_type.configure(state=tk.DISABLED)
                option_7_product_size.configure(state=tk.DISABLED)
                option_7_product_qty.configure(state=tk.DISABLED)

        def activate_option_8_product_extras(e=None):
            if e != '':
                option_8_product_print_type.configure(state=tk.NORMAL)
                option_8_product_size.configure(state=tk.NORMAL)
                option_8_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_8_product_print_type.configure(state=tk.DISABLED)
                option_8_product_size.configure(state=tk.DISABLED)
                option_8_product_qty.configure(state=tk.DISABLED)

        def activate_option_9_product_extras(e=None):
            if e != '':
                option_9_product_print_type.configure(state=tk.NORMAL)
                option_9_product_size.configure(state=tk.NORMAL)
                option_9_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_9_product_print_type.configure(state=tk.DISABLED)
                option_9_product_size.configure(state=tk.DISABLED)
                option_9_product_qty.configure(state=tk.DISABLED)

        def activate_option_10_product_extras(e=None):
            if e != '':
                option_10_product_print_type.configure(state=tk.NORMAL)
                option_10_product_size.configure(state=tk.NORMAL)
                option_10_product_qty.configure(state=tk.NORMAL)
                proceed_button.configure(state=tk.NORMAL)
            else:
                option_10_product_print_type.configure(state=tk.DISABLED)
                option_10_product_size.configure(state=tk.DISABLED)
                option_10_product_qty.configure(state=tk.DISABLED)

        
        def proceed():
            if option_1_product.get() == '' and option_2_product.get() == '' and option_3_product.get() == '' and option_4_product.get() == '' and option_5_product.get() == '' and option_6_product.get() == '' and option_7_product.get() == '' and option_8_product.get() == '' and option_9_product.get() == '' and option_10_product.get() == '':
                messagebox.showerror('No Fields', 'Please select product\\s to proceed!')
            else:
                order_screen.configure(state=tk.NORMAL)
                order_screen.delete('1.0', tk.END)
                if option_1_product.get() == '':pass
                else:
                    order_screen.insert('0.0', f'{option_1_product.get()}\t\t{option_1_product_print_type.get()}\t\t{option_1_product_size.get()}\t{option_1_product_qty.get()}\n')
                if option_2_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_2_product.get()}\t\t{option_2_product_print_type.get()}\t\t{option_2_product_size.get()}\t{option_2_product_qty.get()}\n')
                if option_3_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_3_product.get()}\t\t{option_3_product_print_type.get()}\t\t{option_3_product_size.get()}\t{option_3_product_qty.get()}\n')
                if option_4_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_4_product.get()}\t\t{option_4_product_print_type.get()}\t\t{option_4_product_size.get()}\t{option_4_product_qty.get()}\n')
                if option_5_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_5_product.get()}\t\t{option_5_product_print_type.get()}\t\t{option_5_product_size.get()}\t{option_5_product_qty.get()}\n')
                if option_6_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_6_product.get()}\t\t{option_6_product_print_type.get()}\t\t{option_6_product_size.get()}\t{option_6_product_qty.get()}\n')
                if option_7_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_7_product.get()}\t\t{option_7_product_print_type.get()}\t\t{option_7_product_size.get()}\t{option_7_product_qty.get()}\n')
                if option_8_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_8_product.get()}\t\t{option_8_product_print_type.get()}\t\t{option_8_product_size.get()}\t{option_8_product_qty.get()}\n')
                if option_9_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_9_product.get()}\t\t{option_9_product_print_type.get()}\t\t{option_9_product_size.get()}\t{option_9_product_qty.get()}\n')
                if option_10_product.get() == '': pass
                else:
                    order_screen.insert('0.0', f'{option_10_product.get()}\t\t{option_10_product_print_type.get()}\t\t{option_10_product_size.get()}\t{option_10_product_qty.get()}\n')
                order_screen.configure(state=tk.DISABLED)


        def clear():
            option_1_product.configure(state=tk.DISABLED)
            option_1_product_print_type.configure(state=tk.DISABLED)
            option_1_product_size.configure(state=tk.DISABLED)
            option_1_product_qty.configure(state=tk.DISABLED)
            
            option_2_product.configure(state=tk.DISABLED)
            option_2_product_print_type.configure(state=tk.DISABLED)
            option_2_product_size.configure(state=tk.DISABLED)
            option_2_product_qty.configure(state=tk.DISABLED)

            option_3_product.configure(state=tk.DISABLED)
            option_3_product_print_type.configure(state=tk.DISABLED)
            option_3_product_size.configure(state=tk.DISABLED)
            option_3_product_qty.configure(state=tk.DISABLED)

            option_4_product.configure(state=tk.DISABLED)
            option_4_product_print_type.configure(state=tk.DISABLED)
            option_4_product_size.configure(state=tk.DISABLED)
            option_4_product_qty.configure(state=tk.DISABLED)

            option_5_product.configure(state=tk.DISABLED)
            option_5_product_print_type.configure(state=tk.DISABLED)
            option_5_product_size.configure(state=tk.DISABLED)
            option_5_product_qty.configure(state=tk.DISABLED)

            option_6_product.configure(state=tk.DISABLED)
            option_6_product_print_type.configure(state=tk.DISABLED)
            option_6_product_size.configure(state=tk.DISABLED)
            option_6_product_qty.configure(state=tk.DISABLED)

            option_7_product.configure(state=tk.DISABLED)
            option_7_product_print_type.configure(state=tk.DISABLED)
            option_7_product_size.configure(state=tk.DISABLED)
            option_7_product_qty.configure(state=tk.DISABLED)

            option_8_product.configure(state=tk.DISABLED)
            option_8_product_print_type.configure(state=tk.DISABLED)
            option_8_product_size.configure(state=tk.DISABLED)
            option_8_product_qty.configure(state=tk.DISABLED)

            option_9_product.configure(state=tk.DISABLED)
            option_9_product_print_type.configure(state=tk.DISABLED)
            option_9_product_size.configure(state=tk.DISABLED)
            option_9_product_qty.configure(state=tk.DISABLED)

            option_10_product.configure(state=tk.DISABLED)
            option_10_product_print_type.configure(state=tk.DISABLED)
            option_10_product_size.configure(state=tk.DISABLED)
            option_10_product_qty.configure(state=tk.DISABLED)

            proceed_button.configure(state=tk.DISABLED)

            order_number.configure(state=tk.NORMAL)
            order_number.delete(0, tk.END)
            order_number.insert(0, generate_order_number())
            order_number.configure(state=tk.DISABLED)
            customer.set('Select Customer')
            order_screen.configure(state=tk.NORMAL)
            order_screen.delete(1.0, tk.END)
            order_screen.configure(state=tk.DISABLED)
            option_1_product.set('')
            option_1_product_size.set('')
            option_1_product_print_type.set('')
            option_1_product_qty.set('1')

            option_2_product.set('')
            option_2_product_size.set('')
            option_2_product_print_type.set('')
            option_2_product_qty.set('1')

            option_3_product.set('')
            option_3_product_size.set('')
            option_3_product_print_type.set('')
            option_3_product_qty.set('1')

            option_4_product.set('')
            option_4_product_size.set('')
            option_4_product_print_type.set('')
            option_4_product_qty.set('1')

            option_5_product.set('')
            option_5_product_size.set('')
            option_5_product_print_type.set('')
            option_5_product_qty.set('1')

            option_6_product.set('')
            option_6_product_size.set('')
            option_6_product_print_type.set('')
            option_6_product_qty.set('1')

            option_7_product.set('')
            option_7_product_size.set('')
            option_7_product_print_type.set('')
            option_7_product_qty.set('1')

            option_8_product.set('')
            option_8_product_size.set('')
            option_8_product_print_type.set('')
            option_8_product_qty.set('1')

            option_9_product.set('')
            option_9_product_size.set('')
            option_9_product_print_type.set('')
            option_9_product_qty.set('1')

            option_10_product.set('')
            option_10_product_size.set('')
            option_10_product_print_type.set('')
            option_10_product_qty.set('1')

        def create_order():
            try:
                ask = messagebox.askyesno('Execution', 'Do you wish to proceed with the order creation?')
                if ask:
                    order_number.configure(state=tk.NORMAL)
                    order_db.new_oder(order_number.get(), customer=customer.get(), order=order_screen.get(0.1, tk.END))
                    order_number.configure(state=tk.DISABLED)
                    update_orders_list(order_db.get_all_orders())
                    clear()
            except:
                pass

        # Generate order number
        def generate_order_number():
            return f"{random.choice([i for i in string.ascii_uppercase])}-{random.randint(000000, 999999)}{random.choice([i for i in string.ascii_uppercase])}"

        # 
        order_number_label = customtkinter.CTkLabel(tab1, text='ORDER NUMBER:', corner_radius=40, bg_color='lime', text_color='purple', font=customtkinter.CTkFont("Century Gothic", 14, 'bold'))
        order_number_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        order_number = customtkinter.CTkEntry(tab1, font=customtkinter.CTkFont("Century Gothic", 14, 'bold'), text_color='gold',state=tk.DISABLED)
        order_number.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        order_number.configure(state=tk.NORMAL)
        order_number.insert(0, generate_order_number())
        order_number.configure(state=tk.DISABLED)

        customer = customtkinter.CTkOptionMenu(tab1, values=customers.get_customers_name_list(), font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_products_fields)
        customer.set('Select Customer')
        customer.grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)

        product_label = customtkinter.CTkLabel(tab1, text='Product', font=customtkinter.CTkFont("Century Gothic", 14, 'bold'))
        product_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        size_label = customtkinter.CTkLabel(tab1, text='Size', font=customtkinter.CTkFont("Century Gothic", 14, 'bold'))
        size_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        print_label = customtkinter.CTkLabel(tab1, text='Print Type', font=customtkinter.CTkFont("Century Gothic", 14, 'bold'))
        print_label.grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)

        quantity_label = customtkinter.CTkLabel(tab1, text='Quantity', font=customtkinter.CTkFont("Century Gothic", 14, 'bold'))
        quantity_label.grid(row=1, column=3, sticky=tk.W, padx=10, pady=5)

        products_list_options = ['','Tshirt', 'Shirt', 'Track Suit', 'Umbrella', 'Cap', 'Shopping Bag']
        option_1_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_1_product_extras)
        option_1_product.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        
        option_2_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_2_product_extras)
        option_2_product.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        
        option_3_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_3_product_extras)
        option_3_product.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        option_4_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_4_product_extras)
        option_4_product.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        
        option_5_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, bg_color='transparent', font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_5_product_extras)
        option_5_product.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)

        option_6_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_6_product_extras)
        option_6_product.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

        option_7_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_7_product_extras)
        option_7_product.grid(row=8, column=0, sticky=tk.W, padx=10, pady=5)
        
        option_8_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_8_product_extras)
        option_8_product.grid(row=9, column=0, sticky=tk.W, padx=10, pady=5)
        
        option_9_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_9_product_extras)
        option_9_product.grid(row=10, column=0, sticky=tk.W, padx=10, pady=5)

        option_10_product = customtkinter.CTkOptionMenu(tab1, values=products_list_options, state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=activate_option_10_product_extras)
        option_10_product.grid(row=11, column=0, sticky=tk.W, padx=10, pady=5)

        proceed_button = customtkinter.CTkButton(tab1, text='Proceed', state=tk.DISABLED, font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=proceed)
        proceed_button.grid(row=12, columnspan=2, sticky=tk.W, padx=10, pady=5)

        clear_button = customtkinter.CTkButton(tab1, text='Clear', font=customtkinter.CTkFont("Helvetica", 12, "bold", "italic"), command=clear)
        clear_button.grid(row=12, column=3, sticky=tk.W, padx=10, pady=5)

        # SIZES
        SIZES = ['', 'XXL','XL', 'L', 'M', 'S', 'XS']
        
        option_1_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_2_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_3_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_4_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_5_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_6_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_7_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_8_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_9_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
        option_10_product_size = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=SIZES)
       
        option_1_product_size.grid(row=2, column=1)
        option_2_product_size.grid(row=3, column=1)
        option_3_product_size.grid(row=4, column=1)
        option_4_product_size.grid(row=5, column=1)
        option_5_product_size.grid(row=6, column=1)
        option_6_product_size.grid(row=7, column=1)
        option_7_product_size.grid(row=8, column=1)
        option_8_product_size.grid(row=9, column=1)
        option_9_product_size.grid(row=10, column=1)
        option_10_product_size.grid(row=11, column=1)


        # PRINTING TYPES
        PRINTING_TYPES = ['', 'Front Full Print','Back Full Print', 'Pocket Logo', 'Right Sleeve', 'Left Sleeve', 'Crossover']
        option_1_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_2_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_3_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_4_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_5_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_6_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_7_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_8_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_9_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
        option_10_product_print_type = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=PRINTING_TYPES)
       
        option_1_product_print_type.grid(row=2, column=2, sticky=tk.W, padx=10, pady=5)
        option_2_product_print_type.grid(row=3, column=2, sticky=tk.W, padx=10, pady=5)
        option_3_product_print_type.grid(row=4, column=2, sticky=tk.W, padx=10, pady=5)
        option_4_product_print_type.grid(row=5, column=2, sticky=tk.W, padx=10, pady=5)
        option_5_product_print_type.grid(row=6, column=2, sticky=tk.W, padx=10, pady=5)
        option_6_product_print_type.grid(row=7, column=2, sticky=tk.W, padx=10, pady=5)
        option_7_product_print_type.grid(row=8, column=2, sticky=tk.W, padx=10, pady=5)
        option_8_product_print_type.grid(row=9, column=2, sticky=tk.W, padx=10, pady=5)
        option_9_product_print_type.grid(row=10, column=2, sticky=tk.W, padx=10, pady=5)
        option_10_product_print_type.grid(row=11, column=2, sticky=tk.W, padx=10, pady=5)
       
        #
        option_1_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_2_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_3_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_4_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_5_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_6_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_7_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_8_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_9_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
        option_10_product_qty = customtkinter.CTkOptionMenu(tab1, state=tk.DISABLED, values=[str(i) for i in range(1,101)])
       
        option_1_product_qty.grid(row=2, column=3)
        option_2_product_qty.grid(row=3, column=3)
        option_3_product_qty.grid(row=4, column=3)
        option_4_product_qty.grid(row=5, column=3)
        option_5_product_qty.grid(row=6, column=3)
        option_6_product_qty.grid(row=7, column=3)
        option_7_product_qty.grid(row=8, column=3)
        option_8_product_qty.grid(row=9, column=3)
        option_9_product_qty.grid(row=10, column=3)
        option_10_product_qty.grid(row=11, column=3)
     

        label_4 = customtkinter.CTkLabel(tab4, text="Deals", font=customtkinter.CTkFont("Helvetica", 18, "bold", "italic"))
        label_4.place(x=240, y=0)

        deal1 = customtkinter.CTkButton(tab4, text="deal1", font=customtkinter.CTkFont("Helvetica", 15, "bold", "italic"), bg_color="misty rose")
        deal2 = customtkinter.CTkButton(tab4, text="deal2", font=customtkinter.CTkFont("Helvetica", 15, "bold", "italic"), bg_color="misty rose")
        deal3 = customtkinter.CTkButton(tab4, text="deal3", font=customtkinter.CTkFont("Helvetica", 15, "bold", "italic"), bg_color="misty rose")
        deal4 = customtkinter.CTkButton(tab4, text="deal4", font=customtkinter.CTkFont("Helvetica", 15, "bold", "italic"), bg_color="misty rose")
        deal5 = customtkinter.CTkButton(tab4, text="deal5", font=customtkinter.CTkFont("Helvetica", 15, "bold", "italic"), bg_color="misty rose")

        deal1.place(x=240, y=60)
        deal2.place(x=240, y=150)
        deal3.place(x=240, y=240)
        deal4.place(x=240, y=330)
        deal5.place(x=240, y=420)

        def date_time():
            date = datetime.now().strftime("%d-%m-%Y")
            time = datetime.now().strftime("%H:%M")
            return f"Date:{date}\t\t\tTime:{time}\n"

        order_screen = customtkinter.CTkTextbox(screen_frame, border_width=5, font=customtkinter.CTkFont("Century Gothic", 14, "bold"), border_spacing=5, state=tk.DISABLED)
        order_screen.pack(fill=tk.BOTH, expand=True)

        orders_frame = customtkinter.CTkFrame(screen_frame)
        orders_frame.pack()

        execute_order = customtkinter.CTkButton(orders_frame, text='Execute Order', font=customtkinter.CTkFont("Century Gothic", 14, "bold", "italic"), command=create_order)
        execute_order.pack(side=tk.LEFT, padx=5)

        cancel_order = customtkinter.CTkButton(orders_frame, text='Cancel Order', font=customtkinter.CTkFont("Century Gothic", 14, "bold", "italic"))
        cancel_order.pack(side=tk.LEFT)
        