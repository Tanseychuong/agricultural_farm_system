from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Crop, Worker, Equipment, Farm, Customer, Fertilizer, FertilizerUsage, EquipmentAssignment, EquipmentMaintenance, CropWorker, Harvest, HarvestWorker, Sale, SaleItem

class CropForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=[
            ("Growing", "Growing"),
            ("Harvested", "Harvested"),
        ]
    )

    class Meta:
        model = Crop
        fields = [
            "farm",
            "crop_type",
            "planting_date",
            "expected_harvest_date",
            "status",
            "plot_number",
        ]

        widgets = {
            "planting_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "expected_harvest_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        planting_date = cleaned_data.get("planting_date")
        expected_harvest_date = cleaned_data.get("expected_harvest_date")

        if planting_date and expected_harvest_date:
            if expected_harvest_date <= planting_date:
                raise forms.ValidationError(
                    "Expected harvest date must be after planting date."
                )

        return cleaned_data


class WorkerForm(forms.ModelForm):

    job_role = forms.ChoiceField(
        choices=[
            ("Farm Worker", "Farm Worker"),
        ]
    )

    class Meta:
        model = Worker
        fields = [
            "employee_id",
            "fname",
            "lname",
            "contact_details",
            "job_role",
            "hire_date",
        ]

        widgets = {
            "hire_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"].strip()

        if not employee_id:
            raise forms.ValidationError(
                "Employee ID is required."
            )

        queryset = Worker.objects.filter(
            employee_id=employee_id
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "This employee ID already exists."
            )

        return employee_id

    def clean(self):
        cleaned_data = super().clean()

        hire_date = cleaned_data.get("hire_date")

        from datetime import date

        if hire_date and hire_date > date.today():
            self.add_error(
                "hire_date",
                "Hire date cannot be in the future."
            )

        return cleaned_data



class EquipmentForm(forms.ModelForm):

    equipment_type = forms.ChoiceField(
        choices=[
            ("Cultivator", "Cultivator"),
            ("Cutter", "Cutter"),
            ("Harrow", "Harrow"),
            ("Seeder", "Seeder"),
            ("Sprayer", "Sprayer"),
            ("Tiller", "Tiller"),
            ("Tractor", "Tractor"),
            ("Transport", "Transport"),
            ("Water Pump", "Water Pump"),
            ("Weeder", "Weeder"),
        ]
    )

    status = forms.ChoiceField(
        choices=[
            ("Available", "Available"),
            ("In Use", "In Use"),
            ("Under Maintenance", "Under Maintenance"),
        ]
    )

    def clean_equipment_name(self):
        equipment_name = self.cleaned_data["equipment_name"].strip()

        if not equipment_name:
            raise forms.ValidationError(
                "Equipment name is required."
            )

        return equipment_name

    class Meta:
        model = Equipment
        fields = [
            "equipment_name",
            "equipment_type",
            "status",
        ]


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ["farm_name", "location", "total_size"]

        widgets = {
            "farm_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter farm name",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter farm location",
                }
            ),
            "total_size": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
        }

    def clean_farm_name(self):
        farm_name = self.cleaned_data["farm_name"].strip()

        if not farm_name:
            raise forms.ValidationError(
                "Farm name is required."
            )

        return farm_name

    def clean_location(self):
        location = self.cleaned_data["location"].strip()

        if not location:
            raise forms.ValidationError(
                "Location is required."
            )

        return location

    def clean_total_size(self):
        total_size = self.cleaned_data["total_size"]

        if total_size <= 0:
            raise forms.ValidationError(
                "Farm size must be greater than 0."
            )

        return total_size



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["full_name", "contact_details", "address"]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter customer name",
                }
            ),
            "contact_details": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter contact details",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter customer address",
                }
            ),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()

        if not full_name:
            raise forms.ValidationError(
                "Customer name is required."
            )

        return full_name

    def clean_contact_details(self):
        contact_details = self.cleaned_data["contact_details"].strip()

        if not contact_details:
            raise forms.ValidationError(
                "Contact details are required."
            )

        return contact_details

    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if not address:
            raise forms.ValidationError(
                "Customer address is required."
            )

        return address



class FertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = ["fertilizer_type", "stock_level", "unit"]

        widgets = {
            "fertilizer_type": forms.TextInput(
                attrs={
                    "placeholder": "Enter fertilizer type",
                }
            ),
            "stock_level": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Enter stock level",
                }
            ),
            "unit": forms.Select(
                choices=[
                    ("kg", "kg"),
                    ("litre", "litre"),
                ]
            ),
        }

    def clean_fertilizer_type(self):
        fertilizer_type = self.cleaned_data["fertilizer_type"].strip()

        if not fertilizer_type:
            raise forms.ValidationError(
                "Fertilizer type is required."
            )

        return fertilizer_type

    def clean_stock_level(self):
        stock_level = self.cleaned_data["stock_level"]

        if stock_level < 0:
            raise forms.ValidationError(
                "Stock level cannot be negative."
            )

        return stock_level

    def clean_unit(self):
        unit = self.cleaned_data["unit"].strip()

        if unit not in ["kg", "litre"]:
            raise forms.ValidationError(
                "Unit must be either kg or litre."
            )

        return unit



class FertilizerUsageForm(forms.ModelForm):
    class Meta:
        model = FertilizerUsage
        fields = [
            "fertilizer",
            "crop",
            "quantity_used",
            "usage_date",
        ]

        widgets = {
            "fertilizer": forms.Select(),
            "crop": forms.Select(),
            "quantity_used": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Enter quantity used",
                }
            ),
            "usage_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_quantity_used(self):
        quantity_used = self.cleaned_data["quantity_used"]

        if quantity_used <= 0:
            raise forms.ValidationError(
                "Quantity used must be greater than zero."
            )

        return quantity_used

    def clean_usage_date(self):
        usage_date = self.cleaned_data["usage_date"]

        from django.utils import timezone

        if usage_date > timezone.localdate():
            raise forms.ValidationError(
                "Usage date cannot be in the future."
            )

        return usage_date



class EquipmentAssignmentForm(forms.ModelForm):
    class Meta:
        model = EquipmentAssignment
        fields = [
            "equipment",
            "worker",
            "assigned_date",
            "return_date",
        ]

        widgets = {
            "equipment": forms.Select(),
            "worker": forms.Select(),
            "assigned_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "return_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        assigned_date = cleaned_data.get("assigned_date")
        return_date = cleaned_data.get("return_date")

        from django.utils import timezone

        today = timezone.localdate()

        if assigned_date and assigned_date > today:
            self.add_error(
                "assigned_date",
                "Assignment date cannot be in the future.",
            )

        if return_date and return_date > today:
            self.add_error(
                "return_date",
                "Return date cannot be in the future.",
            )

        if (
            assigned_date
            and return_date
            and return_date < assigned_date
        ):
            self.add_error(
                "return_date",
                "Return date cannot be earlier than the assignment date.",
            )

        return cleaned_data



class EquipmentMaintenanceForm(forms.ModelForm):
    class Meta:
        model = EquipmentMaintenance
        fields = [
            "equipment",
            "maintenance_date",
            "description",
            "status",
        ]

        widgets = {
            "equipment": forms.Select(),

            "maintenance_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Enter maintenance description",
                }
            ),

            "status": forms.Select(
                choices=[
                    ("Completed", "Completed"),
                    ("Scheduled", "Scheduled"),
                ]
            ),
        }

    def clean_maintenance_date(self):
        maintenance_date = self.cleaned_data["maintenance_date"]

        from django.utils import timezone

        if maintenance_date > timezone.localdate():
            raise forms.ValidationError(
                "Maintenance date cannot be in the future."
            )

        return maintenance_date

    def clean_status(self):
        status = self.cleaned_data["status"].strip()

        allowed_statuses = [
            "Completed",
            "Scheduled",
        ]

        if status not in allowed_statuses:
            raise forms.ValidationError(
                "Status must be either Completed or Scheduled."
            )

        return status

    def clean_description(self):
        description = self.cleaned_data["description"].strip()

        if not description:
            raise forms.ValidationError(
                "Maintenance description is required."
            )

        return description


class CropWorkerForm(forms.ModelForm):
    class Meta:
        model = CropWorker
        fields = [
            "crop",
            "worker",
            "assigned_date",
            "task_role",
        ]

        widgets = {
            "crop": forms.Select(),
            "worker": forms.Select(),
            "assigned_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "task_role": forms.Select(
                choices=[
                    ("Crop Care", "Crop Care"),
                    ("Field Preparation", "Field Preparation"),
                ]
            ),
        }

    def clean_assigned_date(self):
        assigned_date = self.cleaned_data["assigned_date"]

        from django.utils import timezone

        if assigned_date > timezone.localdate():
            raise forms.ValidationError(
                "Assigned date cannot be in the future."
            )

        return assigned_date

    def clean_task_role(self):
        task_role = self.cleaned_data["task_role"].strip()

        allowed_roles = [
            "Crop Care",
            "Field Preparation",
        ]

        if task_role not in allowed_roles:
            raise forms.ValidationError(
                "Task role must be either Crop Care or Field Preparation."
            )

        return task_role

    def clean(self):
        cleaned_data = super().clean()

        crop = cleaned_data.get("crop")
        worker = cleaned_data.get("worker")
        assigned_date = cleaned_data.get("assigned_date")

        if crop and worker and assigned_date:
            existing_assignment = (
                CropWorker.objects
                .filter(
                    crop=crop,
                    worker=worker,
                    assigned_date=assigned_date,
                )
                .exclude(
                    pk=self.instance.pk
                )
                .exists()
            )

            if existing_assignment:
                raise forms.ValidationError(
                    "This worker is already assigned to this crop "
                    "on this date."
                )

        return cleaned_data



class HarvestForm(forms.ModelForm):
    class Meta:
        model = Harvest
        fields = [
            "crop",
            "harvest_date",
            "quantity",
        ]

        widgets = {
            "crop": forms.Select(),

            "harvest_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Enter harvest quantity",
                }
            ),
        }

    def clean_harvest_date(self):
        harvest_date = self.cleaned_data["harvest_date"]

        from django.utils import timezone

        if harvest_date > timezone.localdate():
            raise forms.ValidationError(
                "Harvest date cannot be in the future."
            )

        return harvest_date

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity <= 0:
            raise forms.ValidationError(
                "Harvest quantity must be greater than zero."
            )

        return quantity

    def clean(self):
        cleaned_data = super().clean()

        crop = cleaned_data.get("crop")
        harvest_date = cleaned_data.get("harvest_date")

        if crop and harvest_date:
            existing_harvest = (
                Harvest.objects
                .filter(
                    crop=crop,
                    harvest_date=harvest_date,
                )
                .exclude(
                    pk=self.instance.pk
                )
                .exists()
            )

            if existing_harvest:
                raise forms.ValidationError(
                    "A harvest record already exists for this crop "
                    "on this date."
                )

        return cleaned_data


