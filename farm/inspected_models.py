# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Crop(models.Model):
    crop_id = models.AutoField(primary_key=True)
    farm = models.ForeignKey('Farm', models.DO_NOTHING)
    crop_type = models.CharField(max_length=80)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    status = models.CharField(max_length=20)
    plot_number = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'crop'
        unique_together = (('farm', 'plot_number'),)


class CropFertilizer(models.Model):
    pk = models.CompositePrimaryKey('crop_id', 'fertilizer_id', 'usage_date')
    crop_id = models.UUIDField()
    fertilizer_id = models.UUIDField()
    usage_date = models.DateField()
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'crop_fertilizer'


class CropWorker(models.Model):
    crop_worker_id = models.AutoField(primary_key=True)
    crop = models.ForeignKey(Crop, models.DO_NOTHING)
    worker = models.ForeignKey('Worker', models.DO_NOTHING)
    assigned_date = models.DateField()
    task_role = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'crop_worker'
        unique_together = (('crop', 'worker', 'assigned_date'),)


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100)
    address = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'customer'


class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=60)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'equipment'


class EquipmentAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING)
    worker = models.ForeignKey('Worker', models.DO_NOTHING)
    assigned_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_assignment'


class EquipmentMaintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING)
    maintenance_date = models.DateField()
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'equipment_maintenance'


class Farm(models.Model):
    farm_id = models.AutoField(primary_key=True)
    farm_name = models.CharField(unique=True, max_length=100)
    location = models.CharField(max_length=150)
    total_size = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'farm'


class Fertilizer(models.Model):
    fertilizer_id = models.AutoField(primary_key=True)
    fertilizer_type = models.CharField(unique=True, max_length=80)
    stock_level = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'fertilizer'


class FertilizerUsage(models.Model):
    usage_id = models.AutoField(primary_key=True)
    fertilizer = models.ForeignKey(Fertilizer, models.DO_NOTHING)
    crop = models.ForeignKey(Crop, models.DO_NOTHING)
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)
    usage_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'fertilizer_usage'


class Harvest(models.Model):
    harvest_id = models.AutoField(primary_key=True)
    crop = models.ForeignKey(Crop, models.DO_NOTHING)
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'harvest'


class HarvestSale(models.Model):
    pk = models.CompositePrimaryKey('harvest_id', 'sale_id')
    harvest_id = models.UUIDField()
    sale_id = models.UUIDField()
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'harvest_sale'


class HarvestWorker(models.Model):
    harvest_worker_id = models.AutoField(primary_key=True)
    harvest = models.ForeignKey(Harvest, models.DO_NOTHING)
    worker = models.ForeignKey('Worker', models.DO_NOTHING)
    assigned_date = models.DateField()
    task_role = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'harvest_worker'
        unique_together = (('harvest', 'worker'),)


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    sale_date = models.DateField()
    invoice_number = models.CharField(unique=True, max_length=30)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'sale'


class SaleItem(models.Model):
    sale_item_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, models.DO_NOTHING)
    harvest = models.ForeignKey(Harvest, models.DO_NOTHING)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'sale_item'


class Worker(models.Model):
    worker_id = models.AutoField(primary_key=True)
    employee_id = models.CharField(unique=True, max_length=20)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    contact_details = models.CharField(max_length=100)
    job_role = models.CharField(max_length=60)
    hire_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'worker'


class WorkerEquipment(models.Model):
    pk = models.CompositePrimaryKey('worker_id', 'equipment_id', 'assigned_date')
    worker_id = models.UUIDField()
    equipment_id = models.UUIDField()
    assigned_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worker_equipment'
