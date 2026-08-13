from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CropForm, WorkerForm, EquipmentForm, FarmForm, CustomerForm, FertilizerForm, FertilizerUsageForm, EquipmentAssignmentForm, EquipmentMaintenanceForm, CropWorkerForm, HarvestForm, HarvestWorkerForm, SaleForm, SaleItemForm
from .models import Crop, Worker, Equipment, Farm, Customer, Fertilizer, FertilizerUsage, EquipmentAssignment, EquipmentMaintenance, CropWorker, Harvest, HarvestWorker, Sale, SaleItem
from django.db.models import Q

class FarmLoginView(LoginView):
    template_name = "farm/login.html"


class FarmLogoutView(LogoutView):
    next_page = "/login/"


@login_required
def dashboard(request):
    return render(request, "farm/dashboard.html")

@login_required
@permission_required("farm.view_crop", raise_exception=True)
def crop_list(request):
    crops = Crop.objects.select_related("farm").all()

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    if search:
        crops = crops.filter(
            crop_type__icontains=search
        )

    if status:
        crops = crops.filter(status=status)

    statuses = (
        Crop.objects
        .values_list("status", flat=True)
        .distinct()
        .order_by("status")
    )

    return render(
        request,
        "farm/crop_list.html",
        {
            "crops": crops,
            "statuses": statuses,
            "search": search,
            "selected_status": status,
        },
    )

@login_required
@permission_required("farm.add_crop", raise_exception=True)
def crop_create(request):
    if request.method == "POST":
        form = CropForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("crop_list")
    else:
        form = CropForm()

    return render(
        request,
        "farm/crop_form.html",
        {
            "form": form,
            "title": "Add Crop",
        },
    )

@login_required
@permission_required("farm.change_crop", raise_exception=True)
def crop_update(request, crop_id):
    crop = get_object_or_404(Crop, crop_id=crop_id)

    if request.method == "POST":
        form = CropForm(request.POST, instance=crop)

        if form.is_valid():
            form.save()
            return redirect("crop_list")
    else:
        form = CropForm(instance=crop)

    return render(
        request,
        "farm/crop_form.html",
        {
            "form": form,
            "title": "Edit Crop",
        },
    )


@login_required
@permission_required("farm.delete_crop", raise_exception=True)
def crop_delete(request, crop_id):
    crop = get_object_or_404(Crop, crop_id=crop_id)

    if request.method == "POST":
        crop.delete()
        return redirect("crop_list")

    return render(
        request,
        "farm/crop_confirm_delete.html",
        {
            "crop": crop,
        },
    )


@login_required
@permission_required("farm.view_worker", raise_exception=True)
def worker_list(request):
    workers = Worker.objects.all()

    search = request.GET.get("search", "").strip()

    if search:
        workers = workers.filter(
            fname__icontains=search
        ) | workers.filter(
            lname__icontains=search
        ) | workers.filter(
            employee_id__icontains=search
        )

    return render(
        request,
        "farm/worker_list.html",
        {
            "workers": workers,
            "search": search,
        },
    )


@login_required
@permission_required("farm.add_worker", raise_exception=True)
def worker_create(request):
    if request.method == "POST":
        form = WorkerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("worker_list")
    else:
        form = WorkerForm()

    return render(
        request,
        "farm/worker_form.html",
        {
            "form": form,
            "title": "Add Worker",
        },
    )


@login_required
@permission_required("farm.change_worker", raise_exception=True)
def worker_update(request, worker_id):
    worker = get_object_or_404(
        Worker,
        worker_id=worker_id
    )

    if request.method == "POST":
        form = WorkerForm(
            request.POST,
            instance=worker
        )

        if form.is_valid():
            form.save()
            return redirect("worker_list")
    else:
        form = WorkerForm(instance=worker)

    return render(
        request,
        "farm/worker_form.html",
        {
            "form": form,
            "title": "Edit Worker",
        },
    )


@login_required
@permission_required("farm.delete_worker", raise_exception=True)
def worker_delete(request, worker_id):
    worker = get_object_or_404(
        Worker,
        worker_id=worker_id
    )

    if request.method == "POST":
        worker.delete()
        return redirect("worker_list")

    return render(
        request,
        "farm/worker_confirm_delete.html",
        {
            "worker": worker,
        },
    )


