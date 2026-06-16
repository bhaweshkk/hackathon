from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Type a message...'}),
        max_length=1000,
        label='Message'
    )


class NotificationFilterForm(forms.Form):
    unread_only = forms.BooleanField(required=False, initial=False, label='Unread only')
