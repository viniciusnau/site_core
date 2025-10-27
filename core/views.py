from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    FAQ,
    AreaOfActivity,
    AreaOfDuty,
    Banner,
    CardRegister,
    Cards,
    Category,
    Container,
    Core,
    EmailWebsite,
    News,
    NewsAttachment,
    NewsGalleryImage,
    Page,
    Popup,
    Posters,
    QuickAccessButtons,
    Records,
    ServiceButtons,
    SocialMedia,
    Subcategory,
    Tag,
    TypeOfService,
    Unit,
    UnitService,
    WebsiteInformations,
)
from .serializers import (
    AreaOfActivitySerializer,
    AreaOfDutySerializer,
    BannerSerializer,
    CardRegisterSerializer,
    CardsSerializer,
    CategorySerializer,
    ContainerSerializer,
    CoreSerializer,
    EmailWebsiteSerializer,
    FAQSerializer,
    NewsAttachmentSerializer,
    NewsGalleryImageSerializer,
    NewsSerializer,
    PageSerializer,
    PopupSerializer,
    PostersSerializer,
    QuickAccessButtonsSerializer,
    RecordsSerializer,
    ServiceButtonsSerializer,
    SocialMediaSerializer,
    SubcategorySerializer,
    TagSerializer,
    TypeOfServiceSerializer,
    UnitSerializer,
    WebsiteInformationsSerializer, 
    CardRegisterSerializer,
    BannerSerializer,
    ContainerSerializer,
    ServiceButtonsSerializer,
    QuickAccessButtonsSerializer,
    CoresAndUnitSerializer,
    )


