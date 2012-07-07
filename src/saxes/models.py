from django.db import models
from photologue import models as p_models

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=40)
    instrument = models.CharField(max_length=20)
    major = models.CharField(max_length=30)
    year_starting_band = models.PositiveSmallIntegerField(max_length=4)
    year_starting_school = models.PositiveSmallIntegerField()
    best_band_memory = models.TextField(max_length=640)
    #active = models.BooleanField(default=True);
    image = p_models.ImageModel()
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name;
    
class Member_Photo(p_models.ImageModel):
    member = models.OneToOneField(Member, primary_key=True)
    

class Quote(models.Model):
    quote = models.CharField(max_length=160)
    author = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.quote[:15] + '... ' + self.author;
    
class Post(models.Model):
    icon_url = models.CharField(max_length=70)
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title;
    
    def snippet(self, length=60):
        if len(self.body) > length:
            return self.body[:length] + '...'
        else:   
            return self.body;