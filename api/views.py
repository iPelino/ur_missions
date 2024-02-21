from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler

from accounts.models import CustomUser
from core.models import College, Unit, Department, Campus, Staff, MissionOrder, Approval
from api.serializers import CollegeSerializer, UnitReadSerializer, DepartmentReadSerializer, CampusSerializer, \
    StaffReadSerializer, \
    UserSerializer, UnitWriteSerializer, DepartmentWriteSerializer, StaffWriteSerializer, MissionOrderReadSerializer, \
    MissionOrderWriteSerializer, MissionOrderApprovalSerializer


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


class IsSuperuserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Superuser', 'Admin']).exists()


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsSuperuserOrAdmin]


class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated & (IsUnitManager & IsSuperuserOrAdmin)]


class MissionOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MissionOrder.objects.all()
    serializer_class = MissionOrderReadSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MissionOrderReadSerializer
        else:
            return MissionOrderWriteSerializer


class MissionOrderCreateView(generics.CreateAPIView):
    queryset = MissionOrder.objects.all()
    serializer_class = MissionOrderWriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['staff'] = request.user.staff.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MissionApprovalCreateView(generics.CreateAPIView):
    queryset = Approval.objects.all()
    serializer_class = MissionOrderApprovalSerializer
    permission_classes = [IsAuthenticated & (IsUnitManager | IsCampusManager, IsSuperuserOrAdmin)]


class MissionApprovalUpdateView(generics.UpdateAPIView):
    queryset = Approval.objects.all()
    serializer_class = MissionOrderApprovalSerializer
    permission_classes = [IsAuthenticated & (IsAdmin | IsCampusManager | IsUnitManager | IsSuperuserOrAdmin)]
