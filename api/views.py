from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.views import exception_handler

from accounts.models import CustomUser
from core.models import College, Unit, Department, Campus, Staff
from api.serializers import CollegeSerializer, UnitReadSerializer, DepartmentReadSerializer, CampusSerializer, \
    StaffReadSerializer, \
    UserSerializer, UnitWriteSerializer, DepartmentWriteSerializer, StaffWriteSerializer


class IsUnitManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Unit Manager').exists()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()


class IsCampusManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Campus Manager').exists()


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Superuser').exists()


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


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
    permission_classes = [IsAuthenticated & IsUnitManager & IsAdmin]


class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    permission_classes = [IsAuthenticated & IsSuperuser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DepartmentReadSerializer
        else:
            return DepartmentWriteSerializer


class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentWriteSerializer
    permission_classes = [IsAuthenticated & IsUnitManager & IsSuperuser]


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [IsAuthenticated & IsSuperuser]


class StaffRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StaffReadSerializer
        else:
            return StaffWriteSerializer


class StaffCreateView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffWriteSerializer
    permission_classes = [IsAuthenticated & IsUnitManager & IsSuperuser]
