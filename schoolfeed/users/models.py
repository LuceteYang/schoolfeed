from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), max_length=255)
    profile_image = models.ImageField(null=True,blank=True)
    email = models.EmailField(_('email address'),null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            user = User.objects.get(pk=self.pk)
            if user.profile_image != self.profile_image:
                user.profile_image.delete(save=False)
        super(User, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.username