@login_required
@permission_required("farm.view_equipment", raise_exception=True)
def equipment_list(request):
    equipment = Equipment.objects.all()

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    if search:
        equipment = equipment.filter(
            equipment_name__icontains=search
        ) | equipment.filter(
            equipment_type__icontains=search
        )

    if status:
        equipment = equipment.filter(status=status)

    statuses = (
        Equipment.objects
        .values_list("status", flat=True)
        .distinct()
        .order_by("status")
    )

    return render(
        request,
        "farm/equipment_list.html",
        {
            "equipment": equipment,
            "statuses": statuses,
            "search": search,
            "selected_status": status,
        },
    )


@login_required
@permission_required("farm.add_equipment", raise_exception=True)
def equipment_create(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("equipment_list")
    else:
        form = EquipmentForm()

    return render(
        request,
        "farm/equipment_form.html",
        {
            "form": form,
            "title": "Add Equipment",
        },
    )


@login_required
@permission_required("farm.change_equipment", raise_exception=True)
def equipment_update(request, equipment_id):
    equipment = get_object_or_404(
        Equipment,
        equipment_id=equipment_id
    )

    if request.method == "POST":
        form = EquipmentForm(
            request.POST,
            instance=equipment
        )

        if form.is_valid():
            form.save()
            return redirect("equipment_list")
    else:
        form = EquipmentForm(instance=equipment)

    return render(
        request,
        "farm/equipment_form.html",
        {
            "form": form,
            "title": "Edit Equipment",
        },
    )


@login_required
@permission_required("farm.delete_equipment", raise_exception=True)
def equipment_delete(request, equipment_id):
    equipment = get_object_or_404(
        Equipment,
        equipment_id=equipment_id
    )

    if request.method == "POST":
        equipment.delete()
        return redirect("equipment_list")

    return render(
        request,
        "farm/equipment_confirm_delete.html",
        {
            "equipment": equipment,
        },
    )


@login_required
@permission_required("farm.view_farm", raise_exception=True)
def farm_list(request):
    search = request.GET.get("search", "").strip()
    location = request.GET.get("location", "").strip()

    farms = Farm.objects.all().order_by("farm_name")

    if search:
        farms = farms.filter(
            Q(farm_name__icontains=search)
            | Q(location__icontains=search)
        )

    if location:
        farms = farms.filter(location__icontains=location)

    locations = (
        Farm.objects
        .values_list("location", flat=True)
        .distinct()
        .order_by("location")
    )

    return render(
        request,
        "farm/farm_list.html",
        {
            "farms": farms,
            "search": search,
            "location": location,
            "locations": locations,
        },
    )

@login_required
@permission_required("farm.add_farm", raise_exception=True)
def farm_create(request):
    if request.method == "POST":
        form = FarmForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("farm_list")
    else:
        form = FarmForm()

    return render(
        request,
        "farm/farm_form.html",
        {
            "form": form,
            "title": "Add Farm",
        },
    )


@login_required
@permission_required("farm.change_farm", raise_exception=True)
def farm_update(request, farm_id):
    farm = get_object_or_404(Farm, farm_id=farm_id)

    if request.method == "POST":
        form = FarmForm(request.POST, instance=farm)

        if form.is_valid():
            form.save()
            return redirect("farm_list")
    else:
        form = FarmForm(instance=farm)

    return render(
        request,
        "farm/farm_form.html",
        {
            "form": form,
            "title": "Edit Farm",
        },
    )


@login_required
@permission_required("farm.delete_farm", raise_exception=True)
def farm_delete(request, farm_id):
    farm = get_object_or_404(Farm, farm_id=farm_id)

    if request.method == "POST":
        farm.delete()
        return redirect("farm_list")

    return render(
        request,
        "farm/farm_confirm_delete.html",
        {"farm": farm},
    )


@login_required
@permission_required("farm.view_customer", raise_exception=True)
def customer_list(request):
    search = request.GET.get("search", "").strip()
    address = request.GET.get("address", "").strip()

    customers = Customer.objects.all().order_by("full_name")

    if search:
        customers = customers.filter(
            Q(full_name__icontains=search)
            | Q(contact_details__icontains=search)
            | Q(address__icontains=search)
        )

    if address:
        customers = customers.filter(
            address__icontains=address
        )

    addresses = (
        Customer.objects
        .values_list("address", flat=True)
        .distinct()
        .order_by("address")
    )

    return render(
        request,
        "farm/customer_list.html",
        {
            "customers": customers,
            "search": search,
            "address": address,
            "addresses": addresses,
        },
    )


@login_required
@permission_required("farm.add_customer", raise_exception=True)
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm()

    return render(
        request,
        "farm/customer_form.html",
        {
            "form": form,
            "title": "Add Customer",
        },
    )


@login_required
@permission_required("farm.change_customer", raise_exception=True)
def customer_update(request, customer_id):
    customer = get_object_or_404(
        Customer,
        customer_id=customer_id,
    )

    if request.method == "POST":
        form = CustomerForm(
            request.POST,
            instance=customer,
        )

        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)

    return render(
        request,
        "farm/customer_form.html",
        {
            "form": form,
            "title": "Edit Customer",
        },
    )


