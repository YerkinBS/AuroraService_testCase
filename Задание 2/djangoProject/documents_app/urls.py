from django.urls import path
from .views import profile_view, RegisterView, upload_document, delete_document, update_document
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='profile', permanent=True)),
    path('profile/', profile_view, name="profile"),
    path('register/', RegisterView.as_view(), name='register'),
    path('upload_document/', upload_document, name='upload_document'),
    path('delete_document/<int:pk>/', delete_document, name='delete_document'),
    path('update_document/<int:document_id>/', update_document, name='update_document')
]