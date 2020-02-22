from django import forms
from .models import todos


class TodoUpdateForm(forms.ModelForm):
    dueDate = forms.DateTimeField()
    note = forms.Textarea()

    class Meta:
        model = todos
        fields = ['dueDate', 'note']
