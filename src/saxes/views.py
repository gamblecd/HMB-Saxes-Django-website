# Create your views here.

import os, sys
from random import Random

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from photologue.models import Gallery
from models import Member, Quote, Post
from forms import MusicForm
import settings as settings, variables as variables

def home(request, post_pk=None):
    quote = _get_quote()
    if not post_pk:
        posts = Post.objects.all().order_by('-date_created')[:10]
    else:
        posts = Post.objects.filter(id__lte = post_pk).order_by('-date_created')[:10]
    
    return render_to_response('index.html', {'quote':quote,'posts':posts},
                              context_instance=RequestContext(request))

def gallery(request, album=None):
    quote = _get_quote()
    albums = Gallery.objects.all()
    if album:
        album = get_object_or_404(Gallery, title=album).sample()
    else:
        album =[]
        for gallery in albums:
            for image in gallery.sample():
                album.append(image)
    album = sorted(album,key = lambda x: x.title)
    paginator = Paginator(album, 12)
    page = request.GET.get('page')
    if not page: page = 1;
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        images = paginator.page(paginator.num_pages)
    
    return render_to_response('gallery.html', {'quote':quote,'albums':albums, 'album':images},
                              context_instance=RequestContext(request))

def members(request, year=None):
    quote = _get_quote()
    roster = Member.objects.filter().order_by('year_starting_band')
    years = sorted({x.year_starting_band for x in roster})
    if year:
        roster = Member.objects.filter(year_starting_band=year)
    return render_to_response('members.html', {'quote':quote,'years':years,'roster': roster},
                              context_instance=RequestContext(request))

def music(request):
    c = {}
    quote = _get_quote()
    c.update({'quote': quote})
    alto_songs = []
    tenor_songs = []
    for path, dir, f in os.walk(settings.MEDIA_ROOT + 'sheetmusic'):
        for song_name in f:
            if song_name.startswith('alto'):
                alto_songs.append(song_name[5:])
            elif song_name.startswith('tenor'):
                tenor_songs.append(song_name[6:])
            c.update({'alto':sorted(alto_songs), 'tenor': sorted(tenor_songs)})
    return render_to_response('members_section.html', c)

def login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MusicForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == '' and password == '':
                request.session['logged_in'] = True
                return music(request)
            else:
                return error(request, error='Invalid Username or Password', form=form)
    else:
        form = MusicForm() # An unbound form
    c = {}
    quote = _get_quote()
    c.update({'quote': quote})
    c.update({'form': form})
    return render_to_response('login.html', c,
                              context_instance=RequestContext(request))

def error(request, error=None, form=None):
    c = {}
    c.update(csrf(request))
    quote = _get_quote()
    c.update({'quote':quote, 'error':error,'form':form})
    return render_to_response('login.html', c,
                              context_instance=RequestContext(request))
   
def book(request):
    if request.session.get('logged_in'):
            file = open(settings.TEMPLATE_DIRS[0] + '/bookofsax/textfiles/lists/2011.txt')
            text = file.read()
            quote = _get_quote()
            return render_to_response('bookofsax/book_of_sax.html', {'page':text, 'quote':quote},
                                      context_instance=RequestContext(request))
    else:
        return login(request)

def friends(request, friend=None):
    c = {}
    c.update(csrf(request))
    quote = _get_quote()
    if friend:
        friends = [variables.FRIENDS[friend]]
    else:
        friends = sorted(variables.FRIENDS.values(), reverse=True)
    
    c.update({'friends': friends, 'quote':quote})
        
    return render_to_response('friends.html', c, 
                              context_instance=RequestContext(request))

def _get_quote():
    quotes = Quote.objects.all()
    rand = Random()
    return rand.choice(quotes) if len(quotes) > 0 else None
    