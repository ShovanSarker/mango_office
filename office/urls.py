from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from actions.views import login_page, login_auth, home, logout_now, add_employee, change_status
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'office.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/', view=login_page, name='home'),
                       url(r'^login_info/', view=login_auth, name='home'),
                       url(r'^$', view=home, name='home'),
                       url(r'^logout/', view=logout_now, name='home'),
                       url(r'^add_employee/', view=add_employee, name='home'),
                       url(r'^change_status/', view=change_status, name='home'),
                       )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
