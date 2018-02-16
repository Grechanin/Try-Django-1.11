from django.conf import settings
from django.db import models
from django.db.models import Q
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from .validators import validate_category

user = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet):
	def search(self, query):
		if query:
			query = query.strip()
			return self.filter(Q(name__icontains=query) |
						   Q(category__icontains=query) |
						   Q(location__icontains=query) |
						   Q(item__name__icontains=query) |
						   Q(item__contents__icontains=query)
						   ).distinct()
		else:
			return self

class RestaurantLocationManager(models.Manager):
	def get_queryset(self):
		return RestaurantLocationQuerySet(self.model, using=self._db)

	def search(self, query):
		return self.get_queryset(self,).search(query)

class RestaurantLocation(models.Model):
	owner 			= models.ForeignKey(user)
	name 			= models.CharField(max_length = 120)
	location 		= models.CharField(max_length = 120, null=True, blank=True)
	category		= models.CharField(max_length = 120, null=True, blank=True, validators=[validate_category])
	timestamp		= models.DateTimeField(auto_now_add=True)
	update			= models.DateTimeField(auto_now=True)
	slug			= models.SlugField(null=True, blank=True)
	#my_date_field 	= models.DateField(auto_now=False, auto_now_add=False)

	objects			= RestaurantLocationManager()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('restaurants:detail', kwargs={'slug': self.slug})

	@property
	def title(self):
		return self.name


def rl_pre_save_reciver(sender, instance,*args,**kwargs):
	if instance.category:
		instance.category = instance.category.capitalize()
	if not instance.slug:
		instance.slug=unique_slug_generator(instance)

pre_save.connect(rl_pre_save_reciver,RestaurantLocation)