from django import forms
from .models import Country, State, District, Area


from django import forms
from .models import Country


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'currency_code', 'currency_symbol']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country Name'
            }),
            'currency_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Currency Code'
            }),
            'currency_symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Currency Symbol / Emblem'
            }),
        }

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['country', 'name']

        widgets = {
            'country': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State / Province / Emirate Name'
            }),
        }

class DistrictForm(forms.ModelForm):

    class Meta:
        model = District
        fields = ['state', 'name']

        widgets = {
            'state': forms.Select(attrs={
                'class': 'form-control'
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'District Name'
            }),
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['district', 'name']
        widgets = {
            'district': forms.Select(
                attrs={'class': 'area-input'}
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'area-input',
                    'placeholder': 'Enter area name'
                }
            ),
        }