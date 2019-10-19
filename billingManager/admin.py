from django.contrib import admin
from billingManager import models

admin.site.register(models.Bill)
admin.site.register(models.Service)
admin.site.register(models.Slip)
admin.site.register(models.Town)
admin.site.register(models.District)
admin.site.register(models.Provider)
admin.site.register(models.TVA)
admin.site.register(models.RejectionReason)
admin.site.register(models.ServiceSlip)
admin.site.register(models.UserProfile)



