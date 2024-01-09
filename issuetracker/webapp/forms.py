from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets
from .models import Status, Type, Task, Project


class TaskForm(forms.ModelForm):
    summary = forms.CharField(max_length=300, label='Заголовок')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Полное_описание')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус')
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label='Тип',
                                           widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'types']
        widgets = {
            'types': forms.CheckboxSelectMultiple
        }
        error_messages = {
            'description': {
                'required': 'Пожалуйста, введите полное описание'
            },
            'status': {
                'required': 'Пожалуйста, выберите статус'
            }
        }

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if any(word in summary.lower() for word in ['бля', 'нахуй', 'манда']):
            raise forms.ValidationError('Недопустимые слова в заголовке')
        return summary

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(char in description for char in ['!', '@', '#', '$', '%']):
            raise forms.ValidationError('Недопустимые символы в полном описании')
        return description


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProjectForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, label="Название")
    description = forms.CharField(max_length=50, required=True, label="Подробное описание")
    start_date = forms.DateField(required=True, label='Старт')
    end_date = forms.DateField(required=False, label='Окончание')

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)

        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Project
        fields = ["name", "description", "start_date", "end_date"]


class ProjectUsersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = get_user_model().objects.exclude(pk=pk)

    class Meta:
        model = Project
        fields = ("users",)
        widgets = {"users": widgets.CheckboxSelectMultiple}
