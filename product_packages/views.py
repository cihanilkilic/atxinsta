from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductPackage, ProfessionalPackage, StandardPackage, StarterPackage
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta



def product_detail(request, product_detail_pk):
    print("Gelen ID değeri:", product_detail_pk)

    product = ProductPackage.objects.filter(pk=product_detail_pk).first()

    if not product:
        return redirect("atxaisoft:index")

    if request.method == 'POST':
        if request.user.is_authenticated:
            _To_day_ = datetime.today()
            
            firstname_lastname = request.POST.get("FirstnameLastname", "").strip()
            cart_number = request.POST.get("CartNumber", "").strip()
            cart_date = request.POST.get("CartDate", "").strip()
            cart_cvv = request.POST.get("CartCvv", "").strip()

            if not all([firstname_lastname, cart_number, cart_date, cart_cvv]):
                messages.error(request, "Lütfen tüm alanları eksiksiz doldurun.")
            else:
                print(f"Kart Üzerindeki İsim: {firstname_lastname}")
                print(f"Kart Numarası: {cart_number}")
                print(f"Son Kullanma Tarihi: {cart_date}")
                print(f"CVV: ***")

                messages.success(request, "Ödeme işlemi başarılı!")
                
                if product_detail_pk == 1:
                    _next_month_ = _To_day_ + relativedelta(months=3)
                    
                    StarterPackage.objects.create(
                        purchased_by=request.user,
                        user_email=request.user.email,
                        user_full_name=f"{request.user.first_name} {request.user.last_name}",
                        package_id=product_detail_pk,
                        purchase_date=_To_day_.strftime("%Y-%m-%d"),
                        package_price=product.package_price,
                        expiration_date=_next_month_.strftime("%Y-%m-%d"),
                        is_active=True
                    )
                    print("BİR İÇİN Ödeme işlemi başarılı", product_detail_pk)
                
                elif product_detail_pk == 2:
                    _next_month_ = _To_day_ + relativedelta(months=6)
                    
                    ProfessionalPackage.objects.create(
                        purchased_by=request.user,
                        user_email=request.user.email,
                        user_full_name=f"{request.user.first_name} {request.user.last_name}",
                        package_id=product_detail_pk,
                        purchase_date=_To_day_.strftime("%Y-%m-%d"),
                        package_price=product.package_price,
                        expiration_date=_next_month_.strftime("%Y-%m-%d"),
                        is_active=True
                    )
                    print("İKİ İÇİN Ödeme işlemi başarılı", product_detail_pk)
                
                elif product_detail_pk == 3:
                    _next_month_ = _To_day_ + relativedelta(months=12)
                    
                    StandardPackage.objects.create(
                        purchased_by=request.user,
                        user_email=request.user.email,
                        user_full_name=f"{request.user.first_name} {request.user.last_name}",
                        package_id=product_detail_pk,
                        purchase_date=_To_day_.strftime("%Y-%m-%d"),
                        package_price=product.package_price,
                        expiration_date=_next_month_.strftime("%Y-%m-%d"),
                        is_active=True
                    )
                    print("ÜÇ İÇİN Ödeme işlemi başarılı", product_detail_pk)
                
                else:
                    return redirect('atxaisoft:index')

        else:
            messages.error(request, 'Lütfen oturum açtıktan sonra satın alma işlemini gerçekleştirin.')

    return render(request, "products/product_detail.html", {"product": product})
