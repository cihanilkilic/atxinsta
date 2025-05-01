from django.db import models
from django.contrib.auth.models import User

 # PAKET İSİMLERİN OLUŞTURULMASI
class ProductPackage(models.Model):
    package_name = models.CharField(max_length=255)
    package_price = models.DecimalField(max_digits=10, decimal_places=2)
    package_duration = models.CharField(max_length=100, blank=True, null=True)  # Paket süresi eklendi
    feature_1 = models.CharField(max_length=255, blank=True, null=True)
    feature_2 = models.CharField(max_length=255, blank=True, null=True)
    feature_3 = models.CharField(max_length=255, blank=True, null=True)
    feature_4 = models.CharField(max_length=255, blank=True, null=True)
    feature_5 = models.CharField(max_length=255, blank=True, null=True)
    feature_6 = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.package_name


 # Starter Package
class StarterPackage(models.Model):
    user_full_name = models.CharField(max_length=255, blank=True, null=True)  # Kullanıcının tam adı
    purchased_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Satın alan kullanıcı
    user_email = models.EmailField(blank=True, null=True)  # Kullanıcının e-posta adresi
    package_id = models.IntegerField()  # Benzersiz olmayan ve otomatik artmayan paket ID
    package_price = models.DecimalField(max_digits=10, decimal_places=2)  # Paket fiyatı
    purchase_date = models.DateTimeField(auto_now_add=True)  # Paket alış tarihi
    expiration_date = models.DateTimeField(blank=True, null=True)  # Paket bitiş tarihi
    is_active = models.BooleanField(default=False)  # Paket etkin mi


    def __str__(self):
        return f"Starter Package - {self.purchased_by} ({self.user_email})"

 # Professional Package
class ProfessionalPackage(models.Model):
    user_full_name = models.CharField(max_length=255, blank=True, null=True)  # Kullanıcının tam adı
    purchased_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    user_email = models.EmailField(blank=True, null=True)  
    package_id = models.IntegerField()  
    package_price = models.DecimalField(max_digits=10, decimal_places=2)  
    purchase_date = models.DateTimeField(auto_now_add=True)  
    expiration_date = models.DateTimeField(blank=True, null=True)  
    is_active = models.BooleanField(default=False)  


    def __str__(self):
        return f"Professional Package - {self.purchased_by} ({self.user_email})"

 # Standard Package
class StandardPackage(models.Model):
    user_full_name = models.CharField(max_length=255, blank=True, null=True)  # Kullanıcının tam adı
    purchased_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    user_email = models.EmailField(blank=True, null=True)  
    package_id = models.IntegerField()  
    package_price = models.DecimalField(max_digits=10, decimal_places=2)  
    purchase_date = models.DateTimeField(auto_now_add=True)  
    expiration_date = models.DateTimeField(blank=True, null=True)  
    is_active = models.BooleanField(default=False)  

    def __str__(self):
        return f"Standard Package - {self.purchased_by} ({self.user_email})"
    


# AGENTS'S Card and Package(AJAN KARTLARI)
class AgentsCard(models.Model):
    package_name = models.CharField(max_length=255,verbose_name="Cart Adı ")
    package_content = models.CharField(max_length=255, blank=True, null=True,verbose_name="Cart İçeriği ")
    package_price = models.CharField(max_length=20, blank=True, null=True,verbose_name="Cart Etiket Fiyatı ")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi ")

    def __str__(self):
        return self.package_name
    

# AGENTS'S Package(AJAN PAKET BİLGİLERİ)
class AgentsPackage(models.Model):
    package_name = models.ForeignKey(AgentsCard, on_delete=models.CASCADE,verbose_name="Ajan Paket Adı ",related_name="agentscard")  
    package_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Ajan Fiyatı ")
    package_duration = models.CharField(max_length=100, blank=True, null=True,verbose_name="Ajan  Paket Süresi ")  # Paket süresi eklendi
    package_title = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Başlık ")
    package_content = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Kısa İçerik ")
    feature_1 = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Özellik 1 ")
    feature_2 = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Özellik 1 ")
    feature_3 = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Özellik 1 ")
    feature_4 = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Özellik 1 ")
    feature_5 = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Özellik 1 ")
    feature_6 = models.CharField(max_length=255, blank=True, null=True,verbose_name="Ajan Özellik 1 ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.package_name)

    

# AGENTS'S Payments (AJAN ÖDEME BİLGİLERİ (Instagram-Whatsapp Business-Youtube-Yotube Shorts ....))
class AgentsPayment(models.Model):
    user_full_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Kullanıcının Tam Adı"
    )
    purchased_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Satın Alan Kullanıcı"
    )
    user_email = models.EmailField(
        blank=True, null=True, verbose_name="Kullanıcı E-posta"
    )
    package_name = models.CharField( max_length=255,verbose_name="Paket Adı (ID)", blank=True, null=True,)
    package_id = models.IntegerField(verbose_name="Paket ID", blank=True, null=True,)
    agents_name = models.CharField( max_length=255,verbose_name="Ajan Adı (ID)" , blank=True, null=True,)
    agents_id = models.IntegerField(verbose_name="Ajan ID", blank=True, null=True,)
    package_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Paket Fiyatı"
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Satın Alma Tarihi"
    )
    expiration_date = models.DateTimeField(
        blank=True, null=True, verbose_name="Bitiş Tarihi"
    )
    is_active = models.BooleanField(default=False, verbose_name="Aktif mi?")

    class Meta:
        verbose_name = "Agents Ödemesi"
        verbose_name_plural = "Agents Ödemeleri"

    def __str__(self):
        return f"{self.user_full_name or self.purchased_by.username} - Paket {self.package_id}"