import json
from app.models import Problems, ProblemItem
from rest_framework.views import APIView
from app.serializers import ProblemSerializer
from rest_framework.response import Response


class ProblemList(APIView):
    def getSubmissionScore(self, solvedBy, username):
        JSON = json.loads(solvedBy)
        return JSON[username] if username in JSON else 0

    def getAttemptsNumber(self, solvedBy):
        JSON = json.loads(solvedBy)
        return len(JSON)

    def getAcceptedSubmissions(self, solvedBy):
        JSON = json.loads(solvedBy)
        return sum(i == 100 for i in JSON.values())

    def getAcceptance(self, ac, wa):
        if wa == 0:
            return 0
        return (ac / wa) * 100

    def getProblems(self, username):
        problemList = [
            ProblemItem(
                id=problem.id,
                name=problem.problem_name,
                link=problem.problem_link,
                score=self.getSubmissionScore(problem.solvedBy, username),
                acceptance=self.getAcceptance(
                    self.getAcceptedSubmissions(problem.solvedBy),
                    self.getAttemptsNumber(problem.solvedBy)
                ),
            )
            for problem in Problems.objects.all()
        ]
        return problemList

    def get(self, request, format=None):
        username = request.GET['username']
        problems = self.getProblems(username)
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)
