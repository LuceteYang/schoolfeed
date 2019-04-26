from django.db import models
from schoolfeed.users import models as user_models
from schoolfeed.schools import models as school_models
from django.contrib.humanize.templatetags.humanize import naturaltime

# Create your models here.
class Contents(school_models.TimeStampedModel):

	school = models.ForeignKey(school_models.School, null=True, on_delete=models.SET_NULL, related_name="contents")
	creator = models.ForeignKey(user_models.User, related_name='contents', null=True, on_delete=models.SET_NULL)
	main_image = models.ImageField(null=True)
	text = models.TextField(null=True, blank=True)
	deleted_at = models.DateTimeField(null=True)

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
			if Contents.main_image != self.main_image:
				contents.main_image.delete(save=False)
		super(Contents, self).save(*args, **kwargs)