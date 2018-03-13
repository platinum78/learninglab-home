from django import forms

""" DO NOT TOUCH THIS PART """

class UploadFileForm(forms.Form):
    upload_title = forms.CharField(max_length=100)
    upload_file = forms.FileField()
