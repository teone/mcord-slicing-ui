import json
import os
import sys
import traceback
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework import generics
from rest_framework import status
from core.models import *
from xos.apibase import XOSListCreateAPIView, XOSRetrieveUpdateDestroyAPIView, XOSPermissionDenied
from api.xosapi_helpers import XOSViewSet

nodes = [
    {"id": 1, "name": "vRouter", "type": "upstream", "model_id": 1, "plane": "data"},





            {"id": 21, "name": "ran-ru-1", "type": "ran-ru", "model_id": 1, "plane": "data"},
            {"id": 22, "name": "ran-cu-1", "type": "ran-cu", "model_id": 1, "plane": "data"},
            {"id": 23, "name": "sgw-1", "type": "sgw", "model_id": 1, "plane": "data"},
            {"id": 24, "name": "pgw-1", "type": "pgw", "model_id": 1, "plane": "data"},

            {"id": 25, "name": "ran-ru-1", "type": "ran-ru", "model_id": 1, "plane": "control", "model": {"DlSchedType": "RR", "DlAllocRBRate": 30, "UlSchedType": "RR", "UlAllocRBRate": 30}},
            {"id": 26, "name": "ran-cu-1", "type": "ran-cu", "model_id": 1, "plane": "control", "model": {"AdmissionControl": 0,"HandHover": 10}},
            {"id": 27, "name": "sgw-1", "type": "sgw", "model_id": 1, "plane": "control"},
            {"id": 28, "name": "pgw-1", "type": "pgw", "model_id": 1, "plane": "control", "model": {"brand": "Quortus"}},
            {"id": 29, "name": "mme-1", "type": "mme", "model_id": 1, "plane": "control"},

            {"id": 210, "name": "profile-1", "type": "profile", "model_id": 1, "plane": "data", "model": {"start": "2016-01-01T08:00:00.000Z", "end": "2016-12-01T08:00:00.000Z"}},
            {"id": 220, "name": "profile-2", "type": "profile", "model_id": 1, "plane": "data", "model": {"start": "2016-01-01T08:00:00.000Z", "end": "2016-12-01T08:00:00.000Z"}},

            {"id": 211, "name": "ue-1", "type": "ue", "model_id": 1, "plane": "data", "model": {"id": 123}},
            {"id": 212, "name": "ue-2", "type": "ue", "model_id": 1, "plane": "data", "model": {"id": 456}},
            {"id": 221, "name": "ue-3", "type": "ue", "model_id": 1, "plane": "data", "model": {"id": 789}},




            {"id": 31, "name": "ran-ru-2", "type": "ran-ru", "model_id": 1, "plane": "data"},
            {"id": 32, "name": "ran-cu-2", "type": "ran-cu", "model_id": 1, "plane": "data"},
            {"id": 33, "name": "sgw-2", "type": "sgw", "model_id": 1, "plane": "data"},
            {"id": 34, "name": "pgw-2", "type": "pgw", "model_id": 1, "plane": "data"},

            {"id": 35, "name": "ran-ru-2", "type": "ran-ru", "model_id": 1, "plane": "control", "model": {"DlSchedType": "RR", "DlAllocRBRate": 30, "UlSchedType": "RR", "UlAllocRBRate": 30}},
            {"id": 36, "name": "ran-cu-2", "type": "ran-cu", "model_id": 1, "plane": "control", "model": {"AdmissionControl": 1,"HandHover": 10}},
            {"id": 37, "name": "sgw-2", "type": "sgw", "model_id": 1, "plane": "control"},
            {"id": 38, "name": "pgw-2", "type": "pgw", "model_id": 1, "plane": "control", "model": {"brand": "Radysis"}},
            {"id": 39, "name": "mme-2", "type": "mme", "model_id": 1, "plane": "control"},

            {"id": 310, "name": "profile-3", "type": "profile", "model_id": 1, "plane": "data", "model": {"start": "2016-01-01T08:00:00.000Z", "end": "2016-12-01T08:00:00.000Z"}},

            {"id": 311, "name": "ue-4", "type": "ue", "model_id": 1, "plane": "data", "model": {"id": 321}},
            {"id": 312, "name": "ue-5", "type": "ue", "model_id": 1, "plane": "data", "model": {"id": 654}}
]

links = [
    # Slice 1 links
    {"id": 1, "source": 24, "target": 1, "plane": "data"},

    {"id": 2, "source": 21, "target": 22, "plane": "data"},
    {"id": 3, "source": 22, "target": 23, "plane": "data"},
    {"id": 4, "source": 23, "target": 24, "plane": "data"},

    {"id": 5, "source": 21, "target": 25, "plane": "control"},
    {"id": 6, "source": 22, "target": 26, "plane": "control"},
    {"id": 7, "source": 23, "target": 27, "plane": "control"},
    {"id": 8, "source": 24, "target": 28, "plane": "control"},
    {"id": 9, "source": 25, "target": 26, "plane": "control"},
    {"id": 10, "source": 26, "target": 29, "plane": "control"},
    {"id": 11, "source": 27, "target": 28, "plane": "control"},
    {"id": 12, "source": 27, "target": 29, "plane": "control"},

    {"id": 13, "source": 210, "target": 21, "plane": "data"},
    {"id": 14, "source": 220, "target": 21, "plane": "data"},

    {"id": 15, "source": 211, "target": 210, "plane": "data"},
    {"id": 16, "source": 212, "target": 210, "plane": "data"},
    {"id": 17, "source": 221, "target": 220, "plane": "data"},

    # Slice 2 Links
    {"id": 18, "source": 34, "target": 1, "plane": "data"},

    {"id": 19, "source": 31, "target": 32, "plane": "data"},
    {"id": 20, "source": 32, "target": 33, "plane": "data"},
    {"id": 21, "source": 33, "target": 34, "plane": "data"},

    {"id": 22, "source": 31, "target": 35, "plane": "control"},
    {"id": 23, "source": 32, "target": 36, "plane": "control"},
    {"id": 24, "source": 33, "target": 37, "plane": "control"},
    {"id": 25, "source": 34, "target": 38, "plane": "control"},
    {"id": 26, "source": 35, "target": 36, "plane": "control"},
    {"id": 27, "source": 36, "target": 39, "plane": "control"},
    {"id": 28, "source": 37, "target": 38, "plane": "control"},
    {"id": 29, "source": 37, "target": 39, "plane": "control"},

    {"id": 30, "source": 310, "target": 31, "plane": "data"},

    {"id": 31, "source": 311, "target": 310, "plane": "data"},
    {"id": 32, "source": 312, "target": 310, "plane": "data"}

]

class MCORDSlicingUIViewSet(XOSViewSet):
    base_name = "topology"
    method_name = "topology"
    method_kind = "viewset"

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = []

        patterns.append( self.list_url("", {"get": "get_topology"}, "mcord-slicing-topo") )

        return patterns

    def get_topology(self, request):
        result = {
            'nodes': nodes,
            'links': links
        }
        return Response( result )