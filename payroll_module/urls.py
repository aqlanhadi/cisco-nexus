from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='salary-dashboard'),
    path('breakdown/', views.breakdown, name='salary-breakdown'),
    path('history/', views.history, name='salary-history'),
    path('all/', views.EmployeeListView.as_view(), name='salary-list')
]

# [
#     OrderedDict (
#         [
#             ('id', 6), 
#             ('username', 'guard3')
#         ]
#     ), 
#     OrderedDict(
#         [
#             ('id', 7), 
#             ('username', 'guard4')
#         ]
#     ), 
#     OrderedDict(
#         [
#             ('id', 8), 
#             ('username', 'guard5')
#         ]
#     )
# ]