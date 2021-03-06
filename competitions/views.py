from django.db.models.functions import math
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Competition
from practice.models import Practice


class IndexView(generic.ListView):
    template_name = 'competitions/index.html'
    context_object_name = 'latest_competitions_list'

    def get_queryset(self):
        return Competition.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['practices'] = Practice.objects.all()
        context['ongoings'] = Competition.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        context['scheduleds'] = Competition.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        context['pasts'] = Competition.objects.filter(pub_date__gte=timezone.now()).order_by('-pub_date')[:5]
        return context


class DetailView(generic.DetailView):
    model = Competition
    template_name = 'competitions/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Competition.objects.filter(pub_date__lte=timezone.now())

class AttendView(generic.DetailView):
    model = Competition
    template_name = 'competitions/attend.html'

class OngoingView(generic.ListView):
    template_name = 'competitions/ongoing.html'
    context_object_name = 'latest_competitions_list'

    def get_queryset(self):
        return Competition.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')

    def paging(request):
        competitions = Competition.objects
        competitions_list = Competition.objects.filter(pub_date__lte = timezone.now())
        paginator = Paginator(competitions_list, 10)
        page = request.GET.get('page', 1)
        page_range = 5 # 페이지 범위 5
        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        current_block = math.ceil(int(page)/page_range)
        start_block = (current_block - 1)
        end_block = start_block + page_range
        p_range = paginator.page_range[start_block:end_block]
        total_page = page.num_pages()
        posts = paginator.get_page(page)
        return render(request, 'Ongoing.html', {'competitions': competitions, 'p_range': p_range})


class ScheduledView(generic.ListView):
    template_name = 'competitions/scheduled.html'
    context_object_name = 'scheduled_competitions_list'

    def get_queryset(self):
        return Competition.objects.filter(pub_date__lt = timezone.now()).order_by('-pub_date')
    def paging(request):
        competitions = Competition.objects
        competitions_list = Competition.objects.filter(pub_date__lt = timezone.now())
        paginator = Paginator(competitions_list, 1)
        page = request.GET.get('page', 1)
        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        context = {'samelines':lines}
        total_page = page.num_pages()
        posts = paginator.get_page(page)
        return render(request, 'Ongoing.html', {'competitions' : competitions, 'posts' : posts}, context)


class PastView(generic.ListView):
    template_name = 'competitions/past.html'
    context_object_name = 'past_competitions_list'

    def get_queryset(self):
        return Competition.objects.filter(pub_date__gt = timezone.now()).order_by('-pub_date')
    def paging(request):
        competitions = Competition.objects
        competitions_list = Competition.objects.filter(pub_date__gt = timezone.now())
        paginator = Paginator(competitions_list, 1)
        page = request.GET.get('page', 1)
        try:
            lines = paginator.page(page)
        except PageNotAnInteger:
            lines = paginator.page(1)
        except EmptyPage:
            lines = paginator.page(paginator.num_pages)
        context = {'samelines':lines}
        total_page = page.num_pages()
        posts = paginator.get_page(page)
        return render(request, 'Ongoing.html', {'competitions' : competitions, 'posts' : posts}, context)


class PraticeView(generic.ListView):
    template_name = 'competitions/practice.html'

