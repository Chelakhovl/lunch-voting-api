from rest_framework import serializers
from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model.
    Ensures that users cannot vote for the same menu multiple times.
    """

    class Meta:
        model = Vote
        fields = ["id", "menu", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        """
        Validates that a user has not already voted for the given menu.
        """
        user = self.context["request"].user
        menu = data.get("menu")

        if Vote.objects.filter(user=user, menu=menu).exists():
            raise serializers.ValidationError("You have already voted for this menu.")

        return data

    def create(self, validated_data):
        """
        Assigns the current user before saving the vote.
        """
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
