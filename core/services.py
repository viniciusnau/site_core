from django.utils.text import slugify
from core.models import Page


def clean_page_data(request):
    data = request.data.copy()

    text_value = data.get("text")
    if text_value and text_value.strip() == "<p><br></p>":
        data["text"] = None

    return data


def update_pages_path(data, parent_path=""):
    for item in data:
        name = item.get("name", "")
        page_info = item.get("page")
        children = item.get("children", [])
        current_slug = slugify(name)
        current_path = f"{parent_path}/{current_slug}".replace("//", "/")

        if isinstance(page_info, dict) and page_info.get("id"):
            page_id = page_info["id"]
            try:
                page = Page.objects.get(id=page_id)
                page.path = current_path
                page.status = "published"
                page.save(update_fields=["path", "status"])
            except Page.DoesNotExist:
                print(f"⚠️ Página com id={page_id} não encontrada")

        if children:
            update_pages_path(children, current_path)
