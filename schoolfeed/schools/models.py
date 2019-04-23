from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from schoolfeed.users import models as user_models

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 추상클래스
        abstract = True


class School(TimeStampedModel):

    name = models.CharField(_("Name of School"), max_length=140)
    image = models.ImageField(null=True)
    location = models.CharField(_("Location of School"), max_length=140, null=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Subscribe(TimeStampedModel):

	subscriber = models.ForeignKey(user_models.User, null=True, on_delete=models.CASCADE)
	school = models.ForeignKey(School, null=True, on_delete=models.CASCADE, related_name="subscribes")

	def __str__(self):
		return 'User: {} - School Caption: {}'.format(self.subscriber.username, self.school.name)

class Join(TimeStampedModel):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('normal', 'Nomal User'),
    )
    member  = models.ForeignKey(user_models.User, null=True, on_delete=models.CASCADE)
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE, related_name="joins")
    role = models.CharField(max_length=80, choices=ROLE_CHOICES, blank=True)