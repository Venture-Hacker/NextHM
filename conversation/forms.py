from django import forms
from . models import ConversationMessage
INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-2 px-3 rounded-sm border',
                'rows': 3,  # Adjust the number of rows to make it smaller
                'style': 'width: 300px;',  # Adjust the width as needed
            })
        }