@login_required
@permission_required("farm.delete_customer", raise_exception=True)
def customer_delete(request, customer_id):
    customer = get_object_or_404(
        Customer,
        customer_id=customer_id,
    )

    if request.method == "POST":
        customer.delete()
        return redirect("customer_list")

    return render(
        request,
        "farm/customer_confirm_delete.html",
        {
            "customer": customer,
        },
    )



@login_required
@permission_required("farm.view_fertilizer", raise_exception=True)
def fertilizer_list(request):
    search = request.GET.get("search", "").strip()
    unit = request.GET.get("unit", "").strip()

    fertilizers = Fertilizer.objects.all().order_by("fertilizer_type")

    if search:
        fertilizers = fertilizers.filter(
            fertilizer_type__icontains=search
        )

    if unit:
        fertilizers = fertilizers.filter(unit=unit)

    units = (
        Fertilizer.objects
        .values_list("unit", flat=True)
        .distinct()
        .order_by("unit")
    )

    return render(
        request,
        "farm/fertilizer_list.html",
        {
            "fertilizers": fertilizers,
            "search": search,
            "unit": unit,
            "units": units,
        },
    )


@login_required
@permission_required("farm.add_fertilizer", raise_exception=True)
def fertilizer_create(request):
    if request.method == "POST":
        form = FertilizerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("fertilizer_list")
    else:
        form = FertilizerForm()

    return render(
        request,
        "farm/fertilizer_form.html",
        {
            "form": form,
            "title": "Add Fertilizer",
        },
    )


@login_required
@permission_required("farm.change_fertilizer", raise_exception=True)
def fertilizer_update(request, fertilizer_id):
    fertilizer = get_object_or_404(
        Fertilizer,
        fertilizer_id=fertilizer_id,
    )

    if request.method == "POST":
        form = FertilizerForm(
            request.POST,
            instance=fertilizer,
        )

        if form.is_valid():
            form.save()
            return redirect("fertilizer_list")
    else:
        form = FertilizerForm(instance=fertilizer)

    return render(
        request,
        "farm/fertilizer_form.html",
        {
            "form": form,
            "title": "Edit Fertilizer",
        },
    )


@login_required
@permission_required("farm.delete_fertilizer", raise_exception=True)
def fertilizer_delete(request, fertilizer_id):
    fertilizer = get_object_or_404(
        Fertilizer,
        fertilizer_id=fertilizer_id,
    )

    if request.method == "POST":
        fertilizer.delete()
        return redirect("fertilizer_list")

    return render(
        request,
        "farm/fertilizer_confirm_delete.html",
        {
            "fertilizer": fertilizer,
        },
    )



@login_required
@permission_required("farm.view_fertilizerusage", raise_exception=True)
def fertilizer_usage_list(request):
    search = request.GET.get("search", "").strip()
    fertilizer_id = request.GET.get("fertilizer", "").strip()
    crop_id = request.GET.get("crop", "").strip()

    usages = (
        FertilizerUsage.objects
        .select_related("fertilizer", "crop")
        .order_by("-usage_date")
    )

    if search:
        usages = usages.filter(
            Q(fertilizer__fertilizer_type__icontains=search)
            | Q(crop__crop_type__icontains=search)
        )

    if fertilizer_id:
        usages = usages.filter(fertilizer_id=fertilizer_id)

    if crop_id:
        usages = usages.filter(crop_id=crop_id)

    fertilizers = Fertilizer.objects.all().order_by("fertilizer_type")
    crops = Crop.objects.all().order_by("crop_type")

    return render(
        request,
        "farm/fertilizer_usage_list.html",
        {
            "usages": usages,
            "fertilizers": fertilizers,
            "crops": crops,
            "search": search,
            "fertilizer_id": fertilizer_id,
            "crop_id": crop_id,
        },
    )


