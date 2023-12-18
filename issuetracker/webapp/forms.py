from django import forms

from .models import Status, Type, Task


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

