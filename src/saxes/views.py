# Create your views here.

import os, sys
from random import Random

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from jinja2_for_django import jrender_to_response
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from photologue.models import Gallery
from models import Member, Quote, Post, Member_Photo
from forms import LoginForm
import settings as settings, variables as variables
import sax_settings

def home(request, post_pk=None):
    quote = _get_quote()
    print quote
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
    if not _is_logged_in(request):
        return login(request, 'You must log in first to access that.')
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
    return render_to_response('members_section.html', c, context_instance=RequestContext(request))

def login(request, message=''):
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == sax_settings.USERNAME and password == sax_settings.PASSWORD:
                request.session['logged_in'] = True
                #TODO: return to url initially requested.
                return music(request)
            else:
                return form_page(request, error='Invalid Username or Password', form=form)
    else:
        form = LoginForm() # An unbound form
    c = {}
    quote = _get_quote()
    c.update({'quote': quote})
    c.update({'form': form})
    c.update({'error': message})
    c.update({'title': 'Login as a Sax'})
    return render_to_response('form.html', c,
                              context_instance=RequestContext(request))

def add_object(request, objForm, callback, title='Add Object'):
    if not _is_logged_in(request):
        return login(request, 'You must log in first to access that.')
    if request.method == 'POST': # If the form has been submitted...
        
        if objForm().is_multipart():
            form = objForm(request.POST, request.FILES)
        else:
            form = objForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            try:
                success_message = callback(form)
                #TODO: return to previous page.
                return success(request, success_message);
            except Exception as e:
                err = str(e)
                return form_page(request, error=err, form=form)
    else:
        form = objForm() # An unbound form
    c = {}
    quote = _get_quote()
    c.update({'quote': quote})
    c.update({'form': form})
    c.update({'title': title})
    return render_to_response('form.html', c,
                              context_instance=RequestContext(request))
    
def success(request, message='SUCCESS!',ob=None):
    success = message
    quote = _get_quote()
    c = {}
    c.update({'success': success})
    c.update({'quote': quote})
    return render_to_response('form.html', c,
                              context_instance=RequestContext(request))
    
def form_page(request, error=None, form=None):
    c = {}
    c.update(csrf(request))
    quote = _get_quote()
    c.update({'quote':quote, 'error':error,'form':form})
    return render_to_response('form.html', c,
                              context_instance=RequestContext(request))
   
def book(request, page='lists/2011', folder=''):
    if not _is_logged_in(request):
        return login(request, 'You must log in first to access that.')
    toc = open(sax_settings.BOOK_DIR + 'textfiles/toc.txt')
    fpath = '%s.txt' % os.path.join(sax_settings.BOOK_DIR, 'textfiles', folder, page)
    f = open(fpath)
    text = f.read()
    toctext = toc.read() 
    quote = _get_quote()
    f.close()
    toc.close()
    return render_to_response('bookofsax/book_of_sax.html', {'toc': toctext,
                                                             'page':text, 
                                                             'quote':quote},
                                  context_instance=RequestContext(request))
    
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

def _is_logged_in(request):
    return 'logged_in' in request.session and request.session.get('logged_in', False)
           

def _insert_quote(form):
    quote = form.cleaned_data['quote']
    author = form.cleaned_data['author']
    q = Quote(quote=quote, author=author)
    q.validate_unique()
    for quote in Quote.objects.all():
        if quote.quote == q.quote:
            return 'Quote was already in the database, using known author instead.'
    success = 'Added the quote "%s" to the system.' % str(q)
    q.save()
    return success

def _insert_member(form):
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    nickname = form.cleaned_data['nickname']
    instrument = form.cleaned_data['instrument']
    major = form.cleaned_data['instrument']
    year_starting_band = form.cleaned_data['year_starting_band']
    year_starting_school = form.cleaned_data['year_starting_school']
    best_band_memory = form.cleaned_data['best_band_memory']
    photo = form.cleaned_data['photo']
    
    m = Member(first_name=first_name, last_name=last_name, nickname=nickname,
               instrument=instrument, major=major, year_starting_band=year_starting_band,
               year_starting_school=year_starting_school, best_band_memory=best_band_memory)
    mPhoto = Member_Photo(photo)
    
    mPhoto.member = m
    m.image = mPhoto;
    m.validate_unique()
    mPhoto.validate_unique()
    mPhoto.save()
    m.save()
    success = 'Added the member "%s" to the system.' % str(m)
    return success

def _insert_post(form):
    icon = form.cleaned_data['icon']
    title = form.cleaned_data['title']
    body = form.cleaned_data['body']
#    date_created = form.cleaned_data['date_created']
#    date_modified = form.cleaned_data['date_modified']
    p = Post(icon_url=icon, title=title, body=body)
    p.validate_unique()
    success = 'Added the post "%s" to the system.' % str(p)
    p.save()
    return success

def _get_quote():
    quotes = Quote.objects.all()
    rand = Random()
    return rand.choice(quotes) if len(quotes) > 0 else None
    