@login_required
@permission_required("farm.add_fertilizerusage", raise_exception=True)
def fertilizer_usage_create(request):
    if request.method == "POST":
        form = FertilizerUsageForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("fertilizer_usage_list")
    else:
        form = FertilizerUsageForm()

    return render(
        request,
        "farm/fertilizer_usage_form.html",
        {
            "form": form,
            "title": "Add Fertilizer Usage",
        },
    )


@login_required
@permission_required("farm.change_fertilizerusage", raise_exception=True)
def fertilizer_usage_update(request, usage_id):
    usage = get_object_or_404(
        FertilizerUsage,
        usage_id=usage_id,
    )

    if request.method == "POST":
        form = FertilizerUsageForm(
            request.POST,
            instance=usage,
        )

        if form.is_valid():
            form.save()
            return redirect("fertilizer_usage_list")
    else:
        form = FertilizerUsageForm(instance=usage)

    return render(
        request,
        "farm/fertilizer_usage_form.html",
        {
            "form": form,
            "title": "Edit Fertilizer Usage",
        },
    )


@login_required
@permission_required("farm.delete_fertilizerusage", raise_exception=True)
def fertilizer_usage_delete(request, usage_id):
    usage = get_object_or_404(
        FertilizerUsage,
        usage_id=usage_id,
    )

    if request.method == "POST":
        usage.delete()
        return redirect("fertilizer_usage_list")

    return render(
        request,
        "farm/fertilizer_usage_confirm_delete.html",
        {
            "usage": usage,
        },
    )


@login_required
@permission_required(
    "farm.view_equipmentassignment",
    raise_exception=True,
)
def equipment_assignment_list(request):
    search = request.GET.get("search", "").strip()
    equipment_id = request.GET.get("equipment", "").strip()
    worker_id = request.GET.get("worker", "").strip()

    assignments = (
        EquipmentAssignment.objects
        .select_related("equipment", "worker")
        .order_by("-assigned_date")
    )

    if search:
        assignments = assignments.filter(
            Q(equipment__equipment_name__icontains=search)
            | Q(worker__fname__icontains=search)
            | Q(worker__lname__icontains=search)
            | Q(worker__employee_id__icontains=search)
        )

    if equipment_id:
        assignments = assignments.filter(
            equipment_id=equipment_id
        )

    if worker_id:
        assignments = assignments.filter(
            worker_id=worker_id
        )

    equipment = Equipment.objects.all().order_by("equipment_name")
    workers = Worker.objects.all().order_by("fname", "lname")

    return render(
        request,
        "farm/equipment_assignment_list.html",
        {
            "assignments": assignments,
            "equipment": equipment,
            "workers": workers,
            "search": search,
            "equipment_id": equipment_id,
            "worker_id": worker_id,
        },
    )


@login_required
@permission_required(
    "farm.add_equipmentassignment",
    raise_exception=True,
)
def equipment_assignment_create(request):
    if request.method == "POST":
        form = EquipmentAssignmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("equipment_assignment_list")
    else:
        form = EquipmentAssignmentForm()

    return render(
        request,
        "farm/equipment_assignment_form.html",
        {
            "form": form,
            "title": "Add Equipment Assignment",
        },
    )


@login_required
@permission_required(
    "farm.change_equipmentassignment",
    raise_exception=True,
)
def equipment_assignment_update(request, assignment_id):
    assignment = get_object_or_404(
        EquipmentAssignment,
        assignment_id=assignment_id,
    )

    if request.method == "POST":
        form = EquipmentAssignmentForm(
            request.POST,
            instance=assignment,
        )

        if form.is_valid():
            form.save()
            return redirect("equipment_assignment_list")
    else:
        form = EquipmentAssignmentForm(instance=assignment)

    return render(
        request,
        "farm/equipment_assignment_form.html",
        {
            "form": form,
            "title": "Edit Equipment Assignment",
        },
    )