class HarvestWorkerForm(forms.ModelForm):
    class Meta:
        model = HarvestWorker
        fields = [
            "harvest",
            "worker",
            "assigned_date",
            "task_role",
        ]

        widgets = {
            "harvest": forms.Select(),
            "worker": forms.Select(),
            "assigned_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "task_role": forms.Select(
                choices=[
                    ("Harvesting", "Harvesting"),
                ]
            ),
        }

    def clean_assigned_date(self):
        assigned_date = self.cleaned_data["assigned_date"]

        from django.utils import timezone

        if assigned_date > timezone.localdate():
            raise forms.ValidationError(
                "Assigned date cannot be in the future."
            )

        return assigned_date

    def clean_task_role(self):
        task_role = self.cleaned_data["task_role"].strip()

        if task_role != "Harvesting":
            raise forms.ValidationError(
                "Task role must be Harvesting."
            )

        return task_role

    def clean(self):
        cleaned_data = super().clean()

        harvest = cleaned_data.get("harvest")
        worker = cleaned_data.get("worker")

        if harvest and worker:
            existing_assignment = (
                HarvestWorker.objects
                .filter(
                    harvest=harvest,
                    worker=worker,
                )
                .exclude(
                    pk=self.instance.pk
                )
                .exists()
            )

            if existing_assignment:
                raise forms.ValidationError(
                    "This worker is already assigned to this harvest."
                )

        return cleaned_data


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            "customer",
            "sale_date",
            "invoice_number",
            "total_amount",
        ]

        widgets = {
            "customer": forms.Select(),

            "sale_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "invoice_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter invoice number",
                }
            ),

            "total_amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Enter total amount",
                }
            ),
        }

    def clean_sale_date(self):
        sale_date = self.cleaned_data["sale_date"]

        from django.utils import timezone

        if sale_date > timezone.localdate():
            raise forms.ValidationError(
                "Sale date cannot be in the future."
            )

        return sale_date

    def clean_invoice_number(self):
        invoice_number = self.cleaned_data["invoice_number"].strip()

        if not invoice_number:
            raise forms.ValidationError(
                "Invoice number is required."
            )

        existing_sale = (
            Sale.objects
            .filter(invoice_number=invoice_number)
            .exclude(pk=self.instance.pk)
            .exists()
        )

        if existing_sale:
            raise forms.ValidationError(
                "This invoice number already exists."
            )

        return invoice_number

    def clean_total_amount(self):
        total_amount = self.cleaned_data["total_amount"]

        if total_amount <= 0:
            raise forms.ValidationError(
                "Total amount must be greater than zero."
            )

        return total_amount


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = [
            "sale",
            "harvest",
            "quantity_sold",
            "unit_price",
        ]

        widgets = {
            "sale": forms.Select(),
            "harvest": forms.Select(),

            "quantity_sold": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                }
            ),

            "unit_price": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
        }

    def clean_quantity_sold(self):
        quantity_sold = self.cleaned_data["quantity_sold"]

        if quantity_sold <= 0:
            raise forms.ValidationError(
                "Quantity sold must be greater than zero."
            )

        return quantity_sold

    def clean_unit_price(self):
        unit_price = self.cleaned_data["unit_price"]

        if unit_price <= 0:
            raise forms.ValidationError(
                "Unit price must be greater than zero."
            )

        return unit_price

    def clean(self):
        cleaned_data = super().clean()

        harvest = cleaned_data.get("harvest")
        quantity_sold = cleaned_data.get("quantity_sold")

        if harvest and quantity_sold:
            if quantity_sold > harvest.quantity:
                raise forms.ValidationError(
                    "Quantity sold cannot exceed the "
                    "available harvest quantity."
                )

        return cleaned_data


# Role choices mirror the five Django groups seeded by `seed_roles`
# (see farm/management/commands/seed_roles.py). Only reachable by a
# superuser, via the Users screen — see farm/views.py:user_create/user_update.
ROLE_CHOICES = [
    ("Farm Administrator", "Farm Administrator"),
    ("Farm Manager", "Farm Manager"),
    ("Inventory Officer", "Inventory Officer"),
    ("Sales Officer", "Sales Officer"),
    ("Farm Worker", "Farm Worker"),
]


class AdminUserCreateForm(UserCreationForm):
    """Used on the 'Add User' screen — a superuser creates the account and
    assigns it a role in one step."""

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]


class AdminUserEditForm(forms.ModelForm):
    """Used on the 'Edit User' screen — change role or active status.
    Password changes go through the password-reset flow instead."""

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "is_active", "role"]