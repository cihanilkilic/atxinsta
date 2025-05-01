
import re
from django.shortcuts import redirect, render
import google.generativeai as genai
import PIL.Image
import requests
from django.utils.html import escape
from atxaisoft_main import settings
from .models import InstagramAgents
from django.utils.dateparse import parse_date, parse_time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.contrib import messages  # messages'ı eklemeyi unutma
from django.http import JsonResponse
from django.shortcuts import render
from google import genai
from asistan.models import InstagramAgents
from product_packages.models import AgentsCard, AgentsPackage, AgentsPayment
import ast
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import openai
import json
import re
# API istemcisini başlat
API_KEY = "AIzaSyDsUwQdKaXHs06fLsgwXVz70QEaDL7vD3E"
client = genai.Client(api_key=API_KEY)
chat = client.chats.create(model="gemini-2.0-flash")
def process(request):
    if request.method == 'POST':
        user_text = request.POST.get('exampleFormControlTextarea', '').strip()
        image_file = request.FILES.get("imageUpload")
        file_file = request.FILES.get("fileUpload")

        if user_text:
            try:
                response = chat.send_message_stream(user_text)
                ai_result = "".join(chunk.text for chunk in response)
                ai_result = re.sub(r"(\*|\*\*)", "", ai_result)  # Gelen cevabı temizle
                return JsonResponse({'ai_result': ai_result})
            except Exception as e:
                return JsonResponse({'error': f'API isteği başarısız oldu: {str(e)}'}, status=500)

        elif image_file:
            try:
                image = PIL.Image.open(image_file)
                response = chat.send_message_stream(["Resimde ne olduğunu anlat", image])
                ai_result = "".join(chunk.text for chunk in response)
                return JsonResponse({"ai_result": ai_result})
            except Exception as e:
                return JsonResponse({'error': f'Görsel işlenirken hata oluştu: {str(e)}'}, status=500)

        elif file_file:
            try:
                client = genai.Client(api_key="AIzaSyDsUwQdKaXHs06fLsgwXVz70QEaDL7vD3E")  # Replace with your actual API key

                # Dosya işleme kodunu buraya ekleyebilirsin
                file_name = file_file.name
                file_extension = file_name.split('.')[-1].lower()
                file_content = file_file.read()

                # Dosya tipine göre işlem yap
                if file_extension == 'pdf':  # PDF dosyasını işliyoruz
                    # PDF dosyasını bayt olarak okuyoruz
                    doc_data = file_content

                    # AI modeline PDF dosyasını ve promptu gönderiyoruz
                    prompt = "Pdf'te ne olduğunu anlat..."
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            types.Part.from_bytes(
                                data=doc_data,
                                mime_type='application/pdf',
                            ),
                            prompt
                        ]
                    )
                    ai_result = re.sub(r"(\*|\*\*)", "", response.text)  # Gelen cevabı temizle
                return JsonResponse({"ai_result": ai_result})
                
            except Exception as e:
                return JsonResponse({'error': f'Dosya işlenirken hata oluştu: {str(e)}'}, status=500)

        else:
            return JsonResponse({'error': 'Girdi verisi bulunamadı.'}, status=400)

    return render(request, 'chat_user_profil/chat_user_profil.html')

import re
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai

logger = logging.getLogger(__name__)

client = genai.Client(api_key="AIzaSyDsUwQdKaXHs06fLsgwXVz70QEaDL7vD3E")
chat = client.chats.create(model="gemini-2.0-flash")

