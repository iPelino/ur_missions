from rest_framework import serializers

from accounts.models import CustomUser
from core.models import College, Unit, Department, Campus, Staff, MissionOrder, Transportation, MissionAttachment, \
    MissionRoleChoices, DestinationChoices, Approval
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
    password = serializers.CharField(write_only=True)
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
    )
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'password', 'is_active', 'is_staff', 'date_joined', 'last_login', 'groups', 'permissions')

        extra_kwargs = {
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'password': {'write_only': True},
            'permissions': {'read_only': True},
        }

    def get_permissions(self, obj):
        return ([perm.codename for perm in obj.user_permissions.all()] +
                [perm.codename for perm in Permission.objects.filter(group__user=obj)])

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

    def validate(self, attrs):
        groups = attrs.get('groups', [])
        request = self.context.get('request')
        if request and not request.user.is_superuser:
            superuser_group = Group.objects.get(name='Superuser')
            if superuser_group in groups:
                raise serializers.ValidationError("Only a superuser can add someone to the superuser group.")
        return attrs


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


class MissionOrderAttachmentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = MissionAttachment
        fields = ('id', 'mission_order', 'attachment', 'created', 'modified')


class TransportationSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Transportation
        fields = ('id', 'transportation_means', 'vehicle_identification', 'driver_name', 'created', 'modified')


class MissionOrderReadSerializer(BaseSerializer):
    staff = StaffReadSerializer(read_only=True)
    unit = UnitReadSerializer(read_only=True)
    transportation = TransportationSerializer(read_only=True)
    attachments = MissionOrderAttachmentSerializer(many=True, read_only=True)

    class Meta(BaseSerializer.Meta):
        model = MissionOrder
        fields = (
            'id', 'staff', 'unit', 'role', 'purpose_of_mission', 'expected_results', 'destination', 'distance_km',
            'departure_date', 'returning_date', 'duration_days', 'duration_nights', 'transportation', 'supervisor_name',
            'supervisor_signature', 'approval_details', 'attachments', 'created', 'modified'
        )


class MissionOrderWriteSerializer(BaseWriteSerializer):
    staff = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    attachments = MissionOrderAttachmentSerializer(many=True, required=False)
    transportation = TransportationSerializer(required=False)
    role = serializers.ChoiceField(choices=MissionRoleChoices.choices, default=MissionRoleChoices.choices[0][0])
    destination = serializers.ChoiceField(choices=DestinationChoices.choices, default=DestinationChoices.choices[0][0])

    class Meta(BaseSerializer.Meta):
        model = MissionOrder
        fields = (
            'id', 'staff', 'unit', 'role', 'purpose_of_mission', 'expected_results', 'destination', 'distance_km',
            'departure_date', 'returning_date', 'duration_days', 'duration_nights', 'transportation', 'supervisor_name',
            'supervisor_signature', 'approval_details', 'attachments', 'created', 'modified'
        )

    def validate(self, data):
        if data['departure_date'] > data['returning_date']:
            raise serializers.ValidationError("The departure date cannot be later than the returning date.")
        if data['duration_days'] < 1:
            raise serializers.ValidationError("The duration days must be positive numbers.")
        if 'staff' in data and not Staff.objects.filter(id=data['staff']).exists():
            raise serializers.ValidationError("The specified staff does not exist.")
        if 'unit' in data and not Unit.objects.filter(id=data['unit']).exists():
            raise serializers.ValidationError("The specified unit does not exist.")
        return data

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        transportation_data = validated_data.pop('transportation', None)

        # Calculate duration_days and duration_nights
        validated_data['duration_days'] = (validated_data['returning_date'] - validated_data['departure_date']).days
        validated_data['duration_nights'] = validated_data['duration_days'] - 1 if validated_data[
                                                                                       'duration_days'] > 0 else 0

        mission_order = MissionOrder.objects.create(**validated_data)
        for attachment_data in attachments_data:
            MissionAttachment.objects.create(mission_order=mission_order, **attachment_data)
        if transportation_data:
            Transportation.objects.create(mission_order=mission_order, **transportation_data)
        return mission_order


class MissionOrderApprovalSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Approval
        fields = ('id', 'mission_order', 'approver', 'status', 'approval_date', 'comments', 'rejected',
                  'rejection_reason', 'created', 'modified')
