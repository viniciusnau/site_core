from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F, Q
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import Profile

class BasePublishModel(models.Model):
    STATUS_CHOICES = [
        ("published", "Publicado"),
        ("not_published", "Não publicado"),
        ("scheduled", "Agendado"),
    ]

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="not_published"
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.status == "published" and self.published_at is None:
            self.published_at = timezone.now()
        elif self.status == "not_published":
            self.published_at = None
        super().save(*args, **kwargs)


class FAQ(BasePublishModel):
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question


class Cards(BasePublishModel):
    title = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": "Já existe um card com este título."},
    )

    def __str__(self):
        return self.title


class CardRegister(BasePublishModel):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, null=False, related_name="registers")
    title = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": "Já existe um registro de card com este título."},
    )
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="cards/images/", blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Core(BasePublishModel):
    core_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.core_name


class TypeOfService(BasePublishModel):
    service_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.service_name


class AreaOfDuty(BasePublishModel):
    dutie_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.dutie_name


class Unit(BasePublishModel):
    STATE_CHOICES = [
        ("acre", "Acre"),
        ("alagoas", "Alagoas"),
        ("amapa", "Amapá"),
        ("amazonas", "Amazonas"),
        ("bahia", "Bahia"),
        ("ceara", "Ceará"),
        ("distrito_federal", "Distrito Federal"),
        ("espirito_santo", "Espírito Santo"),
        ("goias", "Goiás"),
        ("maranhao", "Maranhão"),
        ("mato_grosso", "Mato Grosso"),
        ("mato_grosso_do_sul", "Mato Grosso do Sul"),
        ("minas_gerais", "Minas Gerais"),
        ("para", "Pará"),
        ("paraiba", "Paraíba"),
        ("parana", "Paraná"),
        ("pernambuco", "Pernambuco"),
        ("piaui", "Piauí"),
        ("rio_de_janeiro", "Rio de Janeiro"),
        ("rio_grande_do_norte", "Rio Grande do Norte"),
        ("rio_grande_do_sul", "Rio Grande do Sul"),
        ("rondonia", "Rondônia"),
        ("roraima", "Roraima"),
        ("santa_catarina", "Santa Catarina"),
        ("sao_paulo", "São Paulo"),
        ("sergipe", "Sergipe"),
        ("tocantins", "Tocantins"),
    ]

    unit_name = models.CharField(max_length=255, blank=True, null=True)
    core = models.ForeignKey(Core, on_delete=models.CASCADE, related_name="units")
    url = models.URLField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    name_dp = models.CharField(max_length=255, blank=True, null=True)
    email_dp = models.EmailField(blank=True, null=True)

    cep = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(
        max_length=255,
        choices=STATE_CHOICES,
        default="santa_catarina",
        blank=True,
        null=True,
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_whatsapp = models.BooleanField(default=False)

    department = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    types_of_service = models.ForeignKey(
        TypeOfService, on_delete=models.SET_NULL, null=True
    )
    schedules = models.TextField(blank=True, null=True)

    area_of_duty = models.ManyToManyField(AreaOfDuty, blank=True)
    link_schedule_service = models.URLField(blank=True, null=True)

    is_principal = models.BooleanField(default=False)

    def __str__(self):
        return self.unit_name


class Email(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="emails")
    email = models.EmailField()

    def __str__(self):
        return self.email


class Contact(BasePublishModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="contacts")
    phone = models.CharField(max_length=20)
    is_whatsapp = models.BooleanField(default=False)
    department = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.phone}"


class UnitService(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="services")
    type_of_service = models.ForeignKey(
        TypeOfService, on_delete=models.SET_NULL, null=True
    )
    schedules = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.unit.unit_name} - {self.type_of_service.service_name}"


class Popup(BasePublishModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="popups/", blank=True, null=True)
    click = models.PositiveIntegerField(default=0)
    visualization = models.PositiveIntegerField(default=0)

    def increment_click(self):
        self.click += 1
        self.save(update_fields=["click"])

    def increment_visualization(self):
        self.visualization += 1
        self.save(update_fields=["visualization"])

    def __str__(self):
        return self.title


class Tag(BasePublishModel):
    name_tag = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        error_messages={"unique": "Já existe uma tag com este nome."},
    )
    times_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name_tag


class AreaOfActivity(BasePublishModel):
    title = models.CharField(max_length=255, blank=True, null=False)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="area_of_activity/", blank=True, null=True)

    def __str__(self):
        return self.title


