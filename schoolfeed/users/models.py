from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("유저의 이름"), max_length=30)
    profile_image = models.ImageField(_("유저의 프로필 이미지"), null=True, blank=True)
    email = models.EmailField(_("유저의 이메일"), null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            user = User.objects.get(pk=self.pk)
            if user.profile_image != self.profile_image:
                user.profile_image.delete(save=False)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
