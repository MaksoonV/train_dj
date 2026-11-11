from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Проверяет ввод и умеет сохранять задачу в базу."""
    class Meta:
        model = Task
        fields = ["title"]
        widgets = {"title": forms.TextInput(attrs={
            "placeholder": "Например: разобраться с views.py",
            "autocomplete": "off",
        })}
