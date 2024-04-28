from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from base.forms import *
from base.models import *


# Create your views here.
@login_required(login_url='admin-sign-in-url')
def dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        stages = Stage.objects.all()
        members = User.objects.filter(is_superuser=False, is_staff=False)
        context = {
            'members': members,
            'stages': stages,
        }
        return render(request, 'admin-site/auth/index.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-sign-in-url')
def search_item(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        query = query.lower()
        try:
            member = None
            stage = None
            members = User.objects.filter(username__contains=query)
            for m in members:
                member = m
            stages = Stage.objects.filter(stage_name__contains=query)
            for s in stages:
                stage = s

            if member and member.username.lower() == query:
                member = member
                member = User.objects.get(id=member.id)
                context = {
                    "member": member,
                }
                return render(request, 'admin-site/auth/member-view.html', context)

            elif stage and stage.stage_name.lower() == query:
                stage = stage
                members = User.objects.filter(stage_id=stage.id)
                contacts = EmergencyContact.objects.filter(name__stage_id=stage.id)
                context = {
                    'stage': stage,
                    "contacts": contacts,
                    "members": members
                }
                return render(request, 'admin-site/auth/admin-stage-view.html', context)
            else:
                messages.error(request, "Result not found!")
                return redirect('admin-dashboard-url')
        except User.DoesNotExist or Stage.DoesNotExist:
            messages.error(request, "Result not found!")
            return redirect('admin-dashboard-url')
    else:
        return redirect("admin-dashboard-url")


def stage_view(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        stage = Stage.objects.get(id=pk)
        members = User.objects.filter(stage_id=stage.id)
        contacts = EmergencyContact.objects.filter(name__stage_id=stage.id)
        context = {
            'stage': stage,
            "contacts": contacts,
            "members": members
        }
        return render(request, 'admin-site/auth/admin-stage-view.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def stage_add(request):
    if request.user.is_superuser or request.user.is_staff:
        form = StageAddForm()
        if request.method == 'POST':
            form = StageAddForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Stage added")
                return redirect('admin-dashboard-url')
        context = {
            "form": form,
        }
        return render(request, 'admin-site/auth/stage-add.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def stage_edit(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        stage = Stage.objects.get(id=pk)
        form = StageForm(instance=stage)
        if request.method == 'POST':
            form = StageForm(request.POST, instance=stage)
            if form.is_valid():
                form.save()
                messages.success(request, "You updated stage details")
                return HttpResponseRedirect('/admin-site/stage/view/' + str(stage.id))
        context = {
            "form": form,
            "stage": stage,
        }
        return render(request, 'admin-site/auth/stage-edit.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def member_view(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        member = User.objects.get(id=pk)
        context = {
            "member": member,
        }
        return render(request, 'admin-site/auth/member-view.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def member_edit(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        member = User.objects.get(id=pk)
        form = UserForm(instance=member)
        if request.method == 'POST':
            form = UserForm(request.POST, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, "You updated member profile")
                return HttpResponseRedirect('/admin-site/member/profile/view/' + str(member.id))
        context = {
            "form": form,
            "member": member,
        }
        return render(request, 'admin-site/auth/member-edit.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def member_add(request):
    if request.user.is_superuser or request.user.is_staff:
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
            try:
                if User.objects.get(username=email):
                    messages.error(request, 'Email already registered')
                elif User.objects.get(phone_number=phone):
                    messages.error(request, 'Phone already registered')
                elif User.objects.get(username=email) and User.objects.get(phone_number=phone):
                    messages.error(request, 'Email and phone already registered')
            except User.DoesNotExist:
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
                )
                messages.success(request, 'Member added successfully')
                return redirect('admin-dashboard-url')

        context = {
            "genders": genders,
            "stages": stages,
        }
        return render(request, 'admin-site/auth/member-add.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def stage_member_add(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        stage = Stage.objects.get(id=pk)
        genders = Gender.objects.all()
        if request.method == 'POST':
            first_name = request.POST.get('firstname').upper()
            second_name = request.POST.get('second_name').upper()
            last_name = request.POST.get('lastname').upper()
            phone = request.POST.get('phone')
            id_number = request.POST.get('id')
            email = request.POST.get('email').lower()
            gender = request.POST.get('gender')
            is_admin = request.POST.get('is_admin')
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
                    is_admin=is_admin,
                )
                messages.success(request, 'Member added successfully')
                return HttpResponseRedirect('/admin-site/stage/view/' + str(stage.id))

        context = {
            "genders": genders,
            "stage": stage,
        }
        return render(request, 'admin-site/auth/stage-member-add.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def stage_admin(request):
    if request.user.is_superuser or request.user.is_staff:
        form = StageAdminForm()
        if request.method == 'POST':
            form = StageAdminForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "You added a stage admin. Now can create account using id provided")
                return redirect('admin-dashboard-url')
        context = {
            "form": form,
        }
        return render(request, 'admin-site/auth/stage-admin.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def emergency_contact_add(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        stage = Stage.objects.get(id=pk)
        members = User.objects.all()
        if request.method == 'POST':
            member_id = request.POST.get('member')
            member = User.objects.get(id=member_id)
            try:
                if EmergencyContact.objects.get(name=member):
                    messages.error(request, 'Member already added as emergency contact')
                    return HttpResponseRedirect('/admin-site/stage/view/' + str(member.stage_id))
            except EmergencyContact.DoesNotExist:
                e = EmergencyContact.objects.create(name=member)
                member.is_emergency_contact = True
                e.save()
                member.save()
                messages.success(request, 'Member added successfully as emergency contact')
                return HttpResponseRedirect('/admin-site/stage/view/' + str(stage.id))
        context = {
            "members": members,
            "stage": stage
        }
        return render(request, 'admin-site/auth/emergency_contact-add.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def emergency_contact_remove(request, pk):
    if request.user.is_superuser or request.user.is_staff:
        contact = EmergencyContact.objects.get(id=pk)
        member = User.objects.get(id=contact.name_id)
        if request.method == 'POST':
            member.is_emergency_contact = False
            member.save()
            contact.delete()
            messages.success(request, "Contact remove successfully")
            return HttpResponseRedirect('/admin-site/stage/view/' + str(member.stage_id))
        context = {
            "contact": contact,
        }
        return render(request, 'admin-site/auth/emergency_contact_remove.html', context)
    else:
        return redirect('dashboard-url')


# USER CREATION AND AUTH FUN
def sign_in(request):
    if request.user.is_authenticated:
        messages.success(request, "You're Logged us " + request.user.username)
        return redirect('admin-dashboard-url')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in")
            return redirect('admin-dashboard-url')
        elif User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('sign-in-url')

    return render(request, 'admin-site/auth/sign-in.html')


@login_required(login_url='admin-site-sign-in-url')
def sign_out(request):
    logout(request)
    return redirect('admin-sign-in-url')


@login_required(login_url='admin-site-sign-in-url')
def my_profile(request):
    if request.user.is_superuser or request.user.is_staff:
        user = User.objects.get(username=request.user.username)
        context = {
            "user": user,
        }
        return render(request, 'admin-site/auth/profile.html', context)
    else:
        return redirect('dashboard-url')


@login_required(login_url='admin-site-sign-in-url')
def user_edit(request):
    if request.user.is_superuser or request.user.is_staff:
        form = UserForm(instance=request.user)
        if request.method == 'POST':
            form = UserForm(request.POST, instance=request.user)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                cleaned_data['second_name'] = cleaned_data[
                    'second_name'].upper()
                form.save()
                messages.success(request, "You updated your profile")
                return redirect('admin-profile-url')
        context = {
            "form": form,
        }
        return render(request, 'admin-site/auth/user-edit.html', context)
    else:
        return redirect('dashboard-url')
