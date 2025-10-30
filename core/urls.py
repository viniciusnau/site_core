from django.urls import path

from core.views import (
    AreaOfActivityView,
    AreaOfDutyView,
    AuthorsByModel,
    BannerView,
    CardRegisterView,
    CardsView,
    CategoryView,
    ContainerView,
    CoreUnitsView,
    CoreView,
    EmailWebsiteView,
    FaqView,
    HeaderView,
    NewsAttachmentView,
    NewsGalleryImageView,
    NewsView,
    PageView,
    PopupIncrementClickView,
    PopupIncrementVisualizationView,
    PopupView,
    PostersView,
    QuickAccessButtonsView,
    RecordsView,
    ServiceButtonsView,
    SocialMediaView,
    SubcategoryView,
    TagView,
    TypeOfServiceView,
    UnitView,
    WebsiteInformationView,
    CoresAndUnitView,
)

urlpatterns = [
    path("faq/", FaqView.as_view(), name="faq-list-create"),
    path("faq/<int:pk>/", FaqView.as_view(), name="faq-detail"),
    path("unit/", UnitView.as_view(), name="unit-list-create"),
    path("unit/<int:pk>/", UnitView.as_view(), name="unit-detail"),
    path("core/", CoreView.as_view(), name="core-list-create"),
    path("core/<int:pk>/", CoreView.as_view(), name="core-detail"),
    path("core/<int:pk>/units/", CoreUnitsView.as_view(), name="core-units"),
    path("cores-units/", CoresAndUnitView.as_view(), name='cores-units-list'),
    path("area-of-duty/", AreaOfDutyView.as_view(), name="area_of_duty-list-create"),
    path(
        "area-of-duty/<int:pk>/", AreaOfDutyView.as_view(), name="area_of_duty-detail"
    ),
    path(
        "type-of-service/",
        TypeOfServiceView.as_view(),
        name="type_of_service-list-create",
    ),
    path(
        "type-of-service/<int:pk>/",
        TypeOfServiceView.as_view(),
        name="type_of_service-detail",
    ),
    path("popup/", PopupView.as_view(), name="popup-list-create"),
    path("popup/<int:pk>/", PopupView.as_view(), name="popup-detail"),
    path(
        "popup/<int:pk>/increment_click/",
        PopupIncrementClickView.as_view(),
        name="popup-increase-click",
    ),
    path(
        "popup/<int:pk>/increment_visualization/",
        PopupIncrementVisualizationView.as_view(),
        name="popup-increase-visualization",
    ),
    path("tag/", TagView.as_view(), name="tag-list-create"),
    path("tag/<int:pk>/", TagView.as_view(), name="tag-detail"),
    path(
        "area-of-activity/",
        AreaOfActivityView.as_view(),
        name="area_of_activity-list-create",
    ),
    path(
        "area-of-activity/<int:pk>/",
        AreaOfActivityView.as_view(),
        name="area_of_activity-detail",
    ),
    path(
        "website-information/",
        WebsiteInformationView.as_view(),
        name="website_information-list-create-detail",
    ),
    path("social-media/", SocialMediaView.as_view(), name="social_media-list-create"),
    path(
        "social-media/<int:pk>/", SocialMediaView.as_view(), name="social_media-detail"
    ),
    path(
        "email-website/", EmailWebsiteView.as_view(), name="email-website-list-create"
    ),
    path(
        "email-website/<int:pk>/",
        EmailWebsiteView.as_view(),
        name="email-website-detail",
    ),
    path(
        "authors/<str:model_name>/", AuthorsByModel.as_view(), name="authors-by-model"
    ),
    path("news/", NewsView.as_view(), name="news-list-create"),
    path("news/<int:pk>/", NewsView.as_view(), name="news-detail"),
    path("news/<slug:slug>/", NewsView.as_view(), name="news-detail"),
    path(
        "card-register/", CardRegisterView.as_view(), name="card_register-list-create"
    ),
    path(
        "card-register/<int:pk>/",
        CardRegisterView.as_view(),
        name="card_register-detail",
    ),
    path(
        "card-register/<slug:slug>/",
        CardRegisterView.as_view(),
        name="card_register-detail",
    ),
    path(
        "news-gallery/", NewsGalleryImageView.as_view(), name="news_gallery-list-create"
    ),
    path(
        "news-gallery/<int:pk>/",
        NewsGalleryImageView.as_view(),
        name="news_gallery-detail",
    ),
    path(
        "news-attachment/",
        NewsAttachmentView.as_view(),
        name="news_attachment-list-create",
    ),
    path(
        "news-attachment/<int:pk>/",
        NewsAttachmentView.as_view(),
        name="news_attachment-detail",
    ),
    path("cards/", CardsView.as_view(), name="cards-list-create"),
    path("cards/<int:pk>/", CardsView.as_view(), name="cards-detail"),
    path("page/", PageView.as_view(), name="page-list-create"),
    path("page/<int:pk>/", PageView.as_view(), name="page-detail"),
    path("posters/", PostersView.as_view(), name="posters-list-create"),
    path("posters/<int:pk>/", PostersView.as_view(), name="posters-detail"),
    path("posters/<slug:slug>/", PostersView.as_view(), name="posters-detail-slug"),
    path("modules/category/", CategoryView.as_view(), name="category-list-create"),
    path(
        "modules/category/<int:pk>/", CategoryView.as_view(), name="category-detail"
    ),
    path(
        "modules/sub-category/",
        SubcategoryView.as_view(),
        name="sub_category-list-create",
    ),
    path(
        "modules/sub-category/<int:pk>/",
        SubcategoryView.as_view(),
        name="sub_category-detail",
    ),
    path("modules/records/", RecordsView.as_view(), name="records-list-create"),
    path("modules/records/<int:pk>/", RecordsView.as_view(), name="records-detail"),
    path("banner/", BannerView.as_view(), name="banner-list-create"),
    path("banner/<int:pk>/", BannerView.as_view(), name="banner-detail"),
    path("container/", ContainerView.as_view(), name="container-list-create"),
    path("container/<int:pk>/", ContainerView.as_view(), name="container-detail"),
    path(
        "service-buttons/",
        ServiceButtonsView.as_view(),
        name="service_buttons-list-create",
    ),
    path(
        "service-buttons/<int:pk>/",
        ServiceButtonsView.as_view(),
        name="service_buttons-detail",
    ),
    path(
        "quick-access-buttons/",
        QuickAccessButtonsView.as_view(),
        name="quick_access_buttons-list-create",
    ),
    path(
        "quick-access-buttons/<int:pk>/",
        QuickAccessButtonsView.as_view(),
        name="quick_access_buttons-detail",
    ),
    path("header/", HeaderView.as_view(), name="header-list-create"),
    path("header/<int:pk>/", HeaderView.as_view(), name="header-detail"),
]
