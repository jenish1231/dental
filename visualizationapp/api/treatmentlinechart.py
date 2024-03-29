import re
from datetime import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from userapp.models import User
from django.http import JsonResponse
from nepali.datetime import NepaliDate
import datetime
from django.db.models import Sum

from rest_framework import filters
from visualizationapp.models import Visualization

from addressapp.models import Ward
from patientapp.models import Patient
from django.db.models.functions import TruncMonth
from django.db.models import Count
import random

date = datetime.date.today()
np_date = NepaliDate.from_date(date)
item = np_date.month



class TreatmentPreventionRatioVisualization(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month = [1,2,3,4,5,6,7,8,9,10,11,12]
            # label_data = [
            #     "Baishakh(Apr/May)",
            #     "Jestha(May/Jun)",
            #     "Asar(Jun/Jul)",
            #     "Shrawan(Jul/Aug)",
            #     "Bhadra(Aug/Sep)",
            #     "Asoj(Sep/Oct)",
            #     "Kartik(Oct/Nov)",
            #     "Mangsir(Nov/Dec)",
            #     "Poush(Dec/Jan)",
            #     "Magh(Jan/Feb)",
            #     "Falgun(Feb/Mar)",
            #     "Chaitra(Mar/Apr)",
            # ]

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
            x=month_obj[::-1]
            for b in x:
                month.insert(0, b)
            y=label_data_obj[::-1]
            for n in y:
                label_data.insert(0, n)

            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v=[]
                for x in month:
                    if Visualization.objects.filter(geography_id=i.id).exists():
                        total_seal = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,seal=True).count()
                        total_fv = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,fv=True).count()
                        total_exo = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,exo=True).count()
                        total_art = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,exo=True).count()
                        total_sdf = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,sdf=True).count()
                        try:
                            preventive_ratio = (total_seal+total_fv)/(total_exo+total_art+total_sdf)
                        except:
                            preventive_ratio=0
                        v.append(preventive_ratio)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)",\
            "rgba(173, 96, 188, 1)","rgba(228, 96, 188, 1)","rgba(228, 29, 182, 1)",\
            "rgba(211, 29, 63, 1)","rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)",\
            "rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)",\
            "rgba(255, 159, 64, 1)"]
            
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': label_data,
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 2.1,
            'maintainAspectRatio': "false",
            'title': {
                'display': '"true"',
                # 'text': "Preventive Ratio distribution by ward",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
              },
              'legend': {
                  'position': "bottom"
              },
              'labels':{
                'usePointStyle': "true"
              },
              'scales': {
                  'yAxes': [{
                      'ticks': {
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold",
                          'beginAtZero': "false",
                         'maxTicksLimit': 6,
                          'padding': 20
                      },
                      'gridLines': {
                          'drawTicks': "true",
                          'display': "true"
                      }

                  }],
                  'xAxes': [{
                      'gridLines': {
                          'zeroLineColor': "transparent"
                      },
                      'ticks': {
                          'padding': 20,
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold"
                      }
                  }]
              }
          }
            }
            return Response({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)


class TreatmentPreventionRatioVisualizationOriginal(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month=[1,2,3,4,5,6,7,8,9,10,11,12]
            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v=[]
                for x in month:
                    if Visualization.objects.filter(geography_id=i.id).exists():
                        total_seal = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,seal=True).count()
                        total_fv = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,fv=True).count()
                        total_exo = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,exo=True).count()
                        total_art = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,exo=True).count()
                        total_sdf = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,sdf=True).count()
                        try:
                            preventive_ratio = (total_seal+total_fv)/(total_exo+total_art+total_sdf)
                        except:
                            preventive_ratio=0
                        v.append(preventive_ratio)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)",\
            "rgba(173, 96, 188, 1)","rgba(228, 96, 188, 1)","rgba(228, 29, 182, 1)",\
            "rgba(211, 29, 63, 1)","rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)",\
            "rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)",\
            "rgba(255, 159, 64, 1)"]
            
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 2.1,
            'maintainAspectRatio': "false",
            'title': {
                'display': '"true"',
                # 'text': "Preventive Ratio distribution by ward",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
              },
              'legend': {
                  'position': "bottom"
              },
              'labels':{
                'usePointStyle': "true"
              },
              'scales': {
                  'yAxes': [{
                      'ticks': {
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold",
                          'beginAtZero': "false",
                         'maxTicksLimit': 6,
                          'padding': 20
                      },
                      'gridLines': {
                          'drawTicks': "true",
                          'display': "true"
                      }

                  }],
                  'xAxes': [{
                      'gridLines': {
                          'zeroLineColor': "transparent"
                      },
                      'ticks': {
                          'padding': 20,
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold"
                      }
                  }]
              }
          }
            }
            return Response({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)


# 2.4 Early Intervention Ratio
class TreatmentEarlyIntervention(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month=[1,2,3,4,5,6,7,8,9,10,11,12]
            # label_data = [
            #     "Baishakh(Apr/May)",
            #     "Jestha(May/Jun)",
            #     "Asar(Jun/Jul)",
            #     "Shrawan(Jul/Aug)",
            #     "Bhadra(Aug/Sep)",
            #     "Asoj(Sep/Oct)",
            #     "Kartik(Oct/Nov)",
            #     "Mangsir(Nov/Dec)",
            #     "Poush(Dec/Jan)",
            #     "Magh(Jan/Feb)",
            #     "Falgun(Feb/Mar)",
            #     "Chaitra(Mar/Apr)",
            # ]

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
            x=month_obj[::-1]
            for b in x:
                month.insert(0, b)
            y=label_data_obj[::-1]
            for n in y:
                label_data.insert(0, n)
            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v=[]
                for x in month:
                    if Visualization.objects.filter(geography_id=i.id).exists():
                        if Visualization.objects.filter(active=True,created_at__month=x,geography_id=i.id).aggregate(Sum('art'))['art__sum'] is not None:
                            total_art = Visualization.objects.filter(active=True,created_at__month=x,geography_id=i.id).aggregate(Sum('art'))['art__sum']  
                        if Visualization.objects.filter(active=True,created_at__month=x,geography_id=i.id).aggregate(Sum('exo'))['exo__sum'] is not None:
                            total_exo = Visualization.objects.filter(active=True,created_at__month=x,geography_id=i.id).aggregate(Sum('exo'))['exo__sum']  
                        if Visualization.objects.filter(active=True,created_at__month=x,geography_id=i.id).aggregate(Sum('sdf'))['sdf__sum'] is not None:
                            total_sdf = Visualization.objects.filter(active=True,created_at__month=x,geography_id=i.id).aggregate(Sum('sdf'))['sdf__sum']  
                        try:
                            early_intervention_ratio = (total_art+total_sdf)/(total_exo)
                        except:
                            early_intervention_ratio=0
                        v.append(early_intervention_ratio)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)",\
            "rgba(173, 96, 188, 1)","rgba(228, 96, 188, 1)","rgba(228, 29, 182, 1)",\
            "rgba(211, 29, 63, 1)","rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)",\
            "rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)",\
            "rgba(255, 159, 64, 1)",]
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': label_data,
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 1.1,
            'maintainAspectRatio': "false",
            'title': {
                'display': '"true"',
                # 'text': "Early Intervention Ratio distribution by ward",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
              },
              'legend': {
                  'position': "bottom"
              },
              'labels':{
                'usePointStyle': "true"
              },
              'scales': {
                  'yAxes': [{
                      'ticks': {
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold",
                          'beginAtZero': "false",
                         'maxTicksLimit': 6,
                          'padding': 20
                      },
                      'gridLines': {
                          'drawTicks': "true",
                          'display': "true"
                      }

                  }],
                  'xAxes': [{
                      'gridLines': {
                          'zeroLineColor': "transparent"
                      },
                      'ticks': {
                          'padding': 20,
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold"
                      }
                  }]
              }
          }
            }
            return Response({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)


class TreatmentEarlyInterventionOriginal(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month=[1,2,3,4,5,6,7,8,9,10,11,12]
            # label_data = [
            #     "Baishakh(Apr/May)",
            #     "Jestha(May/Jun)",
            #     "Asar(Jun/Jul)",
            #     "Shrawan(Jul/Aug)",
            #     "Bhadra(Aug/Sep)",
            #     "Asoj(Sep/Oct)",
            #     "Kartik(Oct/Nov)",
            #     "Mangsir(Nov/Dec)",
            #     "Poush(Dec/Jan)",
            #     "Magh(Jan/Feb)",
            #     "Falgun(Feb/Mar)",
            #     "Chaitra(Mar/Apr)",
            # ]

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
            x=month_obj[::-1]
            for b in x:
                month.insert(0, b)
            y=label_data_obj[::-1]
            for n in y:
                label_data.insert(0, n)
            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v=[]
                for x in month:
                    if Visualization.objects.filter(geography_id=i.id).exists():
                        total_exo = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,exo=True).count()
                        total_art = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,exo=True).count()
                        total_sdf = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,sdf=True).count()
                        try:
                            early_intervention_ratio = (total_art+total_sdf)/(total_exo)
                        except:
                            early_intervention_ratio=0
                        v.append(early_intervention_ratio)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)",\
            "rgba(173, 96, 188, 1)","rgba(228, 96, 188, 1)","rgba(228, 29, 182, 1)",\
            "rgba(211, 29, 63, 1)","rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)",\
            "rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)",\
            "rgba(255, 159, 64, 1)",]
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': label_data,
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 1.1,
            'maintainAspectRatio': "false",
            'title': {
                'display': '"true"',
                # 'text': "Early Intervention Ratio distribution by ward",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
              },
              'legend': {
                  'position': "bottom"
              },
              'labels':{
                'usePointStyle': "true"
              },
              'scales': {
                  'yAxes': [{
                      'ticks': {
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold",
                          'beginAtZero': "false",
                         'maxTicksLimit': 6,
                          'padding': 20
                      },
                      'gridLines': {
                          'drawTicks': "true",
                          'display': "true"
                      }

                  }],
                  'xAxes': [{
                      'gridLines': {
                          'zeroLineColor': "transparent"
                      },
                      'ticks': {
                          'padding': 20,
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold"
                      }
                  }]
              }
          }
            }
            return Response({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)


# 2.5 Recall Percentage
class TreatmentRecallDistribution(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month=[1,2,3,4,5,6,7,8,9,10,11,12]
            # label_data = [
            #     "Baishakh(Apr/May)",
            #     "Jestha(May/Jun)",
            #     "Asar(Jun/Jul)",
            #     "Shrawan(Jul/Aug)",
            #     "Bhadra(Aug/Sep)",
            #     "Asoj(Sep/Oct)",
            #     "Kartik(Oct/Nov)",
            #     "Mangsir(Nov/Dec)",
            #     "Poush(Dec/Jan)",
            #     "Magh(Jan/Feb)",
            #     "Falgun(Feb/Mar)",
            #     "Chaitra(Mar/Apr)",
            # ]

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
            x=month_obj[::-1]
            for b in x:
                month.insert(0, b)
            y=label_data_obj[::-1]
            for n in y:
                label_data.insert(0, n)

            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v=[]
                for x in month:
                    if Visualization.objects.filter(geography_id=i.id).exists():
                        total_encounter = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x).count()
                        
                        total_recall = 0
                        e_male = Visualization.objects.filter(active=True,
                            geography_id=i.id,
                            created_at__month=x,
                        ).values('patiend_id').distinct()
                        for j in e_male:
                            l_en = Visualization.objects.filter(active=True,
                                geography_id=i.id,
                                patiend_id=j["patiend_id"],
                                created_at__month=x,
                                ).order_by('-created_at').first()
                            if l_en:
                                a = Visualization.objects.filter(active=True,
                                    geography_id=i.id,
                                    refer_hp=True,
                                    patiend_id=j["patiend_id"],
                                ).exclude(encounter_id=l_en.encounter_id).order_by('-created_at').first()
                                if a:
                                    if a.recall_date:
                                        d1 = l_en.created_at
                                        d2 = a.recall_date
                                        diff = abs((d1 - d2).days)
                                        if diff < 16 and diff > 0:
                                            total_recall += 1

                        try:
                            recall = round(total_recall * 100/total_encounter,2)
                        except:
                            recall=0
                        v.append(recall)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)",\
            "rgba(173, 96, 188, 1)","rgba(228, 96, 188, 1)","rgba(228, 29, 182, 1)",\
            "rgba(211, 29, 63, 1)","rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)",\
            "rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)",\
            "rgba(255, 159, 64, 1)",]
            
            
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': label_data,
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 1.1,
            'maintainAspectRatio': "false",
            'title': {
                'display': '"true"',
                # 'text': "% Recall distribution by ward",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
              },
              'legend': {
                  'position': "bottom"
              },
              'labels':{
                'usePointStyle': "true"
              },
              'scales': {
                  'yAxes': [{
                      'ticks': {
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold",
                          'beginAtZero': "false",
                         'maxTicksLimit': 6,
                          'padding': 20
                      },
                      'gridLines': {
                          'drawTicks': "true",
                          'display': "true"
                      }

                  }],
                  'xAxes': [{
                      'gridLines': {
                          'zeroLineColor': "transparent"
                      },
                      'ticks': {
                          'padding': 20,
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold"
                      }
                  }]
              }
          }
            }
            return Response({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)


class TreatmentRecallDistributionOriginal(APIView):
      def get(self, request, format=None):
        if User.objects.filter(id=request.user.id).exists():
            month=[1,2,3,4,5,6,7,8,9,10,11,12]
            # label_data = [
            #     "Baishakh(Apr/May)",
            #     "Jestha(May/Jun)",
            #     "Asar(Jun/Jul)",
            #     "Shrawan(Jul/Aug)",
            #     "Bhadra(Aug/Sep)",
            #     "Asoj(Sep/Oct)",
            #     "Kartik(Oct/Nov)",
            #     "Mangsir(Nov/Dec)",
            #     "Poush(Dec/Jan)",
            #     "Magh(Jan/Feb)",
            #     "Falgun(Feb/Mar)",
            #     "Chaitra(Mar/Apr)",
            # ]

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
            x=month_obj[::-1]
            for b in x:
                month.insert(0, b)
            y=label_data_obj[::-1]
            for n in y:
                label_data.insert(0, n)

            geography=[]
            geography_patient=[]
            geography_obj = Ward.objects.filter(status=True)
            for i in geography_obj:
                v=[]
                for x in month:
                    if Visualization.objects.filter(geography_id=i.id).exists():
                        total_encounter = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x).count()
                        total_recall = Visualization.objects.filter(active=True,geography_id=i.id,created_at__month=x,refer_hp=True).count()
                        try:
                            recall = total_recall/total_encounter
                        except:
                            recall=0
                        v.append(recall)
                geography.append(i.name)
                geography_patient.append(v)
            data_data=[]
            datasets1=[]
            cz=["rgba(234, 196, 53, 1)","rgba(49, 55, 21, 1)","rgba(117, 70, 104, 1)",\
            "rgba(127, 184, 0, 1)","rgba(3, 206, 164, 1)","rgba(228, 0, 102, 1)",\
            "rgba(52, 89, 149, 1)","rgba(243, 201, 139, 1)","rgba(251, 77, 61, 1)",\
            "rgba(230, 232, 230, 1)","rgba(248, 192, 200, 1)","rgba(44, 85, 48, 1)",\
            "rgba(231, 29, 54, 1)","rgba(96, 95, 94, 1)","rgba(22, 12, 40, 1)",\
            "rgba(173, 96, 188, 1)","rgba(228, 96, 188, 1)","rgba(228, 29, 182, 1)",\
            "rgba(211, 29, 63, 1)","rgba(255, 99, 132, 1)","rgba(54, 162, 235, 1)",\
            "rgba(255, 206, 86, 1)","rgba(75, 192, 192, 1)","rgba(153, 102, 255, 1)",\
            "rgba(255, 159, 64, 1)",]
            
            
            m=0
            n=0
            for y in geography:
                a={
                'label': y,
                'backgroundColor': "rgba(255, 255, 255, 0)",
                'borderColor':cz[m] ,
                'borderWidth': 1,
                'data': geography_patient[n]
                }
                datasets1.append(a)
                m += 1
                n +=1
            locationChart = {
            'data': {
            'labels': label_data,
            'datasets': datasets1
            },
            'options': {
            'aspectRatio': 1.1,
            'maintainAspectRatio': "false",
            'title': {
                'display': '"true"',
                # 'text': "% Recall distribution by ward",
                'fontSize': 18,
                'fontFamily': "'Palanquin', sans-serif"
              },
              'legend': {
                  'position': "bottom"
              },
              'labels':{
                'usePointStyle': "true"
              },
              'scales': {
                  'yAxes': [{
                      'ticks': {
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold",
                          'beginAtZero': "false",
                         'maxTicksLimit': 6,
                          'padding': 20
                      },
                      'gridLines': {
                          'drawTicks': "true",
                          'display': "true"
                      }

                  }],
                  'xAxes': [{
                      'gridLines': {
                          'zeroLineColor': "transparent"
                      },
                      'ticks': {
                          'padding': 20,
                          'fontColor': "rgba(0,0,0,0.5)",
                          'fontStyle': "bold"
                      }
                  }]
              }
          }
            }
            return Response({"locationChart":locationChart})
        return Response({"message":"only admin can see"},status=400)


