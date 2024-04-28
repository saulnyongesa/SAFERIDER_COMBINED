from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from mapbox import Geocoder

from base.forms import *
from base.models import *


# Create your views here.
@login_required(login_url='sign-in-url')
def dashboard(request):
    user = User.objects.get(id=request.user.id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin-dashboard-url')
    else:
        user = User.objects.get(id=request.user.id)
        stage = Stage.objects.get(id=user.stage_id)
        members = User.objects.filter(stage_id=user.stage_id, is_staff=False, is_superuser=False)
        context = {
            "emergency_count": emergency_count,
            'members': members,
            'stage': stage,
        }
        return render(request, 'other/pg/index.html', context)


@login_required(login_url='sign-in-url')
def emergency_contacts(request):
    user = User.objects.get(id=request.user.id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    stage = Stage.objects.get(id=user.stage_id)
    contacts = EmergencyContact.objects.filter(name__stage_id=stage.id)
    context = {
        "emergency_count": emergency_count,
        "user": user,
        "contacts": contacts,
    }
    return render(request, 'other/auth/emergency_contacts.html', context)


@login_required(login_url='sign-in-url')
def emergency_contact_add(request):
    user = User.objects.get(id=request.user.id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    members = User.objects.filter(stage_id=user.stage_id)
    if request.method == 'POST':
        member = request.POST.get('member').upper()
        member = User.objects.get(id=member)
        try:
            if EmergencyContact.objects.get(name=member):
                messages.error(request, 'Member already added as emergency contact')
                return redirect('emergency-contact-add-url')
        except EmergencyContact.DoesNotExist:
            EmergencyContact.objects.create(
                name=member,
            )
            member.is_emergency_contact = True
            member.save()
            messages.success(request, 'Member added successfully as emergency contact')
            return redirect('emergency-contacts-url')

    context = {
        "emergency_count": emergency_count,
        "members": members,
    }
    return render(request, 'other/auth/emergency_contact-add.html', context)


@login_required(login_url='sign-in-url')
def emergency_contact_remove(request, pk):
    user = User.objects.get(id=request.user.id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    contact = EmergencyContact.objects.get(id=pk)
    member = User.objects.get(id=contact.name_id)
    if request.method == 'POST':
        member.is_emergency_contact = False
        member.save()
        contact.delete()
        messages.success(request, "Contact remove successfully")
        return redirect('emergency-contacts-url')
    context = {
        "emergency_count": emergency_count,
        "contact": contact,
    }
    return render(request, 'other/auth/emergency_contact_remove.html', context)


@login_required(login_url='sign-in-url')
def stage_edit(request):
    user = User.objects.get(id=request.user.id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    stage = Stage.objects.get(id=user.stage_id)
    form = StageForm(instance=stage)
    if request.method == 'POST':
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            messages.success(request, "You updated stage details")
            return redirect('dashboard-url')
    context = {
        "emergency_count": emergency_count,
        "form": form,
    }
    return render(request, 'other/auth/stage-edit.html', context)


@login_required(login_url='sign-in-url')
def member_view(request, pk):
    member = User.objects.get(id=pk)
    emergency_count = Emergency.objects.filter(sender__stage_id=member.stage_id, is_read=False)
    context = {
        "emergency_count": emergency_count,
        "member": member,
    }
    return render(request, 'other/auth/member-view.html', context)


@login_required(login_url='sign-in-url')
def member_edit(request, pk):
    member = User.objects.get(id=pk)
    emergency_count = Emergency.objects.filter(sender__stage_id=member.stage_id, is_read=False)
    form = UserForm(instance=member)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=member)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['second_name'] = cleaned_data[
                'second_name'].upper()
            form.save()
            messages.success(request, "You updated member profile")
            return redirect('dashboard-url')
    context = {
        "emergency_count": emergency_count,
        "form": form,
        "member": member,
    }
    return render(request, 'other/auth/member-edit.html', context)


@login_required(login_url='sign-in-url')
def member_add(request):
    user = User.objects.get(id=request.user.id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    genders = Gender.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('firstname').upper()
        second_name = request.POST.get('second_name').upper()
        last_name = request.POST.get('lastname').upper()
        phone = request.POST.get('phone')
        id_number = request.POST.get('id')
        email = request.POST.get('email').lower()
        gender = request.POST.get('gender')
        motorbike_number = request.POST.get('bike_number').upper()
        try:
            if User.objects.get(username=email):
                messages.error(request, 'Email already registered')
            elif User.objects.get(phone_number=phone):
                messages.error(request, 'Phone already registered')
            elif User.objects.get(username=email) and User.objects.get(phone_number=phone):
                messages.error(request, 'Email and phone already registered')
        except User.DoesNotExist:
            user = User.objects.get(id=request.user.id)
            stage = Stage.objects.get(id=user.stage_id)
            gender = Gender.objects.get(id=gender)
            hashed_password = make_password(id_number)
            User.objects.create(
                first_name=first_name,
                second_name=second_name,
                last_name=last_name,
                username=phone,
                phone_number=phone,
                id_number=id_number,
                gender=gender,
                email=email,
                stage=stage,
                motorbike_reg_number=motorbike_number,
                password=hashed_password,
            )
            messages.success(request, 'Member added successfully')
            return redirect('dashboard-url')

    context = {
        "emergency_count": emergency_count,
        "genders": genders,
    }
    return render(request, 'other/auth/member-add.html', context)


# USER CREATION AND AUTH FUN
def sign_up(request):
    genders = Gender.objects.all()
    stages = Stage.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('firstname').upper()
        second_name = request.POST.get('second_name').upper()
        last_name = request.POST.get('lastname').upper()
        phone = request.POST.get('phone')
        id_number = request.POST.get('id')
        email = request.POST.get('email').lower()
        gender = request.POST.get('gender')
        stage = request.POST.get('stage')
        motorbike_number = request.POST.get('bike_number').upper()

        if User.objects.filter(username=email):
            messages.error(request, 'Email already registered')
        elif User.objects.filter(phone_number=phone):
            messages.error(request, 'Phone already registered')
        elif User.objects.filter(username=email) and User.objects.get(phone_number=phone):
            messages.error(request, 'Email and phone already registered')
        elif not StageAdmin.objects.filter(id_number=id_number):
            messages.error(request,
                           "You're not allowed to register as stage admin-site. Please contact system admin-site")
        else:
            stage = Stage.objects.get(id=stage)
            gender = Gender.objects.get(id=gender)
            hashed_password = make_password(id_number)
            User.objects.create(
                first_name=first_name,
                second_name=second_name,
                last_name=last_name,
                username=phone,
                phone_number=phone,
                id_number=id_number,
                gender=gender,
                email=email,
                stage=stage,
                motorbike_reg_number=motorbike_number,
                password=hashed_password,
                is_admin=True
            )
            messages.success(request, 'Account created successfully')
            return redirect('sign-in-url')

    context = {
        "genders": genders,
        "stages": stages,
    }
    return render(request, 'other/auth/sign-up.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        messages.success(request, "You're Logged us " + request.user.username)
        return redirect('dashboard-url')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in")
            if user.is_staff or user.is_superuser:
                return redirect('admin-dashboard-url')
            else:
                return redirect('dashboard-url')
        elif User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('sign-in-url')

    return render(request, 'other/auth/sign-in.html')


@login_required(login_url='sign-in-url')
def sign_out(request):
    logout(request)
    return redirect('sign-in-url')


@login_required(login_url='sign-in-url')
def my_profile(request):
    user = User.objects.get(username=request.user.username)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    context = {
        "emergency_count": emergency_count,
        "user": user,
    }
    return render(request, 'other/auth/profile.html', context)


@login_required(login_url='sign-in-url')
def user_edit(request):
    user = User.objects.get(username=request.user.username)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['second_name'] = cleaned_data[
                'second_name'].upper()
            form.save()
            messages.success(request, "You updated your profile")
            return redirect('profile-url')
    context = {
        "emergency_count": emergency_count,
        "form": form,
    }
    return render(request, 'other/auth/user-edit.html', context)


def emergencies(request):
    user = User.objects.get(id=request.user.id)
    emergency = Emergency.objects.filter(sender__stage_id=user.stage_id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    context = {
        "emergency_count": emergency_count,
        "emergencies": emergency
    }
    return render(request, 'other/auth/emergencies.html', context)


def emergency_read(request, pk):
    emergency_message_read = Emergency.objects.get(id=pk)
    emergency_message_read.is_read = True
    emergency_message_read.save()

    return redirect('emergencies-url')


def emergency_view(request, pk):
    emergency = Emergency.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    emergency.is_read = True
    emergency.save()
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    context = {
        "emergency_count": emergency_count,
        "emergency": emergency,
        "latitude": emergency.lat,
        "longitude": emergency.lon,
    }
    return render(request, 'other/auth/emergency-view.html', context)


def map_view(request, pk):
    emergency = Emergency.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    emergency_count = Emergency.objects.filter(sender__stage_id=user.stage_id, is_read=False)
    mapbox_access_token = 'sk.eyJ1Ijoic2F1bG55b25nZXNhIiwiYSI6ImNsdmZvOGNmejA4dHAya25wZHl5cTU1NnAifQ.YnOo95SyP0EE8CdP0r8VMw'
    context = {
        "emergency_count": emergency_count,
        "emergency": emergency,
        "latitude": emergency.lat,
        "longitude": emergency.lon,
        "mapbox_access_token": mapbox_access_token
    }
    return render(request, 'other/auth/map.html', context)


def get_address(latitude, longitude):
    geocoder = Geocoder(access_token='sk.eyJ1Ijoic2F1bG55b25nZXNhIiwiYSI6ImNsdmZvOGNmejA4dHAya25wZHl5cTU1NnAifQ'
                                     '.YnOo95SyP0EE8CdP0r8VMw')
    response = geocoder.reverse(lon=longitude, lat=latitude)
    if response.status_code == 200:
        data = response.json()
        address = data['features'][0]['place_name']
        return address
    else:
        return None

