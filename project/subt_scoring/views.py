from rest_framework import views, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone

from .authentications import BearerAuthentication
from .parsers import CBORParser
from . import models as dcm
from . import serializers as dcs

class UserViewSet(viewsets.ModelViewSet):
    """
    This endpoint represents users of the system

    There is a users/current/ endpoint to retrieve the current user
    """
    queryset = User.objects.all()
    serializer_class = dcs.UserBasicSerializer

class TokenViewSet(viewsets.ModelViewSet):
    
    queryset = dcm.Token.objects.all()
    serializer_class = dcs.TokenSerializer


class StatusView(views.APIView):
    """
    Endpoint to receive status of the current run
    """


    def get(self, request, format=None):
        to_return = {}
        to_return['score'] = 9000
        to_return['run_clock'] = 25.98
        to_return['remaining_reports'] = 6
        to_return['current_team'] = request.user.username
        return Response(to_return, content_type="application/json")


class ArtifactReportView(views.APIView):
    """
    Endpoint for submitting artifact reports
    """
    

    def post(self, request, format=None):
        if not isinstance(request.data, dict):
            return Response("Expected JSON object", status=status.HTTP_400_BAD_REQUEST, content_type="application/json")
        try:
            # TODO replace this with proper parsing of data
            request.data["x"]
            request.data["y"]
            request.data["z"]
            request.data["type"]
        except KeyError as e:
            error_string = "Missing field: {}".format(e)
            return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")
        
        to_return = {}
        to_return["url"] = "http://<ipaddress>:<port>/api/artifact_reports/1"
        to_return["id"] = 9
        to_return["x"] = request.data["x"]
        to_return["y"] = request.data["y"]
        to_return["z"] = request.data["z"]
        to_return["type"] = request.data["type"]
        to_return["submitted_datetime"] = timezone.now().isoformat()
        to_return["run_clock"] = 3.14
        to_return["team"] = request.user.username
        to_return["run"] = "1"
        to_return["report_status"] = "scored"

        if request.data["type"].lower() in ["survivor", "backpack", "cell phone", "vent", "gas"]:
            to_return["score_change"] = 1
        else: 
            to_return["score_change"] = 0

        return Response(to_return, status=status.HTTP_201_CREATED, content_type="application/json")



class MapUpdateView(views.APIView):
    """
    Endpoint to submit map telemetry
    """

    parser_classes =  [JSONParser, CBORParser,]

    map_2D = "OccupancyGrid"
    map_3D = "PointCloud2"

    def parse_map_2D(self, msg):
        header = msg.get("header")
        if header:
            stamp = header.get("stamp")
            frame_id = header.get("frame_id")

        try:
            info = msg["info"]
            data = msg["data"]
            compression = msg.get("compression")

            temp = info["resolution"]
            temp = info["width"]
            temp = info["height"]
            origin = info["origin"]

            pos = origin["position"]
            orientation = origin["orientation"]

            temp = pos["x"]
            temp = pos["y"]
            temp = pos["z"]
            temp = orientation["x"]
            temp = orientation["y"]
            temp = orientation["z"]
            temp = orientation["w"]
        except KeyError as e:
            error_string = "Missing field: {}".format(e)
            return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")

        # TODO Do other processing
        return Response(None, content_type="application/json")

    def parse_map_3D(self, msg):
        header = msg.get("header")
        if header:
            stamp = header.get("stamp")
            frame_id = header.get("frame_id")
        
        origin = msg.get("origin")
        if origin:
            origin["position"]
            origin["orientation"]
        
        msg.get("is_bigendian")
        msg.get("compression")

        try:
            point_schema = msg["fields"]
            msg["point_step"]
            msg["data"]
        except KeyError as e:
            error_string = "Missing field: {}".format(e)
            return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")
        
        for field in point_schema:
            pass

        return Response(None, content_type="application/json")

    def post(self, request, format=None):
        if not isinstance(request.data, dict):
            return Response("Expected JSON/CBOR object", status=status.HTTP_400_BAD_REQUEST, content_type="application/json")
        try:
            map_type = request.data["type"]
            map_message = request.data["msg"]
        except KeyError as e:
            error_string = "Missing field: {}".format(e)
            return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")
        
        if map_type == "OccupancyGrid":
            return self.parse_map_2D(map_message)
        elif map_type == "PointCloud2":
            return self.parse_map_3D(map_message)
        else:
            error_string = "Invalid map type, choose between {} or {}".format(map_2D, map_3D)
            return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")

class StateUpdateView(views.APIView):
    """
    Endpoint to submit entity state telemetry
    """

    parser_classes =  [JSONParser, CBORParser,]

    def post(self, request, format=None):
        if not isinstance(request.data, dict):
            return Response("Expected JSON/CBOR object", status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

        header = request.data.get("header")
        if header:
            stamp = header.get("stamp")
            frame_id = header.get("frame_id")

        try:
            list_of_poses = request.data["poses"]
        except KeyError:
            return Response("Missing pose field", status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")

        for index, pose in enumerate(list_of_poses):
            # Do something with each pose
            try:
                pose["position"]["x"]
                pose["position"]["y"]
                pose["position"]["z"]
            except KeyError as e:
                error_string = "Missing position field: {} at pose #: {}".format(e, index)
                return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")
            try:
                pose["orientation"]["x"]
                pose["orientation"]["y"]
                pose["orientation"]["z"]
                pose["orientation"]["w"]
            except KeyError as e:
                error_string = "Missing orientation field: {} at pose #: {}".format(e, index)
                return Response(error_string, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="application/json")


        return Response(None, content_type="application/json")
