from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CollegeViewSet, CampusViewSet, DepartmentRetrieveUpdateDestroyView, \
    DepartmentCreateView, UnitRetrieveUpdateDestroyView, UnitCreateView, StaffCreateView, \
    StaffRetrieveUpdateDestroyView, MissionOrderCreateView, MissionOrderRetrieveUpdateDestroyView, \
    MissionApprovalCreateView, MissionApprovalUpdateView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'campuses', CampusViewSet)
router.register(r'colleges', CollegeViewSet)

urlpatterns = [
    path('units/', UnitCreateView.as_view(), name='unit-create'),
    path('units/<int:pk>/', UnitRetrieveUpdateDestroyView.as_view(), name='unit-detail'),

    path('departments/', DepartmentCreateView.as_view(), name='department-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department-detail'),
    path('staff/', StaffCreateView.as_view(), name='staff-create'),
    path('staff/<int:pk>/', StaffRetrieveUpdateDestroyView.as_view(), name='staff-detail'),

    path('missions-orders/', MissionOrderCreateView.as_view(), name='mission-order-create'),
    path('missions-orders/<int:pk>/', MissionOrderRetrieveUpdateDestroyView.as_view(), name='mission-order-detail'),

    path('missions-approvals/', MissionApprovalCreateView.as_view(), name='mission-approval-create'),
    path('missions-approvals/<int:pk>/', MissionApprovalUpdateView.as_view(), name='mission-approval-update'),


] + router.urls
