
from django.contrib import admin
#from django.conf.urls import include, url

from django.urls import include, path
#from material.frontend import urls as frontend_urls
urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('apv.apps.urls')),
]
