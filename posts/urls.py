from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    # Page navigation urls
    #
    # - index page
    url(r'^$', views.index, name='index'),
    # - post list page with page number specified
    url(r'^postlist/(?P<page>[0-9]+)', views.post_list, name='postlist'),
    # - submit page
    url(r'^submit/$', views.submit, name='submit'),
    # - submit post from submit page
    url(r'^submit_post/$', views.submit_post, name='submit_post'),
    # - detail page
    url(r'^detail/(?P<post_id>[0-9]+)', views.detail, name='detail'),
    # - success page
    url(r'^success/$', views.success, name='success'),
    # - error page
    url(r'^fail/$', views.fail, name='fail'),
    # - about page
    url(r'^about/$', views.about, name='about'),
    # - contact page
    url(r'^contact/$', views.contact, name='contact'),

    # Admin pages urls
    #
    # - django admin index page, don't ever use it....
    url(r'^admin/', admin.site.urls),
    # - main review index page
    url(r'^review/$', views.review, name='review'),
    # - login review pages
    url(r'^review_login/$', views.review_login, name='review_login'),
    # - logout review pages
    url(r'^review_logout/$', views.review_logout, name='review_logout'),
    # - review detail pages
    url(r'^review_detail/(?P<post_id>[0-9]+)$', views.review_detail, name='review_detail'),
    # - save review result
    url(r'^review_save/(?P<post_id>[0-9]+)$', views.review_save, name='review_save'),
    # - save success page
    url(r'^review_success/$', views.review_success, name='review_success'),
    # - save fail page
    url(r'^review_fail/$', views.review_fail, name='review_fail'),


    # Ajax urls
    #
    # - upload image
    url(r'^upload_img/$', views.upload_img, name='uploadimg'),
    # - create a new tag
    url(r'^newtag/$', views.newtag, name='newtag'),
]