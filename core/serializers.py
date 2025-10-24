from django.db.models import Q
from django.utils.text import slugify
from rest_framework import serializers
from django.utils.text import slugify
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Q
from core.models import (
    FAQ,
    AreaOfActivity,
    AreaOfDuty,
    Cards,
    Category,
    Contact,
    Core,
    Email,
    EmailWebsite,
    News,
    NewsAttachment,
    NewsGalleryImage,
    Popup,
    Posters,
    Records,
    SocialMedia,
    Subcategory,
    Records,
    Posters, 
    Cards,
    Banner,
    Tag,
    TypeOfService,
    Unit,
    UnitService,
    WebsiteInformations, 
    CardRegister,
    Container,
    ServiceButtons,
    QuickAccessButtons,
    Header,
)


class FAQSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = FAQ
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class CoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Core
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class TypeOfServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfService
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class AreaOfDutySerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfDuty
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class UnitServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitService
        fields = ["type_of_service", "schedules"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["phone", "is_whatsapp", "department"]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["email", "id"]


class UnitSerializer(serializers.ModelSerializer):
    services = UnitServiceSerializer(many=True, required=False)
    area_of_duty = serializers.SlugRelatedField(
        many=True, queryset=AreaOfDuty.objects.all(), slug_field="dutie_name"
    )
    core = serializers.PrimaryKeyRelatedField(queryset=Core.objects.all())
    contacts = ContactSerializer(many=True)
    emails = EmailSerializer(many=True)

    class Meta:
        model = Unit
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]

    def create(self, validated_data):
        services_data = validated_data.pop("services", [])
        area_data = validated_data.pop("area_of_duty", [])
        contacts_data = validated_data.pop("contacts", [])
        emails_data = validated_data.pop("emails", [])

        unit = Unit.objects.create(**validated_data)
        unit.area_of_duty.set(area_data)

        for service_data in services_data:
            UnitService.objects.create(unit=unit, **service_data)

        for contact_data in contacts_data:
            Contact.objects.create(unit=unit, **contact_data)

        for email_data in emails_data:
            Email.objects.create(unit=unit, **email_data)
        return unit

    def update(self, instance, validated_data):
        services_data = validated_data.pop("services", [])
        area_data = validated_data.pop("area_of_duty", [])
        contacts_data = validated_data.pop("contacts", [])
        emails_data = validated_data.pop("emails", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.area_of_duty.set(area_data)

        instance.services.all().delete()
        for service_data in services_data:
            UnitService.objects.create(unit=instance, **service_data)

        instance.contacts.all().delete()
        for contact_data in contacts_data:
            Contact.objects.create(unit=instance, **contact_data)

        instance.emails.all().delete()
        for email_data in emails_data:
            Email.objects.create(unit=instance, **email_data)

        return instance


class PopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popup
        fields = "__all__"
        read_only_fields = [
            "click",
            "visualization",
            "author",
            "created_at",
            "updated_at",
            "published_at",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = [
            "times_used",
            "author",
            "created_at",
            "updated_at",
            "published_at",
        ]


class AreaOfActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfActivity
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class WebsiteInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteInformations
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class EmailWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailWebsite
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class NewsGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsGalleryImage
        fields = ("id", "image", "caption")


class NewsAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        fields = ("id", "file", "description")


class NewsSerializer(serializers.ModelSerializer):
    gallery = NewsGalleryImageSerializer(many=True, required=False, read_only=True)
    attachments = NewsAttachmentSerializer(many=True, required=False, read_only=True)
    clear_tags = serializers.BooleanField(write_only=True, required=False)
    remove_thumbnail = serializers.BooleanField(write_only=True, required=False)
    removed_gallery = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    removed_attachments = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = News
        fields = "__all__"
        extra_kwargs = {
            "thumbnail": {
                "error_messages": {
                    "invalid_image": "A thumbnail aceita apenas arquivos de imagens."
                }
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.tags.exists():
            data["tags"] = TagSerializer(instance.tags.all(), many=True).data
        else:
            data["tags"] = []

        return data

    def create(self, validated_data):
        validated_data.pop("remove_thumbnail", None)
        validated_data.pop("removed_gallery", None)
        validated_data.pop("removed_attachments", None)
        clear_tags = validated_data.pop("clear_tags", False)
        tags_data = validated_data.pop("tags", [])

        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data.get("title", ""))

        news = News.objects.create(**validated_data)

        if clear_tags:
            pass
        elif tags_data:
            news.tags.set(tags_data)

        request = self.context["request"]

        gallery_files = request.FILES.getlist("gallery")
        gallery_data = self.initial_data.get("gallery", [])
        if not isinstance(gallery_data, list):
            gallery_data = [gallery_data]

        for i, file in enumerate(gallery_files):
            caption = ""
            if i < len(gallery_data) and isinstance(gallery_data[i], dict):
                caption = gallery_data[i].get("caption", "")
            NewsGalleryImage.objects.create(news=news, image=file, caption=caption)

        attachment_files = request.FILES.getlist("attachments")
        attachments_data = self.initial_data.get("attachments", [])
        if not isinstance(attachments_data, list):
            attachments_data = [attachments_data]

        for i, file in enumerate(attachment_files):
            description = ""
            if i < len(attachments_data) and isinstance(attachments_data[i], dict):
                description = attachments_data[i].get("description", "")
            NewsAttachment.objects.create(news=news, file=file, description=description)

        return news

    def update(self, instance, validated_data):
        if not instance.slug:
            instance.slug = slugify(instance.title)

        request = self.context.get("request")
        clear_tags = validated_data.pop("clear_tags", False)

        if validated_data.pop("remove_thumbnail", False):
            if instance.thumbnail:
                instance.thumbnail.delete(save=False)
            instance.thumbnail = None

        removed_gallery_ids = validated_data.pop("removed_gallery", [])
        if removed_gallery_ids:
            instance.gallery.filter(pk__in=removed_gallery_ids).delete()

        removed_attachment_ids = validated_data.pop("removed_attachments", [])
        if removed_attachment_ids:
            instance.attachments.filter(pk__in=removed_attachment_ids).delete()

        gallery_data = self.initial_data.get("gallery", [])
        if not isinstance(gallery_data, list):
            gallery_data = [gallery_data]

        gallery_files = request.FILES.getlist("gallery")
        for i, file in enumerate(gallery_files):
            caption = ""
            if i < len(gallery_data) and isinstance(gallery_data[i], dict):
                caption = gallery_data[i].get("caption", "")
            NewsGalleryImage.objects.create(news=instance, image=file, caption=caption)

        attachments_data = self.initial_data.get("attachments", [])
        if not isinstance(attachments_data, list):
            attachments_data = [attachments_data]

        attachment_files = request.FILES.getlist("attachments")
        for i, file in enumerate(attachment_files):
            description = ""
            if i < len(attachments_data) and isinstance(attachments_data[i], dict):
                description = attachments_data[i].get("description", "")
            NewsAttachment.objects.create(
                news=instance, file=file, description=description
            )

        tags_data = validated_data.pop("tags", None)

        if clear_tags:
            instance.tags.clear()
        elif tags_data is not None:
            instance.tags.set(tags_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]

    def validate(self, attrs):
        category = attrs.get("category")
        sub_category = attrs.get("sub_category")

        if sub_category and category and sub_category.category != category:
            raise serializers.ValidationError(
                {
                    "sub_category": "A subcategoria selecionada não pertence à categoria informada"
                }
            )

        if not sub_category and not category:
            raise serializers.ValidationError(
                {"category": "Informe ao menos uma categoria ou subcategoria"}
            )
        return attrs


class SubcategorySerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title", read_only=True)
    sub_category_title = serializers.CharField(
        source='sub_category.title',
        read_only=True,
        allow_null=True,
    )
    records = RecordsSerializer(many=True, read_only=True)

    
    class Meta:
        model = Subcategory
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]




class CategorySerializer(serializers.ModelSerializer):
    records_count = serializers.SerializerMethodField()
    subcategories = SubcategorySerializer(many=True, read_only=True)
    slug = Category.pk
    records = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]

    def get_records_count(self, obj):
        return Records.objects.filter(
            Q(category=obj) | Q(sub_category__category=obj)
        ).count()

    def get_records(self, obj):
        direct_records = Records.objects.filter(category=obj, status="published")
        sub_records = Records.objects.filter(
            sub_category__category=obj, status="published"
        )
        all_records = direct_records | sub_records
        return RecordsSerializer(all_records, many=True).data


class PostersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posters
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class CardRegisterMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardRegister
        fields = ["id", "title", "slug", "subtitle"]


class CardsSerializer(serializers.ModelSerializer):
    registers = CardRegisterMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Cards
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class CardRegisterSerializer(serializers.ModelSerializer):
    remove_image = serializers.BooleanField(write_only=True, required=False)
    card = serializers.PrimaryKeyRelatedField(
        queryset=Cards.objects.all(),
        write_only=True
    )
    card_detail = CardsSerializer(source="card", read_only=True)
    related_cards = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CardRegister
        fields = "__all__"
        extra_kwargs = {
            "image": {
                "error_messages": {
                    "invalid_image": "Apenas arquivos de imagens."
                }
            }
        }

    def get_related_cards(self, obj):
        queryset = (
            CardRegister.objects
            .filter(card=obj.card)
            .exclude(id=obj.id)
            .order_by("-id")[:3]
        )
        return CardRegisterMiniSerializer(queryset, many=True, context=self.context).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        validated_data.pop("remove_image", None)

        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data.get("title", ""))

        card_register = CardRegister.objects.create(**validated_data)
        return card_register

    def update(self, instance, validated_data):
        if not instance.slug:
            instance.slug = slugify(instance.title)

        if validated_data.pop("remove_image", False):
            if instance.image:
                instance.image.delete(save=False)
            instance.image = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
       
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'updated_at', 'published_at']

    def save_instance(self, instance):
        try:
            instance.full_clean()
            instance.save()
            return instance
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def create(self, validated_data):
        instance = Banner(**validated_data)
        return self.save_instance(instance)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return self.save_instance(instance)
    
class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]

class ServiceButtonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceButtons
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]


class QuickAccessButtonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickAccessButtons
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]
        
class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ["id", "background_color", "name_color", "structure" ]
        read_only_fields = ["author", "created_at", "updated_at", "published_at"]