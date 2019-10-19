
from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=50, verbose_name="Designation du service")
    service_abv = models.CharField(max_length=10, verbose_name='Abreviation du service')

    def __str__(self):
        return self.service_name


class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_designation = models.CharField(max_length=50, verbose_name="Designation du district")

    def __str__(self):
        return self.district_designation


class TVA(models.Model):
    tva_id = models.AutoField(primary_key=True)
    tva_rate = models.FloatField(verbose_name="Taux de TVA")

    def __str__(self):
        return str(self.tva_rate)


class Slip(models.Model):
    slip_id = models.AutoField(primary_key=True, verbose_name="Id du bordereau")
    slip_num = models.IntegerField(verbose_name='Numéro du bordereau')
    closed = models.BooleanField(default=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Service"
                                , blank=True, null=True)

    def __str__(self):
        return str(self.slip_num) + "/" + str(self.service.service_abv)


class ServiceSlip(models.Model):
    slip_id = models.AutoField(primary_key=True, verbose_name="Id du bordereau")
    slip_num = models.IntegerField(verbose_name='Numéro du bordereau')
    closed = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=1, verbose_name='Valide')

    def __str__(self):
        if self.is_valid:
            returned_val = str(self.slip_num) + "/" + 'Validation'
        else:
            returned_val = str(self.slip_num) + "/" + 'Rejet'
        return returned_val


class RejectionReason(models.Model):
    rejection_id = models.AutoField(primary_key=True)
    reason = models.CharField(max_length=100, verbose_name="Motif de rejet")

    def __str__(self):
        return self.reason


class Town(models.Model):
    town_id = models.AutoField(primary_key=True)
    town_name = models.CharField(max_length=30, verbose_name="Nom de la ville")
    postal_code = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Code postal")

    def __str__(self):
        return self.town_name


class Provider(models.Model):
    GENDER = [
        ('1', 'Madame'),
        ('2', 'Monsieur'),
        ('3', 'Mademoiselle'),
    ]

    provider_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=1, choices=GENDER, default='2', verbose_name="Genre")
    provider_last_name = models.CharField(max_length=50, verbose_name="Nom")
    provider_first_name = models.CharField(max_length=50, verbose_name="Prénom")
    provider_address = models.CharField(max_length=150, verbose_name="Addrese")
    town = models.ForeignKey(Town, on_delete=models.PROTECT, verbose_name="Ville")
    email = models.EmailField()
    fixed_phone = models.CharField(max_length=9, verbose_name="Téléphone fix")
    mobile_phone = models.CharField(max_length=10, verbose_name="Téléphone mobile")
    rib = models.CharField(max_length=20, verbose_name="RIB")
    nif = models.CharField(max_length=20, verbose_name="NIF")
    r_commerce = models.CharField(max_length=20, verbose_name="raison Comercial")

    def __str__(self):
        return self.provider_last_name.upper() + " " + self.provider_first_name.capitalize()


class Bill(models.Model):
    DECISION = [
        ('1', 'Non Traiter'),
        ('2', 'Accepter'),
        ('3', 'Refuser'),
    ]

    bill_id = models.AutoField(primary_key=True)
    bill_num = models.CharField(max_length=50, verbose_name="Numéro de facture")
    entry_date = models.DateField(auto_now=True)
    object = models.TextField(max_length=150, verbose_name="Objet")
    bill_type = models.CharField(max_length=100, verbose_name="Type de facture", blank=True)
    decision_ST = models.CharField(max_length=1, choices=DECISION, default='1')
    decision_BO = models.CharField(max_length=1, choices=DECISION, default='1')
    penalty_rate = models.FloatField(default=0, verbose_name="taux de pénalité")
    ht_amount = models.FloatField(verbose_name='Montant HT')
    other_coasts = models.FloatField(default=0, verbose_name="Autres frais")
    decision_FC = models.CharField(max_length=1, choices=DECISION, default='1')
    transfer_order = models.CharField(max_length=20, blank=True, verbose_name="Ordre de virement")
    billing_date = models.DateField(verbose_name="Date de facturation")
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, verbose_name="Fournisseur")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Service")
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="District")
    tva = models.ForeignKey(TVA, on_delete=models.PROTECT, verbose_name="Taux de TVA")
    slip = models.ForeignKey(Slip, on_delete=models.PROTECT, null=True, verbose_name="Numéro du bordereau")
    service_slip = models.ForeignKey(ServiceSlip, on_delete=models.PROTECT, null=True, verbose_name="Numéro du bordereau de service traitant")
    rejection_reasonBO = models.ManyToManyField(RejectionReason, related_name='motif1')
    rejection_reasonST = models.ManyToManyField(RejectionReason, related_name='motif2')
    rejection_reasonFC = models.ManyToManyField(RejectionReason, related_name='motif3')
    entered_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Saisie par')

    def __str__(self):
        return self.bill_num

    class Meta:
        ordering = ('-entry_date',)


class UserProfile(models.Model):
    user_auth = models.OneToOneField(User, primary_key=True, on_delete=models.PROTECT)
    mobile_phone = models.CharField(max_length=9, blank=True, verbose_name='Téléphone portable')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Service", null=True)
    service_all = models.BooleanField(default=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="District", null=True)
    district_all = models.BooleanField(default=False)
    born_date = models.DateField(verbose_name="Date de naissance", blank=True)
    years_seniority = models.IntegerField(verbose_name="Années d'ancienneté", blank=True)

    def __str__(self):
        return self.user_auth.last_name.upper() + " " + self.user_auth.first_name.capitalize()


