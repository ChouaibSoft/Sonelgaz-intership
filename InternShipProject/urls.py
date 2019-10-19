"""InternShipProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL_conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, reverse_lazy
from billingManager import views, models, reporting
from django.views.generic import UpdateView, DeleteView, ListView, DetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_service/', views.create_service, name='create_service'),
    path('create_district/', views.create_district, name='create_district'),
    path('create_town/', views.create_town, name='create_town'),
    path('create_provider/', views.create_provider, name='create_provider'),
    path('create_bill/', views.create_bill, name='create_bill'),
    path('create_tva/', views.create_tva, name='create_tva'),
    path('create_rr/', views.create_rr, name='create_r_r'),
    #path('add_user/', views.add_user, name='add_user'),
    path('connexion/', views.connexion, name='connexion'),
    path('logout/', views.logout_page, name='logout'),

    # Order Office

    path('bill_consulting_opened', views.view_bill_opened, name='bill_consulting_opened'),

    path('bill_consulting_rejected_BO', views.view_bill_rejected_bo, name='bill_consulting_rejected_BO'),

    path('bill_consulting_closed', views.view_bill_closed, name='bill_consulting_closed'),

    path('bill_detail/<pk>', DetailView.as_view(model=models.Bill, template_name='billDetail.html', ),
         name='bill_detail'),

    path('bill_treatment/<pk>', views.bill_treatment, name='bill_treatment'),

    path('BO_treatment/<pk>', views.bo_treatment, name='BO_treatment'),

    path('slip_edit', views.slip_edit, name='slip_edit'),

    path('reporting_BO/<pk>', views.reporting_pdf, name='reporting_BO'),

    # Treating Service

    path('bill_consulting_not_treated_ST', views.view_bill_not_treated_st, name='bill_consulting_not_treated_ST'),

    path('bill_consulting_opened_ST', views.view_bill_opened_st, name='bill_consulting_opened_ST'),

    path('bill_consulting_closed_ST', views.view_bill_closed_st, name='bill_consulting_closed_ST'),


    path('bill_treatment_ST/<pk>', views.bill_treatment_st, name='bill_treatment_ST'),

    path('ST_treatment/<pk>', views.st_treatment, name='ST_treatment'),

    #####

# Financial Service

    path('bill_consulting_not_treated_FC', views.view_bill_not_treated_fc, name='bill_consulting_not_treated_FC'),

    path('bill_consulting_opened_FC', views.view_bill_opened_fc, name='bill_consulting_opened_FC'),

    path('bill_consulting_closed_FC', views.view_bill_closed_fc, name='bill_consulting_closed_FC'),

    path('bill_treatment_FC/<pk>', views.bill_treatment_fc, name='bill_treatment_FC'),

    path('FC_treatment/<pk>', views.fc_treatment, name='FC_treatment'),

    #####

    path('bill/<pk>/delete/', views.bill_delete, name='bill_delete'),

    path('bill/<pk>/update/', views.bill_update, name='bill_update'),

    path('provider_consulting', views.view_provider, name='provider_consulting'),

    path('provider_detail/<pk>', DetailView.as_view(model=models.Provider, template_name='providerDetail.html', ),
         name='provider_detail'),

    path('provider/<pk>/delete/', views.provider_delete, name='provider_delete'),

    path('provider/<pk>/update/', views.provider_update, name='provider_update'),

    path('service_consulting', views.view_service, name='service_consulting'),

    path('service/<pk>/delete/', views.service_delete, name='service_delete'),

    path('service/<pk>/update/', views.service_update, name='service_update'),

    path('town_consulting', views.view_town, name='town_consulting'),

    path('town/<pk>/delete/', views.town_delete, name='town_delete'),

    path('town/<pk>/update/', views.town_update, name='town_update'),

    path('district_consulting', ListView.as_view(model=models.District, template_name='districtConsulting.html', ),
         name='district_consulting'),

    path('district/<pk>/delete/', views.district_delete, name='district_delete'),

    path('district/<pk>/update/', views.district_update, name='district_update'),

    path('tva_consulting', views.view_tva, name='tva_consulting'),

    path('tva/<pk>/delete/', views.tva_delete, name='tva_delete'),

    path('tva/<pk>/update/', views.tva_update, name='tva_update'),

    path('district_consulting', views.view_district, name='district_consulting'),

    path('reasons_consulting', views.view_reason, name='reasons_consulting'),

    path('reason/<pk>/delete/', views.reason_delete, name='reason_delete'),

    path('reason/<pk>/update/', views.reason_update, name='reason_update'),

# Staff

    path('bill_consulting_all', views.view_all_bill, name='bill_consulting_all'),


]