@login_required
@permission_required(
    "farm.delete_equipmentassignment",
    raise_exception=True,
)
def equipment_assignment_delete(request, assignment_id):
    assignment = get_object_or_404(
        EquipmentAssignment,
        assignment_id=assignment_id,
    )

    if request.method == "POST":
        assignment.delete()
        return redirect("equipment_assignment_list")

    return render(
        request,
        "farm/equipment_assignment_confirm_delete.html",
        {
            "assignment": assignment,
        },
    )



@login_required
@permission_required(
    "farm.view_equipmentmaintenance",
    raise_exception=True,
)
def equipment_maintenance_list(request):
    search = request.GET.get("search", "").strip()
    equipment_id = request.GET.get("equipment", "").strip()
    status = request.GET.get("status", "").strip()

    maintenances = (
        EquipmentMaintenance.objects
        .select_related("equipment")
        .order_by("-maintenance_date")
    )

    if search:
        maintenances = maintenances.filter(
            Q(equipment__equipment_name__icontains=search)
            | Q(description__icontains=search)
        )

    if equipment_id:
        maintenances = maintenances.filter(
            equipment_id=equipment_id
        )

    if status:
        maintenances = maintenances.filter(status=status)

    equipment = Equipment.objects.all().order_by("equipment_name")

    statuses = (
        EquipmentMaintenance.objects
        .values_list("status", flat=True)
        .distinct()
        .order_by("status")
    )

    return render(
        request,
        "farm/equipment_maintenance_list.html",
        {
            "maintenances": maintenances,
            "equipment": equipment,
            "statuses": statuses,
            "search": search,
            "equipment_id": equipment_id,
            "status": status,
        },
    )


@login_required
@permission_required(
    "farm.add_equipmentmaintenance",
    raise_exception=True,
)
def equipment_maintenance_create(request):
    if request.method == "POST":
        form = EquipmentMaintenanceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("equipment_maintenance_list")
    else:
        form = EquipmentMaintenanceForm()

    return render(
        request,
        "farm/equipment_maintenance_form.html",
        {
            "form": form,
            "title": "Add Equipment Maintenance",
        },
    )


@login_required
@permission_required(
    "farm.change_equipmentmaintenance",
    raise_exception=True,
)
def equipment_maintenance_update(request, maintenance_id):
    maintenance = get_object_or_404(
        EquipmentMaintenance,
        maintenance_id=maintenance_id,
    )

    if request.method == "POST":
        form = EquipmentMaintenanceForm(
            request.POST,
            instance=maintenance,
        )

        if form.is_valid():
            form.save()
            return redirect("equipment_maintenance_list")
    else:
        form = EquipmentMaintenanceForm(instance=maintenance)

    return render(
        request,
        "farm/equipment_maintenance_form.html",
        {
            "form": form,
            "title": "Edit Equipment Maintenance",
        },
    )


@login_required
@permission_required(
    "farm.delete_equipmentmaintenance",
    raise_exception=True,
)
def equipment_maintenance_delete(request, maintenance_id):
    maintenance = get_object_or_404(
        EquipmentMaintenance,
        maintenance_id=maintenance_id,
    )

    if request.method == "POST":
        maintenance.delete()
        return redirect("equipment_maintenance_list")

    return render(
        request,
        "farm/equipment_maintenance_confirm_delete.html",
        {
            "maintenance": maintenance,
        },
    )



@login_required
@permission_required(
    "farm.view_cropworker",
    raise_exception=True,
)
def crop_worker_list(request):
    search = request.GET.get("search", "").strip()
    crop_id = request.GET.get("crop", "").strip()
    worker_id = request.GET.get("worker", "").strip()
    task_role = request.GET.get("task_role", "").strip()

    assignments = (
        CropWorker.objects
        .select_related("crop", "worker")
        .order_by("-assigned_date")
    )

    if search:
        assignments = assignments.filter(
            Q(crop__crop_type__icontains=search)
            | Q(crop__plot_number__icontains=search)
            | Q(worker__fname__icontains=search)
            | Q(worker__lname__icontains=search)
            | Q(task_role__icontains=search)
        )

    if crop_id:
        assignments = assignments.filter(
            crop_id=crop_id
        )

    if worker_id:
        assignments = assignments.filter(
            worker_id=worker_id
        )

    if task_role:
        assignments = assignments.filter(
            task_role=task_role
        )

    crops = Crop.objects.all().order_by(
        "crop_type",
        "plot_number",
    )

    workers = Worker.objects.all().order_by(
        "fname",
        "lname",
    )

    task_roles = (
        CropWorker.objects
        .values_list("task_role", flat=True)
        .distinct()
        .order_by("task_role")
    )

    return render(
        request,
        "farm/crop_worker_list.html",
        {
            "assignments": assignments,
            "crops": crops,
            "workers": workers,
            "task_roles": task_roles,
            "search": search,
            "crop_id": crop_id,
            "worker_id": worker_id,
            "task_role": task_role,
        },
    )


