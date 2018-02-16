from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import RestaurantLocation
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm

@login_required(login_url='/login/')
def create_restaurantview(request):
	form = RestaurantLocationCreateForm(request.POST or None)
	if form.is_valid():
		if request.user.is_authenticated():
			instance = form.save(commit=False)
			instance.owner = request.user
			instance.save()
			form.save()
			return HttpResponseRedirect('/restaurants/')
		else:
			return 	HttpResponseRedirect("/login/")
	template_name = 'restaurants/form.html'
	context = {'form': form}
	return render(request, template_name, context)

class RestaurantListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		slug = self.kwargs.get('slug')
		if slug:
			queryset = RestaurantLocation.objects.filter(
				Q(category__iexact=slug) |
				Q(category__icontains=slug)
				)
		else:
			queryset = RestaurantLocation.objects.filter(owner=self.request.user)
		return queryset

class RestaurantDetailView (LoginRequiredMixin, DetailView):
	def get_queryset(self):
		queryset = RestaurantLocation.objects.filter(owner=self.request.user)
		return queryset

class RestaurantCreateView (LoginRequiredMixin, CreateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'form.html'
	#success_url = '/restaurants/'
	#login_url = '/login/'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.owner = self.request.user
		return super(RestaurantCreateView, self).form_valid(form)

	def get_context_data(self,*args,**kwargs):
		context = super(RestaurantCreateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Add restaurant'
		return context

class RestaurantUpdateView (LoginRequiredMixin, UpdateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'restaurants/detail-update.html'
	#success_url = '/restaurants/'
	#login_url = '/login/'

	def get_context_data(self,*args,**kwargs):
		context = super(RestaurantUpdateView, self).get_context_data(*args,**kwargs)
		context['title'] = f'Edit restaurant: {self.get_object().name}'
		return context

	def get_queryset(self):
		queryset = RestaurantLocation.objects.filter(owner=self.request.user)
		return queryset
