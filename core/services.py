def clean_page_data(request):
    data = request.data.copy()

    text_value = data.get("text")
    if text_value and text_value.strip() == "<p><br></p>":
        data["text"] = None

    return data

def update_pages_path(data):
    print(data)
