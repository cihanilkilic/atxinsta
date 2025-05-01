from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class InstagramAgents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Kullanıcıya ait içerik
    content = models.TextField()  # İçerik metni
    user_prompt = models.TextField(blank=True, null=True)
    system_prompt = models.TextField(blank=True, null=True)
    image_prompt_agent = models.TextField(blank=True, null=True)
    
    image1 = models.ImageField(upload_to='instagram_images/')  # Ana görsel

    # Ek görsel alanları
    image2 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 2. görsel
    image3 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 3. görsel
    image4 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 4. görsel
    image5 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 5. görsel
    image6 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 6. görsel
    image7 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 7. görsel
    image8 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 8. görsel
    image9 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 9. görsel
    image10 = models.ImageField(upload_to='instagram_images/', blank=True, null=True)  # 10. görsel

    captions = models.TextField(max_length=255, blank=True)  # Açıklama (caption)
    is_active = models.BooleanField(default=True)  # Aktiflik durumu
    hashtag = models.TextField(max_length=255, blank=True)  # Hashtag
    date = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi

    # Yeni eklenen alanlar
    scheduled_date = models.DateField(blank=True, null=True)  # Paylaşım tarihi
    scheduled_time1 = models.CharField(max_length=100, blank=True, null=True)#Paylaşım saati
    scheduled_time2 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time3 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time4 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time5 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time6 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time7 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time8 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time9 = models.CharField(max_length=100, blank=True, null=True)
    scheduled_time10 = models.CharField(max_length=100, blank=True, null=True)
    post_frequency = models.CharField(max_length=100, blank=True)  # Ne sıklıkla paylaşılacak

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    


