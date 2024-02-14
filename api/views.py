from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.views import exception_handler

from accounts.models import CustomUser
from core.models import College, Unit, Department, Campus, Staff
from api.serializers import CollegeSerializer, UnitReadSerializer, DepartmentReadSerializer, CampusSerializer, \
    StaffReadSerializer, \
    CustomUserSerializer, UnitWriteSerializer, DepartmentWriteSerializer, StaffWriteSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class UnitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unit.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UnitReadSerializer
        else:
            return UnitWriteSerializer


class UnitCreateView(generics.CreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitWriteSerializer


class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DepartmentReadSerializer
        else:
            return DepartmentWriteSerializer


class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentWriteSerializer


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class StaffRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StaffReadSerializer
        else:
            return StaffWriteSerializer


class StaffCreateView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffWriteSerializer


