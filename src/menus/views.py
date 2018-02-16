from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, ListView, View, UpdateView

from .forms import ItemForm
from .models import Item

class HomeView(View):
	def get(self, request, *args,**kwargs):
		if not request.user.is_authenticated():
			return render(request, "home.html", {})

		user = request.user
		is_following_user_ids = [x.user.id for x in user.is_following.all()]
		qs = Item.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:3]

		#list_
		#for x in user.is_following.all():
			#list_.append(x.user.id)

		return render(request, "menus/home-feed.html", {'object_list': qs})

class ItemDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin,CreateView):
	form_class = ItemForm
	template_name = 'form.html'

	def get_form_kwargs(self):
		kwargs = super(ItemCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self,*args,**kwargs):
		context = super(ItemCreateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Add menu item'
		return context

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(ItemCreateView, self).form_valid(form)

class ItemListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

class ItemUpdateView(LoginRequiredMixin,UpdateView):
	form_class = ItemForm
	template_name = 'menus/detail-update.html'
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self,*args,**kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Edit menu item'
		return context

	def get_form_kwargs(self):
		kwargs = super(ItemUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs