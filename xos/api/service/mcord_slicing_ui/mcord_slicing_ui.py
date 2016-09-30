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

class MCORDSlicingUIViewSet(XOSViewSet):
    base_name = "mcord"
    method_name = "mcord"
    method_kind = "viewset"

    @classmethod
    def get_urlpatterns(self, api_path="^"):
        patterns = []

        patterns.append( self.list_url("slicing-topo/$", {"get": "get_topology"}, "mcord-slicing-topo") )

        return patterns

    def get_topology(self, request):
        result = {
            nodes: [],
            links: []
        }
        return Response( json.dumps(result) )







