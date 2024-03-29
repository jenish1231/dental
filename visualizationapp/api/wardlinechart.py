import datetime
from django.http import JsonResponse
from nepali.datetime import NepaliDate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from userapp.models import User
from addressapp.models import Ward
from patientapp.models import Patient
from visualizationapp.serializers.visualization import WardlineVisualizationSerializer
from visualizationapp.models import Visualization

date = datetime.date.today()
np_date = NepaliDate.from_date(date)
item = np_date.month


class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


# 2.3 Preventive Ratio Over Time
class WardlineVisualization(APIView):
    def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

            label_data = [
                "Q2(Apr/May)",
                "",
                "",
                "Q3(Jul/Aug)",
                "",
                "",
                "Q4(Oct/Nov)",
                "",
                "",
                "Q1(Jan/Feb)",
                "",
                "",
            ]
            next_month = month.index(item) + 1
            month_obj = month[next_month:]
            label_data_obj = label_data[next_month:]
            for i in month[next_month:]:
                a = month.index(i)
                month.pop(a)
                label_data.pop(a)
            print(month_obj)
            x=month_obj[::-1]
            print(x)

            for b in x:
                month.insert(0, b)
            print(label_data_obj)
            y=label_data_obj[::-1]
            print(y)
            for n in y:
                label_data.insert(0, n)

            geography = []
            geography_patient = []
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v = []
                for x in month:
                    if Visualization.objects.filter(active=True,geography_id=i.id).exists():
                        total_patient = Visualization.objects.filter(
                            geography_id=i.id, created_at__month=x
                        ).count()
                        v.append(total_patient)
                geography.append(i.name)
                geography_patient.append(v)
            data_data = []
            datasets1 = []
            cz = [
                "rgba(234, 196, 53, 1)",
                "rgba(49, 55, 21, 1)",
                "rgba(117, 70, 104, 1)",
                "rgba(127, 184, 0, 1)",
                "rgba(3, 206, 164, 1)",
                "rgba(228, 0, 102, 1)",
                "rgba(52, 89, 149, 1)",
                "rgba(243, 201, 139, 1)",
                "rgba(251, 77, 61, 1)",
                "rgba(230, 232, 230, 1)",
                "rgba(248, 192, 200, 1)",
                "rgba(44, 85, 48, 1)",
                "rgba(231, 29, 54, 1)",
                "rgba(96, 95, 94, 1)",
                "rgba(22, 12, 40, 1)",
                "rgba(173, 96, 188, 1)",
                "rgba(228, 96, 188, 1)",
                "rgba(228, 29, 182, 1)",
                "rgba(211, 29, 63, 1)",
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
                "rgba(255, 159, 64, 1)",
            ]
            m = 0
            n = 0
            for y in geography:
                a = {
                    "label": y,
                    "backgroundColor": "rgba(255, 255, 255, 0)",
                    "borderColor": cz[m],
                    "borderWidth": 1,
                    "data": geography_patient[n],
                }
                datasets1.append(a)
                m += 1
                n += 1
            locationChart = {
                "data": {
                    "labels": label_data,
                    "datasets": datasets1,
                },
                "options": {
                    "aspectRatio": 2.2,
                    "title": {
                        "display": "true",
                        # 'text': "Month-wise contact distribution",
                        "fontSize": 18,
                        "fontFamily": "'Palanquin', sans-serif",
                    },
                    "legend": {"position": "bottom"},
                    "labels": {"usePointStyle": "true"},
                    "scales": {
                        "yAxes": [
                            {
                                "ticks": {
                                    "fontColor": "rgba(0,0,0,0.5)",
                                    "fontStyle": "bold",
                                    "beginAtZero": "false",
                                    "maxTicksLimit": 6,
                                    "padding": 20,
                                },
                                "gridLines": {"drawTicks": "true", "display": "true"},
                            }
                        ],
                        "xAxes": [
                            {
                                "gridLines": {"zeroLineColor": "transparent"},
                                "ticks": {
                                    "padding": 20,
                                    "fontColor": "rgba(0,0,0,0.5)",
                                    "fontStyle": "bold",
                                },
                            }
                        ],
                    },
                },
            }
            return Response({"locationChart": locationChart})
        return Response({"message": "only admin can see"}, status=400)


# class WardlineVisualizationFilter(APIView):
#     permission_classes = (IsPostOrIsAuthenticated,)
#     serializer_class = WardlineVisualizationSerializer
#     def post(self, request, format=None):
#         serializer = WardlineVisualizationSerializer(data=request.data,context={'request': request})
#         if serializer.is_valid():
#             start_date = str(NepaliDate.from_date(serializer.validated_data['start_date']))
#             month=[1,2,3,4,5,6,7,8,9,10,11,12]
#             geography=[]
#             geography_patient=[]
#             geography_obj = Ward.objects.filter(status=True)
#             for i in geography_obj:
#                 v=[]
#                 for x in month:
#                     if Patient.objects.filter(geography__id=i.id).exists():
#                         total_patient = Patient.objects.filter(geography__id=i.id,created_at__month=x,created_at=start_date).count()
#                         v.append(total_patient)
#                 geography.append(i.name)
#                 geography_patient.append(v)
#             data_data=[]
#             datasets1=[]
#             cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
#             "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
#             "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
#             "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
#             "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)"]
#             m=0
#             n=0
#             for y in geography:
#                 a={
#                 'label': y,
#                 'backgroundColor': "rgba(255, 255, 255, 0)",
#                 'borderColor':cz[m] ,
#                 'borderWidth': 1,
#                 'data': geography_patient[n]
#                 }
#                 datasets1.append(a)
#                 m += 1
#                 n +=1
#             locationChart = {
#             'data': {
#             'labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
#             'datasets': datasets1
#             },
#             'options': {
#             'aspectRatio': 2.2,
#             'title': {
#             'display': 'true',
#             # 'text': "Month-wise contact distribution",
#             'fontSize': 18,
#             'fontFamily': "'Palanquin', sans-serif"
#             },
#             'legend': {
#             'position': "bottom"
#             },
#             'labels':{
#             'usePointStyle': 'true'
#             },
#             'scales': {
#             'yAxes': [{
#             'ticks': {
#             'fontColor': "rgba(0,0,0,0.5)",
#             'fontStyle': "bold",
#             'beginAtZero': 'false',
#             'maxTicksLimit': 6,
#             'padding': 20
#             },
#             'gridLines': {
#             'drawTicks': 'true',
#             'display': 'true'
#             }
#             }],
#             'xAxes': [{
#             'gridLines': {
#             'zeroLineColor': "transparent"
#             },
#             'ticks': {
#             'padding': 20,
#             'fontColor': "rgba(0,0,0,0.5)",
#             'fontStyle': "bold"
#             }}]}}
#             }
#             return JsonResponse({"locationChart":locationChart})
#         return Response(serializer.error)
