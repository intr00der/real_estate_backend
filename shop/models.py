from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from shop.utils import make_thumbnail, apply_discount
from conf import settings


class EstateApplication(models.Model):
    title = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    default_price = models.DecimalField(max_digits=12, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=12,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    discount = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   default=0)
    description = models.TextField(null=True, blank=True)
    primary_image = models.ImageField(upload_to='shop/images/',
                                      blank=True,
                                      null=True)
    preview_image = models.ImageField(upload_to='shop/images',
                                      blank=True,
                                      null=True)

    class Meta:
        unique_together = ('country', 'state', 'city', 'street', 'house_number')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.primary_image:
            make_thumbnail(self)

        price_data = apply_discount(self.default_price, self.discount)
        self.default_price = price_data['default_price']
        self.discount = price_data['discount']
        self.discounted_price = price_data['discounted_price']

        return super().save(self, force_update=False, using=None,
             update_fields=None)

    def format_address(self):
        return f'{self.country}, {self.state}, {self.city}, {self.street}, {self.house_number}'

    def __str__(self):
        address_string = self.format_address()
        return f'{self.title} (Price: {self.discounted_price}$, Discount: {self.discount if self.discount else 0}%) ({address_string})'


class AdditionalEstateImage(models.Model):
    title = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='shop/images/')
    estate = models.ForeignKey(EstateApplication, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = 'estate_images'

    def __str__(self):
        return self.title


class EstatePurchaseOrder(models.Model):
    estate = models.ForeignKey(EstateApplication,
                               on_delete=models.PROTECT,
                               related_name='order')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.DecimalField(max_digits=10, decimal_places=0)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    # не могу положить в utils - будет циркулярный импорт
    # Берет данные POST запроса, берет данные по foreignkey на дом, отправляет шаблон с данными
    # prefetch_related чтобы приложить дополнительные фотки объекта, сделав минимум запросов
    def send_estate_order_email(order_data):
        # проверял при помощи smtp.gmail.com,
        # а также при помощи локального smtp-сервера (BASE_DIR/smtp_server.sh)
        estate = EstateApplication.objects.prefetch_related(
            Prefetch('estate_images', queryset=AdditionalEstateImage.objects.filter(estate_id=order_data['estate'])
                     )).get(pk=order_data['estate'])

        html_message = render_to_string('shop/invoice.html', {
            'estate_title': estate.title,
            'estate_country': estate.country,
            'estate_state': estate.state,
            'estate_city': estate.city,
            'estate_street': estate.street,
            'estate_house_number': estate.house_number,
            'estate_buyer_first_name': order_data['first_name'],
            'estate_buyer_last_name': order_data['last_name']
        })

        subject = settings.DEFAULT_EMAIL_SUBJECT
        from_email = settings.EMAIL_HOST_USER
        plain_message = strip_tags(html_message)
        to = order_data['email']
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
        email.attach_alternative(html_message, 'text/html')

        if settings.EMAIL_HOST != 'localhost':
            # чтобы при отправке сообщения локальным smtp-сервером
            # не прикладывались изображения

            if estate.primary_image:
                email.attach_file(estate.preview_image.file.name)
            for image in estate.estate_images.all():
               email.attach_file(image.image.file.name)
        email.send()