@login_required
@permission_required(
    "farm.add_cropworker",
    raise_exception=True,
)
def crop_worker_create(request):
    if request.method == "POST":
        form = CropWorkerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("crop_worker_list")
    else:
        form = CropWorkerForm()

    return render(
        request,
        "farm/crop_worker_form.html",
        {
            "form": form,
            "title": "Add Crop Worker",
        },
    )


@login_required
@permission_required(
    "farm.change_cropworker",
    raise_exception=True,
)
def crop_worker_update(request, crop_worker_id):
    assignment = get_object_or_404(
        CropWorker,
        crop_worker_id=crop_worker_id,
    )

    if request.method == "POST":
        form = CropWorkerForm(
            request.POST,
            instance=assignment,
        )

        if form.is_valid():
            form.save()
            return redirect("crop_worker_list")
    else:
        form = CropWorkerForm(instance=assignment)

    return render(
        request,
        "farm/crop_worker_form.html",
        {
            "form": form,
            "title": "Edit Crop Worker",
        },
    )


@login_required
@permission_required(
    "farm.delete_cropworker",
    raise_exception=True,
)
def crop_worker_delete(request, crop_worker_id):
    assignment = get_object_or_404(
        CropWorker,
        crop_worker_id=crop_worker_id,
    )

    if request.method == "POST":
        assignment.delete()
        return redirect("crop_worker_list")

    return render(
        request,
        "farm/crop_worker_confirm_delete.html",
        {
            "assignment": assignment,
        },
    )


@login_required
@permission_required(
    "farm.view_harvest",
    raise_exception=True,
)
def harvest_list(request):
    search = request.GET.get("search", "").strip()
    crop_id = request.GET.get("crop", "").strip()

    harvests = (
        Harvest.objects
        .select_related("crop")
        .order_by("-harvest_date")
    )

    if search:
        harvests = harvests.filter(
            Q(crop__crop_type__icontains=search)
            | Q(crop__plot_number__icontains=search)
        )

    if crop_id:
        harvests = harvests.filter(
            crop_id=crop_id
        )

    crops = Crop.objects.all().order_by(
        "crop_type",
        "plot_number",
    )

    return render(
        request,
        "farm/harvest_list.html",
        {
            "harvests": harvests,
            "crops": crops,
            "search": search,
            "crop_id": crop_id,
        },
    )


@login_required
@permission_required(
    "farm.add_harvest",
    raise_exception=True,
)
def harvest_create(request):
    if request.method == "POST":
        form = HarvestForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("harvest_list")
    else:
        form = HarvestForm()

    return render(
        request,
        "farm/harvest_form.html",
        {
            "form": form,
            "title": "Add Harvest",
        },
    )


@login_required
@permission_required(
    "farm.change_harvest",
    raise_exception=True,
)
def harvest_update(request, harvest_id):
    harvest = get_object_or_404(
        Harvest,
        harvest_id=harvest_id,
    )

    if request.method == "POST":
        form = HarvestForm(
            request.POST,
            instance=harvest,
        )

        if form.is_valid():
            form.save()
            return redirect("harvest_list")
    else:
        form = HarvestForm(instance=harvest)

    return render(
        request,
        "farm/harvest_form.html",
        {
            "form": form,
            "title": "Edit Harvest",
        },
    )


@login_required
@permission_required(
    "farm.delete_harvest",
    raise_exception=True,
)
def harvest_delete(request, harvest_id):
    harvest = get_object_or_404(
        Harvest,
        harvest_id=harvest_id,
    )

    if request.method == "POST":
        harvest.delete()
        return redirect("harvest_list")

    return render(
        request,
        "farm/harvest_confirm_delete.html",
        {
            "harvest": harvest,
        },
    )


