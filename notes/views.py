from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Note, Folder, NoteVersion, Embedding,Tag,NoteTag
from .serializers import NoteSerializer,FolderSerializer,TagSerializer,NoteTagSerializer
from .embedding_service import get_embedding, cosine
from .summarizer_service import summarize_note_task

# ----------------------------
# FOLDER VIEWS
# ----------------------------

class FolderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        if not name:
            return Response({"error": "Name required"}, status=400)

        folder = Folder.objects.create(user=request.user, name=name)
        return Response({"id": folder.id, "name": folder.name})


class FolderDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            folder = Folder.objects.get(id=pk, user=request.user)
        except Folder.DoesNotExist:
            return Response({"error": "Folder not found"}, status=404)

        folder.delete()
        return Response({"message": "Deleted"})
        

# ----------------------------
# NOTE CRUD VIEWS
# ----------------------------

class NoteListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter( is_deleted=False)

    def perform_create(self, serializer):
            serializer.save()

        



class NoteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        old_note = self.get_object()
        old_content = old_note.content

        note = serializer.save()

        # Create version record
        if old_content != note.content:
            NoteVersion.objects.create(
                note=note,
                title=note.title,
                content=note.content
            )

            # regenerate embedding
            vector = get_embedding(note.content)
            if hasattr(note, "embedding"):
                note.embedding.vector = vector
                note.embedding.save()
            else:
                Embedding.objects.create(note=note, vector=vector)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


# ----------------------------
# FAVORITE & RESTORE
# ----------------------------

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            note = Note.objects.get(id=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        note.favorite = not note.favorite
        note.save()

        return Response({"favorite": note.favorite})


class RestoreNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            note = Note.objects.get(id=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        note.is_deleted = False
        note.save()

        return Response({"message": "Restored"})


# ----------------------------
# SEARCH ENDPOINT
# ----------------------------

class SearchNotesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q")
        if not q:
            return Response({"error": "Missing q"}, status=400)

        query_vec = get_embedding(q)

        results = []
        for emb in Embedding.objects.filter(note__user=request.user):
            score = cosine(query_vec, emb.vector)
            results.append({
                "id": emb.note.id,
                "title": emb.note.title,
                "content": emb.note.content,
                "score": score
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return Response(results[:5])

class TagCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class NoteTagAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteTagSerializer

    def get_queryset(self):
        return NoteTag.objects.filter(note__user=self.request.user)

#SUMMARIZER


class SummarizeNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            note = Note.objects.get(id=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        task = summarize_note_task.delay(note.id)

        return Response({"message": "Summarization started", "task_id": task.id})

        