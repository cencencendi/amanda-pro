from django.urls import path
from . import views_dosing, views_growlights, views_irrigation, views_calibration

app_name = "setting_app"

urlpatterns = [
    path("growlights/", views_growlights.growlights, name="growlights"),
    path(
        "growlights/post-growlights-data/",
        views_growlights.update_growlights_data,
        name="update-growlights-data",
    ),
    path(
        "growlights/get-growlights-data/",
        views_growlights.get_growlights_data,
        name="get-growlights-data",
    ),
    path("irrigation/", views_irrigation.irrigation, name="irrigation"),
    path(
        "irrigation/get-irrigation-data/",
        views_irrigation.get_irrigation_data,
        name="get-irrigation-data",
    ),
    path(
        "irrigation/post-irrigation-data/",
        views_irrigation.update_irrigation_data,
        name="update-irrigation-data",
    ),
    path("dosing/", views_dosing.dosing, name="dosing"),
    path("dosing/get-dosing-data/", views_dosing.get_dosing_data, name="get-dosing-data"),
    path("dosing/post-dosing-data/", views_dosing.update_dosing_data, name="update-dosing-data"),
    path("calibration/", views_calibration.calibration, name="calibration"),
]
