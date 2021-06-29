from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')

        if len(text) < 6:
            self._errors['text'] = self.error_class(['6 caracteres minimo'])

        return self.cleaned_data