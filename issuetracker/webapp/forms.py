from django import forms
from .models import Task, Status, Type


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'task_types']

    status = forms.ModelChoiceField(queryset=Status.objects.all())
    task_types = forms.ModelMultipleChoiceField(queryset=Type.objects.all())


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'task_types']

    status = forms.ModelChoiceField(queryset=Status.objects.all())
    task_types = forms.ModelMultipleChoiceField(queryset=Type.objects.all())
