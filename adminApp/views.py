import os
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from decouple import config
from django.db.models.functions import ExtractHour
from django.forms import model_to_dict
from django.utils.dateparse import parse_date, parse_datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from requests import Response
import openpyxl
from EcomRecomendation import settings
from accounts.models import Account, UserProfile, EventUser
from accounts.views import upload_image_to_cloudflare
from django.shortcuts import redirect
from category.models import CategoryMain, SubCategory
from category.forms import SubCategoryForm, CategoryMainForm
from store.models import Product, Variation, VariationManager, ProductImage
from carts.forms import ProductForm, ProductImageFormSet
from store.forms import variationForm
from orders.forms import OrderForm, OrderUpdateForm
from django.http import HttpResponse, JsonResponse
from orders.models import Order, OrderProduct, Payment
from django.contrib import messages
import json
import pandas as pd
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
import json
from django.db.models import Count
from decouple import config, UndefinedValueError
import json
import requests
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta, date
import logging
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta
import json
from django.db.models import Count
from django.db.models.functions import TruncHour, TruncDate, TruncMonth
from orders.models import Order
from django.db.models import Q


def get_locations(id, parent_id):
    api_url = "https://member.lazada.vn/locationtree/api/getSubAddressList?countryCode=VN"
    if parent_id:
        api_url += f"&addressId={parent_id}"
    response = requests.get(api_url)
    locations = response.json().get('module', [])
    for location in locations:
        if location.get('id') == id:
            return location.get('name')
    return None

def update_dash(request):
    if request.method == "POST":
        timezone.activate(settings.TIME_ZONE)
        today = timezone.now().date()
        users_logged_in_today = Account.objects.filter(last_login__date__gte=today).count()
        users_logged_in_not_today = Account.objects.filter(last_login__date__lt=today, is_login=True).count()
        daily_signins = users_logged_in_today + users_logged_in_not_today
        daily_signup = Account.objects.filter(date_joined__date__gte=today).count()
        daily_order = Order.objects.filter(created_at__date__gte=today).count()
        orders = Order.objects.filter(created_at__gte=today, is_ordered=True)
        daily_total_order = 0
        for order in orders:
            daily_total_order += order.payment.amount_paid
        response = {
            "user_signins": daily_signins,
            "daily_signups": daily_signup,
            "daily_order": daily_order,
            "daily_total_order": round(daily_total_order, 2)
        }
        return JsonResponse(response, safe=False)


