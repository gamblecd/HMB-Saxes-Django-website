from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
from models import Quote

from tinymce.widgets import TinyMCE

                
#QUOTES SETTINGS
QUOTE_QUOTE_LENGTH = 160
QUOTE_AUTHOR_LENGTH = 30
QUOTE_FORM_ACTION = '/add_quote/'

#POST SETTINGS
POST_TITLE_LENGTH = 30
POST_BODY_LENGTH = 1000
POST_ICONS =['news.png',
             'football.png',
             'warning.png',
             ]


POST_ICON_OPTIONS = [(x, mark_safe(_('<img src="%(static_url)simg/%(name)s" class="icon" alt="%(name)s" title="%(name)s" />' % 
                                     {'static_url': settings.STATIC_URL, 'name':x,},))) 
                     for x in POST_ICONS]

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """renders horizontal radio buttons.
    found here:
    https://wikis.utexas.edu/display/~bm6432/Django-Modifying+RadioSelect+Widget+to+have+horizontal+buttons
    """

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

#TODO: FORMS
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    action = '/members_page/'

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
class QuoteForm(forms.ModelForm):
    class Meta:
        model=Quote
#    quote = forms.CharField(min_length=2, max_length=QUOTE_QUOTE_LENGTH)
#    author = forms.CharField(max_length=QUOTE_AUTHOR_LENGTH)
    action = QUOTE_FORM_ACTION
    
class PostForm(forms.Form):
    title = forms.CharField(max_length=POST_TITLE_LENGTH)
    body = forms.CharField(max_length=POST_BODY_LENGTH, widget=TinyMCE(attrs={'cols': 63, 'rows': 25, 'id':'mce'}))
    icon = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices=POST_ICON_OPTIONS)