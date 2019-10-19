from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .models import Bill, Provider, Service, Town, District, TVA, RejectionReason
from .filters import BillFilter, ProviderFilter
from .forms import BillForm, ProviderForm, ServiceForm, TownForm, DistrictForm, TVAForm, ReasonForm
from billingManager import forms, reporting
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from billingManager import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

"""
id    Group_name
1 => 'Bureau_ordre'
2 => 'Service_traitant'
3 => 'Service_finance'
4 => 'Staff'
"""


@login_required
def create_service(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        if request.POST:
            form = forms.FormCreateService(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return redirect("service_consulting")
            else:
                return HttpResponse('echec')
        else:
            form = forms.FormCreateService()
            return render(request, 'order_office/createService.html', {'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_service(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        services = Service.objects.all()
        paginator = Paginator(services, 15)  # Show 15 Service per page
        page = request.GET.get('page')
        service_list = paginator.get_page(page)
        return render(request, "serviceConsulting.html", {'object_list': service_list})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def service_delete(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        service = get_object_or_404(Service, pk=pk)
        data = dict()
        if request.method == 'POST':
            service.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            object_list = Service.objects.all()
            data['html_service_list'] = render_to_string('includes/partial_service_list.html', {
                'object_list': object_list
            })
        else:
            context = {'service': service}
            data['html_form'] = render_to_string('includes/partial_service_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def save_service_form(request, form, template_name):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                object_list = Service.objects.all()
                data['html_service_list'] = render_to_string('includes/partial_service_list.html', {
                    'object_list': object_list
                })
            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def service_update(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        service = get_object_or_404(Service, pk=pk)
        if request.method == 'POST':
            form = ServiceForm(request.POST, instance=service)
        else:
            form = ServiceForm(instance=service)
        return save_service_form(request, form, 'includes/partial_service_update.html')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def create_district(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        if request.POST:
            form = forms.FormCreateDistrict(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return redirect("district_consulting")
            else:
                return HttpResponse('echec')
        else:
            form = forms.FormCreateDistrict()
            return render(request, 'order_office/createDistrict.html', {'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_district(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        district_list = District.objects.all()
        return render(request, "districtConsulting.html", {'objects_list': district_list})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def district_delete(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        district = get_object_or_404(District, pk=pk)
        data = dict()
        if request.method == 'POST':
            district.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            object_list = District.objects.all()
            data['html_district_list'] = render_to_string('includes/partial_district_list.html',
                                                          {'object_list': object_list})
        else:
            context = {'district': district}
            data['html_form'] = render_to_string('includes/partial_district_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def save_district_form(request, form, template_name):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                object_list = District.objects.all()
                data['html_district_list'] = render_to_string('includes/partial_district_list.html',
                                                              {'object_list': object_list})
            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def district_update(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        district = get_object_or_404(District, pk=pk)
        if request.method == 'POST':
            form = DistrictForm(request.POST, instance=district)
        else:
            form = DistrictForm(instance=district)
        return save_district_form(request, form, 'includes/partial_district_update.html')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def create_town(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        if request.POST:
            form = forms.FormCreateTown(request.POST)
            if form.is_valid():
                name = form.cleaned_data['town_name']
                postal_code = form.cleaned_data['postal_code']
                new_town = models.Town(town_name=name, postal_code=postal_code)
                new_town.save()
                return redirect("town_consulting")
            else:
                return HttpResponse('echec')
        else:
            form = forms.FormCreateTown()
            return render(request, 'order_office/createTown.html', {'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_town(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        town_list = Town.objects.all()
        return render(request, "townConsulting.html", {'object_list': town_list})


@login_required
def town_delete(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        town = get_object_or_404(Town, pk=pk)
        data = dict()
        if request.method == 'POST':
            town.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            object_list = Town.objects.all()
            data['html_town_list'] = render_to_string('includes/partial_town_list.html', {
                'object_list': object_list
            })
        else:
            context = {'town': town}
            data['html_form'] = render_to_string('includes/partial_town_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def save_town_form(request, form, template_name):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                object_list = Town.objects.all()
                data['html_town_list'] = render_to_string('includes/partial_town_list.html',
                                                          {'object_list': object_list})
            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def town_update(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        town = get_object_or_404(Town, pk=pk)
        if request.method == 'POST':
            form = TownForm(request.POST, instance=town)
        else:
            form = TownForm(instance=town)
        return save_town_form(request, form, 'includes/partial_town_update.html')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def create_provider(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        if request.POST:
            form = forms.FormCreateProvider(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return redirect("create_provider")
            else:
                return HttpResponse('echec')
        else:
            form = forms.FormCreateProvider()
            return render(request, 'order_office/createProvider.html', {'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


"""
@login_required
def add_user(request):
    if request.POST:
        form = forms.FormAddUser(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            login_var = form.cleaned_data['login']
            email = form.cleaned_data['email']
            born_date = form.cleaned_data['born_date']
            mobile_phone = form.cleaned_data['mobile_phone']
            years_seniority = form.cleaned_data['years_seniority']
            password = form.cleaned_data['password']

            new_user = User.objects.create_user(username=login_var, email=email, password=password)
            new_user.last_name = last_name
            new_user.first_name = first_name
            new_user.is_active = True
            new_user_profile = models.UserProfile(user_auth=new_user, user_last_name=last_name,
                                                  user_first_name=first_name, years_seniority=years_seniority,
                                                  mobile_phone=mobile_phone, born_date=born_date)
            new_user_profile.save()
            return HttpResponse('Utilisateur Créé')
        else:
            return HttpResponse('Création echoue')
    else:
        form = forms.FormAddUser()
        return render(request, 'order_office/addUser.html', {'form': form})
"""


@login_required()
def view_bill_opened(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        bill_list = Bill.objects.filter(slip__closed=False).exclude(decision_BO='1')
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'order_office/billConsultingSlipOpened.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def view_bill_closed(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        bill_list = Bill.objects.filter(slip__closed=True)
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'order_office/billConsultingSlipClosed.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def view_bill_rejected_bo(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        bill_list = Bill.objects.filter(slip=None, decision_BO=3)
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'order_office/billConsultingSlipRejectedBO.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def bill_delete(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        bill = get_object_or_404(Bill, pk=pk)
        data = dict()
        if request.method == 'POST':
            bill.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            bill_filters = Bill.objects.filter(slip__closed=False).exclude(decision_BO='1')
            data['html_bill_list'] = render_to_string('includes/partial_bill_list_opened.html', {
                'bill_filters': bill_filters
            })
        else:
            context = {'bill': bill}
            data['html_form'] = render_to_string('includes/partial_bill_delete.html',
                                                 context,
                                                 request=request,
                                                 )
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def save_bill_form(request, form, template_name):
    groups_id = [1, 3]  # Définition des groups d'autorisation par leur ID pour eviter l'utilisation de OR logique
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                if request.user.groups.all()[0].id == 1:
                    bill_filters = Bill.objects.filter(slip__closed=False).exclude(decision_BO='1')
                    data['html_bill_list'] = render_to_string('includes/partial_bill_list_opened.html', {
                        'bill_filters': bill_filters
                    })
                if request.user.groups.all()[0].id == 3:
                    bill_filters = Bill.objects.filter(decision_FC='2')
                    data['html_bill_list'] = render_to_string('includes/partial_bill_list_opened_FC.html', {
                        'bill_filters': bill_filters
                    })
            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def bill_update(request, pk):
    groups_id = [1, 3]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        bill = get_object_or_404(Bill, pk=pk)
        if request.method == 'POST':
            form = BillForm(request.POST, instance=bill)
        else:
            form = BillForm(instance=bill)
        return save_bill_form(request, form, 'includes/partial_bill_update.html')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def view_provider(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        provider_list = Provider.objects.all()
        provider_pagination = ProviderFilter(request.GET, queryset=provider_list)
        paginator = Paginator(provider_pagination.qs, 15)  # 15 Provider in each page
        page = request.GET.get('page')
        try:
            provider_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            provider_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            provider_filters = paginator.page(paginator.num_pages)
        return render(request, 'providerConsulting.html', {'provider_filters': provider_filters,
                                                           'filter': provider_pagination,
                                                           'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def provider_delete(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        provider = get_object_or_404(Provider, pk=pk)
        data = dict()
        if request.method == 'POST':
            provider.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            provider_filters = Provider.objects.all()
            data['html_provider_list'] = render_to_string('includes/partial_provider_list.html', {
                'provider_filters': provider_filters
            })
        else:
            context = {'provider': provider}
            data['html_form'] = render_to_string('includes/partial_provider_delete.html',
                                                 context,
                                                 request=request,
                                                 )
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def save_provider_form(request, form, template_name):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                provider_filters = Provider.objects.all()
                data['html_provider_list'] = render_to_string('includes/partial_provider_list.html', {
                    'provider_filters': provider_filters
                })
            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def provider_update(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        provider = get_object_or_404(Provider, pk=pk)
        if request.method == 'POST':
            form = ProviderForm(request.POST, instance=provider)
        else:
            form = ProviderForm(instance=provider)
        return save_provider_form(request, form, 'includes/partial_provider_update.html')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def create_bill(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        if request.POST:
            form = forms.FormCreateBill(request.POST)
            if form.is_valid():
                # if {'tva_rate': tva_rate} not in models.TVA.objects.all().values('tva_rate'):
                #    tva.save()

                bill_num = form.cleaned_data['bill_num']
                bill_type = form.cleaned_data['bill_type']
                object = form.cleaned_data['object']
                billing_date = form.cleaned_data['billing_date']
                other_coasts = form.cleaned_data['other_coasts']
                provider = form.cleaned_data['provider']
                penalty_rate = form.cleaned_data['penalty_rate']
                ht_amount = form.cleaned_data['ht_amount']
                service = form.cleaned_data['service']
                district = form.cleaned_data['district']
                tva = form.cleaned_data['tva']
                entered_by = request.user
                if models.Slip.objects.filter(service=service).count() == 0:
                    new_slip = models.Slip(slip_num='1', service=service, closed=False)
                    new_slip.save()
                else:
                    slip = models.Slip.objects.filter(service=service).last()
                    if slip.closed:
                        new_slip = models.Slip(slip_num=slip.slip_num + 1, closed=False, service=service)
                        new_slip.save()
                    else:
                        new_slip = slip

                new_bill = models.Bill(bill_num=bill_num, bill_type=bill_type, object=object, billing_date=billing_date,
                                       other_coasts=other_coasts, provider=provider, penalty_rate=penalty_rate,
                                       ht_amount=ht_amount, district=district, slip=new_slip, tva=tva, service=service,
                                       entered_by=entered_by, decision_BO='2')
                new_bill.save()

                return redirect('create_bill')
            else:
                return render(request, 'order_office/createBill.html', {'form': form})

        else:
            form = forms.FormCreateBill()
            return render(request, 'order_office/createBill.html', {'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def create_tva(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        if request.POST:
            form = forms.FormCreateTVA(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return redirect("tva_consulting")
            else:
                return HttpResponse('echec')
        else:
            form = forms.FormCreateTVA()
            return render(request, 'order_office/createTva.html', {'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_tva(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        tva_list = TVA.objects.all()
        return render(request, "tvaConsulting.html", {'object_list': tva_list})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def tva_delete(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        tva = get_object_or_404(TVA, pk=pk)
        data = dict()
        if request.method == 'POST':
            tva.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            object_list = TVA.objects.all()
            data['html_tva_list'] = render_to_string('includes/partial_tva_list.html', {
                'object_list': object_list
            })
        else:
            context = {'tva': tva}
            data['html_form'] = render_to_string('includes/partial_tva_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def save_tva_form(request, form, template_name):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                object_list = TVA.objects.all()
                data['html_tva_list'] = render_to_string('includes/partial_tva_list.html', {
                    'object_list': object_list
                })
            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def tva_update(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        tva = get_object_or_404(TVA, pk=pk)
        if request.method == 'POST':
            form = TVAForm(request.POST, instance=tva)
        else:
            form = TVAForm(instance=tva)
        return save_tva_form(request, form, 'includes/partial_tva_update.html')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def create_rr(request):
    groups_id = [1, 2, 3]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        if request.POST:
            form = forms.FormCreateRejectionReason(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return redirect("reasons_consulting")
            else:
                return HttpResponse('echec')
        else:
            form = forms.FormCreateRejectionReason()
            return render(request, 'order_office/createRR.html', {'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_reason(request):
    groups_id = [1, 2, 3]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        reason_list = RejectionReason.objects.all()
        return render(request, "reasonsConsulting.html", {'object_list': reason_list})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def reason_delete(request, pk):
    groups_id = [1, 2, 3]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        reason = get_object_or_404(RejectionReason, pk=pk)
        data = dict()
        if request.method == 'POST':
            reason.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            object_list = reason.objects.all()
            data['html_reason_list'] = render_to_string('includes/partial_reason_list.html', {
                'object_list': object_list
            })
        else:
            context = {'reason': reason}
            data['html_form'] = render_to_string('includes/partial_reason_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def save_reason_form(request, form, template_name):
    groups_id = [1, 2, 3]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                object_list = RejectionReason.objects.all()
                data['html_reason_list'] = render_to_string('includes/partial_reason_list.html', {
                    'object_list': object_list
                })
            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def reason_update(request, pk):
    groups_id = [1, 2, 3]
    if request.user.groups.all()[0].id in groups_id:#Vérifier que le User à le droit de la creation
        reason = get_object_or_404(RejectionReason, rejection_id=pk)
        if request.method == 'POST':
            form = ReasonForm(request.POST, instance=reason)
        else:
            form = ReasonForm(instance=reason)
        return save_reason_form(request, form, 'includes/partial_reason_update.html')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def connexion(request):
    if request.POST:
        form = forms.FormConnection(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                if request.user.groups.all()[0].id == 1:
                    return redirect('bill_consulting_opened')
                elif request.user.groups.all()[0].id == 2:
                    return redirect('bill_consulting_not_treated_ST')
                elif request.user.groups.all()[0].id == 3:
                    return redirect('bill_consulting_not_treated_FC')
                elif request.user.groups.all()[0].id == 4:
                    return redirect('bill_consulting_closed_FC')
            else:
                return render(request, 'connexion.html', {'form': form, 'user': user})
        else:
            return render(request, 'connexion.html', {'form': form})
    else:
        form = forms.FormConnection()
        return render(request, 'connexion.html', {'form': form})


@login_required
def logout_page(request):
    logout(request)
    return redirect("connexion")


@login_required()
def reporting_pdf(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        reporting.create_pdf(pk)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def slip_edit(request):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        if request.GET:
            form = forms.FormSlipEdit(request.GET)
            if form.is_valid():
                slip = models.Slip.objects.filter(service=form.cleaned_data['service']).last()

                if (slip is not None) and (not slip.closed):
                    bills_list = models.Bill.objects.filter(slip=slip)
                    paginator = Paginator(bills_list, 15)  # Show 15 bills per page
                    page = request.GET.get('page')
                    bills = paginator.get_page(page)
                    if bills_list.filter(decision_BO='1').count() == 0:
                        slip_id = slip.slip_id
                        return render(request, 'slipEdit.html', {'form': form, 'bills': bills, 'slip_id': slip_id})
                    else:
                        return render(request, 'slipEdit.html', {'form': form, 'slip_id': 0})
                else:
                    return render(request, 'slipEdit.html', {'form': form, 'slip_id': 0})
            else:
                return render(request, 'slipEdit.html', {'form': form, 'slip_id': 0})
        else:
            form = forms.FormSlipEdit()
            return render(request, 'slipEdit.html', {'form': form, 'slip_id': 0})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def bill_treatment(request, pk):
    groups_id = [1]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        bill = models.Bill.objects.get(bill_id=pk)
        if bill.slip is None or not bill.slip.closed:
            if request.GET:
                form = forms.FormBillTreatment(request.GET)
                if form.is_valid():
                    reasons = form.cleaned_data['rejection_reasonBO']
                    bill.rejection_reasonBO.set(reasons)
                    bill.decision_BO = '3'
                    bill.slip = None
                    bill.save()
                    return redirect('bill_consulting_rejected_BO')
                else:
                    return render(request, 'order_office/billTreatmentBO.html', {'bill': bill, 'form': form})
            else:
                form = forms.FormBillTreatment()
                return render(request, 'order_office/billTreatmentBO.html', {'bill': bill, 'form': form})
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def bo_treatment(request, pk):
    if request.user.groups.all()[0].id == 1:  # Vérifier que le User à le droit de creation
        bill = models.Bill.objects.get(bill_id=pk)
        if not bill.slip.closed or bill.slip is None:
            reasons = bill.rejection_reasonBO
            if reasons.count() == 0:
                pass
            else:
                for r_r in bill.rejection_reasonBO:
                    bill.rejection_reasonBO.remove(r_r)
            bill.save()
            return redirect('bill_consulting_not_treated')
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Les Facture qui sont acceptées par le BO, et SLIP_CLOSED=TRUE et pas encore traitées par le ST
def view_bill_not_treated_st(request):
    if request.user.groups.all()[0].id == 2:  # Vérifier que le User à le droit de creation
        user_profile = models.UserProfile.objects.get(user_auth=request.user)
        if user_profile.service_all:
            if user_profile.district_all:
                bill_list = Bill.objects.filter(decision_ST='1', slip__closed=True)
            else:
                bill_list = Bill.objects.filter(decision_ST='1', slip__closed=True, district=user_profile.district)
        else:
            if user_profile.district_all:
                bill_list = Bill.objects.filter(decision_ST='1', slip__closed=True, service=user_profile.service)
            else:
                bill_list = Bill.objects.filter(decision_ST='1', slip__closed=True, service=user_profile.service,
                                                district=user_profile.district)
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'traiting_service/billConsultingNotTreatedST.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_bill_opened_st(request):
    if request.user.groups.all()[0].id == 2:  # Vérifier que le User à le droit de creation
        user_profile = models.UserProfile.objects.get(user_auth=request.user)
        if user_profile.service_all:
            if user_profile.district_all:
                bill_list = Bill.objects.filter(service_slip__closed=False)
            else:
                bill_list = Bill.objects.filter(service_slip__closed=False, district=user_profile.district)
        else:
            if user_profile.district_all:
                bill_list = Bill.objects.filter(service_slip__closed=False, service=user_profile.service)
            else:
                bill_list = Bill.objects.filter(service_slip__closed=False, service=user_profile.service,
                                                district=user_profile.district)
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'traiting_service/billConsultingServiceSlipOpenedST.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Afficher les factures qui sont acceptées par le ST et sont Bordereau Fermée
def view_bill_closed_st(request):
    if request.user.groups.all()[0].id == 2:  # Vérifier que le User à le droit de creation
        user_profile = models.UserProfile.objects.get(user_auth=request.user)
        if user_profile.service_all:
            if user_profile.district_all:
                bill_list = Bill.objects.filter(service_slip__closed=True)
            else:
                bill_list = Bill.objects.filter(service_slip__closed=True, district=user_profile.district)
        else:
            if user_profile.district_all:
                bill_list = Bill.objects.filter(service_slip__closed=True, service=user_profile.service)
            else:
                bill_list = Bill.objects.filter(service_slip__closed=True, service=user_profile.service,
                                                district=user_profile.district)
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'traiting_service/billConsultingServiceSlipClosedST.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def bill_treatment_st(request, pk):
    if request.user.groups.all()[0].id == 2:  # Vérifier que le User à le droit de creation
        user_profile = models.UserProfile.objects.get(user_auth=request.user)
        bill = models.Bill.objects.get(bill_id=pk)
        if (user_profile.service_all and user_profile.district_all) or (user_profile.service_all and bill.district == user_profile.district)\
                or (user_profile.district_all and bill.service == user_profile.service) \
                or (bill.service == user_profile.service and bill.district == user_profile.district):
            if request.GET:
                form = forms.FormBillTreatmentST(request.GET)
                if form.is_valid():
                    reasons = form.cleaned_data['rejection_reasonST']
                    bill.rejection_reasonST.set(reasons)
                    bill.decision_ST = '3'
                    bill.service_slip = None
                    bill.save()
                    return redirect('bill_consulting_not_treated_ST')
                else:
                    return render(request, 'traiting_service/billTreatmentST.html', {'bill': bill, 'form': form})
            else:
                form = forms.FormBillTreatmentST()
                return render(request, 'traiting_service/billTreatmentST.html', {'bill': bill, 'form': form})
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def st_treatment(request, pk):
    if request.user.groups.all()[0].id == 2:  # Vérifier que le User à le droit de creation
        bill = models.Bill.objects.get(bill_id=pk)
        user_profile = models.UserProfile.objects.get(user_auth=request.user)
        if (user_profile.service_all and user_profile.district_all) or (user_profile.service_all and bill.district == user_profile.district)\
                or (user_profile.district_all and bill.service == user_profile.service) \
                or (bill.service == user_profile.service and bill.district == user_profile.district):
            if models.ServiceSlip.objects.filter(is_valid=True).count() == 0:
                new_service_slip = models.ServiceSlip(slip_num='1', is_valid=True, closed=False)
                new_service_slip.save()
            else:
                service_slip = models.ServiceSlip.objects.filter(is_valid=True).last()
                if service_slip.closed:
                    new_service_slip = models.ServiceSlip(slip_num=service_slip.slip_num + 1, closed=False, is_valid=True)
                    new_service_slip.save()
                else:
                    new_service_slip = service_slip

            bill.service_slip = new_service_slip
            bill.decision_ST = '2'

            reasons = bill.rejection_reasonST

            if reasons.count() == 0:
                pass
            else:
                for r_r in bill.rejection_reasonST:
                    bill.rejection_reasonST.remove(r_r)

            bill.save()
            return redirect('bill_consulting_not_treated_ST')
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_bill_not_treated_fc(request):
    if request.user.groups.all()[0].id == 3:  # Vérifier que le User à le droit de creation
        bill_list = Bill.objects.filter(decision_FC='1', service_slip__closed=True).exclude(slip=None)
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'Financial_Service/billConsultingNotTreatedFC.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_bill_opened_fc(request):
    if request.user.groups.all()[0].id == 3:  # Vérifier que le User à le droit de creation
        bill_list = Bill.objects.filter(decision_FC='2', transfer_order='')
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'Financial_Service/billConsultingServiceSlipOpenedFC.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def view_bill_closed_fc(request):
    groups_id = [3, 4]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        bill_list = Bill.objects.exclude(transfer_order="")
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  #15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'Financial_Service/billConsultingServiceSlipClosedFC.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def bill_treatment_fc(request, pk):
    if request.user.groups.all()[0].id == 3:  # Vérifier que le User à le droit de creation
        bill = models.Bill.objects.get(bill_id=pk)
        if request.GET:
            form = forms.FormBillTreatmentFC(request.GET)
            if form.is_valid():
                reasons = form.cleaned_data['rejection_reasonFC']
                bill.rejection_reasonFC.set(reasons)
                bill.decision_FC = '3'
                bill.save()
                return redirect('bill_consulting_not_treated_FC')
            else:
                return render(request, 'Financial_Service/billTreatmentFC.html', {'bill': bill, 'form': form})
        else:
            form = forms.FormBillTreatmentFC()
            return render(request, 'Financial_Service/billTreatmentFC.html', {'bill': bill, 'form': form})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def fc_treatment(request, pk):
    if request.user.groups.all()[0].id == 3:  # Vérifier que le User à le droit de creation
        bill = models.Bill.objects.get(bill_id=pk)
        bill.decision_FC = '2'

        reasons = bill.rejection_reasonFC

        if reasons.count() == 0:
            pass
        else:
            for r_r in bill.rejection_reasonFC:
                bill.rejection_reasonFC.remove(r_r)

        bill.save()
        return redirect('bill_consulting_not_treated_FC')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def view_all_bill(request):
    groups_id = [3, 4]
    if request.user.groups.all()[0].id in groups_id:  # Vérifier que le User à le droit de creation
        bill_list = Bill.objects.all()
        bill_pagination = BillFilter(request.GET, queryset=bill_list)
        paginator = Paginator(bill_pagination.qs, 15)  # 15 Bills in each page
        page = request.GET.get('page')
        try:
            bill_filters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            bill_filters = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            bill_filters = paginator.page(paginator.num_pages)
        return render(request, 'staff/billConsultingAll.html',
                      {'bill_filters': bill_filters, 'filter': bill_pagination,
                       'page': page})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))