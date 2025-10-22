from django.urls import path

from core.views import (
    AreaOfActivityView,
    AreaOfDutyView,
    AuthorsByModel,
    CardsView,
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
    SocialMediaView,
    TagView,
    TypeOfServiceView,
    UnitView,
    WebsiteInformationView, CardRegisterView,
)

urlpatterns = [
    path("faq/", FaqView.as_view(), name="faq-list-create"),
    path("faq/<int:pk>/", FaqView.as_view(), name="faq-detail"),
    path("unit/", UnitView.as_view(), name="unit-list-create"),
    path("unit/<int:pk>/", UnitView.as_view(), name="unit-detail"),
    path("core/", CoreView.as_view(), name="core-list-create"),
    path("core/<int:pk>/", CoreView.as_view(), name="core-detail"),
    path("core/<int:pk>/units/", CoreUnitsView.as_view(), name="core-units"),
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
    path("card-register/", CardRegisterView.as_view(), name="card_register-list-create"),
    path("card-register/<int:pk>/", CardRegisterView.as_view(), name="card_register-detail"),
    path("card-register/<slug:slug>/", CardRegisterView.as_view(), name="card_register-detail"),
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
]
