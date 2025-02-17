from rest_framework import serializers
from votes.models import Vote
from services.validation.validate_vote import validate_user_vote


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
        Validates voting logic using an external validation service.
        """
        user = self.context["request"].user
        menu = data.get("menu")

        validate_user_vote(user, menu)
        return data

    def create(self, validated_data):
        """
        Assigns the current user before saving the vote.
        """
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
