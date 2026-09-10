import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import (
    Reporter, Desk, generate_next_reporter_id,
    News, NEWS_TYPE_CHOICES, NEWS_CATEGORY_CHOICES, NEWS_STATUS_CHOICES
)


# ==========================================
# Custom Auth & Role Helpers
# ==========================================
def get_base_template(user):
    if hasattr(user, 'reporter_profile'):
        return 'reporter/base_reporter.html'
    elif hasattr(user, 'desk_profile'):
        return 'desk/base_desk.html'
    return 'base.html'
def is_reporter_user(user):
    return user.is_authenticated and hasattr(user, 'reporter_profile')


def is_desk_user(user):
    return user.is_authenticated and hasattr(user, 'desk_profile')


def is_admin_user(user):
    return user.is_authenticated and not hasattr(user, 'reporter_profile') and not hasattr(user, 'desk_profile')


def admin_required(view_func):
    """
    Decorator ensuring only Admin users can access the view.
    Reporters and Desk users are redirected to their respective dashboards.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_home')
        if is_reporter_user(request.user):
            return redirect('reporter_dashboard')
        if is_desk_user(request.user):
            return redirect('desk_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def reporter_required(view_func):
    """
    Decorator ensuring only Reporter users can access the view.
    Admins are redirected to Admin Dashboard, Desk users to Desk Dashboard.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_home')
        if is_desk_user(request.user):
            return redirect('desk_dashboard')
        if not is_reporter_user(request.user):
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def desk_required(view_func):
    """
    Decorator ensuring only Desk users can access the view.
    Admins are redirected to Admin Dashboard, Reporters to Reporter Dashboard.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_home')
        if is_reporter_user(request.user):
            return redirect('reporter_dashboard')
        if not is_desk_user(request.user):
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==========================================
# Authentication Views (Admin + Reporter + Desk)
# ==========================================
def login_view(request):
    """
    Multi-Role Login View:
    1. Admin Login (Email/Username + Password)
    2. Reporter Login (Phone Number + Password)
    3. Desk Login (Phone Number + Password)
    """
    if request.user.is_authenticated:
        if is_reporter_user(request.user):
            return redirect('reporter_dashboard')
        if is_desk_user(request.user):
            return redirect('desk_dashboard')
        return redirect('dashboard')

    active_tab = request.GET.get('tab', 'admin')
    admin_error = None
    reporter_error = None
    desk_error = None

    if request.method == 'POST':
        login_type = request.POST.get('login_type', 'admin').strip()
        active_tab = login_type

        if login_type == 'admin':
            email_or_username = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            if not email_or_username or not password:
                admin_error = "Please enter both Email/Username and Password."
            else:
                # Lookup user by email or username
                matched_user = User.objects.filter(email__iexact=email_or_username).first()
                if not matched_user:
                    matched_user = User.objects.filter(username__iexact=email_or_username).first()

                user = None
                if matched_user:
                    # Prevent reporters & desk users from logging in via admin tab
                    if hasattr(matched_user, 'reporter_profile'):
                        admin_error = "This is a Reporter account. Please use the Reporter Login tab."
                    elif hasattr(matched_user, 'desk_profile'):
                        admin_error = "This is a Desk account. Please use the Desk Login tab."
                    else:
                        user = authenticate(request, username=matched_user.username, password=password)
                else:
                    user = authenticate(request, username=email_or_username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        next_url = request.GET.get('next')
                        if next_url and next_url != '/':
                            return redirect(next_url)
                        return redirect('dashboard')
                    else:
                        admin_error = "This admin account has been disabled."
                elif not admin_error:
                    admin_error = "Invalid Admin credentials. Please try again."

        elif login_type == 'reporter':
            phone = request.POST.get('phone', '').strip()
            password = request.POST.get('password', '')

            if not phone or not password:
                reporter_error = "Please enter both Phone Number/Reporter ID and Password."
            else:
                # Find reporter with phone or reporter_id (e.g. NL_1001)
                reporter = Reporter.objects.filter(
                    Q(phone_number=phone) | Q(reporter_id__iexact=phone)
                ).first()
                if not reporter:
                    reporter_error = "No Reporter account found with this Phone Number or Reporter ID."
                elif not reporter.is_active:
                    reporter_error = "Your Reporter account is currently inactive. Contact Admin."
                else:
                    user = authenticate(request, username=reporter.user.username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            return redirect('reporter_dashboard')
                        else:
                            reporter_error = "This Reporter user account has been disabled."
                    else:
                        reporter_error = "Incorrect Password. Please check and try again."

        elif login_type == 'desk':
            phone = request.POST.get('phone', '').strip()
            password = request.POST.get('password', '')

            if not phone or not password:
                desk_error = "Please enter both Phone Number and Password."
            else:
                # Find desk staff with phone
                desk = Desk.objects.filter(phone_number=phone).first()
                if not desk:
                    # Fallback lookup by email just in case
                    desk = Desk.objects.filter(email__iexact=phone).first()

                if not desk:
                    desk_error = "No Desk account found with this Phone Number."
                elif not desk.is_active:
                    desk_error = "Your Desk account is currently inactive. Contact Admin."
                else:
                    user = authenticate(request, username=desk.user.username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            return redirect('desk_dashboard')
                        else:
                            desk_error = "This Desk user account has been disabled."
                    else:
                        desk_error = "Incorrect Password. Please check and try again."

    return render(request, 'login.html', {
        'active_tab': active_tab,
        'admin_error': admin_error,
        'reporter_error': reporter_error,
        'desk_error': desk_error,
    })


def logout_view(request):
    """
    Logs out user and redirects to login.
    """
    logout(request)
    return redirect('login_home')


def reporter_logout_view(request):
    """
    Logs out reporter and redirects to login with reporter tab active.
    """
    logout(request)
    return redirect('/?tab=reporter')


def desk_logout_view(request):
    """
    Logs out desk staff and redirects to login with desk tab active.
    """
    logout(request)
    return redirect('/?tab=desk')


# ==========================================
# Admin Control Panel - Dashboard & Profile
# ==========================================
@admin_required
def dashboard_view(request):
    """
    Admin Dashboard with Reporter & Desk metrics and quick overview.
    """
    total_reporters = Reporter.objects.count()
    active_reporters = Reporter.objects.filter(is_active=True).count()
    districts_count = Reporter.objects.values('district').distinct().count()
    recent_reporters = Reporter.objects.all()[:6]

    total_desks = Desk.objects.count()
    active_desks = Desk.objects.filter(is_active=True).count()
    recent_desks = Desk.objects.all()[:6]

    total_news = News.objects.count()
    recent_news = News.objects.select_related('reporter', 'author').order_by('-created_at')[:6]

    context = {
        'active_page': 'dashboard',
        'total_reporters': total_reporters,
        'active_reporters': active_reporters,
        'districts_count': districts_count,
        'recent_reporters': recent_reporters,
        'total_desks': total_desks,
        'active_desks': active_desks,
        'recent_desks': recent_desks,
        'total_news': total_news,
        'recent_news': recent_news,
    }
    return render(request, 'dashboard.html', context)


@admin_required
def profile_view(request):
    """
    Admin Profile page.
    """
    context = {
        'active_page': 'profile',
        'admin_user': request.user,
        'total_reporters': Reporter.objects.count(),
        'total_desks': Desk.objects.count(),
    }
    return render(request, 'profile.html', context)


# ==========================================
# Reporter Management Views (Admin Control)
# ==========================================
@admin_required
def reporter_list_view(request):
    """
    Reporter List with search, district filter, and management table.
    """
    query = request.GET.get('q', '').strip()
    district_filter = request.GET.get('district', '').strip()
    status_filter = request.GET.get('status', '').strip()

    reporters = Reporter.objects.all()

    if query:
        reporters = reporters.filter(
            Q(reporter_id__icontains=query) |
            Q(name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(district__icontains=query) |
            Q(address__icontains=query)
        )

    if district_filter:
        reporters = reporters.filter(district__iexact=district_filter)

    if status_filter == 'active':
        reporters = reporters.filter(is_active=True)
    elif status_filter == 'inactive':
        reporters = reporters.filter(is_active=False)

    all_districts = Reporter.objects.values_list('district', flat=True).distinct().order_by('district')

    context = {
        'active_page': 'reporter_list',
        'reporters': reporters,
        'all_districts': all_districts,
        'query': query,
        'district_filter': district_filter,
        'status_filter': status_filter,
    }
    return render(request, 'admin/reporter_list.html', context)


@admin_required
def reporter_add_view(request):
    """
    Add New Reporter form.
    Fields: Name, Address, Phone Number, Dist Name, Reporter ID (auto/custom), Aadhar Card image, Profile image, Password & Confirm Password.
    """
    errors = {}
    form_data = {}
    next_reporter_id = generate_next_reporter_id()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        district = request.POST.get('district', '').strip()
        reporter_id = request.POST.get('reporter_id', '').strip() or next_reporter_id
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        aadhar_image = request.FILES.get('aadhar_image')
        profile_image = request.FILES.get('profile_image')

        form_data = {
            'name': name,
            'address': address,
            'phone_number': phone_number,
            'district': district,
            'reporter_id': reporter_id,
        }

        # Validation
        if not name:
            errors['name'] = "Reporter Name is required."
        if not address:
            errors['address'] = "Address is required."
        if not phone_number:
            errors['phone_number'] = "Phone Number is required."
        elif Reporter.objects.filter(phone_number=phone_number).exists() or User.objects.filter(username=phone_number).exists():
            errors['phone_number'] = "A Reporter or User with this Phone Number already exists."
        if not district:
            errors['district'] = "District Name is required."
        if reporter_id and Reporter.objects.filter(reporter_id__iexact=reporter_id).exists():
            errors['reporter_id'] = f"Reporter ID '{reporter_id}' is already registered."
        if not password:
            errors['password'] = "Password is required."
        elif len(password) < 4:
            errors['password'] = "Password should be at least 4 characters long."
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."

        if not errors:
            # 1. Create Django Auth User
            user = User.objects.create_user(
                username=phone_number,
                first_name=name,
                password=password
            )

            # 2. Create Reporter Profile
            reporter = Reporter(
                user=user,
                reporter_id=reporter_id,
                name=name,
                phone_number=phone_number,
                address=address,
                district=district,
                is_active=True
            )
            if aadhar_image:
                reporter.aadhar_image = aadhar_image
            if profile_image:
                reporter.profile_image = profile_image

            reporter.save()

            messages.success(request, f'Reporter "{reporter.name}" has been registered successfully with ID: {reporter.reporter_id}!')
            return redirect('reporter_list')

    context = {
        'active_page': 'reporter_add',
        'errors': errors,
        'form_data': form_data,
        'next_reporter_id': next_reporter_id,
    }
    return render(request, 'admin/reporter_add.html', context)


@admin_required
def reporter_detail_view(request, pk):
    """
    View Reporter full details / ID card / documents.
    """
    reporter = get_object_or_404(Reporter, pk=pk)
    context = {
        'active_page': 'reporter_list',
        'reporter': reporter,
    }
    return render(request, 'admin/reporter_view.html', context)


@admin_required
def reporter_edit_view(request, pk):
    """
    Edit existing Reporter information.
    """
    reporter = get_object_or_404(Reporter, pk=pk)
    errors = {}

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        district = request.POST.get('district', '').strip()
        reporter_id = request.POST.get('reporter_id', '').strip()
        is_active = request.POST.get('is_active') == '1'
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        profile_image = request.FILES.get('profile_image')
        aadhar_image = request.FILES.get('aadhar_image')
        remove_profile = request.POST.get('remove_profile') == '1'
        remove_aadhar = request.POST.get('remove_aadhar') == '1'

        if not name:
            errors['name'] = "Name is required."
        if not address:
            errors['address'] = "Address is required."
        if not phone_number:
            errors['phone_number'] = "Phone Number is required."
        elif Reporter.objects.filter(phone_number=phone_number).exclude(pk=reporter.pk).exists():
            errors['phone_number'] = "Another Reporter with this phone number already exists."
        if not district:
            errors['district'] = "District Name is required."
        if reporter_id and Reporter.objects.filter(reporter_id__iexact=reporter_id).exclude(pk=reporter.pk).exists():
            errors['reporter_id'] = f"Another Reporter with ID '{reporter_id}' already exists."

        if new_password:
            if len(new_password) < 4:
                errors['new_password'] = "Password must be at least 4 characters."
            if new_password != confirm_password:
                errors['confirm_password'] = "Passwords do not match."

        if not errors:
            reporter.name = name
            if reporter_id:
                reporter.reporter_id = reporter_id
            reporter.address = address
            reporter.district = district
            reporter.is_active = is_active

            # Update User username if phone changed
            user = reporter.user
            user.first_name = name
            if phone_number != reporter.phone_number:
                reporter.phone_number = phone_number
                user.username = phone_number

            if new_password:
                user.set_password(new_password)

            user.is_active = is_active
            user.save()

            if remove_profile and reporter.profile_image:
                reporter.profile_image.delete(save=False)
                reporter.profile_image = None
            elif profile_image:
                reporter.profile_image = profile_image

            if remove_aadhar and reporter.aadhar_image:
                reporter.aadhar_image.delete(save=False)
                reporter.aadhar_image = None
            elif aadhar_image:
                reporter.aadhar_image = aadhar_image

            reporter.save()
            messages.success(request, f'Reporter "{reporter.name}" was updated successfully.')
            return redirect('reporter_list')

    context = {
        'active_page': 'reporter_list',
        'reporter': reporter,
        'errors': errors,
    }
    return render(request, 'admin/reporter_edit.html', context)


@admin_required
def reporter_delete_view(request, pk):
    """
    Delete Reporter and linked auth User.
    """
    reporter = get_object_or_404(Reporter, pk=pk)
    name = reporter.name
    
    # Delete images
    if reporter.profile_image:
        reporter.profile_image.delete(save=False)
    if reporter.aadhar_image:
        reporter.aadhar_image.delete(save=False)
    
    # Deleting user will cascade delete reporter
    user = reporter.user
    user.delete()

    messages.success(request, f'Reporter "{name}" has been deleted successfully.')
    return redirect('reporter_list')


# ==========================================
# Desk Management Views (Admin Control)
# ==========================================
@admin_required
def desk_list_view(request):
    """
    Desk Staff List with search, status filtering, and management actions (View, Edit, Delete).
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    desks = Desk.objects.all()

    if query:
        desks = desks.filter(
            Q(name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    if status_filter == 'active':
        desks = desks.filter(is_active=True)
    elif status_filter == 'inactive':
        desks = desks.filter(is_active=False)

    context = {
        'active_page': 'desk_list',
        'desks': desks,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'admin/desk_list.html', context)


@admin_required
def desk_add_view(request):
    """
    Add New Desk Staff form.
    Fields: Name, Phone number, Gmail ID, Password, Confirm Password, and Save button.
    """
    errors = {}
    form_data = {}

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        form_data = {
            'name': name,
            'phone_number': phone_number,
            'email': email,
        }

        # Validation
        if not name:
            errors['name'] = "Desk Staff Name is required."

        if not phone_number:
            errors['phone_number'] = "Phone Number is required."
        elif Desk.objects.filter(phone_number=phone_number).exists() or User.objects.filter(username=phone_number).exists():
            errors['phone_number'] = "An account with this Phone Number already exists."

        if not email:
            errors['email'] = "Gmail / Email ID is required."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Please enter a valid email address (e.g. example@gmail.com)."

            if not errors.get('email') and (Desk.objects.filter(email__iexact=email).exists() or User.objects.filter(email__iexact=email).exists()):
                errors['email'] = "An account with this Email ID already exists."

        if not password:
            errors['password'] = "Password is required."
        elif len(password) < 4:
            errors['password'] = "Password must be at least 4 characters long."

        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."

        if not errors:
            # 1. Create Django Auth User
            user = User.objects.create_user(
                username=phone_number,
                email=email,
                first_name=name,
                password=password
            )

            # 2. Create Desk Profile
            desk = Desk.objects.create(
                user=user,
                name=name,
                phone_number=phone_number,
                email=email,
                is_active=True
            )

            messages.success(request, f'Desk user "{desk.name}" registered successfully!')
            return redirect('desk_list')

    context = {
        'active_page': 'desk_add',
        'errors': errors,
        'form_data': form_data,
    }
    return render(request, 'admin/desk_add.html', context)


@admin_required
def desk_detail_view(request, pk):
    """
    View Desk full details / ID card.
    """
    desk = get_object_or_404(Desk, pk=pk)
    context = {
        'active_page': 'desk_list',
        'desk': desk,
    }
    return render(request, 'admin/desk_view.html', context)


@admin_required
def desk_edit_view(request, pk):
    """
    Edit existing Desk user information.
    """
    desk = get_object_or_404(Desk, pk=pk)
    errors = {}

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        is_active = request.POST.get('is_active') == '1'
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not name:
            errors['name'] = "Name is required."

        if not phone_number:
            errors['phone_number'] = "Phone Number is required."
        elif Desk.objects.filter(phone_number=phone_number).exclude(pk=desk.pk).exists() or \
             User.objects.filter(username=phone_number).exclude(pk=desk.user.pk).exists():
            errors['phone_number'] = "Another account with this Phone Number already exists."

        if not email:
            errors['email'] = "Email ID is required."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Please enter a valid email address."

            if not errors.get('email') and (
                Desk.objects.filter(email__iexact=email).exclude(pk=desk.pk).exists() or
                User.objects.filter(email__iexact=email).exclude(pk=desk.user.pk).exists()
            ):
                errors['email'] = "Another account with this Email ID already exists."

        if new_password:
            if len(new_password) < 4:
                errors['new_password'] = "Password must be at least 4 characters long."
            if new_password != confirm_password:
                errors['confirm_password'] = "Passwords do not match."

        if not errors:
            desk.name = name
            desk.email = email
            desk.is_active = is_active

            # Update linked Auth User
            user = desk.user
            user.first_name = name
            user.email = email
            user.is_active = is_active

            if phone_number != desk.phone_number:
                desk.phone_number = phone_number
                user.username = phone_number

            if new_password:
                user.set_password(new_password)

            user.save()
            desk.save()

            messages.success(request, f'Desk user "{desk.name}" updated successfully.')
            return redirect('desk_list')

    context = {
        'active_page': 'desk_list',
        'desk': desk,
        'errors': errors,
    }
    return render(request, 'admin/desk_edit.html', context)


@admin_required
def desk_delete_view(request, pk):
    """
    Delete Desk staff and linked auth User.
    """
    desk = get_object_or_404(Desk, pk=pk)
    name = desk.name
    user = desk.user
    user.delete()

    messages.success(request, f'Desk user "{name}" has been deleted successfully.')
    return redirect('desk_list')


# ==========================================
# Reporter Portal Views (Separate Section)
# ==========================================
@reporter_required
def reporter_dashboard_view(request):
    """
    Reporter's Personal Dashboard.
    """
    reporter = request.user.reporter_profile
    my_news_count = News.objects.filter(Q(reporter=reporter) | Q(author=request.user)).count()
    recent_news = News.objects.filter(Q(reporter=reporter) | Q(author=request.user)).order_by('-created_at')[:5]
    context = {
        'active_page': 'reporter_dashboard',
        'reporter': reporter,
        'my_news_count': my_news_count,
        'recent_news': recent_news,
    }
    return render(request, 'reporter/dashboard.html', context)


@reporter_required
def reporter_profile_view(request):
    """
    Reporter's Personal Profile & ID Card View.
    """
    reporter = request.user.reporter_profile
    context = {
        'active_page': 'reporter_profile',
        'reporter': reporter,
    }
    return render(request, 'reporter/profile.html', context)


# ==========================================
# Desk Portal Views (Separate Section)
# ==========================================
@desk_required
def desk_dashboard_view(request):
    """
    Desk Staff Personal Dashboard.
    """
    desk = request.user.desk_profile
    total_reporters = Reporter.objects.count()
    active_reporters = Reporter.objects.filter(is_active=True).count()
    districts_count = Reporter.objects.values('district').distinct().count()
    recent_reporters = Reporter.objects.all()[:6]
    total_news = News.objects.count()
    recent_news = News.objects.select_related('reporter', 'author').order_by('-created_at')[:6]

    context = {
        'active_page': 'desk_dashboard',
        'desk': desk,
        'total_reporters': total_reporters,
        'active_reporters': active_reporters,
        'districts_count': districts_count,
        'recent_reporters': recent_reporters,
        'total_news': total_news,
        'recent_news': recent_news,
    }
    return render(request, 'desk/dashboard.html', context)


@desk_required
def desk_profile_view(request):
    """
    Desk Staff Personal Profile & Workspace Info.
    """
    desk = request.user.desk_profile
    context = {
        'active_page': 'desk_profile',
        'desk': desk,
    }
    return render(request, 'desk/profile.html', context)


# ==========================================
# 7. News Management Views (Reporter, Admin, Desk)
# ==========================================
@login_required
def news_list_view(request):
    """
    Lists all submitted news stories with search, filter, and management actions.
    Role-aware: Reporters see their news / district news, Admin & Desk see all.
    """
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '').strip()
    category_filter = request.GET.get('category', '').strip()
    district_filter = request.GET.get('district', '').strip()
    status_filter = request.GET.get('status', '').strip()
    scope = request.GET.get('scope', '').strip()

    news_qs = News.objects.select_related('reporter', 'author').all()

    if is_reporter_user(request.user) and scope == 'my':
        news_qs = news_qs.filter(author=request.user)

    if query:
        news_qs = news_qs.filter(
            Q(headline__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(district__icontains=query) |
            Q(byte_interview__icontains=query) |
            Q(reporter__name__icontains=query) |
            Q(reporter__reporter_id__icontains=query)
        )

    if type_filter:
        news_qs = news_qs.filter(news_type=type_filter)

    if category_filter:
        news_qs = news_qs.filter(category=category_filter)

    if district_filter:
        news_qs = news_qs.filter(district__iexact=district_filter)

    if status_filter:
        news_qs = news_qs.filter(status=status_filter)

    all_districts = News.objects.values_list('district', flat=True).distinct().order_by('district')
    if not all_districts:
        all_districts = Reporter.objects.values_list('district', flat=True).distinct().order_by('district')

    context = {
        'active_page': 'news_list',
        'news_list': news_qs,
        'all_districts': all_districts,
        'news_types': [c[0] for c in NEWS_TYPE_CHOICES],
        'news_categories': [c[0] for c in NEWS_CATEGORY_CHOICES],
        'news_statuses': [c[0] for c in NEWS_STATUS_CHOICES],
        'query': query,
        'type_filter': type_filter,
        'category_filter': category_filter,
        'district_filter': district_filter,
        'status_filter': status_filter,
        'scope': scope,
        'base_template': get_base_template(request.user),
        'is_reporter': is_reporter_user(request.user),
        'is_desk': is_desk_user(request.user),
        'is_admin': is_admin_user(request.user),
    }
    return render(request, 'news/news_list.html', context)


@login_required
def news_add_view(request):
    """
    Add / Submit News form.
    Fields: News Headline, News Type (AVO, Byte, AVO Byte, PKG),
    Category, Location, District, News Description,
    Media File (Video/Image), Byte Interview (Optional), Byte Media (Optional).
    """
    errors = {}
    default_district = ''
    if is_reporter_user(request.user):
        default_district = request.user.reporter_profile.district

    form_data = {
        'district': default_district,
        'category': 'General',
        'news_type': 'AVO',
    }

    if request.method == 'POST':
        headline = request.POST.get('headline', '').strip()
        news_type = request.POST.get('news_type', '').strip()
        category = request.POST.get('category', '').strip()
        location = request.POST.get('location', '').strip()
        district = request.POST.get('district', '').strip()
        description = request.POST.get('description', '').strip()
        byte_interview = request.POST.get('byte_interview', '').strip()

        media_file = request.FILES.get('media_file')
        byte_media = request.FILES.get('byte_media')

        form_data = {
            'headline': headline,
            'news_type': news_type,
            'category': category,
            'location': location,
            'district': district,
            'description': description,
            'byte_interview': byte_interview,
        }

        # Validation
        if not headline:
            errors['headline'] = "News Headline is required."
        if not news_type:
            errors['news_type'] = "Please select News Type (AVO, Byte, AVO Byte, PKG)."
        elif news_type not in [c[0] for c in NEWS_TYPE_CHOICES]:
            errors['news_type'] = "Invalid News Type selected."
        if not location:
            errors['location'] = "Location / Incident Spot is required."
        if not district:
            errors['district'] = "District Name is required."
        if not description:
            errors['description'] = "News Description / Story Script is required."

        if not errors:
            news = News(
                headline=headline,
                news_type=news_type,
                category=category or 'General',
                location=location,
                district=district,
                description=description,
                byte_interview=byte_interview,
                author=request.user,
                status='Submitted'
            )
            if is_reporter_user(request.user):
                news.reporter = request.user.reporter_profile

            if media_file:
                news.media_file = media_file
            if byte_media:
                news.byte_media = byte_media

            news.save()
            messages.success(request, f'News "{news.headline}" has been submitted successfully!')
            return redirect('news_list')

    context = {
        'active_page': 'news_add',
        'errors': errors,
        'form_data': form_data,
        'news_types': NEWS_TYPE_CHOICES,
        'news_categories': NEWS_CATEGORY_CHOICES,
        'base_template': get_base_template(request.user),
        'is_reporter': is_reporter_user(request.user),
        'is_desk': is_desk_user(request.user),
        'is_admin': is_admin_user(request.user),
    }
    return render(request, 'news/news_add.html', context)


@login_required
def news_detail_view(request, pk):
    """
    Detailed View of a Single News Story.
    Displays Headline, Type, Category, Location, District, Media Player/Image,
    Description, Byte Interview details, and Reporter Info.
    """
    news = get_object_or_404(News.objects.select_related('reporter', 'author'), pk=pk)
    context = {
        'active_page': 'news_list',
        'news': news,
        'base_template': get_base_template(request.user),
        'is_reporter': is_reporter_user(request.user),
        'is_desk': is_desk_user(request.user),
        'is_admin': is_admin_user(request.user),
    }
    return render(request, 'news/news_view.html', context)


@login_required
def news_edit_view(request, pk):
    """
    Edit existing News Story.
    """
    news = get_object_or_404(News, pk=pk)
    errors = {}

    # Check permission
    if is_reporter_user(request.user) and news.author != request.user and news.reporter != request.user.reporter_profile:
        messages.error(request, "You do not have permission to edit this news story.")
        return redirect('news_list')

    if request.method == 'POST':
        headline = request.POST.get('headline', '').strip()
        news_type = request.POST.get('news_type', '').strip()
        category = request.POST.get('category', '').strip()
        location = request.POST.get('location', '').strip()
        district = request.POST.get('district', '').strip()
        description = request.POST.get('description', '').strip()
        byte_interview = request.POST.get('byte_interview', '').strip()
        status = request.POST.get('status', news.status).strip()

        media_file = request.FILES.get('media_file')
        byte_media = request.FILES.get('byte_media')
        remove_media = request.POST.get('remove_media') == '1'
        remove_byte_media = request.POST.get('remove_byte_media') == '1'

        if not headline:
            errors['headline'] = "News Headline is required."
        if not news_type:
            errors['news_type'] = "Please select News Type."
        if not location:
            errors['location'] = "Location is required."
        if not district:
            errors['district'] = "District is required."
        if not description:
            errors['description'] = "News Description is required."

        if not errors:
            news.headline = headline
            news.news_type = news_type
            news.category = category or 'General'
            news.location = location
            news.district = district
            news.description = description
            news.byte_interview = byte_interview

            if not is_reporter_user(request.user) and status in [c[0] for c in NEWS_STATUS_CHOICES]:
                news.status = status

            if remove_media and news.media_file:
                news.media_file.delete(save=False)
                news.media_file = None
            elif media_file:
                news.media_file = media_file

            if remove_byte_media and news.byte_media:
                news.byte_media.delete(save=False)
                news.byte_media = None
            elif byte_media:
                news.byte_media = byte_media

            news.save()
            messages.success(request, f'News "{news.headline}" was updated successfully!')
            return redirect('news_list')

    context = {
        'active_page': 'news_list',
        'news': news,
        'errors': errors,
        'news_types': NEWS_TYPE_CHOICES,
        'news_categories': NEWS_CATEGORY_CHOICES,
        'news_statuses': NEWS_STATUS_CHOICES,
        'base_template': get_base_template(request.user),
        'is_reporter': is_reporter_user(request.user),
        'is_desk': is_desk_user(request.user),
        'is_admin': is_admin_user(request.user),
    }
    return render(request, 'news/news_edit.html', context)


@login_required
def news_delete_view(request, pk):
    """
    Delete News Story with confirmation.
    """
    news = get_object_or_404(News, pk=pk)

    if is_reporter_user(request.user) and news.author != request.user and news.reporter != request.user.reporter_profile:
        messages.error(request, "You do not have permission to delete this news story.")
        return redirect('news_list')

    headline = news.headline
    if news.media_file:
        news.media_file.delete(save=False)
    if news.byte_media:
        news.byte_media.delete(save=False)
    news.delete()

    messages.success(request, f'News "{headline}" was deleted successfully.')
    return redirect('news_list')
