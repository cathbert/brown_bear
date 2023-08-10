from django.db import models
import random, string
from datetime import datetime
import uuid
from django.contrib.auth.models import User



class Customer(models.Model):
    f_name = models.CharField(max_length=255, blank=False)
    l_name = models.CharField(max_length=255, blank=False, unique=True)
    cell_number = models.IntegerField(blank=False, unique=True)
    email = models.EmailField(default="client@unavailable.com")
    address_line_1 = models.CharField(max_length=150, null=True)
    address_line_2 = models.CharField(max_length=150, null=True)
    address_line_3 = models.CharField(max_length=150, null=True)
    zip_code = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100, null=True)
    total_bonus_point = models.IntegerField(null=False, default=0)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField(null=True)
    is_administrator = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    login_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("f_name",)

    def __str__(self):
        return f"{self.f_name} {self.l_name} - {self.cell_number}"

class Job(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    order_number = models.CharField(max_length=50, blank=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    order = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class Diary(models.Model):
    STATUS_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    entry_title = models.CharField(max_length=255)
    entry_theme = models.CharField(max_length=255)
    entry_date = models.DateField(blank=False, )
    entry_time = models.TimeField(blank=False)
    entry_info = models.TextField(blank=True)
    entry_code = models.CharField(max_length=255, unique=True,
                                  default=f"{random.choice([i for i in string.ascii_uppercase])}-"
                                          f"{random.randint(000000, 999999)}"
                                          f"{random.choice([i for i in string.ascii_uppercase])}")
    number_of_attendees = models.IntegerField(default=0)
    entry_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='personal')

    class Meta:
        ordering = ("entry_date",)

    def __str__(self):
        return f"{self.entry_code} {self.entry_title}"


class Booking(models.Model):
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    booking_code = models.CharField(max_length=255, unique=True,
                                    default=f"{random.choice([i for i in string.ascii_uppercase])}-"
                                            f"{random.randint(000000, 999999)}"
                                            f"{random.choice([i for i in string.ascii_uppercase])}")

    class Meta:
        ordering = ("diary",)

    def __str__(self):
        return f"{self.booking_code}"

class SnippetCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Snippet(models.Model):
    category = models.ForeignKey(SnippetCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    code = models.TextField()
    date = models.CharField(max_length=255, blank=False)

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=255, blank=False)
    genre = models.CharField(max_length=255, blank=False)

class Dictionary(models.Model):
    word = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField()

class ToDo(models.Model):
    title = models.CharField(max_length=255, blank=False)
    note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class WikiSearch(models.Model):
    title = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class WorldHistoryDictionary(models.Model):
    title = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class KnowledgeSection(models.Model):
    title = models.CharField(max_length=255, blank=False, unique=True)
    class Meta: ordering = ('title',)


class KnowledgeThematic(models.Model):
    knowledge_section = models.ForeignKey(KnowledgeSection, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, unique=True)

    class Meta: ordering = ('title',)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Knowledge(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    knowledge_section = models.ForeignKey(KnowledgeSection, on_delete=models.CASCADE)
    knowledge_thematic = models.ForeignKey(KnowledgeThematic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, unique=True)
    info = models.TextField(blank=False)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='published')
    created = models.DateTimeField(auto_now_add=True)
    visited = models.DateTimeField(auto_now=True)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

class Cashier(models.Model):
    # REQUIRED_FIELDS = []
    # USERNAME_FIELD = 'user_name'
    user_name = models.CharField(max_length=100, unique=True, null=False) 
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    identity_number = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField()
    is_administrator =  models.BooleanField(default=False, null=False)
    is_active =  models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    login_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    # is_anonymous = models.BooleanField(default=False, null=False)
    # is_authenticated = models.BooleanField(default=False, null=False)
    # is_staff = models.BooleanField(default=False, null=False)
    # has_module_perms = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"<Cashier(name='{self.name}', last_name='{self.last_name}', user_name='{self.user_name}')>"


class Store(models.Model):
    pass   


class Closure(models.Model):
    closure_unique_id = models.UUIDField(uuid.uuid4())
    closure_number = models.IntegerField(null=False)
    pos_id = models.IntegerField(null=False)
    fk_store_id = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    closure_date = models.DateTimeField(auto_now=True, null=False)
    total_document_count = models.IntegerField(null=False)
    gross_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    gross_total_vat_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    daily_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    daily_total_vat_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    valid_receipt_count = models.IntegerField(null=False)
    valid_invoice_count = models.IntegerField(null=False)
    canceled_receipt_count = models.IntegerField(null=False)
    canceled_invoice_count = models.IntegerField(null=False)
    canceled_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    valid_receipt_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    valid_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    valid_receipt_vat_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    valid_invoice_vat_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    bonus_point_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    discount_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    waybill_count = models.IntegerField(null=False)
    canceled_waybill_count = models.IntegerField(null=False)
    waybill_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_waybill_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    return_count = models.IntegerField(null=False)
    canceled_return_count = models.IntegerField(null=False)
    return_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_return_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    diplomatic_invoice_count = models.IntegerField(null=False)
    canceled_diplomatic_invoice_count = models.IntegerField(null=False)
    diplomatic_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_diplomatic_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    electronic_receipt_count = models.IntegerField(null=False)
    canceled_electronic_receipt_count = models.IntegerField(null=False)
    electronic_receipt_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_electronic_receipt_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    electronic_invoice_count = models.IntegerField(null=False)
    canceled_electronic_invoice_count = models.IntegerField(null=False)
    electronic_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_electronic_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    electronic_corporate_invoice_count = models.IntegerField(null=False)
    canceled_electronic_corporate_invoice_count = models.IntegerField(null=False)
    electronic_corporate_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_electronic_corporate_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    electronic_individual_invoice_count = models.IntegerField(null=False)
    canceled_electronic_individual_invoice_count = models.IntegerField(null=False)
    electronic_individual_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_electronic_individual_invoice_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    expanse_count = models.IntegerField(null=False)
    canceled_expanse_count = models.IntegerField(null=False)
    expanse_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_expanse_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    paid_out_count = models.IntegerField(null=False)
    canceled_paid_out_count = models.IntegerField(null=False)
    paid_out_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_paid_out_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    paid_in_count = models.IntegerField(null=False)
    canceled_paid_in_count = models.IntegerField(null=False)
    paid_in_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    canceled_paid_in_total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    description = models.TextField()
    is_canceled = models.BooleanField(default=False, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField(null=True)
    is_modified = models.BooleanField(default=False, null=False)
    fk_cashier_modified_id = models.ForeignKey(Cashier, related_name="closure_cashier_modified" ,on_delete=models.DO_NOTHING)
    modified_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="closure_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="closure_cashier_updated" ,on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Closure(closure_unique_id='{self.closure_unique_id}', closure_date='{self.closure_date}')>"

class ClosureCurrency(models.Model):
    fk_closure_id = models.ForeignKey(Closure, on_delete=models.DO_NOTHING)
    currency_code = models.IntegerField(null=False)
    currency_total = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    currency_exchange_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField()
    is_modified = models.BooleanField(default=False, null=False)
    fk_cashier_modified_id = models.ForeignKey(Cashier, on_delete=models.DO_NOTHING)
    modified_description = models.TextField()
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="closure_currency_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="closure_currency_cashier_updated", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f"<ClosureCurrency(currency_code='{self.currency_code}', currency_total='{self.currency_total}')>"

class Vat(models.Model):
    name = models.CharField(max_length=50, null=False)
    no = models.IntegerField(null=False)
    rate = models.IntegerField(null=False)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="vat_currency_cashier_created_id" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="vat_currency_cashier_updated_id", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Vat(name='{self.name}', no='{self.no}', rate='{self.rate}')>"


class DepartmentMainGroup(models.Model):
    name = models.CharField(max_length=50, null=False)
    no = models.IntegerField(null=False)
    fk_vat_id = models.ForeignKey(Vat, related_name="department_main_group_vat" ,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    max_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="department_main_group_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="department_main_group_cashier_updated", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<DepartmentMainGroup(name='{self.name}', no='{self.no}', description='{self.description}')>"


class DepartmentSubGroup(models.Model):
    name = models.CharField(max_length=50, null=False)
    no = models.IntegerField(null=False)
    fk_department_main_group_id = models.ForeignKey(DepartmentMainGroup, related_name="department_sub_group_vat" ,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    max_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="department_sub_group_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="department_sub_group_cashier_updated", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<DepartmentSubGroup(name='{self.name}', no='{self.no}', description='{self.description}')>"


class ClosureTotal(models.Model):
    fk_closure_id = models.ForeignKey(Closure, on_delete=models.DO_NOTHING)
    fk_department_main_group_id = models.ForeignKey(DepartmentMainGroup, on_delete=models.DO_NOTHING)
    department_count = models.IntegerField(null=False)
    total_department = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_department_vat = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField(null=True)
    is_modified = models.BooleanField(default=False, null=False)
    fk_cashier_modified_id = models.ForeignKey(Cashier, related_name="closure_total_cashier_modified" ,on_delete=models.DO_NOTHING)
    modified_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="closure_total_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="closure_total_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<ClosureTotal(total_department='{self.total_department}', total_department_vat='{self.total_department_vat}')>"

class ProductUnitId(models.Model):
    name = models.CharField(max_length=50, null=False)
    no = models.IntegerField(null=False)
    description = models.TextField(null=False)
    base_id = models.IntegerField(null=False)
    base_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    symbol = models.CharField(max_length=10, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="product_unit_id_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="product_unit_id_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<ProductUnit(name='{self.name}', no='{self.no}', description='{self.description}')>"


class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    short_name = models.CharField(max_length=50, null=True)
    code = models.IntegerField(null=False)
    old_code = models.IntegerField(null=True)
    keyboard_value = models.CharField(max_length=10, null=True)
    description = models.TextField(null=True)
    description_on_screen = models.CharField(max_length=150, null=True)
    description_on_shelf = models.CharField(max_length=150, null=True)
    description_on_scale = models.CharField(max_length=150, null=True)
    is_scalable = models.BooleanField(null=False)
    is_allowed_free_discount = models.BooleanField(null=False)
    is_allowed_negative_stock = models.BooleanField(null=False)
    is_allowed_return = models.BooleanField(null=False)
    purchase_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(null=False)
    alert_min_stock_number = models.IntegerField(null=False)
    alert_max_stock_number = models.IntegerField(null=False)
    fk_vat_id = models.ForeignKey(Vat, related_name='product_vat', on_delete=models.DO_NOTHING)
    fk_product_unit_id = models.ForeignKey(ProductUnitId(), related_name='product_unit_id', on_delete=models.DO_NOTHING)
    fk_department_main_group_id = models.ForeignKey(DepartmentMainGroup, related_name='product_department_main_group', on_delete=models.DO_NOTHING)
    fk_department_sub_group_id = models.ForeignKey(DepartmentSubGroup, related_name='product_department_subgroup', on_delete=models.DO_NOTHING)
    fk_store_id = models.ForeignKey(Store, related_name='product_store', on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(null=False, default=False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="product_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="product_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Product(name='{self.name}', code='{self.code}', price='{self.price}')>"


class ProductBarcodeMask(models.Model):
    fk_product_id = models.ForeignKey(Product, related_name="product_barcode_mask_product" ,on_delete=models.DO_NOTHING)
    code_started_at = models.IntegerField(null=False)
    code_length = models.IntegerField(null=False)
    quantity_started_at = models.IntegerField(null=False)
    quantity_length = models.IntegerField(null=False)
    weight_started_at = models.IntegerField(null=False)
    weight_length = models.IntegerField(null=False)
    price_started_at = models.IntegerField(null=False)
    price_length = models.IntegerField(null=False)
    color_started_at = models.IntegerField(null=False)
    color_length = models.IntegerField(null=False)
    size_started_at = models.IntegerField(null=False)
    size_length = models.IntegerField(null=False)
    description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="product_barcode_mask_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="product_barcode_mask_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<ProductBarcode(name='{self.name}', barcode='{self.barcode}'>"


class ProductBarcode(models.Model):
    fk_product_id = models.ForeignKey(Product, related_name="product_barcode_product" ,on_delete=models.DO_NOTHING)
    barcode = models.CharField(max_length=50, null=False)
    is_allowed_negative_stock = models.BooleanField(null=False)
    is_allowed_return = models.BooleanField(null=False)
    purchase_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(null=False)
    description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="product_barcode_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="product_barcode_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductUnit(models.Model):
    name = models.CharField(max_length=50, null=False)
    no = models.IntegerField(null=False)
    description = models.TextField(null=True)
    base_id = models.IntegerField(null=False)
    base_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    symbol = models.CharField(max_length=10, null=False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="product_unit_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="product_unit_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<ProductUnit(name='{self.name}', no='{self.no}', description='{self.description}')>"


class TransactionHeadTemp(models.Model):
    transaction_unique_id = models.URLField(uuid.uuid4())
    pos_id = models.IntegerField(null=False)
    transaction_date_time = models.DateTimeField(auto_now_add=True, null=False)
    document_type = models.CharField(max_length=50, null=False)
    fk_customer_id = models.ForeignKey(Customer, related_name="transaction_head_temp_customer_id", on_delete=models.DO_NOTHING)
    receipt_number = models.IntegerField(null=False)
    batch_number = models.IntegerField(null=False)
    total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_vat_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_discount_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_surcharge_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_payment_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_change_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    description = models.TextField()
    is_closed = models.BooleanField(null=False, default= False)
    is_pending = models.BooleanField(null=False, default= False)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_head_temp_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_head_temp_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionHeadTemp(transaction_unique_id='{self.transaction_unique_id}', transaction_date_time='{self.transaction_date_time}')>"

class TransactionProductTemp(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHeadTemp, related_name="transaction_head_temp_ident" ,on_delete=models.DO_NOTHING)
    line_no = models.IntegerField(null=False)
    fk_department_main_group_id = models.ForeignKey(DepartmentMainGroup, related_name="department_main_grp" ,on_delete=models.DO_NOTHING, null=False)
    fk_department_sub_group_id = models.ForeignKey(DepartmentSubGroup, related_name="department_subgrp_id" ,on_delete=models.DO_NOTHING, null=True)
    fk_product_id = models.ForeignKey(Product, related_name="transaction_product_id" ,on_delete=models.DO_NOTHING, null=True)
    fk_product_barcode_id = models.ForeignKey(ProductBarcode, related_name="broduct_barcode_1" ,on_delete=models.DO_NOTHING, null=True)
    fk_product_barcode_mask_id = models.ForeignKey(ProductBarcodeMask, related_name="product_barcode_mask_1" ,on_delete=models.DO_NOTHING, null=True)
    vat_rate = models.IntegerField(null=False)
    unit_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    unit_discount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_vat = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_product_temp_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_product_temp_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionProductTemp(total_price='{self.total_price}')>"


class TransactionPaymentTemp(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHeadTemp, related_name="transaction_head_temp1_id", on_delete=models.DO_NOTHING)
    line_no = models.IntegerField(null=False)
    payment_type = models.CharField(max_length=50, null=False)
    payment_total = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    currency_code = models.IntegerField(null=False)
    currency_total = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    currency_exchange_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    installment_count = models.IntegerField(null=False)
    payment_tool_id = models.CharField(max_length=50, null=True)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_head_temp1_cashier_created_id" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_head_temp1_cashier_updated_id" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"<TransactionPaymentTemp(payment_type='{self.payment_type}', payment_total='{self.payment_total}')>"

class TransactionTotalTemp(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHeadTemp, related_name="total_transaction_head_temp1_id", on_delete=models.DO_NOTHING)
    line_no = line_no = models.IntegerField(null=False)
    fk_department_main_group_id = models.ForeignKey(DepartmentMainGroup, related_name="total_department_main_grp" ,on_delete=models.DO_NOTHING, null=False)
    total_department = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_department_vat = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_total_temp_cashier_created_id" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_total_temp_cashier_updated_id" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionTotalTemp(total_department='{self.total_department}', total_department_vat='{self.total_department_vat}')>"


class TransactionDiscount(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHeadTemp, related_name="transaction_dicount_head", on_delete=models.DO_NOTHING)
    fk_transaction_product_id = models.ForeignKey(TransactionProductTemp, related_name="transaction_dicount_product", on_delete=models.DO_NOTHING, null=True)
    fk_transaction_payment_id = models.ForeignKey(TransactionPaymentTemp, related_name="transaction_dicount_payment", on_delete=models.DO_NOTHING, null=True)
    fk_transaction_total_id = models.ForeignKey(TransactionTotalTemp, related_name="transaction_dicount_total", on_delete=models.DO_NOTHING, null=True)
    line_no = models.IntegerField(null=False)
    discount_type = models.CharField(max_length=50, null=False)
    discount_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    discount_code = models.CharField(max_length=15, null=True)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_dicount_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_dicount_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionDiscount(discount_type='{self.discount_type}', discount_amount='{self.discount_amount}')>"


class TransactionHead(models.Model):
    transaction_unique_id = models.URLField(uuid.uuid4())
    pos_id = models.IntegerField(null=False)
    transaction_date_time = models.DateTimeField(auto_now_add=True)
    document_type = models.CharField(max_length=50, null=False)
    fk_customer_id = models.ForeignKey(Customer, related_name="transaction_head_customer_id", on_delete=models.DO_NOTHING)
    closure_number = models.IntegerField(null=False)
    receipt_number = models.IntegerField(null=False)
    total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_vat_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_discount_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_surcharge_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_payment_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_change_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    description = models.TextField()
    is_closed = models.BooleanField(null=False, default= False)
    is_pending = models.BooleanField(null=False, default= False)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_head_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_head_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionHead(transaction_unique_id='{self.transaction_unique_id}', transaction_date_time='{self.transaction_date_time}')>"


class TransactionPayment(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHead, related_name="transaction_head1_id", on_delete=models.DO_NOTHING)
    line_no = models.IntegerField(null=False)
    payment_type = models.CharField(max_length=50, null=False)
    payment_total = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    currency_code = models.IntegerField(null=False)
    currency_total = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    currency_exchange_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    installment_count = models.IntegerField(null=False)
    payment_tool_id = models.CharField(max_length=50, null=True)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_head1_cashier_created_id" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_head1_cashier_updated_id" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionPayment(payment_type='{self.payment_type}', payment_total='{self.payment_total}')>"


class TransactionProduct(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHead, related_name="transaction_head_ident" ,on_delete=models.DO_NOTHING)
    line_no = models.IntegerField(null=False)
    fk_department_main_group_id = models.ForeignKey(DepartmentMainGroup, related_name="product_department_main_grp" ,on_delete=models.DO_NOTHING, null=False)
    fk_department_sub_group_id = models.ForeignKey(DepartmentSubGroup, related_name="product_department_subgrp_id" ,on_delete=models.DO_NOTHING, null=True)
    fk_product_id = models.ForeignKey(Product, related_name="product_transaction_product_id" ,on_delete=models.DO_NOTHING, null=True)
    fk_product_barcode_id = models.ForeignKey(ProductBarcode, related_name="product_broduct_barcode_1" ,on_delete=models.DO_NOTHING, null=True)
    fk_product_barcode_mask_id = models.ForeignKey(ProductBarcodeMask, related_name="product_product_barcode_mask_1" ,on_delete=models.DO_NOTHING, null=True)
    vat_rate = models.IntegerField(null=False)
    unit_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    unit_discount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_vat = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="product_1_product_temp_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="product_1_product_temp_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionProduct(total_price='{self.total_price}')>"


class TransactionTotal(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHeadTemp, related_name="total_1_transaction_head_temp1_id", on_delete=models.DO_NOTHING)
    line_no = line_no = models.IntegerField(null=False)
    fk_department_main_group_id = models.ForeignKey(DepartmentMainGroup, related_name="total_1_department_main_grp" ,on_delete=models.DO_NOTHING, null=False)
    total_department = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_department_vat = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_total_1_temp_cashier_created_id" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_total_1_temp_cashier_updated_id" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionTotal(total_department='{self.total_department}', total_department_vat='{self.total_department_vat}')>"

class TransactionDiscountTemp(models.Model):
    fk_transaction_head_id = models.ForeignKey(TransactionHeadTemp, related_name="transaction_dicount_temp_head", on_delete=models.DO_NOTHING)
    fk_transaction_product_id = models.ForeignKey(TransactionProductTemp, related_name="transaction_dicount_temp_product", on_delete=models.DO_NOTHING, null=True)
    fk_transaction_payment_id = models.ForeignKey(TransactionPaymentTemp, related_name="transaction_dicount_temp_payment", on_delete=models.DO_NOTHING, null=True)
    fk_transaction_total_id = models.ForeignKey(TransactionTotalTemp, related_name="transaction_dicount_temp_total", on_delete=models.DO_NOTHING, null=True)
    line_no = models.IntegerField(null=False)
    discount_type = models.CharField(max_length=50, null=False)
    discount_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    discount_code = models.CharField(max_length=15, null=True)
    is_cancel = models.BooleanField(null=False, default= False)
    is_deleted = models.BooleanField(null=False, default= False)
    delete_description = models.TextField(null=True)
    fk_cashier_create_id = models.ForeignKey(Cashier, related_name="transaction_dicount_temp_cashier_created" ,on_delete=models.DO_NOTHING)
    fk_cashier_update_id = models.ForeignKey(Cashier, related_name="transaction_dicount_temp_cashier_updated" ,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<TransactionDiscountTemp(discount_type='{self.discount_type}', discount_amount='{self.discount_amount}')>"
