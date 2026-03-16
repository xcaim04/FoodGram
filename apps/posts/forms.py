from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'food_name', 'caption', 'location', 'category']
        widgets = {
            'food_name': forms.TextInput(attrs={
                'placeholder': '¿Cómo se llama este plato?',
            }),
            'caption': forms.Textarea(attrs={
                'placeholder': 'Cuéntanos sobre esta comida, la receta, dónde la probaste...',
                'rows': 4,
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Restaurante, ciudad o país',
            }),
            'image': forms.FileInput(attrs={
                'accept': 'image/*',
            }),
        }
        labels = {
            'food_name': 'Nombre del plato',
            'caption': 'Descripción',
            'location': 'Ubicación',
            'category': 'Categoría',
            'image': 'Foto del plato',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('La imagen no puede superar los 10 MB.')
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Añade un comentario...',
                'autocomplete': 'off',
            }),
        }
        labels = {'text': ''}
