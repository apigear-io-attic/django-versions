from django.contrib.auth.models import User, Group
from .models import Document
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action

from reversion.models import Version
from actstream.models import Action, action_object_stream


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'content']


class DocumentActionSerializer(serializers.ModelSerializer):
    actor = DocumentSerializer()

    class Meta:
        model = Action
        fields = ['id', 'verb', 'timestamp', 'actor']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows documents to be viewed or edited.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        doc = self.get_object()
        serializer = self.get_serializer(doc)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def activity(self, request, pk=None):
        doc = self.get_object()
        activities = doc.actor_actions.all()
        serializer = DocumentActionSerializer(activities, many=True)
        return Response(serializer.data)