@login_required(login_url='login')
def index(request):
    if request.user.is_superuser:
        return render(request, 'adminApp/dashboard.html')
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_infor(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                data = {
                    'date_of_birth': user_profile.date_of_birth.strftime(
                        "%Y-%m-%d") if user_profile.date_of_birth else None,
                    'sex': user_profile.sex,
                    'road': user_profile.road,
                    'ward': user_profile.ward,
                    'district': user_profile.district,
                    'city': user_profile.city,
                    'profile_picture': user_profile.profile_picture,
                    'bio': user_profile.bio
                }
                return JsonResponse(data)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'User profile not found'}, status=404)
        else:
            return JsonResponse({'error': 'You are not authorized to view this page'}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request, only POST method is allowed'}, status=400)


@login_required(login_url='login')
def user_list(request):
    if request.user.is_superuser:
        profiles = UserProfile.objects.all().order_by('-user__date_joined')
        profile_user = UserProfile.objects.get(user__pk=request.user.id)
        context = {
            'profiles': profiles,
            'profile_user': profile_user
        }
        return render(request, 'adminApp/users/user_list.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_profile(request, pk):
    if request.user.is_superuser:
        if request.method == 'POST':
            user = request.user
            profile = UserProfile.objects.get(user__pk=pk)
            user.full_name = request.POST.get('full_name')
            user.username = request.POST.get('user_name')
            user.phone_number = request.POST.get('phone_number')
            user.save()

            date_of_birth = request.POST.get('date_of_birth')
            if date_of_birth:
                try:
                    datetime.strptime(date_of_birth, '%Y-%m-%d')
                    profile.date_of_birth = date_of_birth
                except ValueError:
                    print("Incorrect date format")

            profile.sex = request.POST.get('sex')
            profile.road = request.POST.get('road')
            profile.ward = request.POST.get('ward')
            profile.district = request.POST.get('district')
            profile.city = request.POST.get('city')
            profile.bio = request.POST.get('bio')

            # Xử lý file ảnh
            if 'profile_picture' in request.FILES:
                try:
                    image_url = upload_image_to_cloudflare(request.FILES['profile_picture'], request)
                    if image_url is not None:
                        profile.profile_picture = image_url
                except Exception as e:
                    messages.error(request, f"Failed to upload image: {str(e)}")

            profile.save()

            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if old_password and new_password and confirm_password:
                if new_password == confirm_password:
                    if user.check_password(old_password):
                        user.set_password(new_password)
                        user.save()
                    else:
                        messages.error(request, "Old password is incorrect.")
                else:
                    messages.error(request, "New password and confirm password do not match.")

            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile', pk=profile.pk)

        profile = UserProfile.objects.get(user__pk=pk)
        context = {
            'profile': profile,
        }
        return render(request, 'adminApp/users/user_profile.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_delete(request, pk):
    if request.user.is_superuser:
        user = Account.objects.get(pk=pk)
        user.delete()
        return redirect('user_list')
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_block(request, pk):
    if request.user.is_superuser:
        user = Account.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return redirect('user_list')
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_unblock(request, pk):
    if request.user.is_superuser:
        user = Account.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return redirect('user_list')
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def get_login_frequency(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            data = json.loads(request.body)
            start_date = parse_datetime(data['start_date'])
            end_date = parse_datetime(data['end_date'])
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)
        except (ValueError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        events = EventUser.objects.filter(
            event_timestamp__range=[start_date, end_date],
            event_type='login'
        ).annotate(hour=ExtractHour('event_timestamp')).values('hour').annotate(count=Count('id')).order_by('hour')

        data = [0] * 12
        for event in events:
            hour_index = event['hour'] // 2
            if hour_index < 12:
                data[hour_index] += event['count']

        return JsonResponse({'data': data})
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def get_user_acquisition(request):
    if request.method == 'POST' and request.user.is_superuser:
        data = json.loads(request.body)
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') + timedelta(days=1)

        events = EventUser.objects.filter(
            event_timestamp__range=[start_date, end_date],
            event_type__in=['view', 'cart', 'pay']  # Chỉ xử lý các sự kiện này
        ).annotate(hour=ExtractHour('event_timestamp')).values('hour', 'event_type').annotate(count=Count('id')).order_by('hour')

        result = {
            'View': [0]*12, 'Cart': [0]*12, 'Pay': [0]*12
        }

        for event in events:
            hour_index = event['hour'] // 2
            event_type = event['event_type'].capitalize()
            if event_type in result:
                result[event_type][hour_index] += 1

        return JsonResponse(result)
    else:
        return HttpResponse('You are not authorized to view this page', status=403)


# User based views ends here ##############################################################

# Category based views ##############################################################

@login_required(login_url='login')
def main_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CategoryMainForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('main_category')
        data = SubCategory.objects.all()
        main = CategoryMain.objects.all()
        form = CategoryMainForm()
        context = {
            'main': main,
            'sub': data,
            'form': form,
        }
        return render(request, 'adminApp/Category/MainCategory.html', context)
    return HttpResponse('You are not authorized to view this page')


def main_category_edit(request, pk):
    if request.user.is_superuser:
        main = CategoryMain.objects.get(pk=pk)
        data = SubCategory.objects.all()
        form = CategoryMainForm(instance=main)
        mains = CategoryMain.objects.all()
        if request.method == 'POST':
            form = CategoryMainForm(request.POST, instance=main)
            if form.is_valid():
                form.save()
                return redirect('main_category')
            else:
                print(form.errors)

        context = {
            'main': main,
            'edit_form': form,
            'sub': data,
            'mains': mains,
        }
        return render(request, 'adminApp/Category/MainCategoryedit.html', context)

    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def main_category_delete(request, pk):
    if request.user.is_superuser:
        main = CategoryMain.objects.get(pk=pk)
        main.delete()
        return redirect('main_category')
    return HttpResponse('You are not authorized to view this page')


# Sub Category based views ##############################################################

@login_required(login_url='login')
def sub_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SubCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('sub_category')
        data = SubCategory.objects.all()
        form = SubCategoryForm()
        context = {
            'sub': data,
            'form': form,

        }
        return render(request, 'adminApp/Category/SubCategory.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def sub_category_edit(request, pk):
    sub = SubCategory.objects.get(pk=pk)
    form = SubCategoryForm(instance=sub)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SubCategoryForm(request.POST, request.FILES, instance=sub)
            if form.is_valid():
                form.save()
                return redirect('sub_category')
            else:
                print(form.errors)

        context = {
            'sub': sub,
            'edit_form': form,
        }
        return render(request, 'adminApp/Category/SubCategoryedit.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def sub_category_delete(request, pk):
    if request.user.is_superuser:
        sub = SubCategory.objects.get(pk=pk)
        sub.delete()
        return redirect('sub_category')
    return HttpResponse('You are not authorized to view this page')


# Product based views ##############################################################
@login_required(login_url='login')
def product_list(request):
    if request.user.is_superuser:
        product = Product.objects.all()
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            image_formset = ProductImageFormSet(request.POST, request.FILES)
            if form.is_valid() and image_formset.is_valid():
                # Lưu sản phẩm trước
                product = form.save()
                # Gán sản phẩm cho các ảnh trong formset
                image_formset.instance = product
                image_formset.save()
                return redirect('product_list')
            else:
                print("Form errors:", form.errors)
                print("Formset errors:", image_formset.errors)
        else:
            form = ProductForm()
            image_formset = ProductImageFormSet()

        context = {
            'product': product,
            'addProduct': form,
            'image_formset': image_formset,
        }
        return render(request, 'adminApp/Products/product_list.html', context)
    return HttpResponse('You are not authorized to view this page')

@login_required(login_url='login')
def product_edit(request, pk):
    if request.user.is_superuser:
        Allproduct = Product.objects.all()
        product = Product.objects.get(pk=pk)
        form = ProductForm(instance=product)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product = form.save()
                # Xử lý upload ảnh
                if 'image' in request.FILES:
                    image_type = request.POST.get('image_type', 'default')
                    # Kiểm tra xem đã có ảnh với image_type này chưa
                    try:
                        product_image = ProductImage.objects.get(
                            product=product,
                            image_type=image_type
                        )
                        # Nếu đã có ảnh, cập nhật ảnh mới
                        product_image.image = request.FILES['image']
                        product_image.save()
                    except ProductImage.DoesNotExist:
                        # Nếu chưa có ảnh, tạo mới
                        ProductImage.objects.create(
                            product=product,
                            image_type=image_type,
                            image=request.FILES['image']
                        )
                return redirect('product_list')
            else:
                print(form.errors)

        context = {
            'product': Allproduct,
            'product_editing': product,
            'edit_form': form,
        }
        return render(request, 'adminApp/Products/product_edit.html', context)
    else:
        return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def product_delete(request, pk):
    if request.user.is_superuser:
        product = Product.objects.get(pk=pk)
        product.delete()
        return redirect('product_list')
    return HttpResponse('You are not authorized to view this page')


# product variations based views ##############################################################

@login_required(login_url='login')
def add_variations(request):
    if request.user.is_superuser:
        existing_variations = Variation.objects.all()
        if request.method == 'POST':
            form = variationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('add_variations')
        form = variationForm

        context = {
            'existing_variations': existing_variations,
            'form': form,
        }
        return render(request, 'AdminApp/Variations/add_variations.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def edit_variations(request, pk):
    if request.user.is_superuser:
        # Thêm phân trang
        page = request.GET.get('page', 1)
        items_per_page = 10  # Số item trên mỗi trang
        
        existing_variations = Variation.objects.all()
        
        # Phân trang
        paginator = Paginator(existing_variations, items_per_page)
        try:
            variations_page = paginator.page(page)
        except:
            variations_page = paginator.page(1)
            
        variation = Variation.objects.get(pk=pk)
        form = variationForm(instance=variation)
        if request.method == 'POST':
            form = variationForm(request.POST, request.FILES, instance=variation)
            if form.is_valid():
                form.save()
                return redirect('add_variations')
            else:
                print(form.errors)

        context = {
            'existing_variations': variations_page,
            'variation_editing': variation,
            'form': form,
        }
        return render(request, 'adminApp/Variations/edit_variations.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def delete_variations(request, pk):
    if request.user.is_superuser:
        variation = Variation.objects.get(pk=pk)
        variation.delete()
        return redirect('add_variations')
    return HttpResponse('You are not authorized to view this page')


# Orders based views ##############################################################
@login_required(login_url='login')
def download_order_report(request):
    if request.method == 'POST' and request.user.is_superuser:
        data = json.loads(request.body)
        start_date = parse_datetime(data['start_date'])
        end_date = parse_datetime(data['end_date'])
        end_date = end_date + timedelta(days=1) - timedelta(seconds=1)
        orders = Order.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).values(
            'id', 'order_number', 'created_at', 'user__full_name', 'user__email',
            'order_total', 'payment__status', 'order_status', 'phone', 'road', 'ward', 'district', 'city'
        )

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Orders Report"

        columns = ["ID", "Order Number", "Full Name", "Phone Number", "Email", "Address",
                   "Created At", "Payment Status", "Order Status",  "Total ($)"]
        ws.append(columns)

        for order in orders:
            address = f"{order['road']}, {get_locations(order['ward'], order['district'])}, {get_locations(order['district'], order['city'])}, {get_locations(order['city'], '')}"
            row = [
                order['id'], order['order_number'], order['user__full_name'], order['phone'],
                order['user__email'], address, order['created_at'].strftime('%Y-%m-%d %H:%M:%S'), order['payment__status'],
                order['order_status'], order['order_total']
            ]
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="orders_report_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.xlsx"'
        wb.save(response)

        return response

    return HttpResponse("Invalid request", status=400)


@login_required(login_url='login')
def export_payments_to_excel(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            data = json.loads(request.body)
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not start_date or not end_date:
                return JsonResponse({'error': 'Missing start_date or end_date'}, status=400)

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        totals = {}

        payments = Payment.objects.filter(
            order__created_at__range=[start_date, end_date],
            order__is_ordered=True
        ).values('order__city', 'amount_paid')

        for payment in payments:
            city_name = payment['order__city']
            if city_name:
                if city_name not in totals:
                    totals[city_name] = 0
                totals[city_name] += payment['amount_paid']

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Payments by City"

        ws.append(["City", "Revenue"])

        for city, total in totals.items():
            ws.append([get_locations(city, ''), total])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="payments_by_city.xlsx"'

        wb.save(response)

        return response

    return HttpResponse('You are not authorized to view this page', status=403)


def get_order_stats(request):
    if request.method == 'POST' and request.user.is_superuser:
        data = json.loads(request.body)
        start_date = parse_date(data.get('start_date'))
        end_date = parse_date(data.get('end_date'))
        period = data.get('period')

        orders = Order.objects.filter(created_at__date__range=[start_date, end_date])

        response_data = {
            'labels': [],
            'accepted': [],
            'ready_to_ship': [],
            'on_shipping': [],
            'delivered': [],
            'cancelled': [],
            'returned': []
        }

        if period == 'hour':
            for hour in range(24):
                start_time = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=hour)
                end_time = start_time + timedelta(hours=1)
                response_data['labels'].append(f"{hour:02d}:00-{hour + 1:02d}:00")
                response_data['accepted'].append(
                    orders.filter(created_at__time__range=[start_time.time(), end_time.time()],
                                  order_status='Accepted').count())
                response_data['ready_to_ship'].append(
                    orders.filter(created_at__time__range=[start_time.time(), end_time.time()],
                                  order_status='Ready to ship').count())
                response_data['on_shipping'].append(
                    orders.filter(created_at__time__range=[start_time.time(), end_time.time()],
                                  order_status='On shipping').count())
                response_data['delivered'].append(
                    orders.filter(created_at__time__range=[start_time.time(), end_time.time()],
                                  order_status='Delivered').count())
                response_data['cancelled'].append(
                    orders.filter(created_at__time__range=[start_time.time(), end_time.time()],
                                  order_status='Cancelled').count())
                response_data['returned'].append(
                    orders.filter(created_at__time__range=[start_time.time(), end_time.time()],
                                  order_status='Return').count())

        elif period == 'day':
            for day in range((end_date - start_date).days + 1):
                current_date = start_date + timedelta(days=day)
                response_data['labels'].append(current_date.strftime('%d %b'))
                response_data['accepted'].append(
                    orders.filter(created_at__date=current_date, order_status='Accepted').count())
                response_data['ready_to_ship'].append(
                    orders.filter(created_at__date=current_date, order_status='Ready to ship').count())
                response_data['on_shipping'].append(
                    orders.filter(created_at__date=current_date, order_status='On shipping').count())
                response_data['delivered'].append(
                    orders.filter(created_at__date=current_date, order_status='Delivered').count())
                response_data['cancelled'].append(
                    orders.filter(created_at__date=current_date, order_status='Cancelled').count())
                response_data['returned'].append(
                    orders.filter(created_at__date=current_date, order_status='Return').count())

        elif period == 'month':
            for month in range(start_date.month, end_date.month + 1):
                month_start_date = start_date.replace(day=1, month=month)
                month_end_date = (month_start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                response_data['labels'].append(month_start_date.strftime('%B'))
                response_data['accepted'].append(
                    orders.filter(created_at__date__range=[month_start_date, month_end_date],
                                  order_status='Accepted').count())
                response_data['ready_to_ship'].append(
                    orders.filter(created_at__date__range=[month_start_date, month_end_date],
                                  order_status='Ready to ship').count())
                response_data['on_shipping'].append(
                    orders.filter(created_at__date__range=[month_start_date, month_end_date],
                                  order_status='On shipping').count())
                response_data['delivered'].append(
                    orders.filter(created_at__date__range=[month_start_date, month_end_date],
                                  order_status='Delivered').count())
                response_data['cancelled'].append(
                    orders.filter(created_at__date__range=[month_start_date, month_end_date],
                                  order_status='Cancelled').count())
                response_data['returned'].append(
                    orders.filter(created_at__date__range=[month_start_date, month_end_date],
                                  order_status='Return').count())

        return JsonResponse(response_data)
    return HttpResponse('You are not authorized to view this page', status=403)

@login_required(login_url='login')
def order_status_data(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            data = json.loads(request.body)
            start_date = parse_date(data.get('start_date'))
            end_date = parse_date(data.get('end_date'))
        except (ValueError, KeyError):
            return HttpResponse('Invalid data', status=400)

        status_color_mapping = {
            'Accepted': '#80e1c1',
            'Ready to ship': '#f3d676',
            'On shipping': '#f2994a',
            'Delivered': '#4c84ff',
            'Cancelled': '#ff7b7b',
            'Return': '#bb6bd9',
        }

        # Filter orders between start_date and end_date
        queryset = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).values('order_status').annotate(total=Count('id'))

        labels = []
        data = []
        backgroundColor = []

        for item in queryset:
            status = item['order_status']
            if status in status_color_mapping:
                labels.append(status)
                data.append(item['total'])
                backgroundColor.append(status_color_mapping[status])

        response_data = {
            'labels': labels,
            'data': data,
            'backgroundColor': backgroundColor
        }
        return JsonResponse(response_data)
    return HttpResponse('You are not authorized to view this page', status=403)


@login_required(login_url='login')
def get_payment_by_city(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            data = json.loads(request.body)
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not start_date or not end_date:
                return JsonResponse({'error': 'Missing start_date or end_date'}, status=400)

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        city_ids = {
            'R1973756': 'VN-SG',
            'R1875748': 'An Giang',
            'R1873533': 'VN-55',
            'R1904296': 'Bà Rịa–Vũng Tàu',
            'R1902941': 'Bắc Giang',
            'R1903471': 'Bắc Kạn',
            'R1902690': 'Bắc Ninh',
            'R1875968': 'Bến Tre',
            'R1906037': 'Bình Dương',
            'R1889794': 'Bình Định',
            'R1898841': 'Bình Phước',
            'R1904231': 'Bình Thuận',
            'R1873490': 'Cà Mau',
            'R1844412': 'Cao Bằng',
            'R1874283': 'VN-CT',
            'R1891418': 'VN-DN',
            'R1884034': 'Đắk Lắk',
            'R1884042': 'VN-72',
            'R1903340': 'Điện Biên',
            'R1904421': 'Đồng Nai',
            'R1875866': 'Đồng Tháp',
            'R1884018': 'Gia Lai',
            'R1903478': 'Hà Giang',
            'R1902686': 'Hải Dương',
            'R1902682': 'Hải Phòng',
            'R1901010': 'Hà Nam',
            'R1903516': 'VN-HN',
            'R1898458': 'Hà Tĩnh',
            'R1874249': 'Hậu Giang',
            'R1902973': 'Hòa Bình',
            'R1901032': 'Hưng Yên',
            'R1887959': 'Khánh Hòa',
            'R1874471': 'Kiên Giang',
            'R1879515': 'Kon Tum',
            'R1903322': 'Lai Châu',
            'R5522596': 'Lạng Sơn',
            'R1903400': 'Lào Cai',
            'R1885367': 'Lâm Đồng',
            'R1877236': 'Long An',
            'R1901008': 'Nam Định',
            'R1898509': 'Nghệ An',
            'R1900963': 'Ninh Bình',
            'R1886159': 'Ninh Thuận',
            'R1902930': 'Phú Thọ',
            'R1889204': 'Phú Yên',
            'R1896050': 'Quảng Bình',
            'R1891352': 'Quảng Nam',
            'R1890793': 'Quảng Ngãi',
            'R1902947': 'Quảng Ninh',
            'R1895630': 'Quảng Trị',
            'R1873632': 'Sóc Trăng',
            'R1903291': 'Sơn La',
            'R1898961': 'Tây Ninh',
            'R1901019': 'Thái Bình',
            'R1902967': 'Thái Nguyên',
            'R1898590': 'Thanh Hóa',
            'R1891483': 'Thừa Thiên–Huế',
            'R1876011': 'Tiền Giang',
            'R1873642': 'Trà Vinh',
            'R1903418': 'Tuyên Quang',
            'R1875887': 'Vĩnh Long',
            'R1902889': 'Vĩnh Phúc',
            'R1903199': 'Yên Bái'
        }

        totals = {name: 0 for name in city_ids.values()}

        payments = Payment.objects.filter(
            order__created_at__range=[start_date, end_date],
            order__city__in=city_ids.keys(),
            order__is_ordered=True
        ).values('order__city', 'amount_paid')

        for payment in payments:
            city_name = city_ids.get(payment['order__city'])
            if city_name:
                totals[city_name] += payment['amount_paid']

        result = [['City', 'Revenue']]
        for city, total in totals.items():
            result.append([city, total])

        return JsonResponse(result, safe=False)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def top_purchase(request):
    if request.method == 'POST' and  request.user.is_superuser:
        try:
            data = json.loads(request.body)
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not start_date or not end_date:
                return JsonResponse({'error': 'Missing start_date or end_date'}, status=400)

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        payments = Payment.objects.filter(
            order__created_at__range=[start_date, end_date],
            order__is_ordered=True
        ).values('order__city').annotate(
            total_paid=Sum('amount_paid')
        ).order_by('-total_paid')[:3]

        response = {
            'labels': [get_locations(payment['order__city'], '') for payment in payments],
            'data': [round(payment['total_paid'], 2) for payment in payments]
        }

        return JsonResponse(response)

    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def recent_orders(request):
    if request.method == 'POST' and request.user.is_superuser:
        orders = Order.objects.prefetch_related('orderproduct_set__product').order_by('-created_at')[:5]
        orders_data = []
        current_site = get_current_site(request)
        for order in orders:
            products_info = [
                {
                    'product_name': op.product.product_name,
                    'quantity': op.quantity,
                    'product_price': op.product_price,
                    "product_url": f"http://{current_site}/store/{op.product.category_main.slug}/{op.product.sub_category.slug}/{op.product.slug}"
                }
                for op in order.orderproduct_set.all()
            ]
            order_dict = {
                "order_id": order.id,
                "order_number": order.order_number,
                "order_date": order.created_at.strftime("%b %d, %Y"),
                "order_cost": order.order_total,
                "status": order.order_status,
                "products": products_info,
                'url_view': f"http://{current_site}/accounts/order_details/{order.order_number}",
                'url_edit': f"http://{current_site}/admin/order_update/{str(order.id)}",
            }
            orders_data.append(order_dict)
        return JsonResponse(orders_data, safe=False)
    return HttpResponse('You are not authorized to view this page')

@login_required(login_url='login')
def order_list(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
        order_products = OrderProduct.objects.all()
        print(order_update)
        context = {
            'orders': orders,
            'order_products': order_products,
        }
        return render(request, 'adminApp/Orders/order_list.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def order_update(request, pk):
    if request.user.is_superuser:
        orders = Order.objects.get(pk=pk)
        update_order = Order.objects.get(pk=pk)
        form = OrderUpdateForm(instance=update_order)
        if request.method == 'POST':
            form = OrderUpdateForm(request.POST, instance=update_order)
            if form.is_valid():
                form.save()
                return redirect('order_list')
            else:
                print(form.errors)

        context = {
            'orders': orders,
            'form': form,
        }
        return render(request, 'adminApp/Orders/order_update.html', context)
    return HttpResponse('You are not authorized to view this page')


AES_KEY = base64.urlsafe_b64decode(config('AES_KEY'))


@login_required(login_url='login')
def encrypt(data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.urlsafe_b64encode(iv + encrypted_data).decode('utf-8')


@login_required(login_url='login')
def decrypt(encrypted_data):
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)
    iv = encrypted_data[:16]
    encrypted_message = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_message = decryptor.update(encrypted_message) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    return decrypted_message.decode('utf-8')


@login_required(login_url='login')
@csrf_exempt
def get_folders(request):
    response = requests.get(config('GET'))
    if response.status_code == 200:
        data = response.json()
        decrypted_folders = [decrypt(folder) for folder in data['folders']]
        return JsonResponse({"folders": decrypted_folders})
    else:
        return JsonResponse({"status": "error", "message": "Failed to get folders"}, status=500)


@login_required(login_url='login')
@csrf_exempt
def process_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        encrypted_folder_name = encrypt(json.dumps({"folder_name": folder_name}))
        response = requests.post(config('POST'), json={"data": encrypted_folder_name})
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"status": "error", "message": "Failed to process folder"}, status=500)
        
        
# @login_required(login_url='login')
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save()
#             return JsonResponse({'message': 'Product created', 'id': product.id}, status=201)
#         return JsonResponse({'error': form.errors}, status=400)
    
#     return JsonResponse({'error': 'Invalid request'}, status=405)

@login_required(login_url='login')
def get_order_alerts(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            # Parse request body
            if not request.body:
                return JsonResponse({'error': 'Empty request body'}, status=400)
            
            data = json.loads(request.body)
            
            # Get and validate inputs
            start_date_str = data.get('start_date', '2025-06-01')
            end_date_str = data.get('end_date', '2025-06-17')
            time_period = data.get('time_period', 'hour').lower()
            
            if time_period not in ['hour', 'day', 'month']:
                return JsonResponse({'error': f'Invalid time_period: {time_period}'}, status=400)
            
            # Parse dates
            try:
                start_date = parse_date(start_date_str).date()
                end_date = parse_date(end_date_str).date()
            except (ValueError, TypeError) as e:
                return JsonResponse({'error': f'Invalid date format: {str(e)}'}, status=400)

            # Aggregate data based on time period
            if time_period == 'hour':
                orders = Order.objects.filter(
                    created_at__date__range=[start_date, end_date]
                ).annotate(
                    hour=TruncHour('created_at')
                ).values('order_status', 'hour').annotate(total=Count('id')).order_by('hour')
            elif time_period == 'day':
                orders = Order.objects.filter(
                    created_at__date__range=[start_date, end_date]
                ).values('order_status', 'created_at__date').annotate(total=Count('id')).order_by('created_at__date')
            else:  # month
                orders = Order.objects.filter(
                    created_at__date__range=[start_date, end_date]
                ).annotate(
                    month=TruncMonth('created_at')
                ).values('order_status', 'month').annotate(total=Count('id')).order_by('month')

            daily_counts = {}
            for order in orders:
                if time_period == 'hour':
                    time_key = order['hour'].strftime('%Y-%m-%d %H:00:00')
                elif time_period == 'month':
                    time_key = order['month'].strftime('%Y-%m-01')
                else:  # day
                    time_key = order['created_at__date']
                
                status = order['order_status']
                if time_key not in daily_counts:
                    daily_counts[time_key] = {
                        'Accepted': 0, 'Ready to ship': 0, 'On shipping': 0,
                        'Delivered': 0, 'Cancelled': 0, 'Return': 0
                    }
                daily_counts[time_key][status] = order['total']

            # Ensure end_date is not in the future
            today = timezone.now().date()

            alerts = []
            total_days = (end_date - start_date).days + 1
            
            if total_days >= 1:  # Minimum data requirement
                # Calculate mid-point
                mid_point = start_date + timedelta(days=total_days // 2)

                # Split into first and second halves
                if time_period == 'hour':
                    hours = [
                        datetime.combine(start_date, datetime.min.time()) + timedelta(hours=x)
                        for x in range(int((end_date - start_date).days * 24) + 24)
                    ]
                    mid_hour = hours[len(hours) // 2] if hours else datetime.combine(start_date, datetime.min.time())
                    first_half_times = [h.strftime('%Y-%m-%d %H:00:00') for h in hours if h <= mid_hour]
                    second_half_times = [h.strftime('%Y-%m-%d %H:00:00') for h in hours if h > mid_hour and h.date() <= today]
                elif time_period == 'month':
                    months = [
                        (start_date + timedelta(days=x*30)).replace(day=1)
                        for x in range((end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1)
                    ]
                    mid_month = months[len(months) // 2] if months else start_date
                    first_half_times = [m.strftime('%Y-%m-01') for m in months if m <= mid_month]
                    second_half_times = [m.strftime('%Y-%m-01') for m in months if m > mid_month and m.date() <= today]
                else:  # day
                    first_half_days = [start_date + timedelta(days=x) for x in range((mid_point - start_date).days + 1)]
                    second_half_days = [
                        mid_point + timedelta(days=x)
                        for x in range((end_date - mid_point).days + 1)
                        if (mid_point + timedelta(days=x)) <= today
                    ]
                    first_half_times = first_half_days
                    second_half_times = second_half_days

                # Calculate averages
                first_half_avg = {
                    'Accepted': 0, 'Ready to ship': 0, 'On shipping': 0,
                    'Delivered': 0, 'Cancelled': 0, 'Return': 0
                }
                second_half_avg = {
                    'Accepted': 0, 'Ready to ship': 0, 'On shipping': 0,
                    'Delivered': 0, 'Cancelled': 0, 'Return': 0
                }
                total_orders = 0

                # Aggregate for first half
                for time_key in first_half_times:
                    counts = daily_counts.get(str(time_key), {})
                    for status in first_half_avg:
                        first_half_avg[status] += counts.get(status, 0)

                # Aggregate for second half
                for time_key in second_half_times:
                    counts = daily_counts.get(str(time_key), {})
                    for status in second_half_avg:
                        second_half_avg[status] += counts.get(status, 0)

                first_half_count = len(first_half_times)
                second_half_count = len(second_half_times)

                if first_half_count > 0:
                    for status in first_half_avg:
                        first_half_avg[status] /= first_half_count
                if second_half_count > 0:
                    for status in second_half_avg:
                        second_half_avg[status] /= second_half_count

                total_orders = sum(sum(day.values()) for day in daily_counts.values())

                # Rule 1: Rising then reducing Accepted trend
                threshold_drop = 1.2 if time_period in ['day', 'month'] else 1.5
                if first_half_avg['Accepted'] > second_half_avg['Accepted'] * threshold_drop and first_half_avg['Accepted'] > 0:
                    alert_msg = "Warning: Accepted orders are rising in the first half but have reduced significantly in the second half."
                    suggestion = "Consider launching a targeted marketing campaign to boost demand, such as discounts or promotions."
                    if time_period == 'hour':
                        alert_msg += " (Hourly spike detected)"
                        suggestion += " Focus on peak hours."
                    alerts.append({'trend_alert': alert_msg, 'suggestion': suggestion})

                # Rule 2: High Cancellation Rate
                cancelled_total = sum(daily_counts.get(time_key, {}).get('Cancelled', 0) for time_key in daily_counts)
                threshold_cancel = 15 if time_period in ['day', 'month'] else 25
                if total_orders > 0 and (cancelled_total / total_orders) * 100 > threshold_cancel:
                    alert_msg = f"Warning: Cancellation rate exceeds {threshold_cancel}% of total orders."
                    suggestion = "Review product quality or customer service to reduce cancellations."
                    if time_period == 'hour':
                        alert_msg += " (Hourly cancellations may indicate specific issues)"
                    alerts.append({'trend_alert': alert_msg, 'suggestion': suggestion})

                # Rule 3: Stagnant On Shipping
                if first_half_avg['On shipping'] >= second_half_avg['On shipping'] and second_half_avg['Ready to ship'] > first_half_avg['Ready to ship']:
                    alert_msg = "Warning: On Shipping orders are stagnant or decreasing while Ready to Ship increases."
                    suggestion = "Check for logistics bottlenecks or improve shipping process efficiency."
                    if time_period == 'hour':
                        alert_msg += " (Hourly bottleneck possible)"
                    alerts.append({'trend_alert': alert_msg, 'suggestion': suggestion})

            response_data = {
                'alerts': alerts,
                'time_period': time_period,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid date format: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
    return HttpResponse('You are not authorized to view this page', status=403)

@login_required(login_url='login')
def get_user_alerts(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            data = json.loads(request.body)
            start_date = parse_datetime(data['start_date'])
            end_date = parse_datetime(data['end_date'])
            end_date = end_date + timedelta(days=1)
        except (ValueError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        # Check if date range is exactly 1 day
        date_range = (end_date - start_date).days
        if date_range != 1:
            return JsonResponse({'alerts': [{'trend_alert': 'No significant user activity detected.', 'suggestion': 'System is operating normally.'}]})

        # Aggregate login events for the day
        login_events = EventUser.objects.filter(
            event_timestamp__range=[start_date, end_date],
            event_type='login'
        ).annotate(hour=ExtractHour('event_timestamp')).values('hour').annotate(count=Count('id')).order_by('hour')
        login_data = [0] * 24  # Hourly data for the day
        for event in login_events:
            hour_index = event['hour']
            if hour_index < 24:
                login_data[hour_index] += event['count']

        # Get users who have not placed orders in the date range
        ordered_users = Order.objects.filter(
            created_at__range=[start_date, end_date],
            is_ordered=True
        ).values_list('user', flat=True).distinct()
        all_users = Account.objects.values_list('id', flat=True)
        inactive_users = set(all_users) - set(ordered_users)

        alerts = []
        total_users = len(all_users)
        inactive_count = len(inactive_users)

        # Rule: High percentage of users with no orders
        if total_users > 0 and (inactive_count / total_users) * 100 > 90:  # More than 90% inactive
            alert_msg = f"{inactive_count} out of {total_users} users ({(inactive_count/total_users*100):.1f}%) did not place orders today."
            suggestion = "Consider targeted promotions or engagement campaigns to activate inactive users."
            alerts.append({'trend_alert': alert_msg, 'suggestion': suggestion})

        # Rule: Low login activity
        if sum(login_data) < 10:  # Less than 10 logins in the day
            alert_msg = "Low user login activity detected today."
            suggestion = "Consider sending reminders or notifications to encourage user engagement."
            alerts.append({'trend_alert': alert_msg, 'suggestion': suggestion})

        # Rule: High login in an hour
        high_login_hour = max(login_data)
        if high_login_hour > 5:  # More than 5 logins in any hour
            high_login_hour_index = login_data.index(high_login_hour)
            alert_msg = f"High user login activity detected at hour {high_login_hour_index}:00 with {high_login_hour} logins."
            suggestion = "Monitor system performance and consider scaling resources if needed."
            alerts.append({'trend_alert': alert_msg, 'suggestion': suggestion})

        response_data = {
            'alerts': alerts if alerts else [{'trend_alert': 'No significant user activity detected.', 'suggestion': 'System is operating normally.'}]
        }
        return JsonResponse(response_data)

    return HttpResponse('You are not authorized to view this page', status=403)

# Fetch API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in environment variables")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@login_required(login_url='login')
def get_gemini_chat(request):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            if not request.body:
                return JsonResponse({'error': 'Empty request body'}, status=400)
            
            data = json.loads(request.body)
            
            start_date_str = data.get('start_date', '2025-06-01')
            end_date_str = data.get('end_date', '2025-06-17')
            time_period = data.get('time_period', 'day').lower()
            user_message = data.get('user_message', '').strip()
            context = data.get('context', 'order').lower()
            alerts = data.get('alerts', [])  # Alerts provided by front-end

            if time_period not in ['hour', 'day', 'month']:
                return JsonResponse({'error': f'Invalid time_period: {time_period}'}, status=400)
            
            try:
                start_date = parse_date(start_date_str).date()
                end_date = parse_date(end_date_str).date()
            except (ValueError, TypeError) as e:
                return JsonResponse({'error': f'Invalid date format: {str(e)}'}, status=400)
            
            today = timezone.now().date()
            if end_date > today:
                end_date = today
            if start_date > end_date:
                return JsonResponse({'error': 'Start date cannot be after end date'}, status=400)

            if not user_message:  # Initial rule-based response
                response_text = f'Analyzing {context.replace("users", "Current Users").replace("order", "Order Details")} from {start_date} to {end_date} with {time_period} granularity.'
                if alerts:
                    response_text += ' Alerts:'
                    for i, alert in enumerate(alerts, 1):
                        response_text += f' {i}. {alert.get("trend_alert", "No alert description")} Suggestion: {alert.get("suggestion", "No suggestion available")}.'
                else:
                    response_text += ' No alerts available for the selected period.'
                response_text += ' That’s the overview! Let me know if you’d like more details or have other questions.'
            else:  # Follow-up response using Gemini
                # Prepare context for Gemini with detailed data
                context_data = f"Data from {start_date} to {end_date} with {time_period} granularity. Alerts: {json.dumps(alerts)}. "
                prompt = f"{context_data} User asked: {user_message}. Provide a concise response with short, precise suggestions, using **bold** for key points and newlines where needed."

                # Call Gemini API
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }]
                }
                response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
                response.raise_for_status()
                gemini_response = response.json()

                # Extract the response text from Gemini
                try:
                    response_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError) as e:
                    response_text = "Sorry, I couldn’t process that request. Please try again."

            response_data = {
                'alerts': alerts if not user_message else [],  # Pass back alerts for initial response
                'response': response_text
            }
            return JsonResponse(response_data)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'API request failed: {str(e)}'}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid date format: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
    return HttpResponse('You are not authorized to view this page', status=403)