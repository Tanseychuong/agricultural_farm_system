"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path

from farm.views import (
    FarmLoginView,
    FarmLogoutView,
    register,
    dashboard,

    crop_list,
    crop_create,
    crop_update,
    crop_delete,

    worker_list,
    worker_create,
    worker_update,
    worker_delete,

    equipment_list,
    equipment_create,
    equipment_update,
    equipment_delete,

    farm_list,
    farm_create,
    farm_update,
    farm_delete,

    customer_list,
    customer_create,
    customer_update,
    customer_delete,

    fertilizer_list,
    fertilizer_create,
    fertilizer_update,
    fertilizer_delete,

    fertilizer_usage_list,
    fertilizer_usage_create,
    fertilizer_usage_update,
    fertilizer_usage_delete,

    equipment_assignment_list,
    equipment_assignment_create,
    equipment_assignment_update,
    equipment_assignment_delete,

    equipment_maintenance_list,
    equipment_maintenance_create,
    equipment_maintenance_update,
    equipment_maintenance_delete,

    crop_worker_list,
    crop_worker_create,
    crop_worker_update,
    crop_worker_delete,

    harvest_list,
    harvest_create,
    harvest_update,
    harvest_delete,

    harvest_worker_list,
    harvest_worker_create,
    harvest_worker_update,
    harvest_worker_delete,

    sale_list,
    sale_create,
    sale_update,
    sale_delete,

    sale_item_list,
    sale_item_create,
    sale_item_update,
    sale_item_delete,
)


