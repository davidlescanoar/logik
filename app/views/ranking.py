from app.models import *
import json
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers import RankingSerializer


class RankingTable(APIView):
    def exists(self, user, db):
        return user in db

    def getUsers(self, input):
        return json.loads(input).items()

    def getScores(self, problems, users, blacklist):
        scores = {str(user): 0 for user in users if not self.exists(user, blacklist)}
        for problem in problems:
            for user, score in self.getUsers(problem.solvedBy):
                if not self.exists(user, blacklist):
                    scores[user] += score
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)

    def getTable(self, scores):
        ranking_table = []
        lastScore, currentRanking, ranking = -1, 1, 1
        for score in scores:
            if score[1] != lastScore:
                lastScore, currentRanking = score[1], ranking
            ranking_table.append(
                Ranking(
                    rank=currentRanking,
                    user=score[0],
                    score=score[1]
                )
            )
            ranking += 1
        return ranking_table

    def getRanking(self):
        problems = Problems.objects.all()
        users = User.objects.all()
        blacklist = set(bu.black_user for bu in BlackList.objects.all())
        scores = self.getScores(problems, users, blacklist)
        ranking = self.getTable(scores)
        return ranking

    def get(self, request, format=None):
        ranking = self.getRanking()
        serializer = RankingSerializer(ranking, many=True)
        return Response(serializer.data)
