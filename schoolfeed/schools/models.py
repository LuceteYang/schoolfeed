from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from schoolfeed.users import models as user_models


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(_("생성 시간"), auto_now_add=True)
    updated_at = models.DateTimeField(_("수정 시간"), auto_now=True)

    class Meta:
        # 추상클래스
        abstract = True


class School(TimeStampedModel):

    name = models.CharField(_("학교 이름"), max_length=140)
    image = models.ImageField(_("학교 사진"), null=True)
    location = models.CharField(_("학교 위치"), max_length=140, null=True)
    deleted_at = models.DateTimeField(_("학교 삭제 시간"), null=True)
    creator = models.ForeignKey(user_models.User, help_text="학교 생성자", null=True, on_delete=models.SET_NULL, related_name="school")
    subscribe_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='subscribe_user_set',
        through='Subscribe'
    )
    member_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='member_user_set',
        through='Member'
    )
    @property
    def subscriber_count(self):
        return self.subscribe_user_set.count()

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


class Contents(TimeStampedModel):

    school = models.ForeignKey(School, help_text="학교", null=True, on_delete=models.SET_NULL, related_name="contents")
    creator = models.ForeignKey(user_models.User, help_text="컨텐츠 생성자", related_name='contents', null=True, on_delete=models.SET_NULL)
    main_image = models.ImageField(_("컨텐츠 사진"), null=True)
    text = models.TextField(_("컨텐츠 내용"), null=True, blank=True)
    deleted_at = models.DateTimeField(_("컨텐츠 생성시간"), null=True)

    @property
    def natural_time(self):
        return naturaltime(self.created_at)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.pk:
            contents = Contents.objects.get(pk=self.pk)
            if contents.main_image != self.main_image:
                contents.main_image.delete(save=False)
        super(Contents, self).save(*args, **kwargs)


class Subscribe(TimeStampedModel):

    subscriber = models.ForeignKey(user_models.User, help_text="학교 구독자", null=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, help_text="학교", null=True, on_delete=models.SET_NULL, related_name="subscribes")

    def __str__(self):
        return 'User: {} - School Caption: {}'.format(self.subscriber.username, self.school.name)


class Member(TimeStampedModel):

    member = models.ForeignKey(user_models.User, help_text="학교 구성원", null=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, help_text="학교", null=True, on_delete=models.SET_NULL, related_name="joins")
    role = models.IntegerField(_("학교 역할"), default=0)
