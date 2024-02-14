from django.db import models

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


class Staff(TimestampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    type = models.CharField(max_length=20, choices=TypeChoices.choices, default=TypeChoices.ACADEMIC)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    def __str__(self):
        return self.user.email
