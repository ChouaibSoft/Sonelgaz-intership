from django.contrib.auth import authenticate
from billingManager import models
from django import forms
from .models import Bill, Provider, Service, Town, District, TVA, RejectionReason


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = (
            'bill_num', 'provider', 'object', 'bill_type', 'penalty_rate', 'ht_amount', 'other_coasts', 'billing_date',
            'service', 'district', 'tva', 'transfer_order')


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = (
            'gender', 'provider_last_name', 'provider_first_name', 'provider_address', 'town', 'email', 'fixed_phone',
            'mobile_phone', 'rib', 'nif', 'r_commerce')


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            'service_name', 'service_abv')


class TownForm(forms.ModelForm):
    class Meta:
        model = Town
        fields = (
            'town_name', 'postal_code')


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = (
            'district_designation',)


class TVAForm(forms.ModelForm):
    class Meta:
        model = TVA
        fields = (
            'tva_rate',)


class ReasonForm(forms.ModelForm):
    class Meta:
        model = RejectionReason
        fields = (
            'reason',)


class FormCreateBill(forms.ModelForm):
    class Meta:
        model = models.Bill
        exclude = ('decision_ST', 'decision_FC', 'entry_date', 'rejection_reasonFC', 'slip', 'service_slip',
                   'rejection_reasonST', 'transfer_order', 'rejection_reasonBO', 'decision_BO', 'entered_by')


class FormCreateTown(forms.ModelForm):
    class Meta:
        model = models.Town
        fields = '__all__'


class FormCreateProvider(forms.ModelForm):
    class Meta:
        model = models.Provider
        fields = '__all__'


class FormCreateSlip(forms.ModelForm):
    class Meta:
        model = models.Slip
        fields = '__all__'


class FormCreateService(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'


class FormCreateDistrict(forms.ModelForm):
    class Meta:
        model = models.District
        fields = '__all__'


class FormCreateTVA(forms.ModelForm):
    class Meta:
        model = models.TVA
        fields = '__all__'


class FormCreateRejectionReason(forms.ModelForm):
    class Meta:
        model = models.RejectionReason
        fields = '__all__'


class FormAddUser(forms.Form):
    last_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    login = forms.CharField(max_length=50, label="Nom d'utilisateur")
    email = forms.EmailField(label="Email")
    born_date = forms.DateField(widget=forms.DateInput)
    mobile_phone = forms.CharField(max_length=9)
    years_seniority = forms.IntegerField()
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_bis = forms.CharField(label="Validation du mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(FormAddUser, self).clean()
        password = cleaned_data.get('password')
        password_bis = self.cleaned_data.get('password_bis')
        if password and password_bis and password != password_bis:
            raise forms.ValidationError("Passwords are not identical.")
        return cleaned_data


class FormConnection(forms.Form):
    username = forms.CharField(max_length=50, label="Nom d'utilisateur")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(FormConnection, self).clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong login or password")
        return cleaned_data


class FormSlipEdit(forms.ModelForm):
    class Meta:
        model = models.Slip
        fields = ('service',)


class FormBillTreatment(forms.ModelForm):
    class Meta:
        model = models.Bill
        fields = ('rejection_reasonBO', )


class FormBillTreatmentST(forms.ModelForm):
    class Meta:
        model = models.Bill
        fields = ('rejection_reasonST', )


class FormBillTreatmentFC(forms.ModelForm):
    class Meta:
        model = models.Bill
        fields = ('rejection_reasonFC', )