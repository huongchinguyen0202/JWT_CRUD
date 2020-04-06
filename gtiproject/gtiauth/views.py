from django.views import View
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from gtiauth.utils.jsonreader import JsonReader
from gtiauth.models import User
from django.core.serializers import serialize
from gtiauth import UserSerializer
import requests
import json

class GtiAuth(View):
    serializer_class = UserSerializer

    @api_view(["POST"])
    def api_login(request):
        """
        post:
        This view is called through API POST with a json body like so:

        {
            "username": "admin",
            "password": "admin"
        }

        :param request:
        :return:
        """
        data = JsonReader.read_body(request)

        response_login = requests.post(
            request.build_absolute_uri(reverse('obtain_jwt_token')),
            data=data
        )
        response_login_dict = json.loads(response_login.content)
        # response_login_dict["user"] = json.loads(serialize('json', User.objects.raw("SELECT * FROM gti.gtiauth_user;")))
        # userSerializer = UserSerializer(User.objects.raw("SELECT * FROM gti.gtiauth_user;"), many = True)
        userSerializer = UserSerializer(User.objects.all(), many = True)
        # response_login_dict["user"] = JSONRenderer().render(serializer.data)

        return Response(response_login_dict, response_login.status_code)

    @api_view(['GET', 'PUT'])
    def api_user_detail(request, pk):
        """
        get:
        Detail one user.
        put:
        Update one user.
        """
        try:
            user_inst = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        voter = UserVoter(request)
        if not voter.user_can_manage_me(user_inst):
            return Response({'error': "User API is not allowed"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = UserSerializer(user_inst)
            return Response(serializer.data)

        elif request.method == 'PUT':
            data = JsonReader.read_body(request)
            if 'is_staff' in data:
                if not voter.is_superuser():
                    return Response({'error': "Non admin cannot update admin attributes"}, status=status.HTTP_403_FORBIDDEN)
            serializer = UserSerializer(user_inst, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)