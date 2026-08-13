from django.db import models


class Farm(models.Model):
    farm_id = models.AutoField(primary_key=True)
    farm_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=150)
    total_size = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "farm"

    def __str__(self):
        return self.farm_name


class Crop(models.Model):
    crop_id = models.AutoField(primary_key=True)
    farm = models.ForeignKey(
        Farm,
        on_delete=models.DO_NOTHING,
        db_column="farm_id"
    )
    crop_type = models.CharField(max_length=80)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    status = models.CharField(max_length=20)
    plot_number = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "crop"
        constraints = [
            models.UniqueConstraint(
                fields=["farm", "plot_number"],
                name="uq_farm_plot_crop"
            )
        ]

    def __str__(self):
        return f"{self.crop_type} - {self.plot_number}"


class Worker(models.Model):
    worker_id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    contact_details = models.CharField(max_length=100)
    job_role = models.CharField(max_length=60)
    hire_date = models.DateField()

    class Meta:
        managed = False
        db_table = "worker"

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=60)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = "equipment"

    def __str__(self):
        return self.equipment_name


class Fertilizer(models.Model):
    fertilizer_id = models.AutoField(primary_key=True)
    fertilizer_type = models.CharField(max_length=80, unique=True)
    stock_level = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = "fertilizer"

    def __str__(self):
        return self.fertilizer_type


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100)
    address = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = "customer"

    def __str__(self):
        return self.full_name


class Harvest(models.Model):
    harvest_id = models.AutoField(primary_key=True)
    crop = models.ForeignKey(
        Crop,
        on_delete=models.DO_NOTHING,
        db_column="crop_id"
    )
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "harvest"

    def __str__(self):
        return f"{self.crop.crop_type} - {self.harvest_date}"


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
        db_column="customer_id"
    )
    sale_date = models.DateField()
    invoice_number = models.CharField(max_length=30, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = "sale"

    def __str__(self):
        return self.invoice_number


class CropWorker(models.Model):
    crop_worker_id = models.AutoField(primary_key=True)
    crop = models.ForeignKey(
        Crop,
        on_delete=models.DO_NOTHING,
        db_column="crop_id"
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.DO_NOTHING,
        db_column="worker_id"
    )
    assigned_date = models.DateField()
    task_role = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = "crop_worker"
        constraints = [
            models.UniqueConstraint(
                fields=["crop", "worker", "assigned_date"],
                name="uq_crop_worker"
            )
        ]


class EquipmentAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.DO_NOTHING,
        db_column="equipment_id"
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.DO_NOTHING,
        db_column="worker_id"
    )
    assigned_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "equipment_assignment"


class EquipmentMaintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.DO_NOTHING,
        db_column="equipment_id"
    )
    maintenance_date = models.DateField()
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = "equipment_maintenance"


class FertilizerUsage(models.Model):
    usage_id = models.AutoField(primary_key=True)
    fertilizer = models.ForeignKey(
        Fertilizer,
        on_delete=models.DO_NOTHING,
        db_column="fertilizer_id"
    )
    crop = models.ForeignKey(
        Crop,
        on_delete=models.DO_NOTHING,
        db_column="crop_id"
    )
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)
    usage_date = models.DateField()

    class Meta:
        managed = False
        db_table = "fertilizer_usage"


class HarvestWorker(models.Model):
    harvest_worker_id = models.AutoField(primary_key=True)
    harvest = models.ForeignKey(
        Harvest,
        on_delete=models.DO_NOTHING,
        db_column="harvest_id"
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.DO_NOTHING,
        db_column="worker_id"
    )
    assigned_date = models.DateField()
    task_role = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = "harvest_worker"
        constraints = [
            models.UniqueConstraint(
                fields=["harvest", "worker"],
                name="uq_harvest_worker"
            )
        ]


class SaleItem(models.Model):
    sale_item_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(
        Sale,
        on_delete=models.DO_NOTHING,
        db_column="sale_id"
    )
    harvest = models.ForeignKey(
        Harvest,
        on_delete=models.DO_NOTHING,
        db_column="harvest_id"
    )
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = "sale_item"