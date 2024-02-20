from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.models import CustomUser


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class College(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'

    def __str__(self):
        return self.short_name


class Unit(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    description = models.TextField(max_length=500, blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    manager = models.OneToOneField('Staff', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='unit_manager'
                                   )

    class Meta:
        verbose_name = 'School/Unit'
        verbose_name_plural = 'Schools/Units'

    def __str__(self):
        return self.short_name


class Department(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    description = models.TextField(max_length=500, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name


# generate choices for gender
class GenderChoices(models.TextChoices):
    MALE = 'MALE', 'M'
    FEMALE = 'FEMALE', 'F'


class TypeChoices(models.TextChoices):
    ACADEMIC = 'ACADEMIC', 'T'
    NON_ACADEMIC = 'NON_ACADEMIC', 'NT'


class Campus(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class RoleChoices(models.TextChoices):
    STAFF = 'STAFF', 'Staff'
    UNIT_MANAGER = 'UNIT_MANAGER', 'Unit Manager'
    CAMPUS_MANAGER = 'CAMPUS_ADMIN', 'Campus Admin'
    DVC = 'DVC', 'DVC'
    VC = 'VC', 'VC'


class Staff(TimestampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    type = models.CharField(max_length=20, choices=TypeChoices.choices, default=TypeChoices.ACADEMIC)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    # role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.STAFF)

    def __str__(self):
        return self.user.email

    def get_next_approver(self):
        if self.groups.filter(name='Staff').exists():
            return self.unit.manager
        elif self.groups.filter(name='Unit Manager').exists():
            return Staff.objects.filter(groups__name='Campus Manager', unit__college=self.unit.college).first()
        elif self.groups.filter(name='Campus Manager').exists():
            return Staff.objects.filter(groups__name__in=['VC', 'DVC']).first()


class TransportationChoices(models.TextChoices):
    PROVIDED = 'PROVIDED', 'Provided'
    PERSONAL = 'PERSONAL', 'Personal'
    PUBLIC = 'PUBLIC', 'Public'


class Transportation(TimestampedModel):
    transportation_means = models.CharField(max_length=100, choices=TransportationChoices.choices)
    vehicle_identification = models.CharField(max_length=100, blank=True, null=True)
    driver_name = models.CharField(max_length=100, blank=True, null=True)


class ApprovalDetails(TimestampedModel):
    done_at = models.CharField(max_length=100)
    done_on = models.DateField()
    authorized_by = models.CharField(max_length=100)
    authorized_signature = models.CharField(max_length=100)
    acknowledged_by_hr = models.CharField(max_length=100)
    visa_for_destination = models.CharField(max_length=100, blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)


class MissionAttachment(TimestampedModel):
    mission_order = models.ForeignKey('MissionOrder', on_delete=models.CASCADE, related_name='attachments')
    attachment = models.FileField(upload_to='mission_attachments')


class MissionRoleChoices(models.TextChoices):
    STAFF = 'STAFF', 'Staff'
    TUTORIAL_ASSISTANT = 'TUTORIAL_ASSISTANT', 'Tutorial Assistant'
    ASSISTANT_LECTURER = 'ASSISTANT_LECTURER', 'Assistant Lecturer'
    LECTURER = 'LECTURER', 'Lecturer'
    SENIOR_LECTURER = 'SENIOR_LECTURER', 'Senior Lecturer'
    ASSOCIATE_PROFESSOR = 'ASSOCIATE_PROFESSOR', 'Associate Professor'
    PROFESSOR = 'PROFESSOR', 'Professor'


class DestinationChoices(models.TextChoices):
    KIGALI = 'KIGALI', 'Kigali'
    HUYE = 'HUYE', 'Huye'
    MUSANZE = 'MUSANZE', 'Musanze'
    RUBAVU = 'RUBAVU', 'Rubavu'
    NYAGATARE = 'NYAGATARE', 'Nyagatare'
    RUSIZI = 'RUSIZI', 'Rusizi'
    KARONGI = 'KARONGI', 'Karongi'
    NYANZA = 'NYANZA', 'Nyanza'
    GAKENKE = 'GAKENKE', 'Gakenke'
    NGORORERO = 'NGORORERO', 'Ngororero'
    KAMONYI = 'KAMONYI', 'Kamonyi'
    RULINDO = 'RULINDO', 'Rulindo'
    BUGESERA = 'BUGESERA', 'Bugesera'
    NYAMASHEKE = 'NYAMASHEKE', 'Nyamasheke'
    NYARUGURU = 'NYARUGURU', 'Nyaruguru'
    GICUMBI = 'GICUMBI', 'Gicumbi'
    KIREHE = 'KIREHE', 'Kirehe'
    RWAMAGANA = 'RWAMAGANA', 'Rwamagana'
    KAYONZA = 'KAYONZA', 'Kayonza'
    GATSIBO = 'GATSIBO', 'Gatsibo'
    NGOMA = 'NGOMA', 'Ngoma'
    BURERA = 'BURERA', 'Burera'
    NYAMAGABE = 'NYAMAGABE', 'Nyamagabe'
    RUHAANGO = 'RUHAANGO', 'Ruhaango'
    RUTSIRO = 'RUTSIRO', 'Rutsiro'


class MissionOrder(TimestampedModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='mission_orders')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=MissionRoleChoices.choices)
    purpose_of_mission = models.TextField()
    expected_results = models.TextField()
    destination = models.CharField(max_length=100, choices=DestinationChoices.choices)
    distance_km = models.IntegerField(null=True, blank=True)
    departure_date = models.DateField()
    returning_date = models.DateField()
    duration_days = models.IntegerField(editable=False)
    duration_nights = models.IntegerField(editable=False)
    transportation = models.OneToOneField(Transportation, on_delete=models.CASCADE)
    supervisor_name = models.CharField(max_length=100)
    supervisor_signature = models.CharField(max_length=100)
    approval_details = models.OneToOneField(ApprovalDetails, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.duration_days = (self.returning_date - self.departure_date).days
        self.duration_nights = self.duration_days - 1
        super(MissionOrder, self).save(*args, **kwargs)

    # def get_next_approver(self):
    #     if self.issued_to.role == RoleChoices.STAFF:
    #         return self.issued_to.unit.manager
    #     elif self.issued_to.role == RoleChoices.UNIT_MANAGER:
    #         return Staff.objects.filter(role=RoleChoices.CAMPUS_MANAGER,
    #                                     unit__college=self.issued_to.unit.college).first()
    #     elif self.issued_to.role == RoleChoices.CAMPUS_MANAGER:
    #         return Staff.objects.filter(role__in=[RoleChoices.VC, RoleChoices.DVC]).first()


@receiver(post_save, sender=MissionOrder)
def request_approval(sender, instance, created, **kwargs):
    next_approver = instance.get_next_approver()
    if next_approver:
        Approval.objects.create(mission_order=instance, approver=next_approver)


class ApprovalStatusChoices(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class Approval(TimestampedModel):
    mission_order = models.ForeignKey(MissionOrder, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ApprovalStatusChoices.choices,
                              default=ApprovalStatusChoices.PENDING
                              )
    approval_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    def approve(self):
        self.status = ApprovalStatusChoices.APPROVED
        self.approval_date = timezone.now()
        self.save()

    def reject(self, reason=''):
        self.status = ApprovalStatusChoices.REJECTED
        self.rejected = True
        self.rejection_reason = reason
        self.save()
