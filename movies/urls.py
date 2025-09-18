from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('<int:id>/review/<int:review_id>/reply/', views.create_reply, name='movies.create_reply'),
    path('<int:id>/review/<int:review_id>/reply/<int:parent_reply_id>/', views.create_reply, name='movies.create_nested_reply'),
    path('petitions/', views.petitions, name='movies.petitions'),
    path('petitions/create/', views.create_petition, name='movies.create_petition'),
    path('petitions/<int:petition_id>/vote/', views.vote_petition, name='movies.vote_petition'),
]