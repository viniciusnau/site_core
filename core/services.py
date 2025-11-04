from copy import deepcopy
from django.utils.text import slugify
from django.db import transaction
from core.models import Page, News, Posters, CardRegister


def update_path_on_page_deletion(page):
    if page.has_posters:
        Posters.objects.all().update(path=None)
    if page.has_news:
        News.objects.all().update(path=None)
    if page.card:
        page.card.path = None
        page.card.status = "not_published"
        page.card.save()
        registers = CardRegister.objects.filter(card=page.card)
        if registers:
            for register in registers:
                register.path = None
                register.save()


def clean_page_data(request):
    data = request.data.copy()

    text_value = data.get("text")
    if text_value and text_value.strip() == "<p><br></p>":
        data["text"] = None

    return data


def update_news_path(path):
    news_list = News.objects.all()
    for news in news_list:
        news.path = f'{path}/{news.slug}'
        news.save()


def update_posters_path(path):
    posters_list = Posters.objects.all()
    for poster in posters_list:
        poster.path = f'{path}/{poster.slug}'
        poster.save()


def update_pages_path(structure):
    data_copy = deepcopy(structure)
    id_list = []

    def _walk(nodes, parent_slug_path=""):
        for node in nodes:
            name = node.get("name", "")
            slug = slugify(name)
            if parent_slug_path:
                current_path = f"{parent_slug_path.rstrip('/')}/{slug}"
            else:
                current_path = f"/{slug}" if slug else ""

            if current_path and not current_path.startswith("/"):
                current_path = "/" + current_path.lstrip("/")

            page_info = node.get("page")
            if isinstance(page_info, dict) and page_info.get("id"):
                page_id = page_info["id"]
                try:
                    with transaction.atomic():
                        page_obj = Page.objects.select_for_update().get(id=page_id)
                        if page_obj.has_news:
                            update_news_path(current_path)
                        if page_obj.has_posters:
                            update_posters_path(current_path)
                        id_list.append(page_id)
                        page_obj.path = current_path
                        page_obj.status = "published"
                        page_obj.save(update_fields=["path", "status"])
                        node.setdefault("page", {})["path"] = current_path
                except Page.DoesNotExist:
                    node["page"] = None
            else:
                if isinstance(page_info, dict):
                    node.setdefault("page", {})["path"] = page_info.get("path")

            children = node.get("children") or []
            if children:
                _walk(children, current_path)

    _walk(data_copy, "")
    Page.objects.exclude(id__in=id_list).update(status="not_published", path=None)
    return data_copy
