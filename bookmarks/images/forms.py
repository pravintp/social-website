from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from urllib.request import urlopen

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title", "url", "description", "user")
        widgets = {"user": forms.HiddenInput()}

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not match valid image extensions."
            )
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        url = self.cleaned_data["url"]
        name = self.get_name(image.title, url)
        file = self.get_file(url)
        image.image.save(name, file, save=False)
        if commit:
            image.save()
        return image

    def get_name(self, title, url):
        extension = url.rsplit(".", 1)[1].lower()
        name = f"{slugify(title)}.{extension}"
        return name

    def get_file(self, url):
        response = urlopen(url)
        return ContentFile(response.read())
