from django.urls import path
from . import views

app_name = "graph_app"

urlpatterns = [
    path("", views.graph, name="graph"),
    path("get-date-selection/", views.get_date_selection, name="get-date-selection"),
    path("post-selected-data/", views.post_selected_data, name="post-selected-data"),
]
