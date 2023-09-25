from django import forms
from .models import Question, Answer, Category, Image


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'category']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'})
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']