# IMPORT ALL REQUIRED MODULES AND LIBRARIES
import datetime
import django
from cryptography.fernet import Fernet
import pickle
import os
import subprocess as sp
from utils import mypath
from tkinter import messagebox
from datetime import datetime
import wikipedia
import warnings
from functools import lru_cache

warnings.catch_warnings()
warnings.simplefilter("ignore")

# SET DJANGO ENVIRONMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BrownBear.settings')
django.setup()

# DJANGO IMPORTS
from accounts.models import Customer, Booking, Diary,Snippet, Dictionary, WikiSearch, \
                            Job, SnippetCategory, Knowledge,KnowledgeSection,KnowledgeThematic, WorldHistoryDictionary
import accounts
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
#from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.utils.timezone import datetime

# 
if not os.path.exists(os.path.join(mypath.this_file_path(), "user_password_encryption_key.pickle")):
    key = Fernet.generate_key()  # ----- This is your "password" to unlock and lock files
    # ----- Create a pickle file and dump key into it
    with open(os.path.join(mypath.this_file_path(), 'user_password_encryption_key.pickle'), 'wb') as f:
        pickle.dump(key, f)
    sp.call(["attrib", "+H", f"{os.path.join(mypath.this_file_path(), 'user_password_encryption_key.pickle')}"])


class CustomerDatabase:
    def new_customer(self, fname=None, lname=None, cell_number=None, email=None, home_address1=None, home_address2=None, home_address3=None):
        try:
            if len(fname) > 0 and len(lname) > 0 and len(cell_number) > 0 and len(email) > 0 and len(home_address1) > 0:
                customer = Customer(f_name=fname, l_name=lname, cell_number=cell_number, email=email,
                                address_line_1=home_address1, address_line_2=home_address2, address_line_3=home_address3)
                customer.save()
                messagebox.showinfo("Success", "Customer successfully added to database!")
            elif len(fname) == 0: messagebox.showerror("Missing", "Please do provide First name and Last name!")
            elif len(lname) == 0: messagebox.showerror("Missing", "Please do provide First name and Last name!")
            else:
                customer = Customer(f_name=fname, l_name=lname, cell_number=cell_number,address_line_1=home_address1,address_line_2=home_address2,address_line_3=home_address3)
                customer.save()
                messagebox.showinfo("Success", "customer successfully added to database without email and home address!")
                return True

        except django.db.utils.IntegrityError as e: return django.db.utils.IntegrityError # messagebox.showerror("Oops!", 'customer already saved in the system, please search!')
        except ValueError: return False # messagebox.showerror("Error", "Please remember cellphone number is required and you did not provide.")
        except IndexError as e: return IndexError # print(e)

    def get_customer_object(self, name): return Customer.objects.get(f_name=name)

    def delete_customer(self, name):
        try:
            Customer.objects.get(f_name=name).delete()
            return True
        except Exception: return False

    def get_customer_info_by_id(self, customer_id):
        try:
            customer = Customer.objects.get(pk=customer_id)
            info = {
                "firstname": customer.f_name,
                "lastname": customer.l_name,
                "cell_number": customer.cell_number,
                "email": customer.email,
                "address_line_1": customer.address_line_1,
                "address_line_2": customer.address_line_2,
                "address_line_3": customer.address_line_3
            }
            return info
        except:
            return f"record with id {id} does not exist"

    def get_customer_info_by_name(self, name):
        try:
            customer = Customer.objects.get(f_name=name)
            info = {
                "firstname": customer.f_name,
                "lastname": customer.l_name,
                "cell_number": customer.cell_number,
                "email": customer.email,
                "address_line_1": customer.address_line_1,
                "address_line_2": customer.address_line_2,
                "address_line_3": customer.address_line_3
            }
            return info
        except: return f"record with name {name} does not exist"

    def get_all_customers(self):
        customers = Customer.objects.all().order_by('-id')
        data = []
        for i in customers:
            data.append((i.id, i.f_name, i.l_name, i.cell_number, i.email, i.address_line_1, i.address_line_2,i.address_line_3))
        return data

    def edit_customer(self, id, fname=None, lname=None, cell_number=None, email=None, home_address1=None,home_address2=None,home_address3=None):
        try:
            customer = Customer.objects.get(pk=id)
            if fname is not None: customer.f_name = fname
            if lname is not None: customer.l_name = lname
            if cell_number is not None: customer.cell_number = cell_number
            if email is not None: customer.email = email
            if home_address1 is not None: 
                customer.address_line_1 = home_address1
                customer.address_line_2 = home_address2
                customer.address_line_3 = home_address3
            msg = messagebox.askyesno('Check', 'Are you sure you want to save these changes?')
            if msg:
                customer.save()
                return True

        except Exception as e:
            return False

    def get_customer_id_from_name(self, name):
        customer = Customer.objects.get(f_name=name)
        return customer.id

    def get_customers_name_list(self):
        data = Customer.objects.all()
        return [i.f_name for i in data]


