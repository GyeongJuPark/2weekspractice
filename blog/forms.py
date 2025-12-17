from django import forms
from .models import Post, Comment, Category, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '내용을 입력하세요'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'category': '카테고리',
            'tags': '태그',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '댓글을 입력하세요'
            }),
        }
        labels = {
            'content': '',
        }
