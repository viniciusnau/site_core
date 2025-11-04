from copy import deepcopy
from django.utils.text import slugify
from django.db import transaction
from core.models import Page


def clean_page_data(request):
    data = request.data.copy()

    text_value = data.get("text")
    if text_value and text_value.strip() == "<p><br></p>":
        data["text"] = None

    return data


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