class BookingsDatabase:
    def new_booking(self, customer_f_name=None, customer_l_name=None, customer_cell_number=None, customer_email=None,
                    customer_home_address=None, event_title=None, event_date=None, event_theme=None,
                    event_info=None):
        try:
            if customer_f_name is not None and customer_l_name is not None and customer_cell_number is not None:
                book = Booking(customer_f_name=customer_f_name, customer_l_name=customer_l_name,
                               customer_cell_number=customer_cell_number,
                               customer_email=customer_email, customer_home_address=customer_home_address,
                               event_title=event_title,
                               event_date=event_date, event_theme=event_theme, event_info=event_info)
                book.save()
                return "booked successfully"
        except Exception as e:
            return "booking failed " + str(e)


class DiaryDatabase:
    def get_entry_by_date(self, date):
        entries = Diary.objects.all().filter(entry_date=date)
        data = []
        for i in entries:
            data.append((i.entry_title, i.entry_theme, i.entry_date, i.entry_time, i.entry_info, i.entry_code))
        return data

    def delete_this_day_entries(self, date):
        this_day_entries = Diary.objects.all().filter(entry_date=date)
        for entry in this_day_entries:
            entry.delete()

    def delete_single_entry(self, title):
        try:
            this_entry = Diary.objects.get(entry_title=title)
            this_entry.delete()
        except Exception as e:
            print(e)

    def create_an_entry(self, entrytitle=None, entrytheme=None, entrydate=None, entrytime=None, entryinfo=None):
        try:
            entry = Diary(entry_title=entrytitle, entry_theme=entrytheme, entry_date=entrydate, entry_time=entrytime,
                          entry_info=entryinfo)
            entry.save()
        except Exception as e:
            print(e)

    def get_all_entries(self):
        entries = Diary.objects.all().order_by('id')
        data = []
        for i in entries:
            data.append((i.entry_title, i.entry_theme, i.entry_date, i.entry_time, i.entry_info, i.entry_code))
        return data

    def check_if_entries_are_available(self, date):
        this_day_entries = Diary.objects.all().filter(entry_date=date)
        if this_day_entries.count() > 0: return True
        else: return False

    def get_selected_entry(self, title): return Diary.objects.get(entry_title=title)

    def get_selected_entry_id(self, title): return Diary.objects.get(entry_title=title).id

    def edit_entry(self, id): return Diary.objects.get(id=id)


class SnippetsDatabase:
    def new_snippet(self, title, code, category):
        try:
            if len(title) > 0 and len(code) > 0:
                snippet = Snippet(title=title.lower(), code=code, category=SnippetCategoryDatabase().get_category_object(category), date=datetime.now())
                snippet.save()
                return 'saved'
        
        except django.db.utils.IntegrityError as e: return 'exist'
        except ValueError as e: return 'value error'
        except Exception as e: return e

    def get_snippet_object(self, title): return Snippet.objects.get(title=title)

    def delete_snippet(self, title):
        try:
            Snippet.objects.get(title=title).delete()
            return True
        except Exception: return False

    def get_snippet_info_by_id(self, snippet_id):
        try:
            snippet = Snippet.objects.get(pk=snippet_id)
            info = {
                "title": snippet.title,
                "code": snippet.code,
                "dte": snippet.date 
            }
            return info
        except: return f"record with id {id} does not exist"

    def get_snippet_info_by_name(self, name):
        try:
            snippet = Snippet.objects.get(title=name)
            info = {
                "title": snippet.title,
                "code": snippet.code,
                "dte": snippet.date
            }
            return info
        except: return f"record with name {name} does not exist"

    def get_all_snippets(self):
        snippets = Snippet.objects.all().order_by('-id')
        data = []
        for i in snippets:
            data.append(i.title)
        return data

    def edit_snippet(self, id, title, code):
        try:
            snippet = Snippet.objects.get(pk=id)
            if title != '':
                snippet.title = title
            if code != '':
                snippet.code = code
            
            snippet.date = datetime.now()
    
            snippet.save()
            return True

        except Exception as e: return False

    def get_snippet_id_from_name(self, name): return Snippet.objects.get(title=name).id

    def list_snippets_by_category(self, category): 
        data = []
        for i in Snippet.objects.all().filter(category=category).order_by('-date'):
            if i.title.endswith("readme") or i.title.endswith("requirements"):
                continue
            else:
                data.append(i.title.lower())
        return data

    def list_snippets_ids_by_category(self, category): return [str(i.id) for i in Snippet.objects.all().filter(category=category)]

    def search_snippet(self, title):
        try:
            code = Snippet.objects.get(title=title)
            return [code.id,code.title, code.code, code.category] 
        except Exception as e: return []

    def update_snippet_category(self, snippet_id, category_object):
        snippet = Snippet.objects.get(pk=snippet_id)
        try:
            snippet.category = category_object
            snippet.save()
            return True
        except Exception as e: return False

    def count_all_snippets_by_category(self, category): return Snippet.objects.all().filter(category=category).count()

    def get_readme_file(self, title):
        try:
            readme = Snippet.objects.get(title=title+" readme")
            return readme
        except accounts.models.Snippet.DoesNotExist:
            return None

    def get_requirements_file(self, title):
        try:
            readme = Snippet.objects.get(title=title+" requirements")
            return readme
        except accounts.models.Snippet.DoesNotExist:
            return None


