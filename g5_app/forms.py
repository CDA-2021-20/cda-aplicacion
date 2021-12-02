from django import forms
from .models import CsvFileUpload


class CsvForm(forms.ModelForm):
    csv_file = forms.FileField()

    class Meta:
        model = CsvFileUpload
        fields = ["csv_file"]
