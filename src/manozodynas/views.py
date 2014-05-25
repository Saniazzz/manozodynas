from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import LoginForm
from django.contrib.auth import login
from manozodynas.models import *
from django.views.generic import CreateView, ListView, DeleteView

class WordDelete(DeleteView):
    model = Word
    success_url = '/words'

class WordList(ListView):
    model = Word
    paginate_by = 3
    success_url = 'index/'
    template_name = 'manozodynas/words.html'
    def get_context_data(self, **kwargs):
        context = super(WordList, self).get_context_data(**kwargs)
        return context

class WordCreate(CreateView):
    model = Word
    template_name = 'manozodynas/word.html'
    success_url = '/words'

def index_view(request):
    return render(request, 'manozodynas/index.html', {})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    #import ipdb; ipdb.set_trace()
    return render(request, 'manozodynas/login.html', {'form':form})