class DictionaryDatabase:
    @lru_cache(None)
    def search_all_matching(self, word):
        try: return [i.word for i in Dictionary.objects.all().filter(word__istartswith=word)]
        except accounts.models.Dictionary.DoesNotExist: return []

    def search_word(self, word):
        try: return Dictionary.objects.get(word=word).description
        except accounts.models.Dictionary.DoesNotExist: return ''

    @lru_cache(None)
    def get_all_words(self): return [i.word for i in Dictionary.objects.all()]


class WikipediaDatabase:
    
    def search_all_matching_wikis(self, wiki):
        try:
            wikis = WikiSearch.objects.all().filter(title__istartswith=wiki)
            return [i.title for i in wikis]
        except accounts.models.WikiSearch.DoesNotExist :
            return []

    def search_wiki(self, wiki):
        try:
            data =  WikiSearch.objects.get(title=wiki)
            return data
        except accounts.models.WikiSearch.DoesNotExist:
            try:
                data = wikipedia.page(wiki)
                return self.add_wiki(data.title, data.content)
            except wikipedia.exceptions.DisambiguationError as e:
                return e.options

    def get_all_wikis(self): return [i.title for i in WikiSearch.objects.all()]

    def add_wiki(self, title, description):
        try:
            wiki = WikiSearch.objects.create(title=title, description=description)
            wiki.save()
            return wiki
        except django.db.utils.IntegrityError:
            return self.search_wiki(title)

class WorldHistoryDictionaryDatabase:
    
    def search_all_matching_words(self, word):
        try:
            data = WorldHistoryDictionary.objects.all().filter(title__istartswith=word)
            return [i.title for i in data]
        except accounts.models.WorldHistoryDictionary.DoesNotExist :
            return []

    def search_word(self, title):
        try:
            data =  WorldHistoryDictionary.objects.get(title=title)
            return data
        except accounts.models.WorldHistoryDictionary.DoesNotExist:
            return None

    def get_all_words(self): return [i.title for i in WorldHistoryDictionary.objects.all().order_by('-id')]

    def add_word(self, title, description):
        try:
            data = WorldHistoryDictionary.objects.create(title=title.strip().lower(), description=description)
            data.save()
            return True
        except django.db.utils.IntegrityError:
            return False

    def get_id(self, title):
        _id = WorldHistoryDictionary.objects.get(title=title).id
        return _id

    def delete(self, _id):
        try:
            item = WorldHistoryDictionary.objects.get(id=_id)
            item.delete()
            return True
        except Exception as e:
            return False

    def edit(self, _id, title, description):
        try:
            item = WorldHistoryDictionary.objects.get(id=_id)
            item.title = title.strip().lower()
            item.description = description
            item.save()
            return True
        except accounts.models.WorldHistoryDictionary.DoesNotExist as e:
            return False



#app = WikipediaDatabase()
#print(app.search_wiki('cronicles'))

class UserDatabase:
    def authenticate_user(name, password):
        print(User.objects.all()) 
        user = authenticate(username='nezi', password='eagle501')
        if user:
            # User is authenticated)
            return True
        #print(dir(User.username_validator))
        #is_authenticated
        #is_anonymous
        # from events.models import Event


