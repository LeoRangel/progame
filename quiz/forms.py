from django import forms

from quiz.models import LinkAjuda


class LinkAjudaForm(forms.ModelForm):
    class Meta:
        model = LinkAjuda
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LinkAjudaForm, self).__init__(*args, **kwargs)

        self.fields['nome'].label = ''
        self.fields['nome'].widget.attrs = {'placeholder': 'Nome'}
        self.fields['url'].label = ''
        self.fields['url'].widget.attrs = {'placeholder': 'Url'}
