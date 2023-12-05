from django.shortcuts import render, redirect, get_object_or_404
from .models import MaintenanceRequest, Tenant, StaffMember
from .forms import MaintenanceRequestForm, TenantForm  # Assuming these forms are defined in your forms.py
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import MaintenanceRequest
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime, timedelta
# Tenant Views
def submit_maintenance_request(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = MaintenanceRequestForm()
    return render(request, 'submit_request.html', {'form': form})

# Staff Views
def view_requests(request):
    requests = MaintenanceRequest.objects.all()
    # Example filter: filter by status
    status = request.GET.get('status')
    if status:
        requests = requests.filter(status=status)
    # Add more filters as needed...
    return render(request, 'view_requests.html', {'requests': requests})




# Manager Views
def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_app:manager_view')  # Redirect after successful submission
    else:
        form = TenantForm()
    return render(request, 'add_tenant.html', {'form': form})


def move_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('maintenance_app:manager_view')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'add_tenant.html', {'form': form, 'tenant': tenant})






@require_POST  # Ensures that this view can only be accessed with a POST request
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    tenant.delete()  # Delete the tenant from the database
    return redirect('maintenance_app:manager_view')  # Make sure this is the name of your manager view URL




def tenant_view(request):
    tenant_id = None
    requests = None
    apartment_number = request.GET.get('apartment_number', '')

    if apartment_number:
        try:
            tenant = Tenant.objects.get(apartment_number=apartment_number)
            tenant_id = tenant.id
        except Tenant.DoesNotExist:
            tenant_id = None

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES)
        if tenant_id:
            tenant = Tenant.objects.get(pk=tenant_id)
            if form.is_valid():
                maintenance_request = form.save(commit=False)
                maintenance_request.tenant = tenant  # Set the tenant automatically
                maintenance_request.save()
                return HttpResponseRedirect(request.path_info)  # Redirect to the same page
            else:
                print("Form Invalid", form.errors)  # Print form errors (for debugging)
        else:
            print("Tenant ID not found for given apartment number")  # Print an error message (for debugging)

    else:
        form = MaintenanceRequestForm()  # Initialize an empty form for GET request

    if tenant_id:
        requests = MaintenanceRequest.objects.filter(tenant_id=tenant_id)  # Fetch maintenance requests for the tenant

    return render(request, 'tenant_view.html', {
        'form': form,
        'requests': requests,
        'tenant_id': tenant_id
    })






def manager_view(request):
    tenants = Tenant.objects.all()  # Get all tenants
    return render(request, 'manager_view.html', {'tenants': tenants})





def homepage(request):
    return render(request, 'homepage.html')


def maintenance_view(request):
    requests = MaintenanceRequest.objects.all()

    # Filtering logic
    apartment_number = request.GET.get('apartment_number', '')
    area = request.GET.get('area', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    status = request.GET.get('status', '')

    if apartment_number:
        requests = requests.filter(tenant__apartment_number=apartment_number)
    if area:
        requests = requests.filter(problem_area=area)
    if status:
        requests = requests.filter(status=status)
    if start_date:
        start_date = parse_date(start_date)
        requests = requests.filter(request_date__gte=start_date)
    if end_date:
        end_date = parse_date(end_date)
        # Adjust to include the full day of end_date
        end_date_full_day = datetime.combine(end_date, datetime.max.time())
        requests = requests.filter(request_date__lte=end_date_full_day)

    return render(request, 'maintenance_view.html', {'requests': requests})


# Include the update_request_status view as well if not already included

@require_POST
def update_request_status(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    maintenance_request.status = 'completed'  # Directly set status to 'completed'
    maintenance_request.save()
    return redirect('maintenance_app:maintenance_view')




@require_POST
def toggle_request_status(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    if maintenance_request.status == 'pending':
        maintenance_request.status = 'completed'
    else:
        maintenance_request.status = 'pending'
    maintenance_request.save()
    return redirect('maintenance_app:maintenance_view')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import MaintenanceRequest


@require_POST  # This decorator ensures the view only handles POST requests
def delete_request(request, request_id):
    # Get the MaintenanceRequest object by its ID or return a 404 error if not found
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)

    # Optional: Check if the user has permission to delete the request
    # if not request.user.has_perm('maintenance_app.delete_maintenancerequest'):
    #     messages.error(request, 'You do not have permission to delete this request.')
    #     return redirect('maintenance_app:maintenance_view')

    # Delete the MaintenanceRequest object
    maintenance_request.delete()

    # Optional: Add a success message for feedback
    messages.success(request, 'Maintenance request deleted successfully.')

    # Redirect to the view that displays the list of maintenance requests
    return redirect('maintenance_app:maintenance_view')