urlpatterns = [
    path("admin/", admin.site.urls),

# Authentication Path
    path("login/", FarmLoginView.as_view(), name="login"),
    path("logout/", FarmLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),

    # Dashboard path
    path("", dashboard, name="dashboard"),

    # Crop Management Path
    path("crops/", crop_list, name="crop_list"),
    path("crops/add/", crop_create, name="crop_create"),
    path(
        "crops/<int:crop_id>/edit/",
        crop_update,
        name="crop_update",
    ),
    path(
        "crops/<int:crop_id>/delete/",
        crop_delete,
        name="crop_delete",
    ),

    # Worker Management Path
    path("workers/", worker_list, name="worker_list"),
    path("workers/add/", worker_create, name="worker_create"),
    path(
        "workers/<int:worker_id>/edit/",
        worker_update,
        name="worker_update",
    ),
    path(
        "workers/<int:worker_id>/delete/",
        worker_delete,
        name="worker_delete",
    ),

    # Equipment Management Path
    path("equipment/", equipment_list, name="equipment_list"),
    path("equipment/add/", equipment_create, name="equipment_create"),
    path(
        "equipment/<int:equipment_id>/edit/",
        equipment_update,
        name="equipment_update",
    ),
    path(
        "equipment/<int:equipment_id>/delete/",
        equipment_delete,
        name="equipment_delete",
    ),

    # Farm Management
    path("farms/", farm_list, name="farm_list"),
    path("farms/add/", farm_create, name="farm_create"),
    path(
        "farms/<int:farm_id>/edit/",
        farm_update,
        name="farm_update",
    ),
    path(
        "farms/<int:farm_id>/delete/",
        farm_delete,
        name="farm_delete",
    ),

        # Customer Management
    path("customers/", customer_list, name="customer_list"),
    path("customers/add/", customer_create, name="customer_create"),
    path(
        "customers/<int:customer_id>/edit/",
        customer_update,
        name="customer_update",
    ),
    path(
        "customers/<int:customer_id>/delete/",
        customer_delete,
        name="customer_delete",
    ),

    # Fertilizer Management
    path("fertilizers/", fertilizer_list, name="fertilizer_list"),
    path("fertilizers/add/", fertilizer_create, name="fertilizer_create"),
    path(
        "fertilizers/<int:fertilizer_id>/edit/",
        fertilizer_update,
        name="fertilizer_update",
    ),
    path(
        "fertilizers/<int:fertilizer_id>/delete/",
        fertilizer_delete,
        name="fertilizer_delete",
    ),

    # Fertilizer Usage Management
    path(
        "fertilizer-usage/",
        fertilizer_usage_list,
        name="fertilizer_usage_list",
    ),
    path(
        "fertilizer-usage/add/",
        fertilizer_usage_create,
        name="fertilizer_usage_create",
    ),
    path(
        "fertilizer-usage/<int:usage_id>/edit/",
        fertilizer_usage_update,
        name="fertilizer_usage_update",
    ),
    path(
        "fertilizer-usage/<int:usage_id>/delete/",
        fertilizer_usage_delete,
        name="fertilizer_usage_delete",
    ),

        # Equipment Assignment Management
    path(
        "equipment-assignments/",
        equipment_assignment_list,
        name="equipment_assignment_list",
    ),
    path(
        "equipment-assignments/add/",
        equipment_assignment_create,
        name="equipment_assignment_create",
    ),
    path(
        "equipment-assignments/<int:assignment_id>/edit/",
        equipment_assignment_update,
        name="equipment_assignment_update",
    ),
    path(
        "equipment-assignments/<int:assignment_id>/delete/",
        equipment_assignment_delete,
        name="equipment_assignment_delete",
    ),

    # Equipment Maintenance Management
    path(
        "equipment-maintenance/",
        equipment_maintenance_list,
        name="equipment_maintenance_list",
    ),
    path(
        "equipment-maintenance/add/",
        equipment_maintenance_create,
        name="equipment_maintenance_create",
    ),
    path(
        "equipment-maintenance/<int:maintenance_id>/edit/",
        equipment_maintenance_update,
        name="equipment_maintenance_update",
    ),
    path(
        "equipment-maintenance/<int:maintenance_id>/delete/",
        equipment_maintenance_delete,
        name="equipment_maintenance_delete",
    ),


        # Crop Worker Management
    path(
        "crop-workers/",
        crop_worker_list,
        name="crop_worker_list",
    ),
    path(
        "crop-workers/add/",
        crop_worker_create,
        name="crop_worker_create",
    ),
    path(
        "crop-workers/<int:crop_worker_id>/edit/",
        crop_worker_update,
        name="crop_worker_update",
    ),
    path(
        "crop-workers/<int:crop_worker_id>/delete/",
        crop_worker_delete,
        name="crop_worker_delete",
    ),

        # Harvest Management
    path(
        "harvests/",
        harvest_list,
        name="harvest_list",
    ),
    path(
        "harvests/add/",
        harvest_create,
        name="harvest_create",
    ),
    path(
        "harvests/<int:harvest_id>/edit/",
        harvest_update,
        name="harvest_update",
    ),
    path(
        "harvests/<int:harvest_id>/delete/",
        harvest_delete,
        name="harvest_delete",
    ),
    # Harvest Worker Management
    path(
        "harvest-workers/",
        harvest_worker_list,
        name="harvest_worker_list",
    ),
    path(
        "harvest-workers/add/",
        harvest_worker_create,
        name="harvest_worker_create",
    ),
    path(
        "harvest-workers/<int:harvest_worker_id>/edit/",
        harvest_worker_update,
        name="harvest_worker_update",
    ),
    path(
        "harvest-workers/<int:harvest_worker_id>/delete/",
        harvest_worker_delete,
        name="harvest_worker_delete",
    ),

    # Sale Management
    path(
        "sales/",
        sale_list,
        name="sale_list",
    ),
    path(
        "sales/add/",
        sale_create,
        name="sale_create",
    ),
    path(
        "sales/<int:sale_id>/edit/",
        sale_update,
        name="sale_update",
    ),
    path(
        "sales/<int:sale_id>/delete/",
        sale_delete,
        name="sale_delete",
    ),

    # Sale Item Management
path(
    "sale-items/",
    sale_item_list,
    name="sale_item_list",
),
path(
    "sale-items/add/",
    sale_item_create,
    name="sale_item_create",
),
path(
    "sale-items/<int:sale_item_id>/edit/",
    sale_item_update,
    name="sale_item_update",
),
path(
    "sale-items/<int:sale_item_id>/delete/",
    sale_item_delete,
    name="sale_item_delete",
),
]