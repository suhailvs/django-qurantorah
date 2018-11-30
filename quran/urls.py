from django.urls import path
from . import views
urlpatterns = [
    # Examples:
    path('',views.showline),
    path('<int:sura>/<int:line>/', views.showline, name='showline'),
    path('ajaxview/', views.AjaxView.as_view()),
    # Parts : 
	# url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/$', views.aya, name='quran_aya'),
 #    url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/(?P<word_number>\d+)/$', views.word, name='quran_word'),
 #    url(r'^lemma/(?P<lemma_id>\d+)/$', views.lemma, name='quran_lemma'),
 #    url(r'^root/(?P<root_id>\d+)/$', views.root, name='quran_root'),
 #    url(r'^root/$', views.root_index, name='quran_root_list'),
]