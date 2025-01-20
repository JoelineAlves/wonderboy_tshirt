# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'
        unique_together = (('user', 'primary'), ('user', 'email'),)


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CheckoutOrder(models.Model):
    order_number = models.CharField(max_length=32)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=2)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    town_or_city = models.CharField(max_length=40)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, blank=True, null=True)
    county = models.CharField(max_length=80, blank=True, null=True)
    date = models.DateTimeField()
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    order_total = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    grand_total = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    original_bag = models.TextField()
    stripe_pid = models.CharField(max_length=254)
    user_profile = models.ForeignKey('ProfilesUserprofile', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checkout_order'


class CheckoutOrderlineitem(models.Model):
    product_size = models.CharField(max_length=2, blank=True, null=True)
    quantity = models.IntegerField()
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    order = models.ForeignKey(CheckoutOrder, models.DO_NOTHING)
    product = models.ForeignKey('ProductsProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'checkout_orderlineitem'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'django_site'


class FavoriteFavorite(models.Model):
    product = models.ForeignKey('ProductsProduct', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'favorite_favorite'
        unique_together = (('user', 'product'),)


class NewsletterNewsletters(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateTimeField()
    image_url = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField()
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'newsletter_newsletters'


class NewsletterSubscribetonewsletter(models.Model):
    email = models.CharField(max_length=254, blank=True, null=True)
    date_added = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'newsletter_subscribetonewsletter'


class ProductsCategory(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_category'


class ProductsProduct(models.Model):
    sku = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    rating = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    image_url = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(ProductsCategory, models.DO_NOTHING, blank=True, null=True)
    has_sizes = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_product'


class ProductsProductreview(models.Model):
    title = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveIntegerField()
    date = models.DateTimeField()
    product = models.ForeignKey(ProductsProduct, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_productreview'


class ProfilesUserprofile(models.Model):
    default_phone_number = models.CharField(max_length=20, blank=True, null=True)
    default_country = models.CharField(max_length=2, blank=True, null=True)
    default_postcode = models.CharField(max_length=20, blank=True, null=True)
    default_town_or_city = models.CharField(max_length=40, blank=True, null=True)
    default_street_address1 = models.CharField(max_length=80, blank=True, null=True)
    default_street_address2 = models.CharField(max_length=80, blank=True, null=True)
    default_county = models.CharField(max_length=80, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profiles_userprofile'


class ReviewsProductreview(models.Model):
    title = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    date = models.DateTimeField()
    product = models.ForeignKey(ProductsProduct, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reviews_productreview'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=200)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    extra_data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)
    provider_id = models.CharField(max_length=200)
    settings = models.JSONField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class SubscribeSubscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    date_subscribed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'subscribe_subscriber'
