from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # 대개 name은 view name과 같게 하여 헷갈림을 방지. 그러나 정확히는 해당 url path의 호출명을 의미함.
    path(route='', view=views.post_list, name='list'),
    path('<int:post_id>/', views.post_detail, name='detail'),
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/update/', views.update_post, name='update'),
    path('<int:post_id>/delete/', views.delete_post, name='delete'),
]
