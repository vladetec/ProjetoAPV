from django import forms
from .models import Doador, Operador, Entregador, Cobranca

class DoadorForm(forms.ModelForm):
    class Meta:
        model = Doador
        fields = '__all__'

class OperadorForm(forms.ModelForm):
    class Meta:
        model = Operador
        fields = '__all__'

class EntregadorForm(forms.ModelForm):
    class Meta:
        model = Entregador
        fields = '__all__'

class CobrancaForm(forms.ModelForm):
    class Meta:
        model = Cobranca
        fields = '__all__'