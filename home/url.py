from django.urls import path
from . import views


app_name = "home"
urlpatterns = [
    path('',views.HomePage.as_view() , name="homepage"),
    path('post/<int:post_id>/<slug:post_slug>/' , views.PostDetailView.as_view() , name='post_detail')
]