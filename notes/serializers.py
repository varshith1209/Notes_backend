from rest_framework import serializers
from .models import Note, NoteVersion, Embedding, Folder,Tag,NoteTag
from .embedding_service import get_embedding


# ---------------------------
# Folder Serializer
# ---------------------------
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["id", "name"]  # include id so frontend can use it


# ---------------------------
# Note Serializer
# ---------------------------
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ["user"]  # prevent spoofing

    def create(self, validated_data):
        # Attach the user automatically from request
        user = self.context["request"].user
        note = Note.objects.create(user=user, **validated_data)

        # generate embedding
        vector = get_embedding(note.content)
        Embedding.objects.create(note=note, vector=vector)

        return note

    def update(self, instance, validated_data):
        old_content = instance.content

        # normal update
        instance = super().update(instance, validated_data)

        # if content changed → create version + regenerate embedding
        if "content" in validated_data and validated_data["content"] != old_content:

            # Create a version log
            NoteVersion.objects.create(
                note=instance,
                title=instance.title,
                content=instance.content
            )

            # Recompute embedding
            vector = get_embedding(instance.content)

            if hasattr(instance, "embedding"):
                instance.embedding.vector = vector
                instance.embedding.save()
            else:
                Embedding.objects.create(note=instance, vector=vector)

        return instance
 
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

    def validate_name(self, value):
        user = self.context["request"].user
        if Tag.objects.filter(name=value, user=user).exists():
            raise serializers.ValidationError("You already created this tag.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return Tag.objects.create(user=user, **validated_data)

class NoteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTag
        fields = ["tag", "note"]

    def validate(self, data):
        if NoteTag.objects.filter(tag=data["tag"], note=data["note"]).exists():
            raise serializers.ValidationError("Tag already assigned to note.")
        return data

    def create(self, validated_data):
        return NoteTag.objects.create(**validated_data)

        
            
            
                    