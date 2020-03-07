from django.urls import path
from . import views
urlpatterns = [
	path('',views.showline, name='home'),
	path('<slug:title>/<int:chapter>/<int:line>/', views.showline, name='showline'),
    path('word/',views.showword),
    path('ajaxview/', views.AjaxView.as_view()),
]