@login_required
@permission_required(
    "farm.view_harvestworker",
    raise_exception=True,
)
def harvest_worker_list(request):
    search = request.GET.get("search", "").strip()
    harvest_id = request.GET.get("harvest", "").strip()
    worker_id = request.GET.get("worker", "").strip()
    task_role = request.GET.get("task_role", "").strip()

    assignments = (
        HarvestWorker.objects
        .select_related("harvest", "harvest__crop", "worker")
        .order_by("-assigned_date")
    )

    if search:
        assignments = assignments.filter(
            Q(harvest__crop__crop_type__icontains=search)
            | Q(harvest__crop__plot_number__icontains=search)
            | Q(worker__fname__icontains=search)
            | Q(worker__lname__icontains=search)
            | Q(task_role__icontains=search)
        )

    if harvest_id:
        assignments = assignments.filter(
            harvest_id=harvest_id
        )

    if worker_id:
        assignments = assignments.filter(
            worker_id=worker_id
        )

    if task_role:
        assignments = assignments.filter(
            task_role=task_role
        )

    harvests = (
        Harvest.objects
        .select_related("crop")
        .order_by("-harvest_date")
    )

    workers = Worker.objects.all().order_by(
        "fname",
        "lname",
    )

    task_roles = (
        HarvestWorker.objects
        .values_list("task_role", flat=True)
        .distinct()
        .order_by("task_role")
    )

    return render(
        request,
        "farm/harvest_worker_list.html",
        {
            "assignments": assignments,
            "harvests": harvests,
            "workers": workers,
            "task_roles": task_roles,
            "search": search,
            "harvest_id": harvest_id,
            "worker_id": worker_id,
            "task_role": task_role,
        },
    )


@login_required
@permission_required(
    "farm.add_harvestworker",
    raise_exception=True,
)
def harvest_worker_create(request):
    if request.method == "POST":
        form = HarvestWorkerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("harvest_worker_list")
    else:
        form = HarvestWorkerForm()

    return render(
        request,
        "farm/harvest_worker_form.html",
        {
            "form": form,
            "title": "Add Harvest Worker",
        },
    )


@login_required
@permission_required(
    "farm.change_harvestworker",
    raise_exception=True,
)
def harvest_worker_update(request, harvest_worker_id):
    assignment = get_object_or_404(
        HarvestWorker,
        harvest_worker_id=harvest_worker_id,
    )

    if request.method == "POST":
        form = HarvestWorkerForm(
            request.POST,
            instance=assignment,
        )

        if form.is_valid():
            form.save()
            return redirect("harvest_worker_list")
    else:
        form = HarvestWorkerForm(instance=assignment)

    return render(
        request,
        "farm/harvest_worker_form.html",
        {
            "form": form,
            "title": "Edit Harvest Worker",
        },
    )


@login_required
@permission_required(
    "farm.delete_harvestworker",
    raise_exception=True,
)
def harvest_worker_delete(request, harvest_worker_id):
    assignment = get_object_or_404(
        HarvestWorker,
        harvest_worker_id=harvest_worker_id,
    )

    if request.method == "POST":
        assignment.delete()
        return redirect("harvest_worker_list")

    return render(
        request,
        "farm/harvest_worker_confirm_delete.html",
        {
            "assignment": assignment,
        },
    )


@login_required
@permission_required(
    "farm.view_sale",
    raise_exception=True,
)
def sale_list(request):
    search = request.GET.get("search", "").strip()
    customer_id = request.GET.get("customer", "").strip()

    sales = (
        Sale.objects
        .select_related("customer")
        .order_by("-sale_date")
    )

    if search:
        sales = sales.filter(
            Q(customer__full_name__icontains=search)
            | Q(customer__contact_details__icontains=search)
            | Q(customer__address__icontains=search)
            | Q(invoice_number__icontains=search)
        )

    if customer_id:
        sales = sales.filter(
            customer_id=customer_id
        )

    customers = Customer.objects.all().order_by("full_name")

    return render(
        request,
        "farm/sale_list.html",
        {
            "sales": sales,
            "customers": customers,
            "search": search,
            "customer_id": customer_id,
        },
    )


