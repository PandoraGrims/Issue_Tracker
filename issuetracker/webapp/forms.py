from django import forms
from .models import Status, Type


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=300, label='Заголовок')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Полное_описание')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус')
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label='Тип',
                                           widget=forms.CheckboxSelectMultiple)
