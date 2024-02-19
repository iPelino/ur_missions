from rest_framework import serializers

from accounts.models import CustomUser
from core.models import College, Unit, Department, Campus, Staff
from django.contrib.auth.models import Group, Permission


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
        read_only_fields = ('created', 'modified')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_staff:
            representation['created'] = instance.created
            representation['modified'] = instance.modified
        else:
            del representation['created']
            del representation['modified']
        return representation


class BaseWriteSerializer(BaseSerializer):
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("The name field cannot be blank.")
        if self.Meta.model.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"A {self.Meta.model.__name__.lower()} with this name already exists.")
        return value

    def validate_short_name(self, value):
        if not value:
            raise serializers.ValidationError("The short_name field cannot be blank.")
        if self.Meta.model.objects.filter(short_name=value).exists():
            raise serializers.ValidationError(
                f"A {self.Meta.model.__name__.lower()} with this short name already exists.")
        return value


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    user_permissions = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_active', 'is_staff', 'date_joined', 'last_login', 'groups', 'user_permissions')


class CollegeSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = College
        fields = ('id', 'name', 'short_name', 'created', 'modified')


class UnitReadSerializer(BaseSerializer):
    college = CollegeSerializer(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Unit
        fields = ('id', 'name', 'short_name', 'description', 'college', 'created', 'modified')


class UnitWriteSerializer(BaseWriteSerializer):
    class Meta(BaseSerializer.Meta):
        model = Unit
        fields = ('id', 'name', 'short_name', 'description', 'college', 'created', 'modified')

    def validate_description(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("The description is too long.")
        return value


class DepartmentReadSerializer(BaseSerializer):
    unit = UnitReadSerializer(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Department
        fields = ('id', 'name', 'short_name', 'description', 'unit', 'created', 'modified')


class DepartmentWriteSerializer(BaseWriteSerializer):
    class Meta(BaseSerializer.Meta):
        model = Department
        fields = ('id', 'name', 'short_name', 'description', 'unit', 'created', 'modified')

    def validate_unit(self, value):
        if not Unit.objects.filter(id=value).exists():
            raise serializers.ValidationError("The specified unit does not exist.")
        return value


class CampusSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Campus
        fields = ('id', 'name', 'description', 'created', 'modified')


class StaffReadSerializer(BaseSerializer):
    user = UserSerializer(read_only=True)
    unit = UnitReadSerializer(read_only=True)
    campus = CampusSerializer(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Staff
        fields = (
            'id', 'user', 'first_name', 'last_name', 'gender', 'type', 'unit', 'campus', 'phone_number', 'created',
            'modified')


class StaffWriteSerializer(BaseWriteSerializer):
    phone_number = serializers.CharField(error_messages={'invalid': 'Invalid phone number.'})

    class Meta(BaseSerializer.Meta):
        model = Staff
        fields = (
            'id', 'user', 'first_name', 'last_name', 'gender', 'type', 'unit', 'campus', 'phone_number', 'created',
            'modified')

    def validate_user(self, value):
        if not CustomUser.objects.filter(id=value).exists():
            raise serializers.ValidationError("The specified user does not exist.")
        if Staff.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("The specified user is already a staff.")
        return value

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("The first_name field cannot be blank.")
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("The last_name field cannot be blank.")
        return value

    def validate_gender(self, value):
        if value not in ['M', 'F']:
            raise serializers.ValidationError("The gender must be either 'M' or 'F'.")
        return value

    def validate_type(self, value):
        if value not in ['T', 'NT']:
            raise serializers.ValidationError("The type must be either 'T' (Teaching) or 'NT' (Non-Teaching).")
        return value

    def validate_unit(self, value):
        if not Unit.objects.filter(id=value).exists():
            raise serializers.ValidationError("The specified unit does not exist.")
        return value

    def validate_campus(self, value):
        if not Campus.objects.filter(id=value).exists():
            raise serializers.ValidationError("The specified campus does not exist.")
        return value

    def validate_phone_number(self, value):
        # Check if phone number starts with country code and total length is 12
        if not (value.isdigit() and len(value) == 12):
            raise serializers.ValidationError("The phone number must start with country code (without '+') and the "
                                              "total length should be 12 characters.")
        return value