class JobDatabase:
    def new_oder(self, order_number=None, customer=None, order=None):
        try:
            data = Job.objects.create(order_number=order_number, customer=CustomerDatabase().get_customer_object(customer), order=order)
            data.save()
        except Exception as e:
            print(e)

    def get_all_orders(self): return [i.order_number for i in Job.objects.all()]

    def get_selected_order(self, order_number):
        try:
            return Job.objects.get(order_number=order_number).order
        except accounts.models.Job.DoesNotExist:
            messagebox.showerror('Selection', 'Please select order to open!')

    def get_pending_orders(self): return [i.order_number for i in Job.objects.all().filter(status='pending')]

    def get_completed_orders(self): return [i.order_number for i in Job.objects.all().filter(status='completed')]

class SnippetCategoryDatabase:
    def get_category_object(self, title):
        category_obj = SnippetCategory.objects.get(title=title)
        return category_obj

    def get_all_categories(self):
        data = SnippetCategory.objects.all()
        return [i.title for i in data]

    def new_category(self, name):
        cat = SnippetCategory.objects.create(title=name)
        cat.save()


class KnowledgeDatabase: 
    def search(self, text):
        search_by_title = Knowledge.objects.filter(title__icontains=text)
        search_by_info = Knowledge.objects.filter(info__icontains=text)
        data = [*[i for i in search_by_title],*[i for i in search_by_info]]
        return set(data)   

    def get_five_recently_added(self):
        visited = Knowledge.objects.all().order_by('-visited')[:10]
        return (i for i in visited)

    def add_new_knowledge(self, knowledge_sec, knowledge_th, knowledge_title, knowledge_info):
        try:
            knw = Knowledge.objects.create(knowledge_section=knowledge_sec, knowledge_thematic=knowledge_th, title=knowledge_title.lower().strip(), info=knowledge_info)
            knw.save()
            return True
            
        except Exception as e:
            return False

    def get_all_sections(self): return [i.title for i in KnowledgeSection.objects.all()]

    def get_all_thematics_by_section(self, section): return [i.title for i in KnowledgeThematic.objects.all().filter(knowledge_section=section)]

    def get_section_object_by_title(self, title): return KnowledgeSection.objects.get(title=title)

    def get_thematic_object_by_title(self, title): return KnowledgeThematic.objects.get(title=title)

    def get_single_selected_knowledge(self, title): 
        know = Knowledge.objects.get(title=title)
        self.update_visited_date_and_time(Knowledge.objects.get(title=title))
        return know

    def update_visited_date_and_time(self, know_obj):
        know_obj.visited= datetime.now()
        know_obj.save()

    def update_knowledge(self, id, knowledge_sec, knowledge_th, knowledge_title, knowledge_info):
        
        try:
            know = Knowledge.objects.get(id=id)
            know.knowledge_section = knowledge_sec
            know.knowledge_thematic = knowledge_th
            know.title = knowledge_title
            know.info = knowledge_info
            know.save()
            print("Update")
        except Exception as e:
            print(str(e))

   
#s = WorldHistoryDictionaryDatabase()
#s.new_category('blender')
'''
s = SnippetCategoryDatabase()
#print(s.get_category_object('python'))
t = SnippetsDatabase()
for i in t.get_all_snippets():
    e = t.update_snippet_category(t.get_snippet_id_from_name(i), s.get_category_object('python'))
    print(f'{i} is {e} ID: {t.get_snippet_id_from_name(i)}')
'''

#print(s.delete_snippet('Testing'))

# book = BookingsDatabase()
# print(book.new_booking(customer_f_name="Cathbert", customer_l_name="Mutaurwa", entry_title="Boat Cruise",
# customer_cell_number=937746675, customer_email="", entry_theme="TAste and taste",customer_home_address="", entry_info="Rnjoy"))

# service = ServicesDatabase()
# service.add_new_service("Speaker hire")
# print(service.get_service_id_from_name("Boat Cruise"))
# print(service.get_all_services())

# customer = CustomerDatabase()
# print(customer.get_all_customers())
# print(customer.get_customer_info_by_name("Cathbert"))
# print(customer.get_customer_info_by_id(3))
# customer.edit_customer(customer.get_customer_id_from_name("Neziswa"), "Neziswa", "Mutaurwa", 716063217, 'luthulilove@gmail.com', "321 Dutoit Street, Pitori")
# print(customer.get_customer_info_by_id(3))
# print(customer.delete_customer("Cathbert"))
# print(customer.get_customer_object('Neiswa'))
# customer.new_customer("Neiswa", "Luthuli",8477577744, "luthuline@gmail.com", "321 Dutoit Street")
