from django import forms
import sax_settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
                

POST_ICON_OPTIONS = [
                     (x, mark_safe(_('<img src="%(static_url)simg/%(name)s" class="icon" alt="%(name)s" title="%(name)s" />' % 
                  {'static_url': settings.STATIC_URL, 'name':x,},
                  ))) for x in sax_settings.POST_ICON_OPTIONS]

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
    
class QuoteForm(forms.Form):
    quote = forms.CharField(min_length=2, max_length=sax_settings.QUOTE_QUOTE_LENGTH)
    author = forms.CharField(max_length=sax_settings.QUOTE_AUTHOR_LENGTH)
    action = sax_settings.QUOTE_FORM_ACTION
    
class PostForm(forms.Form):
    title = forms.CharField(max_length=sax_settings.POST_TITLE_LENGTH)
    body = forms.CharField(max_length=sax_settings.POST_BODY_LENGTH, widget=forms.Textarea)
    icon = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices=POST_ICON_OPTIONS)
    