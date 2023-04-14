from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import *


class APIView(viewsets.ViewSet):

    @staticmethod
    def serializer_error_response(errors, param='id'):
        message = ''
        for k, v in errors.items():
            message += f'{k}: {str(*v)}'
        if param == 'state':
            return Response({'message': message, 'state': 0}, status=400)
        else:
            return Response({'message': message, 'id': None}, status=400)

    def create_dependence(self, serializer):
        if serializer.is_valid():
            return serializer.save()
        else:
            return self.serializer_error_response(serializer.errors)

    @swagger_auto_schema(methods=['post'], request_body=PassSerializer)
    @api_view(['POST'])
    def post(self, request):
        try:
            data = request.data
            if not data:
                return Response({'message': 'Empty request', 'id': None}, status=400)

            try:
                user = User.objects.get(email=data['user']['email'])
                user_serializer = UserSerializer(user, data=data['user'])
            except:
                user_serializer = UserSerializer(data=data['user'])

            try:
                images = data['images']
                data.pop('images')
            except:
                images = []

            serializer = PassSerializer(data=data)
            if serializer.is_valid():
                try:
                    data.pop('user')
                    pass_new = Pass.objects.create(
                        user=self.create_dependence(user_serializer),
                        coords=self.create_dependence(CoordinatesSerializer(data=data.pop('coordinates'))),
                        levels=self.create_dependence(LevelSerializer(data=data.pop('level'))),
                        **data)
                except Exception as e:
                    return Response({'message': str(e), 'id': None}, status=400)
            else:
                return self.serializer_error_response(serializer.errors)

            for image in images:
                image['pass'] = pass_new.id
                self.create_dependence(ImagesSerializer(data=image))

            return Response({'message': 'Success', 'id': pass_new.id}, status=200)

        except Exception as e:
            return Response({'message': str(e), 'id': None}, status=500)
