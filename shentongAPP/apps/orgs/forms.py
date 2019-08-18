from django import forms
from operations.models import UserAsk
import re


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'phone', 'course']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        regex_phone = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        P = re.compile(regex_phone)
        if P.match(phone):
            return phone
        else:
            raise forms.ValidationError("手机号码格式不正确", code="phone_invalid")
