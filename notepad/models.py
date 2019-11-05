from django.db import models
from django.conf import settings
#from django.contrib.auth import get_user_model

# Create your models here.
class Note(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #user= models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    title = models.CharField(max_length= 120)
    image= models.ImageField(null= True, blank= True)
    url= models.URLField(null= True, blank= True)
    datestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_delete_url(self):
        return "/notes/{}/delete".format(self.pk)

    def get_update_url(self):
        return f"/notes/{self.pk}/update"
