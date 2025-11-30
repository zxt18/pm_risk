from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    can_edit_all_pms = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Book(models.Model):
    pm = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    name = models.CharField(max_length=80)
        
    created_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('pm', 'name')

    def __str__(self):
        return f"{self.pm.username} | {self.name}"
     
class DailyRisk(models.Model):
    date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="daily_risks")
    
    # Daily values
    risk = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    target = models.DecimalField(max_digits=12, decimal_places=2, null=True,blank=True)
    stop = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    worst_case_bp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    worst_case_k = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('book','date') #Ensures unique books for each date for each PM
        ordering = ['book__name']

    def __str__(self):
        return f"{self.book.pm.username} | {self.date} | {self.book.name}"
    
class BookPermission(models.Model):
    VIEW = "view"
    EDIT = "edit"

    PERMISSION_CHOICES = [
        (VIEW, "View"),
        (EDIT, "Edit"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pm = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pm_permissions")
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ("user", "pm", "permission")