from rest_framework.views import APIView
from app.models import Recommended, RecommendedItem
import json
from rest_framework.response import Response
from app.serializers import RecommendedSerializer

class RecommendedList(APIView):
    def getSubmissionScore(self, solvedBy, username):
        JSON = json.loads(solvedBy)
        return JSON[username] if username in JSON else 0

    def getRecommended(self, username):
        recommended = [
            RecommendedItem(
                id=problem.id,
                name=problem.problem_name,
                link=problem.problem_link,
                score=self.getSubmissionScore(problem.solvedBy, username)
            )
            for problem in Recommended.objects.all()
        ]
        return recommended

    def get(self, request, format=None):
        username = request.GET['username']
        recommended = self.getRecommended(username)
        serializer = RecommendedSerializer(recommended, many=True)
        return Response(serializer.data)