from django.db import models
from django.contrib.auth.models import User

class DailyRisk(models.Model):
    pm = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    
    book = models.CharField(max_length=80)
    risk = models.DecimalField(max_digits=12, decimal_places=2)
    target = models.DecimalField(max_digits=12, decimal_places=2, null=True,blank=True)
    stop = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    worst_case_bp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    worst_case_k = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('pm', 'date', 'book') #Ensures unique books for each date for each PM
        ordering = ['book']
        
    def __str__(self):
        return f"{self.pm.username} | {self.date} | {self.book}"

        
    
    