@login_required
@permission_required(
    "farm.add_sale",
    raise_exception=True,
)
def sale_create(request):
    if request.method == "POST":
        form = SaleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("sale_list")
    else:
        form = SaleForm()

    return render(
        request,
        "farm/sale_form.html",
        {
            "form": form,
            "title": "Add Sale",
        },
    )


@login_required
@permission_required(
    "farm.change_sale",
    raise_exception=True,
)
def sale_update(request, sale_id):
    sale = get_object_or_404(
        Sale,
        sale_id=sale_id,
    )

    if request.method == "POST":
        form = SaleForm(
            request.POST,
            instance=sale,
        )

        if form.is_valid():
            form.save()
            return redirect("sale_list")
    else:
        form = SaleForm(instance=sale)

    return render(
        request,
        "farm/sale_form.html",
        {
            "form": form,
            "title": "Edit Sale",
        },
    )


@login_required
@permission_required(
    "farm.delete_sale",
    raise_exception=True,
)
def sale_delete(request, sale_id):
    sale = get_object_or_404(
        Sale,
        sale_id=sale_id,
    )

    if request.method == "POST":
        sale.delete()
        return redirect("sale_list")

    return render(
        request,
        "farm/sale_confirm_delete.html",
        {
            "sale": sale,
        },
    )


@login_required
@permission_required(
    "farm.view_saleitem",
    raise_exception=True,
)
def sale_item_list(request):
    search = request.GET.get("search", "").strip()
    sale_id = request.GET.get("sale", "").strip()
    harvest_id = request.GET.get("harvest", "").strip()

    sale_items = (
        SaleItem.objects
        .select_related(
            "sale",
            "sale__customer",
            "harvest",
            "harvest__crop",
        )
        .order_by("-sale__sale_date", "sale_item_id")
    )

    if search:
        sale_items = sale_items.filter(
            Q(sale__invoice_number__icontains=search)
            | Q(sale__customer__full_name__icontains=search)
            | Q(harvest__crop__crop_type__icontains=search)
            | Q(harvest__crop__plot_number__icontains=search)
        )

    if sale_id:
        sale_items = sale_items.filter(
            sale_id=sale_id
        )

    if harvest_id:
        sale_items = sale_items.filter(
            harvest_id=harvest_id
        )

    sales = (
        Sale.objects
        .select_related("customer")
        .order_by("-sale_date")
    )

    harvests = (
        Harvest.objects
        .select_related("crop")
        .order_by("-harvest_date")
    )

    return render(
        request,
        "farm/sale_item_list.html",
        {
            "sale_items": sale_items,
            "sales": sales,
            "harvests": harvests,
            "search": search,
            "sale_id": sale_id,
            "harvest_id": harvest_id,
        },
    )


@login_required
@permission_required(
    "farm.add_saleitem",
    raise_exception=True,
)
def sale_item_create(request):
    if request.method == "POST":
        form = SaleItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("sale_item_list")
    else:
        form = SaleItemForm()

    return render(
        request,
        "farm/sale_item_form.html",
        {
            "form": form,
            "title": "Add Sale Item",
        },
    )


@login_required
@permission_required(
    "farm.change_saleitem",
    raise_exception=True,
)
def sale_item_update(request, sale_item_id):
    sale_item = get_object_or_404(
        SaleItem,
        sale_item_id=sale_item_id,
    )

    if request.method == "POST":
        form = SaleItemForm(
            request.POST,
            instance=sale_item,
        )

        if form.is_valid():
            form.save()
            return redirect("sale_item_list")
    else:
        form = SaleItemForm(instance=sale_item)

    return render(
        request,
        "farm/sale_item_form.html",
        {
            "form": form,
            "title": "Edit Sale Item",
        },
    )


@login_required
@permission_required(
    "farm.delete_saleitem",
    raise_exception=True,
)
def sale_item_delete(request, sale_item_id):
    sale_item = get_object_or_404(
        SaleItem,
        sale_item_id=sale_item_id,
    )

    if request.method == "POST":
        sale_item.delete()
        return redirect("sale_item_list")

    return render(
        request,
        "farm/sale_item_confirm_delete.html",
        {
            "sale_item": sale_item,
        },
    )