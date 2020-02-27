from django.urls import path
from apv.apps import views as v


app_name = 'apps'


urlpatterns = [
    path('', v.index, name='index'),
	path('doador/pdf/', v.doador_pdf, name='pdf'),
    #path('<str:nome>/', v.doadorview, name='list'),
    path('doador/list/', v.doadorview, name='list'),
]