@csrf_exempt
def process2(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Yalnızca POST isteği kabul edilir!'}, status=405)

    try:
        user_text = request.POST.get('exampleFormControlTextarea', '').strip()
        if not user_text:
            return JsonResponse({'error': 'Boş metin gönderildi!'}, status=400)

        # Kullanıcının mesajını sohbete ekleyerek devam et
        response = chat.send_message(user_text)

        # Yanıtı temizleyerek JSON olarak döndür
        ai_result = re.sub(r"(\*|\*\*)", "", response.text)  

        # Sohbet geçmişini al ve istemciye gönder
        history = [
            {"role": message.role, "text": message.parts[0].text}
            for message in chat.get_history()
        ]

        return JsonResponse({'ai_result': ai_result, 'history': history})

    except Exception as e:
        logger.error(f"API isteği başarısız oldu: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Sunucu hatası oluştu, lütfen tekrar deneyin.'}, status=500)




def agents(request):
    agents_cards = AgentsCard.objects.all().order_by('-created_at')
    return render(request,'chat_user_profil/agents.html', {'agents_cards': agents_cards})


def agents_game(request):
    return render(request,'chat_user_profil/agents_game.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




from google import genai

import google.generativeai as genai

API_KEY = "AIzaSyDsUwQdKaXHs06fLsgwXVz70QEaDL7vD3E"
genai.configure(api_key=API_KEY)
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# GenAI modelini içe aktarman gerekiyor (örneğin Google AI SDK'sı).

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=role)

    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text if response else "Hata: Yanıt alınamadı."

# 🚀 Oyun Geliştirme Ajanları
agents_S = {
    "game_designer": Agent("Oyun Tasarımcısı", "Oyunun temel fikrini ve mekaniklerini belirle."),
    "artist": Agent("Sanatçı", "Oyun için konsept tasarımlar ve görseller oluştur."),
    "sound_designer": Agent("Ses Tasarımcısı", "Oyunun müzik ve ses efektlerini tasarla."),
    "story_writer": Agent("Hikaye Yazarı", "Oyunun hikayesini ve diyaloglarını yaz."),
    "developer": Agent("Geliştirici", "Oyunun kodlarını yaz ve mekanikleri uygula."),
    "tester": Agent("Testçi", "Oyunu test et, hataları bul ve geri bildirim ver.")
}

@csrf_exempt
def agents_process(request):
    if request.method == 'POST':
        try:
            input_data = request.POST.get('input', '').strip()
            if input_data:
                # Oyun tasarımcısı fikri oluşturur
                game_design_response = agents_S["game_designer"].generate_response(input_data)
                print(f"🎮 Game Designer: {game_design_response}")

                # Sanatçı konsept tasarımlar oluşturur
                artist_response = agents_S["artist"].generate_response(game_design_response)
                print(f"🎨 Artist: {artist_response}")

                # Ses tasarımcısı sesleri oluşturur
                sound_response = agents_S["sound_designer"].generate_response(artist_response)
                print(f"🎼 Sound Designer: {sound_response}")

                # Hikaye yazarı diyalogları ve hikayeyi oluşturur
                story_response = agents_S["story_writer"].generate_response(sound_response)
                print(f"🎭 Story Writer: {story_response}")

                # Geliştirici kodları yazar
                dev_response = agents_S["developer"].generate_response(story_response)
                print(f"🛠 Developer: {dev_response}")

                # Testçi oyunu test eder ve geri bildirim verir
                tester_response = agents_S["tester"].generate_response(dev_response)
                print(f"🐞 Tester: {tester_response}")

                return JsonResponse({'game_result': tester_response})

            return JsonResponse({'error': 'Boş giriş ile işlem yapılamaz'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Geçersiz JSON formatı'}, status=400)

    return JsonResponse({'error': 'Geçersiz istek'}, status=400)



# @csrf_exempt  # Eğer CSRF token'ını kullanmak istemiyorsanız
# def agents_process(request):
#     if request.method == 'POST':
#         input_data = request.POST.get('input', '').strip()
#         if input_data:
#             response = chat.send_message_stream(input_data)
#             ai_result = "".join(chunk.text for chunk in response)
#             ai_result = re.sub(r"(\*|\*\*)", "", ai_result)  # Gelen cevabı temizle
#             return JsonResponse({'ai_result': ai_result})

#     return JsonResponse({'error': 'Geçersiz istek'}, status=400)




def agents_payment(request, agents_id):
    print("Gelen agents_id:", agents_id)
    agents_pay = AgentsPackage.objects.filter(id=agents_id).first()
    print("Paket adı",agents_pay.package_name,"Paket Id",agents_pay.package_name.id,"Paket süresi",agents_pay.package_duration,"PAKET ADI ",agents_pay.package_title)
    user_email=request.user.email,
    user_full_name=f"{request.user.first_name} {request.user.last_name}",
    print(user_email,user_full_name)
    _To_day_ = datetime.today()
    if agents_pay:
        if request.method == 'POST':
            if request.user.is_authenticated:
                _To_day_ = datetime.today()
                print("Bugünün tarihi:", _To_day_)

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
                    print(f"CVV: ***", cart_cvv)

                    if "3" in agents_pay.package_duration:
                        _next_month_ = _To_day_ + relativedelta(months=3)
                        
                        AgentsPayment.objects.create(
                            purchased_by=request.user,
                            user_email=request.user.email,
                            user_full_name=f"{request.user.first_name} {request.user.last_name}",
                            package_name=agents_pay.package_title,
                            package_id=agents_id,
                            agents_name=agents_pay.package_name,
                            agents_id=agents_pay.package_name.pk,
                            purchase_date=_To_day_.strftime("%Y-%m-%d"),
                            package_price=agents_pay.package_price,
                            expiration_date=_next_month_.strftime("%Y-%m-%d"),
                            is_active=True
                        )      
                        print("3 aylık")

                    elif "6" in agents_pay.package_duration:
                        _next_month_ = _To_day_ + relativedelta(months=6)
                        
                        AgentsPayment.objects.create(
                            purchased_by=request.user,
                            user_email=request.user.email,
                            user_full_name=f"{request.user.first_name} {request.user.last_name}",
                            package_name=agents_pay.package_title,
                            package_id=agents_id,
                            agents_name=agents_pay.package_name,
                            agents_id=agents_pay.package_name.pk,
                            purchase_date=_To_day_.strftime("%Y-%m-%d"),
                            package_price=agents_pay.package_price,
                            expiration_date=_next_month_.strftime("%Y-%m-%d"),
                            is_active=True
                        )  
                        print("6 aylık")

                    elif "12" in agents_pay.package_duration:
                        _next_month_ = _To_day_ + relativedelta(months=12)
                        
                        AgentsPayment.objects.create(
                            purchased_by=request.user,
                            user_email=request.user.email,
                            user_full_name=f"{request.user.first_name} {request.user.last_name}",
                            package_name=agents_pay.package_title,
                            package_id=agents_id,
                            agents_name=agents_pay.package_name,
                            agents_id=agents_pay.package_name.pk,
                            purchase_date=_To_day_.strftime("%Y-%m-%d"),
                            package_price=agents_pay.package_price,
                            expiration_date=_next_month_.strftime("%Y-%m-%d"),
                            is_active=True
                        )  
                        print("12 aylık")
                    else:
                        return redirect("atxaisoft:index")

                    messages.success(request, "Ödeme işlemi başarılı!")
            else:
                messages.error(request, 'Lütfen oturum açtıktan sonra satın alma işlemini gerçekleştirin.')

        return render(request, 'chat_user_profil/agents_payment.html', {'agents_pay': agents_pay})
    else:
        return redirect("atxaisoft:index")

def agents_detail(request,agents_id):
    # agents_id'ye göre AgentsPackage kaydını alıyoruz.

    try:
        agent = AgentsPackage.objects.filter(package_name=agents_id)
    except AgentsPackage.DoesNotExist:
        return redirect("atxaisoft:index")
    # Şablona 'agent' objesini gönderiyoruz.
    return render(request, 'chat_user_profil/agents_detail.html', {'agent': agent})

def instagram(request):
    return render(request,'chat_user_profil/instagram.html')

def x_twitter(request):
    return render(request,'chat_user_profil/x_twitter.html')

def yotube(request):
    return render(request,'chat_user_profil/yotube.html')

def yotube_shorts(request):
    return render(request,'chat_user_profil/youtube_shorts.html')


def whatsapp_business(request):
    return render(request,'chat_user_profil/whatsapp_business.html')



def apps(request):
    return render(request,'apps/apps.html')





class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=role)

    def generate_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text if response else "Hata: Yanıt alınamadı."
    
content_agent = Agent("İçerik Ajanı", 
    "Sen sadece kullanıcıdan gelen metni analiz ederek Instagram için etkileyici, akıcı ve doğal bir paylaşım metni oluşturacaksın. "
    "Yazdığın metin cümlelerden oluşmalı, birbirine bağlanan fikirler içermeli. Metin parçalı, kısa sloganlar şeklinde olmamalı. "
    "Sadece içerik yaz. Hashtag, başlık, görsel açıklaması gibi görevler senin sorumluluğunda değil. "
    "Cümle yapısına ve yazım diline dikkat et. Sanki bir insan yazmış gibi doğal ve anlamlı yaz. "
    "En ama en önemli kural: Açıklama **kesinlikle** 2100 karakteri geçmeyecek. Lütfen bu sınıra göre içerik üret. "
    "Karakter sınırına yakın ama aşmayacak şekilde içerik uzunluğunu ayarla. Yazının sonu doğal şekilde bitmeli. "
    "2100 karakteri geçmemek için metni dikkatli ve dengeli oluştur.Başlık, madde işareti, sayı, emoji ve ** işaretini kesinlikle kullanma. Metinlerin estetik, sade ve dikkat çekici olmalı; kullanıcıların paylaşmak isteyeceği türde olmalı."
)

hashtag_agent = Agent("Hashtag Ajanı", 
    "Sadece sana verilen içerik metnine göre 5 ila 6 adet alakalı ve popüler hashtag oluşturacaksın. "
    "Hashtag dışında hiçbir şey yazmayacaksın. Başlık, açıklama veya başka içerik üretmek senin görevin değil. "
    "Sadece '#' ile başlayan kısa etiketler yaz. Uyarı: Görev sınırlarını aşma!")

image_prompt_agent = Agent("Görsel Ajanı", 
    "Sen sadece kullanıcıdan gelen metne göre, en fazla iki cümlelik bir görsel tanımı yapacaksın. "
    "Görsel tanımı dışında başka açıklama, içerik ya da hashtag vermeyeceksin. "
    "Başka görevleri üstlenmeye çalışma, bu senin işin değil.")

title_agent = Agent("Başlık Ajanı", 
    "Sadece sana verilen içerik metnine göre en fazla 5 kelimeden oluşan dikkat çekici bir başlık yazacaksın. "
    "Hashtag, içerik metni veya görsel açıklaması gibi şeylerle ilgilenme. "
    "Unutma: Senin görevin sadece başlık yazmak, fazlası değil. Sadece bir başlık oluştur.")
@csrf_exempt
def instagram_agents_start(request):
    if request.method == 'POST':
        # ig_user_id = request.POST.get('IgUserId')
        # access_token = request.POST.get('AccessToken')
        # system_prompt = request.POST.get('SystemPrompt')
        # user_prompt = request.POST.get('UserPrompt')
        # date = request.POST.get('date')
        # share_type = request.POST.get('shareType')
        # selected_times = request.POST.get('selectedTimes')

        # POST verilerini temizle
        ig_user_id = escape(request.POST.get('IgUserId', '').strip())
        access_token = escape(request.POST.get('AccessToken', '').strip())
        system_prompt = escape(request.POST.get('SystemPrompt', '').strip())
        user_prompt = escape(request.POST.get('UserPrompt', '').strip())
        date = escape(request.POST.get('date', '').strip())
        share_type = escape(request.POST.get('shareType', '').strip())
        selected_times = escape(request.POST.get('selectedTimes', '').strip())
        # Görselleri al
        files = []
        index = 0
        while True:
            file = request.FILES.get(f'image_{index}')
            if not file:
                break
            files.append(file)
            index += 1

        # Ortak içerikler
        generated_content = content_agent.generate_response(user_prompt)
        generated_hashtags = hashtag_agent.generate_response(generated_content)
        generated_image_prompt = image_prompt_agent.generate_response(generated_content)
        generated_title = title_agent.generate_response(generated_content).title()

        print("İçerik:", generated_content)
        print("Hashtagler:", generated_hashtags)
        print("Görsel Tanımı:", generated_image_prompt)
        print("Başlık:", generated_title)

        try:
            time_list = ast.literal_eval(selected_times)
        except (ValueError, SyntaxError):
            time_list = []

        times = []
        for t in time_list:
            t = t.strip()
            if t:
                parsed_time = parse_time(t)
                if parsed_time:
                    times.append(parsed_time)

        if files:
            # Kullanıcı görsel yüklemişse onu kullan
            first_file = files[0]
            saved_path = default_storage.save(f'instagram_images/{first_file.name}', first_file)
            files[0] = saved_path
            image_url = request.build_absolute_uri(default_storage.url(saved_path))

        else:
            import time
            
            # Kullanıcı görsel yüklemediyse OpenAI ile oluştur
            image_prompt = system_prompt
            timestamp = int(time.time())
            short_name = generated_title[:20].strip().replace(" ", "_")
            file_name = f"post_{short_name}_{timestamp}.png"

            try:
                image_response = openai.Image.create(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    n=1
                )
                image_url = image_response['data'][0]['url']
                img_data = requests.get(image_url)

                if img_data.status_code == 200 and img_data.content:
                    file_path = f'instagram_images/{file_name}'
                    file_content = ContentFile(img_data.content)
                    default_storage.save(file_path, file_content)
                    files.append(file_path)
                else:
                    return JsonResponse({'status': 'error', 'message': 'OpenAI resmi indirilemedi.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'OpenAI görsel hatası: {str(e)}'})

        # InstagramAgents kaydet
        instagram_agent = InstagramAgents(
            user=request.user,
            content=generated_content,
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            captions=generated_title,
            hashtag=generated_hashtags,
            scheduled_date=parse_date(date),
            post_frequency=share_type,
            image_prompt_agent=generated_image_prompt,
        )

        for i, file in enumerate(files):
            setattr(instagram_agent, f'image{i + 1}', file)

        for i, time in enumerate(times):
            if i < 10:
                setattr(instagram_agent, f'scheduled_time{i + 1}', time)

        instagram_agent.save()

        # Instagram paylaşımı
        PAGE_ACCESS_TOKEN = access_token or "EAAJlO7ZAAo8YBOyo7HkCk0pz3Q9LNtnDIMCRUskbr9ZAm1wHI0TKJ0l0jVK2qQrCty0yItLBcBrQFXr52efqiFYX4iQ92J3ZBYaL21qykJwjy80UfOOGueDW6EW4CVOBe7D55056GX6I9k5Gjiwxb3VtetsvP9YSPFjqngww88H1s5lvfmFzt9BcZBbquDdFAwZDZD"
        IG_USER_ID = ig_user_id or "17841473186163452"

        container_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
        container_payload = {
            "image_url": image_url,
            "caption": f"{generated_title}\n\n{generated_content}\n\n{generated_hashtags}",
            "access_token": PAGE_ACCESS_TOKEN,
        }
        container_res = requests.post(container_url, data=container_payload).json()
        print("📦 Container Yanıtı:", container_res)

        if "id" not in container_res:
            return JsonResponse({
                'status': 'error',
                'message': 'Instagram medya oluşturulamadı.',
                'detail': container_res
            })

        creation_id = container_res["id"]

        publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": PAGE_ACCESS_TOKEN,
        }
        publish_res = requests.post(publish_url, data=publish_payload).json()
        print("✅ Yayın Yanıtı:", publish_res)

        if "id" not in publish_res:
            return JsonResponse({
                'status': 'error',
                'message': 'Instagram paylaşımı başarısız.',
                'detail': publish_res
            })

        return JsonResponse({
            'status': 'success',
            'message': 'Görsel başarıyla Instagram’da paylaşıldı.',
            'image_url': image_url,
            "caption": f"{generated_title}\n\n{generated_content}\n\n{generated_hashtags}",
            'instagram_post_id': publish_res.get("id"),
        })
import time
from datetime import datetime

# def sistem_saatini_goster():
#     while True:
#         simdi = datetime.now()
#         saat = simdi.hour
#         dakika = simdi.minute
#         saniye = simdi.second
#         gün = simdi.day
        
        
#         print(f"Sistem saati: {saat:02d}:{dakika:02d}:{saniye:02d}:{gün:02}")
#         time.sleep(1)


# def sistem_saatini_goster(request):
#     while True:
#         simdi = datetime.now()
#         saat = simdi.hour
#         dakika = simdi.minute
#         saniye = simdi.second
#         tumu= saat,dakika,saniye
#         tarih = simdi.strftime("%Y-%m-%d")  # Bugünün tarihi
#         insta_share = InstagramAgents.objects.filter(scheduled_date=tarih,scheduled_time1=tumu)
        
#         print(f"Tarih: {tarih} - Saat: {saat:02d}:{dakika:02d}:{saniye:02d}")
#         time.sleep(1)
#         return request
# sistem_saatini_goster()



# def auto_instagram_post():
#     print("🚀 Otomatik Instagram paylaşım servisi başlatıldı.")
#     while True:
#         try:
#             now = datetime.now()
#             today = now.date()
#             current_time = now.strftime("%H:%M:%S")
#             print(f"⏰ Şu anki zaman: {current_time} | Tarih: {today}")

#             agents = InstagramAgents.objects.filter(is_active=True, scheduled_date=today)
#             print(f"🔍 Bugün ({today}) için aktif ajan sayısı: {agents.count()}")

#             for agent in agents:
#                 print(f"👤 Kullanıcı: {agent.user.username}")
#                 times = [
#                     agent.scheduled_time1, agent.scheduled_time2, agent.scheduled_time3, agent.scheduled_time4,
#                     agent.scheduled_time5, agent.scheduled_time6, agent.scheduled_time7, agent.scheduled_time8,
#                     agent.scheduled_time9, agent.scheduled_time10,
#                 ]
#                 clean_times = list(filter(None, times))
#                 print(f"📅 Ayarlanmış saatler: {clean_times}")

#                 if current_time[:5] in [t[:5] for t in clean_times if t]:
#                     print(f"📢 [{agent.user.username}] için paylaşım zamanı geldi! ({current_time})")
#                     try:
#                         share_to_instagram(agent)
#                         print(f"✅ [{agent.user.username}] için paylaşım başarılı.")
#                     except Exception as e:
#                         print(f"❌ [{agent.user.username}] paylaşım hatası: {e}")
#                 else:
#                     print(f"🕒 [{agent.user.username}] için şu an paylaşım saati değil.")
#         except Exception as outer_err:
#             print("💥 Genel bir hata oluştu:", outer_err)

#         print("🔁 60 saniye bekleniyor...\n")
#         time.sleep(60)
# def share_to_instagram(agent):
#     from django.conf import settings

#     PAGE_ACCESS_TOKEN = "EAAJlO7ZAAo8YBOyo7HkCk0pz3Q9LNtnDIMCRUskbr9ZAm1wHI0TKJ0l0jVK2qQrCty0yItLBcBrQFXr52efqiFYX4iQ92J3ZBYaL21qykJwjy80UfOOGueDW6EW4CVOBe7D55056GX6I9k5Gjiwxb3VtetsvP9YSPFjqngww88H1s5lvfmFzt9BcZBbquDdFAwZDZD"
#     IG_USER_ID = "17841473186163452"

#     try:
#         # Görsel URL’sini hazırla
#         image_path = agent.image1.url
#         image_url = f"{settings.DOMAIN_URL}{image_path}"
#         print(f"🖼️ Görsel URL'si: {image_url}")

#         # Container oluştur
#         container_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
#         container_payload = {
#             "image_url": image_url,
#             "caption": f"{agent.content}\n\n{agent.hashtag}",
#             "access_token": PAGE_ACCESS_TOKEN,
#         }
#         print(f"📦 Container oluşturuluyor... URL: {container_url}")
#         container_res = requests.post(container_url, data=container_payload).json()
#         print("📦 Container Yanıtı:", container_res)

#         if "id" not in container_res:
#             raise Exception(f"Container oluşturulamadı. Yanıt: {container_res}")

#         creation_id = container_res["id"]

#         # Yayınla
#         publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
#         publish_payload = {
#             "creation_id": creation_id,
#             "access_token": PAGE_ACCESS_TOKEN,
#         }
#         print(f"🚀 Yayın başlatılıyor... URL: {publish_url}")
#         publish_res = requests.post(publish_url, data=publish_payload).json()
#         print("✅ Yayın Yanıtı:", publish_res)

#         if "id" not in publish_res:
#             raise Exception(f"Yayın başarısız. Yanıt: {publish_res}")

#     except Exception as e:
#         print(f"❌ [{agent.user}] paylaşım hatası: {e}")

# auto_instagram_post()
