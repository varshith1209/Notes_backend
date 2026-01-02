from django.urls import path
from .views import (
    FolderListCreateView,
    FolderDeleteView,
    NoteListCreateView,
    NoteRetrieveUpdateDeleteView,
    ToggleFavoriteView,
    RestoreNoteView,
    SearchNotesView,
    TagCreate,
    NoteTagAPI,
    SummarizeNoteView,
)

urlpatterns = [

    # ----------------------
    # FOLDER ROUTES
    # ----------------------
    path("folders/", FolderListCreateView.as_view(), name="folder-list-create"),
    path("folders/<int:pk>/delete/", FolderDeleteView.as_view(), name="folder-delete"),

    # ----------------------
    # NOTE ROUTES
    # ----------------------
    path("notes/", NoteListCreateView.as_view(), name="note-list-create"),
    path("notes/<int:pk>/", NoteRetrieveUpdateDeleteView.as_view(), name="note-detail"),

    # ----------------------
    # FAVORITE / RESTORE
    # ----------------------
    path("notes/<int:pk>/favorite/", ToggleFavoriteView.as_view(), name="toggle-favorite"),
    path("notes/<int:pk>/restore/", RestoreNoteView.as_view(), name="restore-note"),

    # ----------------------
    # SEMANTIC SEARCH
    # ----------------------
    path("search/", SearchNotesView.as_view(), name="search-notes"),
    path("tags/", TagCreate.as_view(), name="tags"),
    path("note-tag/", NoteTagAPI.as_view(), name="note-tag"),
    
    #SUMMARIZE
    path("notes/<int:pk>/summarize/", SummarizeNoteView.as_view()),


    
]
