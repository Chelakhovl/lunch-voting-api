from django.utils.timezone import now
from rest_framework import generics, permissions
from rest_framework.response import Response
from votes.models import Vote
from votes.serializers import VoteSerializer
from restaurants.models import Menu
from services.votes.vote_service import get_voting_results


class VoteCreateView(generics.CreateAPIView):
    """
    API endpoint for users to cast a vote for a specific menu.
    """

    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Saves the vote with the authenticated user.
        """
        serializer.save(user=self.request.user)


class VoteResultsView(generics.ListAPIView):
    """
    API endpoint to retrieve voting results for the current day.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Returns a sorted list of menu votes for the current day.
        """
        today = now().date()
        results = get_voting_results(today)
        return Response(results)
