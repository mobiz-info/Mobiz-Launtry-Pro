from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Country, State, District, Area
from .forms import CountryForm, StateForm, DistrictForm, AreaForm


# =========================
# COUNTRY
# =========================

def country_list(request):
    countries = Country.objects.all().order_by('name')

    return render(
        request,
        'country/list.html',
        {'countries': countries}
    )


def country_create(request):
    form = CountryForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Country created successfully.')
        return redirect('country_list')

    return render(
        request,
        'country/create.html',
        {'form': form, 'title': 'Create Country'}
    )


def country_edit(request, id):
    country = get_object_or_404(Country, id=id)

    form = CountryForm(
        request.POST or None,
        instance=country
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Country updated successfully.')
        return redirect('country_list')

    return render(request, 'country/edit.html', {
        'form': form,
        'title': 'Edit Country'
    })
def country_delete(request, id):
    country = get_object_or_404(Country, id=id)
    country.delete()

    messages.success(request, 'Country deleted successfully.')
    return redirect('country_list')


# =========================
# STATE
# =========================

def state_list(request):
    states = State.objects.select_related(
        'country'
    ).all().order_by('name')

    return render(
        request,
        'state/list.html',
        {'states': states}
    )


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import State
from .forms import StateForm


def state_create(request):
    if request.method == 'POST':
        form = StateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'State created successfully.')
            return redirect('state_list')

    else:
        form = StateForm()

    return render(
        request,
        'state/create.html',
        {
            'form': form,
            'title': 'Add State'
        }
    )

def state_edit(request, id):
    state = get_object_or_404(State, id=id)

    if request.method == 'POST':
        form = StateForm(request.POST, instance=state)

        if form.is_valid():
            form.save()
            messages.success(request, 'State updated successfully.')
            return redirect('state_list')

    else:
        form = StateForm(instance=state)

    return render(
        request,
        'state/edit.html',
        {
            'form': form,
            'title': 'Edit State'
        }
    )

def state_delete(request, id):
    state = get_object_or_404(State, id=id)
    state.delete()

    messages.success(request, 'State deleted successfully.')

    return redirect('state_list')

def state_list(request):
    states = State.objects.select_related('country').all()

    return render(
        request,
        'state/list.html',
        {
            'states': states
        }
    )

# =========================
# DISTRICT
# =========================

def district_list(request):
    districts = District.objects.select_related(
        'state',
        'state__country'
    ).all().order_by('name')

    return render(
        request,
        'district/list.html',
        {'districts': districts}
    )


def district_create(request):
    form = DistrictForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'District created successfully.')
        return redirect('district_list')

    return render(
        request,
        'district/create.html',
        {
            'form': form,
            'title': 'Create District'
        }
    )


def district_edit(request, id):
    district = get_object_or_404(District, id=id)

    form = DistrictForm(
        request.POST or None,
        instance=district
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'District updated successfully.')
        return redirect('district_list')

    return render(
        request,
        'district/create.html',
        {
            'form': form,
            'title': 'Edit District'
        }
    )


def district_delete(request, id):
    district = get_object_or_404(District, id=id)
    district.delete()

    messages.success(request, 'District deleted successfully.')
    return redirect('district_list')


# =========================
# AREA
# =========================

def area_list(request):
    areas = Area.objects.select_related(
        'district',
        'district__state',
        'district__state__country'
    ).all().order_by('name')

    return render(request, 'area/list.html', {
        'areas': areas
    })


def area_create(request):
    form = AreaForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Area created successfully.')
        return redirect('area_list')

    return render(
        request,
        'area/create.html',
        {
            'form': form,
            'title': 'Create Area'
        }
    )


def area_edit(request, id):
    area = get_object_or_404(Area, id=id)
    form = AreaForm(request.POST or None, instance=area)

    if form.is_valid():
        form.save()
        messages.success(request, 'Area updated successfully.')
        return redirect('area_list')

    return render(request, 'area/edit.html', {
        'form': form,
        'title': 'Edit Area'
    })
def area_delete(request, id):
    area = get_object_or_404(Area, id=id)
    area.delete()

    messages.success(request, 'Area deleted successfully.')
    return redirect('area_list')