class WebsiteInformations(BasePublishModel):
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Defensoria Pública do Estado de Santa Catarina",
    )
    slogan = models.CharField(max_length=400, blank=True, null=True)
    key_words = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class SocialMedia(BasePublishModel):
    NETWORK_CHOICES = [
        ("facebook", "Facebook"),
        ("x", "X"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("linkedin", "LinkedIn"),
    ]

    network = models.CharField(max_length=20, choices=NETWORK_CHOICES, unique=True)
    url = models.URLField(blank=True, null=True, default="")

    def __str__(self):
        return f"{self.get_network_display()}: {self.url or 'sem URL'} - {self.status}"


class EmailWebsite(BasePublishModel):
    LOCATION_CHOICES = [
        ("email_website", "Email do Website"),
        ("comentarios", "Comentários"),
        ("faq", "FAQ"),
        ("relato_de_erros", "Relato de Erros"),
    ]
    location = models.CharField(
        max_length=255, choices=LOCATION_CHOICES, blank=True, null=True, unique=True
    )
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.location


class News(BasePublishModel):
    NEWS_CHOICES = [
        ("normal", "Normal"),
        ("main", "Principal"),
        ("secondary", "Secundária"),
    ]
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    title = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": "Já existe uma notícia com este título."},
    )
    subtitle = models.TextField(max_length=500, blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    highlight = models.CharField(max_length=20, choices=NEWS_CHOICES, default="normal")
    tags = models.ManyToManyField(Tag, blank=True)
    text = models.TextField()

    def clean(self):
        super().clean()
        if self.highlight == "main":
            exists = News.objects.exclude(pk=self.pk).filter(highlight="main").exists()
            if exists:
                raise ValidationError("Já existe uma notícia com destaque Principal.")

        if self.highlight == "secondary":
            count = (
                News.objects.exclude(pk=self.pk).filter(highlight="secondary").count()
            )
            if count >= 3:
                raise ValidationError("Já existem 3 notícias com destaque Secundária.")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.slug = slugify(self.title)
        if self.status == "scheduled" and self.published_at is None:
            self.published_at = self.scheduled_at
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"


class NewsGalleryImage(models.Model):
    news = models.ForeignKey(News, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="news/gallery/")
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.caption


class NewsAttachment(models.Model):
    news = models.ForeignKey(News, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to="news/attachments/")
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description


class Category(BasePublishModel):
    title = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": "Já existe uma categoria com este título."},
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @property
    def records_count(self):
        return Records.objects.filter(
            Q(category=self) | Q(sub_category__category=self), status="published"
        ).count()


class Subcategory(BasePublishModel):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    sub_category = models.ForeignKey('self', null=True, blank=True, 
                                    related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Records(BasePublishModel):
    title = models.CharField(max_length=255, unique=True)
    attachment = models.FileField(upload_to="records/attachments/")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    sub_category = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="records",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="records",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Posters(BasePublishModel):
    title = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": "Já existe uma cartilha com este título."},
    )
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="posters/images/")
    attachment = models.FileField(upload_to="posters/attachments/")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Banner(BasePublishModel):
    GROUP_CHOICES = [
        ("slides", "Slides"),
        ("footer_banner", "Banner do rodapé"),
    ]

    banner = models.ImageField(upload_to="banner/images/")
    banner_mobile = models.ImageField(upload_to="banner/images/", null=True, blank=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    alt = models.TextField(blank=True)
    group = models.CharField(max_length=255, choices=GROUP_CHOICES)
    position = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["group"],
                condition=models.Q(group="footer_banner"),
                name="unique_footer_banner"
            )
        ]

    def delete(self, *args, **kwargs):
        if self.group == "slides":
            with transaction.atomic():
                Banner.objects.filter(
                    group="slides",
                    position__gt=self.position
                ).update(position=F("position") - 1)
        super().delete(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.group == "footer_banner":
            exists = Banner.objects.exclude(pk=self.pk).filter(group="footer_banner").exists()
            if exists:
                raise ValidationError("Já existe um banner no rodapé.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.group == "slides":
            if not self.position or self.position < 1:
                self.position = 1

            with transaction.atomic():
                if not self.pk:
                    Banner.objects.filter(
                        group="slides",
                        position__gte=self.position
                    ).update(position=F("position") + 1)
                else:
                    old_position = Banner.objects.get(pk=self.pk).position
                    if old_position < self.position:
                        Banner.objects.filter(
                            group="slides",
                            position__gt=old_position,
                            position__lte=self.position
                        ).update(position=F("position") - 1)
                    elif old_position > self.position:
                        Banner.objects.filter(
                            group="slides",
                            position__gte=self.position,
                            position__lt=old_position
                        ).update(position=F("position") + 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.alt or "Banner sem descrição"
    
class Container(BasePublishModel):
    show_title = models.BooleanField(default=False)
    title = models.CharField(max_length=255, default="Título Padrão")
    title_color = models.CharField(max_length=255, blank=True, null=True)
    background_color = models.CharField(max_length=255, blank=True, null=True)
    redirect_button = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
    
class ServiceButtons(BasePublishModel):
    image = models.ImageField(upload_to="service/images/")
    title = models.CharField(max_length=255)
    title_color = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    position = models.PositiveSmallIntegerField(default=1)

    def clean(self):
        super().clean()
        count = (
            ServiceButtons.objects.exclude(pk=self.pk).filter().count()
        )
        if count >= 3:
            raise ValidationError("Já existem 3 botões.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.position or self.position < 1:
            self.position = 1

        with transaction.atomic():
            if not self.pk:
                ServiceButtons.objects.filter(
                    position__gte=self.position
                ).update(position=F("position") + 1)
            else:
                old_position = ServiceButtons.objects.get(pk=self.pk).position
                if old_position < self.position:
                    ServiceButtons.objects.filter(
                        position__gt=old_position,
                        position__lte=self.position
                    ).update(position=F("position") - 1)
                elif old_position > self.position:
                    ServiceButtons.objects.filter(
                        position__gte=self.position,
                        position__lt=old_position
                    ).update(position=F("position") + 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class QuickAccessButtons(BasePublishModel):
    GROUP_CHOICES = [
        ("above_group", "Parte superior"),
        ("under_group", "Parte inferior"),
    ]

    title = models.CharField(max_length=255)
    title_color = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="quick_access/images/")
    background_color = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, choices=GROUP_CHOICES)
    position = models.PositiveSmallIntegerField(default=1)
    link = models.CharField(max_length=255)

    def clean(self):
        if QuickAccessButtons.objects.exclude(pk=self.pk).filter(group=self.group).count() >= 6:
            raise ValidationError(
                f"Atingiu o limite máximo de Botões no grupo: {self.get_group_display()}"
            )

    
    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.position or self.position < 1:
            self.position = 1

        with transaction.atomic():
            if not self.pk:
                QuickAccessButtons.objects.filter(
                    group=self.group,
                    position__gte=self.position
                ).update(position=F("position") + 1)
            else:
                old = QuickAccessButtons.objects.get(pk=self.pk)
                if old.group != self.group:
                    QuickAccessButtons.objects.filter(
                        group=old.group,
                        position__gt=old.position
                    ).update(position=F("position") - 1)
                    QuickAccessButtons.objects.filter(
                        group=self.group,
                        position__gte=self.position
                    ).update(position=F("position") + 1)
                elif old.position != self.position:
                    if old.position < self.position:
                        QuickAccessButtons.objects.filter(
                            group=self.group,
                            position__gt=old.position,
                            position__lte=self.position
                        ).update(position=F("position") - 1)
                    else:
                        QuickAccessButtons.objects.filter(
                            group=self.group,
                            position__gte=self.position,
                            position__lt=old.position
                        ).update(position=F("position") + 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Page(BasePublishModel):
    title = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": "Já existe uma página com este título."},
    )
    text = models.TextField(blank=True, null=True)
    has_faq = models.BooleanField(default=False)
    has_news = models.BooleanField(default=False)
    has_posters = models.BooleanField(default=False)
    has_cores = models.BooleanField(default=False)
    card = models.ForeignKey(
        "Cards", on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    allowed_users = models.ManyToManyField(
        Profile,
        blank=True,
        related_name="manageable_pages",
        verbose_name="Usuários com permissão para editar/excluir esta página",
    )

    class Meta:
        permissions = [
            ("can_create_page", "Pode criar páginas"),
        ]

    def __str__(self):
        return self.title

class Header(BasePublishModel):
    background_color = models.CharField(max_length=255, blank=True, null=True)
    name_color = models.CharField(max_length=255, blank=True, null=True)
    structure = models.JSONField()

    def __str__(self):
        return f"Header {self.id}"