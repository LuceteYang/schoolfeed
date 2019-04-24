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
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL, related_name="school")
    deleted_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            school = School.objects.get(pk=self.pk)
            if school.image != self.image:
                school.image.delete(save=False)
        super(School, self).save(*args, **kwargs)

    # @property
    # def member_count(self):
    #     return self.comments.all().count()

    def __str__(self):
        return self.name

class Subscribe(TimeStampedModel):

	subscriber = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL)
	school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL, related_name="subscribes")

	def __str__(self):
		return 'User: {} - School Caption: {}'.format(self.subscriber.username, self.school.name)

class Member(TimeStampedModel):
    ROLE_CHOICES = (
        (1, '관리자'),
        (0, '일반 회원'),
    )
    POSITION_CHOICES = (
        (0, '학생'),
        (1, '선생님'),
        (2, '기타'),
    )
    member  = models.ForeignKey(user_models.User, null=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL, related_name="joins")
    position = models.IntegerField(choices=POSITION_CHOICES, blank=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)


