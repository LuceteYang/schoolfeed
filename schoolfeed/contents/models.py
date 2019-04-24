from django.db import models
from schoolfeed.users import models as user_models
from schoolfeed.schools import models as school_models

# Create your models here.
class Contents(school_models.TimeStampedModel):

	school = models.ForeignKey(school_models.School, null=True, on_delete=models.SET_NULL, related_name="contents")
	creator = models.ForeignKey(user_models.User, related_name='contents', null=True, on_delete=models.SET_NULL)
	main_image = models.ImageField(null=True)
	text = models.TextField(null=True, blank=True)
	deleted_at = models.DateTimeField(null=True)
	
	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.text