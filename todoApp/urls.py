from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.user_login),
    url(r'^register$', views.user_register),
    url(r'^logout$', views.user_logout),
    url(r'^todo$', views.todo_operation),
    url(r'^yourtodo$', views.your_todo_operation),
    url(r'^task/(?P<tid>[0-9]+)$', views.single_task_operation),
    url(r'^statuschange$', views.change_status),
    url(r'^error$', views.error)
]
