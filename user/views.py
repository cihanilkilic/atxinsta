from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str  # force_str burada değiştirildi
from django.shortcuts import get_object_or_404
from django.utils import timezone

from product_packages.models import ProfessionalPackage
from user.tokens import account_activation_token  # Token işlemleri için
#dxkruwwjoggbcowv


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('atxaisoft:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('atxaisoft:index')
            else:
                messages.error(request, 'Kullanıcı adı veya şifre geçersiz.')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre geçersiz.')
    else:
        form = AuthenticationForm()

    return render(request, 'user/sign_in.html', {'form': form})




def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('inputName')
        last_name = request.POST.get('inputLastname')
        username = request.POST.get('inputUsername')
        email = request.POST.get('inputEmail')
        password1 = request.POST.get('inputPassword1')
        password2 = request.POST.get('inputPassword2')
        
        if not all([first_name, last_name, username, email, password1, password2]):
            return render(request, 'user/sign_up.html', {'msg': 'Lütfen tüm alanları doldurun.', 'title': 'Kayıt Ol!'})
        
        if password1 != password2:
            return render(request, 'user/sign_up.html', {'msg': 'Şifreler eşleşmiyor.', 'title': 'Kayıt Ol!'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'user/sign_up.html', {'msg': 'Bu kullanıcı adı zaten kullanılıyor.', 'title': 'Kayıt Ol!'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'user/sign_up.html', {'msg': 'Bu e-posta adresi zaten kullanılıyor.', 'title': 'Kayıt Ol!'})
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password1),
            is_active=False
        )
        user.save()
        
        current_site = get_current_site(request)
        mail_subject = 'Aktivasyon bağlantısı e-posta kimliğinize gönderildi'
        message = render_to_string('user/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email_message = EmailMessage(mail_subject, message, to=[email])
        email_message.send()
        
        return render(request, 'user/email.html', {'msg': 'Kaydı tamamlamak için lütfen e-posta adresinizi doğrulayın.'})
    
    return render(request, 'user/sign_up.html')



# KULLANICI (MAİL) AKTİFLEME KODU *
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # force_str kullanımı
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Hesabınız başarıyla aktifleştirildi!')
        return redirect('user:login')
    else:
        messages.error(request, 'Aktivasyon bağlantısı geçersiz!')
        return redirect('user:register')



def profil(request):
    if request.user.is_authenticated:
        _To_day_ = timezone.now()
        print(_To_day_.strftime("%Y-%m-%d"))

        # Adım 1: Kullanıcının süresi dolmuş aktif paketlerini bulup 'is_active' değerini False yapalım
        expired_packages = ProfessionalPackage.objects.filter(
            purchased_by=request.user, is_active=True, expiration_date__lt=_To_day_,package_id=2
        )
        for package in expired_packages:
            package.is_active = False
            package.save()  # Değişiklikleri kaydet

        # Kullanıcının aktif paketini bul
        Professional_Package = ProfessionalPackage.objects.filter(
            purchased_by=request.user, is_active=True,package_id=2
        ).first()

        if Professional_Package:
            # Aktif paket varsa, bu paketi kontrol et
            if Professional_Package.expiration_date < _To_day_:
                # Eğer aktif paketin süresi dolmuşsa, kullanıcıyı yönlendir
                return redirect('atxaisoft:index')  # Paket süresi dolmuş, yönlendir
            return render(request, "chat_user_profil/chat_user_profil.html", {
                "package_status": "active"  # Paket hâlâ geçerli
            })

        # Kullanıcının paketi yoksa, yönlendir
        return redirect('atxaisoft:index')  # Kullanıcının paketi yok, yönlendir

    else:
        return redirect('atxaisoft:index')  # Kullanıcı oturum açmamışsa yönlendir




def user_logout(request):
    logout (request)
    return redirect("atxaisoft:index")