class FaqView(generics.GenericAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        faqs = self.get_queryset()
        
        published_param = request.query_params.get("published")
        if published_param and published_param.lower() == "true":
            faqs = faqs.filter(status="published")
        
        faqs = faqs.order_by('-created_at')

        serializer = self.get_serializer(faqs, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        try:
            faq = FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            return Response(
                {"error": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND
            )

        faq.delete()
        return Response(
            {"message": f"FAQ {pk}, deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def patch(self, request, pk, *args, **kwargs):
        try:
            faq = FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            return Response(
                {"error": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoreView(generics.GenericAPIView):
    queryset = Core.objects.all()
    serializer_class = CoreSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        core = self.get_queryset().order_by('-created_at')

        published_param = request.query_params.get("published")
        if published_param and published_param.lower() == "true":
            core = core.filter(status="published")
        
        serializer = self.get_serializer(core, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            core = Core.objects.get(pk=pk)
        except Core.DoesNotExist:
            return Response(
                {"error": "Core not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(core, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            core = Core.objects.get(pk=pk)
        except Core.DoesNotExist:
            return Response(
                {"error": "Core not found"}, status=status.HTTP_404_NOT_FOUND
            )

        core.delete()
        return Response(
            {"message": f"Core {pk}, deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class UnitView(generics.GenericAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        unit = self.get_queryset().order_by('-created_at')

        published_param = request.query_params.get("published")
        if published_param and published_param.lower() == "true":
            unit = unit.filter(status="published")

        serializer = self.get_serializer(unit, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        services_data = request.data.pop("services", [])
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            unit = serializer.save(author=request.user)

            for service_item in services_data:
                UnitService.objects.create(
                    unit=unit,
                    type_of_service_id=service_item["type_of_service"],
                    schedules=service_item.get("schedules", ""),
                )
            return Response(
                self.get_serializer(unit).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            unit = Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            return Response(
                {"Error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND
            )

        services_data = request.data.pop("services", [])
        serializer = self.get_serializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            unit = serializer.save(author=request.user)

            unit.services.all().delete()
            for service_item in services_data:
                UnitService.objects.create(
                    unit=unit,
                    type_of_service_id=service_item["type_of_service"],
                    schedules=service_item.get("schedules", ""),
                )

            return Response(self.get_serializer(unit).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            unit = Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            return Response(
                {"Error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND
            )

        unit.delete()
        return Response(
            {"message": f"Unit {pk}, deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CoreUnitsView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            core = Core.objects.get(pk=pk)
        except Core.DoesNotExist:
            return Response(
                {"error": "Core not found"}, status=status.HTTP_404_NOT_FOUND
            )

        units = core.units.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)


class AreaOfDutyView(generics.GenericAPIView):
    queryset = AreaOfDuty.objects.all()
    serializer_class = AreaOfDutySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        duty = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(duty, many=True)
        return Response(serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        try:
            duty = AreaOfDuty.objects.get(pk=pk)
        except AreaOfDuty.DoesNotExist:
            return Response(
                {"Error": "Duty not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(duty, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            duty = AreaOfDuty.objects.get(pk=pk)
        except AreaOfDuty.DoesNotExist:
            return Response(
                {"Error": "Duty not found"}, status=status.HTTP_404_NOT_FOUND
            )

        duty.delete()
        return Response(
            {"message": f"Duty {pk}, deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TypeOfServiceView(generics.GenericAPIView):
    queryset = TypeOfService.objects.all()
    serializer_class = TypeOfServiceSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        type_of_service = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(type_of_service, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            type_of_service = TypeOfService.objects.get(pk=pk)
        except TypeOfService.DoesNotExist:
            return Response(
                {"Error": "Type of service not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            type_of_service, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            type_of_service = TypeOfService.objects.get(pk=pk)
        except TypeOfService.DoesNotExist:
            return Response(
                {"Error": "Type of service not found"}, status=status.HTTP_404_NOT_FOUND
            )

        type_of_service.delete()
        return Response(
            {"message": f"Type of service {pk}, deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class PopupView(generics.GenericAPIView):
    queryset = Popup.objects.all()
    serializer_class = PopupSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        popup = self.get_queryset()
        serializer = self.get_serializer(popup, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            popup = Popup.objects.get(pk=pk)
        except Popup.DoesNotExist:
            return Response({"Error": "Popup not found"})

        serializer = self.get_serializer(popup, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            popup = Popup.objects.get(pk=pk)
        except Popup.DoesNotExist:
            return Response(
                {"Error": "Popup not found"}, status=status.HTTP_404_NOT_FOUND
            )

        popup.delete()
        return Response(
            {"message": f"Popup {pk}, deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class PopupIncrementClickView(generics.GenericAPIView):
    def post(self, request, pk):
        try:
            popup = Popup.objects.get(pk=pk)
        except Popup.DoesNotExist:
            return Response(
                {"error": "Popup not found"}, status=status.HTTP_404_NOT_FOUND
            )

        popup.increment_click()
        return Response({"Clicks": popup.click}, status=status.HTTP_200_OK)


class PopupIncrementVisualizationView(generics.GenericAPIView):
    def post(self, request, pk):
        try:
            popup = Popup.objects.get(pk=pk)
        except Popup.DoesNotExist:
            return Response(
                {"error": "Popup not found"}, status=status.HTTP_404_NOT_FOUND
            )

        popup.increment_visualization()
        return Response(
            {"Visualization": popup.visualization}, status=status.HTTP_200_OK
        )


class TagView(generics.GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        tag = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(tag, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(
                {"Error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(tag, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(
                {"Error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND
            )

        tag.delete()
        return Response(
            {f"Tag {pk}, deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class AreaOfActivityView(generics.GenericAPIView):
    queryset = AreaOfActivity.objects.all()
    serializer_class = AreaOfActivitySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        area_of_activity = self.get_queryset()
        serializer = self.get_serializer(area_of_activity, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            area_of_activity = AreaOfActivity.objects.get(pk)
        except AreaOfActivity.DoesNotExist:
            return Response(
                {"Error": "Area of Activity not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(
            area_of_activity, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            area_of_activity = AreaOfActivity.objects.get(pk)
        except AreaOfActivity.DoesNotExist:
            return Response(
                {"Error": "Area of Activity not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        area_of_activity.delete()
        return Response(
            {f"Area of Activity {pk}, deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class WebsiteInformationView(generics.GenericAPIView):
    serializer_class = WebsiteInformationsSerializer
    queryset = WebsiteInformations.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        website_information = WebsiteInformations.objects.first()
        if not website_information:
            return Response(
                {"error": "there is no information to show"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(website_information)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if WebsiteInformations.objects.exists():
            return Response(
                {"error": "it already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        website_information = WebsiteInformations.objects.first()
        if not website_information:
            return Response(
                {"error": "there is no information to edit"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(
            website_information, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        website_information = WebsiteInformations.objects.first()
        if not website_information:
            return Response(
                {"error": "there is no information to delete"},
                status=status.HTTP_404_NOT_FOUND,
            )

        website_information.delete()
        return Response(
            {"Website information deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class SocialMediaView(generics.GenericAPIView):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET", "PATCH"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        social_media = self.get_queryset()
        serializer = self.get_serializer(social_media, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            social_media = SocialMedia.objects.get(pk=pk)
        except SocialMedia.DoesNotExist:
            return Response(
                {"error": "Social media not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(social_media, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            social_media = SocialMedia.objects.get(pk=pk)
        except SocialMedia.DoesNotExist:
            return Response(
                {"error": "Social media not found"}, status=status.HTTP_404_NOT_FOUND
            )

        social_media.delete()
        return Response(
            {f"Social media {pk}, deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class EmailWebsiteView(generics.GenericAPIView):
    queryset = EmailWebsite.objects.all()
    serializer_class = EmailWebsiteSerializer

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        email_website = self.get_queryset()
        serializer = self.get_serializer(email_website, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        try:
            email_website = EmailWebsite.objects.get(pk=pk)
        except EmailWebsite.DoesNotExist:
            return Response(
                {"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(email_website, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            email_website = EmailWebsite.objects.get(pk=pk)
        except EmailWebsite.DoesNotExist:
            return Response(
                {"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND
            )

        email_website.delete()
        return Response(
            {f"Email {pk}, deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class AuthorsByModel(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        model_name = kwargs.get("model_name")
        try:
            apps.get_model("core", model_name.capitalize())
        except LookupError:
            return JsonResponse({"error": "Modelo inválido"}, status=400)

        authors = User.objects.filter(**{f"{model_name}__isnull": False}).distinct()
        data = [{"id": u.id, "name": u.get_full_name() or u.username} for u in authors]
        return JsonResponse(data, safe=False)


class NewsView(generics.GenericAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        if slug:
            news = get_object_or_404(News, slug=slug)
            serializer = self.get_serializer(news)
            return Response(serializer.data)

        news = self.get_queryset().order_by('-created_at')
        now = timezone.now()
        News.objects.filter(status="scheduled", published_at__lte=now).update(
            status="published"
        )

        published_param = request.query_params.get("published")
        if published_param is not None and published_param.lower() == "true":
            news = news.filter(status="published", published_at__lte=now)

        serializer = self.get_serializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        news = get_object_or_404(News, pk=pk)
        serializer = self.get_serializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        news = get_object_or_404(News, pk=pk)

        news.delete()
        return Response(
            f"News {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class NewsGalleryImageView(generics.GenericAPIView):
    serializer_class = NewsGalleryImageSerializer
    queryset = NewsGalleryImage.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                gallery = self.get_object()
                serializer = self.get_serializer(gallery)
                return Response(serializer.data)
            except NewsGalleryImage.DoesNotExist:
                return Response(
                    {"Error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND
                )

        gallery = self.get_queryset()
        serializer = self.get_serializer(gallery, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        gallery = self.get_serializer(data=request.data)
        if gallery.is_valid():
            gallery.save(author=request.user)
            return Response(
                "Gallery has been created successfully", status=status.HTTP_201_CREATED
            )
        return Response(
            f"Gallery could not be created: {gallery.errors}",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        gallery = get_object_or_404(NewsGalleryImage, pk=pk)

        serializer = self.get_serializer(gallery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        gallery = get_object_or_404(NewsGalleryImage, pk=pk)

        gallery.delete()
        return Response(
            f"Gallery {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class NewsAttachmentView(generics.GenericAPIView):
    serializer_class = NewsAttachmentSerializer
    queryset = NewsAttachment.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                attachment = self.get_object()
                serializer = self.get_serializer(attachment)
                return Response(serializer.data)
            except NewsAttachment.DoesNotExist:
                return Response(
                    {"Error": "Attachment not found"}, status=status.HTTP_404_NOT_FOUND
                )

        attachment = self.get_queryset()
        serializer = self.get_serializer(attachment, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        attachment = self.get_serializer(data=request.data)
        if attachment.is_valid():
            attachment.save(author=request.user)
            return Response(
                "Attachment has been created successfully",
                status=status.HTTP_201_CREATED,
            )
        return Response(
            f"Attachment could not be created: {attachment.errors}",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        attachment = get_object_or_404(NewsAttachment, pk=pk)

        serializer = self.get_serializer(attachment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        attachment = get_object_or_404(NewsAttachment, pk=pk)

        attachment.delete()
        return Response(
            f"Attachment {pk} was deleted successfully",
            status=status.HTTP_204_NO_CONTENT,
        )


class CategoryView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            serializer = self.get_serializer(category)
            return Response(serializer.data)

        ids = request.query_params.get("ids")
        status_param = request.query_params.get("status")
        queryset = self.get_queryset()

        if status_param and status_param != "all":
            queryset = queryset.filter(status=status_param)

        if ids:
            try:
                ids_list = [int(i) for i in ids.split(",")]
                queryset = queryset.filter(id__in=ids_list)
            except ValueError:
                return Response(
                    {"error": "IDs devem ser números separados por vírgula"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        queryset = queryset.order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        category = self.get_serializer(data=request.data)
        if category.is_valid():
            category.save(author=request.user)
            return Response(
                "Category has been created successfully",
                status=status.HTTP_201_CREATED,
            )
        return Response(
            f"Category could not be created: {category.errors}",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.get_serializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(
            f"Category {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class SubcategoryView(generics.GenericAPIView):
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, pk=None, *args, **kwargs):
        if pk:

            sub_category = get_object_or_404(Subcategory, pk=pk)
            serializer = self.get_serializer(sub_category)
        else:
            
            sub_category = self.get_queryset().order_by('-created_at')
            serializer = self.get_serializer(sub_category, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        sub_category = self.get_serializer(data=request.data)
        if sub_category.is_valid():
            sub_category.save(author=request.user)
            return Response(
                "Sub category has been created successfully",
                status=status.HTTP_201_CREATED,
            )
        return Response(
            f"Sub category could not be created: {sub_category.errors}",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        sub_category = get_object_or_404(Subcategory, pk=pk)
        serializer = self.get_serializer(sub_category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        sub_category = get_object_or_404(Subcategory, pk=pk)
        sub_category.delete()
        return Response(
            f"Sub category {pk} was deleted successfully",
            status=status.HTTP_204_NO_CONTENT,
        )


class RecordsView(generics.GenericAPIView):
    serializer_class = RecordsSerializer
    queryset = Records.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        records = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        records = self.get_serializer(data=request.data)
        if records.is_valid():
            records.save(author=request.user)
            return Response(
                "Records has been created successfully", status=status.HTTP_201_CREATED
            )
        return Response(
            f"Records could not be created: {records.errors}",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        records = get_object_or_404(Records, pk=pk)
        serializer = self.get_serializer(records, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        records = get_object_or_404(Records, pk=pk)
        records.delete()
        return Response(
            f"Records {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class PostersView(generics.GenericAPIView):
    serializer_class = PostersSerializer
    queryset = Posters.objects.all()
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        if slug:
            poster = get_object_or_404(Posters, slug=slug)
            serializer = self.get_serializer(poster)
            return Response(serializer.data)
        posters = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(posters, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        poster = self.get_serializer(data=request.data)
        if poster.is_valid():
            poster.save(author=request.user)
            return Response(
                "Poster has been created successfully", status=status.HTTP_201_CREATED
            )
        return Response(
            f"Poster could not be created: {poster.errors}",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        poster = get_object_or_404(Posters, pk=pk)
        serializer = self.get_serializer(poster, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        poster = get_object_or_404(Posters, pk=pk)
        poster.delete()
        return Response(
            f"Poster {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class CardsView(generics.GenericAPIView):
    serializer_class = CardsSerializer
    queryset = Cards.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if pk is not None:
            try:
                card = self.get_queryset().prefetch_related("registers").get(pk=pk)
            except Cards.DoesNotExist:
                return Response({"detail": "Card não encontrado."}, status=404)
            serializer = self.get_serializer(card)
        else:
            cards = self.get_queryset()
            serializer = self.get_serializer(cards, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        cards = get_object_or_404(Cards, pk=pk)
        serializer = self.get_serializer(cards, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        cards = get_object_or_404(Cards, pk=pk)
        cards.delete()
        return Response(
            f"Cards {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class CardRegisterView(generics.GenericAPIView):
    serializer_class = CardRegisterSerializer
    queryset = CardRegister.objects.all()
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        if slug:
            card_register = get_object_or_404(CardRegister, slug=slug)
            serializer = self.get_serializer(card_register)
            return Response(serializer.data)

        card_register = self.get_queryset()
        serializer = self.get_serializer(card_register, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        card_register = get_object_or_404(CardRegister, pk=pk)
        serializer = self.get_serializer(card_register, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        card_register = get_object_or_404(CardRegister, pk=pk)
        card_register.delete()
        return Response(
            f"CardRegister {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT
        )
   
class BannerView(generics.GenericAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()

    def get(self, request, *args, **kwargs):
        banners = self.get_queryset()
        published_param = request.query_params.get("published")
        if published_param is not None and published_param.lower() == "true":
            banners = banners.filter(status="published")

        serializer = self.get_serializer(banners, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            banner = serializer.save(author=request.user)
            return Response(self.get_serializer(banner).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        banner = get_object_or_404(Banner, pk=pk)
        serializer = self.get_serializer(banner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        banner = get_object_or_404(Banner, pk=pk)
        banner.delete()
        return Response(f"Banner {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT)
    
class ContainerView(generics.GenericAPIView):
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()

    def get(self, request, *args, **kwargs):
        containers = self.get_queryset()
        serializer = self.get_serializer(containers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            containers = serializer.save(author=request.user)
            return Response(self.get_serializer(containers).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        containers = get_object_or_404(Container, pk=pk)
        serializer = self.get_serializer(containers, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        containers = get_object_or_404(Container, pk=pk)
        containers.delete()
        return Response(f"Container {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT)
    
class ServiceButtonsView(generics.GenericAPIView):
    serializer_class = ServiceButtonsSerializer
    queryset = ServiceButtons.objects.all()

    def get(self, request, *args, **kwargs):
        services_buttons = self.get_queryset()
        serializer = self.get_serializer(services_buttons, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        services_buttons = get_object_or_404(ServiceButtons, pk=pk)
        serializer = self.get_serializer(services_buttons, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        services_buttons = get_object_or_404(ServiceButtons, pk=pk)
        services_buttons.delete()
        return Response(f"Service buttons {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT)

class QuickAccessButtonsView(generics.GenericAPIView):
    serializer_class = QuickAccessButtonsSerializer
    queryset = QuickAccessButtons.objects.all()

    def get(self, request, *args, **kwargs):
        quick_access_buttons = self.get_queryset()
        serializer = self.get_serializer(quick_access_buttons, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                if hasattr(e, "message_dict"):
                    return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        quick_access_buttons = get_object_or_404(QuickAccessButtons, pk=pk)
        serializer = self.get_serializer(quick_access_buttons, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        quick_access_buttons = get_object_or_404(QuickAccessButtons, pk=pk)
        quick_access_buttons.delete()
        return Response(f"Quick access buttons {pk} was deleted successfully", status=status.HTTP_204_NO_CONTENT)
    

class CoresAndUnitView(generics.GenericAPIView):
    queryset = Core.objects.all()
    serializer_class = CoresAndUnitSerializer

    def get(self, request, *args, **kwargs):
        cores_and_unit = self.get_queryset().order_by('-created_at')
        cores_with_units = cores_and_unit.filter(units__isnull=False).distinct()
        published_param = request.query_params.get("published")
        
        if published_param and published_param.lower() == "true":
            cores_with_units = cores_with_units.filter(status="published")

        serializer = self.get_serializer(cores_with_units, many=True)
        return Response(serializer.data)
