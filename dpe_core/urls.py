from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import (
    AreaOfActivityView,
    AreaOfDutyView,
    AuthorsByModel,
    CategoryView,
    CoreUnitsView,
    CoreView,
    EmailWebsiteView,
    FaqView,
    NewsAttachmentView,
    NewsGalleryImageView,
    NewsView,
    PopupIncrementClickView,
    PopupIncrementVisualizationView,
    PopupView,
    PostersView,
    RecordsView,
    SocialMediaView,
    SubcategoryView,
    TagView,
    TypeOfServiceView,
    UnitView,
    WebsiteInformationView,
    BannerView,
    ContainerView,
    ServiceButtonsView,
    QuickAccessButtonsView,
    CoresAndUnitView,
)
from dpe_core import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("api/", include("accounts.urls")),
    path("api/faq/", FaqView.as_view(), name="faq-list-create"),
    path("api/faq/<int:pk>/", FaqView.as_view(), name="faq-detail"),
    path("api/unit/", UnitView.as_view(), name="unit-list-create"),
    path("api/unit/<int:pk>/", UnitView.as_view(), name="unit-detail"),
    path("api/core/", CoreView.as_view(), name="core-list-create"),
    path("api/core/<int:pk>/", CoreView.as_view(), name="core-detail"),
    path("api/core/<int:pk>/units/", CoreUnitsView.as_view(), name="core-units"),
    path("api/cores-units/", CoresAndUnitView.as_view(), name='cores-units-list'),

    path(
        "api/area-of-duty/", AreaOfDutyView.as_view(), name="area_of_duty-list-create"
    ),
    path(
        "api/area-of-duty/<int:pk>/",
        AreaOfDutyView.as_view(),
        name="area_of_duty-detail",
    ),
    path(
        "api/type-of-service/",
        TypeOfServiceView.as_view(),
        name="type_of_service-list-create",
    ),
    path(
        "api/type-of-service/<int:pk>/",
        TypeOfServiceView.as_view(),
        name="type_of_service-detail",
    ),
    path("api/popup/", PopupView.as_view(), name="popup-list-create"),
    path("api/popup/<int:pk>/", PopupView.as_view(), name="popup-detail"),
    path(
        "api/popup/<int:pk>/increment_click/",
        PopupIncrementClickView.as_view(),
        name="popup-increase-click",
    ),
    path(
        "api/popup/<int:pk>/increment_visualization/",
        PopupIncrementVisualizationView.as_view(),
        name="popup-increase-visualization",
    ),
    path("api/tag/", TagView.as_view(), name="tag-list-create"),
    path("api/tag/<int:pk>/", TagView.as_view(), name="tag-detail"),
    path(
        "api/area-of-activity/",
        AreaOfActivityView.as_view(),
        name="area_of_activity-list-create",
    ),
    path(
        "api/area-of-activity/<int:pk>/",
        AreaOfActivityView.as_view(),
        name="area_of_activity-detail",
    ),
    path(
        "api/website-information/",
        WebsiteInformationView.as_view(),
        name="website_information-list-create-detail",
    ),
    path(
        "api/social-media/", SocialMediaView.as_view(), name="social_media-list-create"
    ),
    path(
        "api/social-media/<int:pk>/",
        SocialMediaView.as_view(),
        name="social_media-detail",
    ),
    path(
        "api/email-website/",
        EmailWebsiteView.as_view(),
        name="email-website-list-create",
    ),
    path(
        "api/email-website/<int:pk>/",
        EmailWebsiteView.as_view(),
        name="email-website-detail",
    ),
    path(
        "api/authors/<str:model_name>/",
        AuthorsByModel.as_view(),
        name="authors-by-model",
    ),
    path("api/news/", NewsView.as_view(), name="news-list-create"),
    path("api/news/<int:pk>/", NewsView.as_view(), name="news-detail"),
    path("api/news/<slug:slug>/", NewsView.as_view(), name="news-detail-slug"),
    path(
        "api/news-gallery/",
        NewsGalleryImageView.as_view(),
        name="news_gallery-list-create",
    ),
    path(
        "api/news-gallery/<int:pk>/",
        NewsGalleryImageView.as_view(),
        name="news_gallery-detail",
    ),
    path(
        "api/news-attachment/",
        NewsAttachmentView.as_view(),
        name="news_attachment-list-create",
    ),
    path(
        "api/news-attachment/<int:pk>/",
        NewsAttachmentView.as_view(),
        name="news_attachment-detail",
    ),
    path("api/posters/", PostersView.as_view(), name="posters-list-create"),
    path("api/posters/<int:pk>/", PostersView.as_view(), name="posters-detail"),
    path("api/posters/<slug:slug>/", PostersView.as_view(), name="posters-detail-slug"),
    path("api/modules/category/", CategoryView.as_view(), name="category-list-create"),
    path(
        "api/modules/category/<int:pk>/", CategoryView.as_view(), name="category-detail"
    ),
    path(
        "api/modules/sub-category/",
        SubcategoryView.as_view(),
        name="sub_category-list-create",
    ),
    path(
        "api/modules/sub-category/<int:pk>/",
        SubcategoryView.as_view(),
        name="sub_category-detail",
    ),
    path("api/modules/records/", RecordsView.as_view(), name="records-list-create"),
    path("api/modules/records/<int:pk>/", RecordsView.as_view(), name="records-detail"),
    path("api/posters/", PostersView.as_view(), name="posters-list-create"),
    path("api/posters/<int:pk>/", PostersView.as_view(), name="posters-detail"),
    path("api/posters/<slug:slug>/", PostersView.as_view(), name="posters-datail-slug"),

    path('api/banner/', BannerView.as_view(), name='banner-list-create'),
    path('api/banner/<int:pk>/', BannerView.as_view(), name='banner-detail'),

    path('api/container/', ContainerView.as_view(), name='container-list-create'),
    path('api/container/<int:pk>/', ContainerView.as_view(), name='container-detail'),

    path('api/service-buttons/', ServiceButtonsView.as_view(), name='service_buttons-list-create'),
    path('api/service-buttons/<int:pk>/', ServiceButtonsView.as_view(), name='service_buttons-detail'),

    path('api/quick-access-buttons/', QuickAccessButtonsView.as_view(), name='quick_access_buttons-list-create'),
    path('api/quick-access-buttons/<int:pk>/', QuickAccessButtonsView.as_view(), name='quick_access_buttons-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
