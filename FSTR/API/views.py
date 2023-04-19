from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import *
from .models import *


class PassViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer

    @staticmethod
    def serializer_error_response(errors, param='id'):
        message = ''
        for k, v in errors.items():
            message += f'{k}: {str(*v)}'
        if param == 'state':
            return Response({'message': message, 'state': 0}, status=400)
        else:
            return Response({'message': message, 'id': None}, status=400)

    def validation(self, serializer):
        if serializer.is_valid():
            return serializer.save()
        else:
            return self.serializer_error_response(serializer.errors)

    @action(methods=['post'], detail=True)
    def post(self, request):
        data = request.data
        if not data:
            return Response({'message': 'Пустой запрос', 'id': None}, status=400)

        user = MyUser.objects.get_or_create(fam=data['user']['fam'],
                                            name=data['user']['name'],
                                            otc=data['user']['otc'],
                                            phone=data['user']['phone'],
                                            email=data['user']['email'])[0]
        user_serializer = UserSerializer(user, data=data['user'])

        coord = Coordinates.objects.get_or_create(latitude=data['coordinates']['latitude'],
                                                  longitude=data['coordinates']['longitude'],
                                                  height=data['coordinates']['height'])[0]
        coord_serializer = CoordinatesSerializer(coord, data=data['coordinates'])

        lvl = Level.objects.get_or_create(winter_level=data['levels']['winter_level'],
                                          summer_level=data['levels']['summer_level'],
                                          autumn_level=data['levels']['autumn_level'],
                                          spring_level=data['levels']['spring_level'])[0]
        lvl_serializer = LevelSerializer(lvl, data=data['levels'])

        try:
            images = data['images']
            data.pop('images')
        except:
            images = []

        try:
            self.validation(user_serializer)
            self.validation(coord_serializer)
            self.validation(lvl_serializer)
        except Exception as e:
            return Response({'message': str(e), 'id': None}, status=400)

        pass_serializer = PassSerializer(data=data)
        if pass_serializer.is_valid():
            try:
                data.pop('user')
                data.pop('coordinates')
                data.pop('levels')
                pass_new = Pass.objects.create(
                    user=user,
                    coordinates=coord,
                    levels=lvl,
                    **data)
            except Exception as e:
                return Response({'message': str(e), 'id': None}, status=400)
        else:
            return self.serializer_error_response(serializer.errors)

        for image in images:
            image['pass'] = pass_new.id
            self.validation(ImagesSerializer(data=image))

        return Response({'message': 'Успешно', 'id': pass_new.id}, status=200)

    @action(methods=['get'], detail=False)
    def get_email(self, request, **kwargs):
        try:
            user = MyUser.objects.get(email=request.GET['user_email'])
            passages = Pass.objects.filter(user=user)
            data = PassSerializer(passages, many=True).data
            return Response(data, status=200)
        except:
            return Response({'message': 'Записи не найдены'}, status=200)

    @action(method=['get'], detail=True)
    def get_one(self, request, **kwargs):
        try:
            pass_one = Pass.objects.get(pk=kwargs['pk'])
            data = PassSerializer(pass_one).data
            return Response(data, status=200)
        except:
            return Response({'message': "Такой записи не существует", 'id': None}, status=400)

    @action(methods=['patch'], detail=True)
    def change(self, request, **kwargs):
        try:
            pass_one = Pass.objects.get(pk=kwargs['pk'])
        except:
            return Response({'message': "Такой записи не существует", 'state': 0}, status=400)
        if pass_one.status == 'new':
            data = request.data
            data.pop('user')
            Images.objects.filter(passes=pass_one.id).delete()
            images = data.pop('images')
            serializers = []
            serializers.append(CoordinatesSerializer(Coordinates.objects.get(id=pass_one.coordinates_id),
                                                     data=data.pop('coordinates')))
            serializers.append(LevelSerializer(Level.objects.get(id=pass_one.levels_id), data=data.pop('levels')))
            serializers.append((PassSerializer(pass_one, data=data)))
            for image in images:
                image['pass'] = pass_one.id
                serializers.append(ImagesSerializer(data=image))
            for serializer in serializers:
                if serializer.is_valid():
                    serializer.save()
                else:
                    return self.serializer_error_response(serializer.errors)

            return Response({'message': 'Успешно', 'state': 1}, status=200)
        else:
            return Response({'message': "Статус записи не 'new'", 'state': 0}, status=400)
