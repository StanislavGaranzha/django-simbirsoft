from django.urls import path
from django.conf.urls import handler403, handler404, handler500

from .views import NoteCreateUpdateView, NoteDeleteView, NoteListView

app_name = 'notes'

handler403 = 'notes.views.permission_denied'
handler404 = 'notes.views.page_not_found'
handler500 = 'notes.views.server_error'


urlpatterns = [
    path('note/new/', NoteCreateUpdateView.as_view(),
         name='note_new'),
    path('author/<int:author_id>/', NoteListView.as_view(),
         name='notes_list'),
    path('note/<int:pk>/edit/', NoteCreateUpdateView.as_view(),
         name='note_edit'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(),
         name='note_delete'),
]
