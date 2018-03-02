from django import forms

class UploadFileForm(forms.Form):
    upload_title = forms.CharField(max_length=100)
    upload_file = forms.FileField()
