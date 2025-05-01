# from datetime import datetime, time
# from django.test import TestCase

# import time
# from datetime import datetime

# import requests

# from asistan.models import InstagramAgents

# # def sistem_saatini_goster():
# #     while True:
# #         simdi = datetime.now()
# #         saat = simdi.hour
# #         dakika = simdi.minute
# #         saniye = simdi.second
# #         print(f"Sistem saati: {saat:02d}:{dakika:02d}:{saniye:02d}")
# #         time.sleep(1)

# # sistem_saatini_goster()


# PAGE_ACCESS_TOKEN = "EAAJlO7ZAAo8YBOyo7HkCk0pz3Q9LNtnDIMCRUskbr9ZAm1wHI0TKJ0l0jVK2qQrCty0yItLBcBrQFXr52efqiFYX4iQ92J3ZBYaL21qykJwjy80UfOOGueDW6EW4CVOBe7D55056GX6I9k5Gjiwxb3VtetsvP9YSPFjqngww88H1s5lvfmFzt9BcZBbquDdFAwZDZD"
# IG_USER_ID = "17841473186163452"

# def zaman_uyumlu_kayitlari_getir():
#     simdi = datetime.now()
#     bugun = simdi.date()
#     saat_dakika = f"{simdi.hour:02d}:{simdi.minute:02d}"
#     filtre = {
#         "is_active": True,
#         "scheduled_date": bugun
#     }

#     # scheduled_timeX alanlarında şu anki saat dakikaya uyan içerikleri filtrele
#     queryset = InstagramAgents.objects.filter(**filtre)
#     sonuc = []

#     for kayit in queryset:
#         for i in range(1, 11):
#             zaman_alan = getattr(kayit, f"scheduled_time{i}")
#             if zaman_alan and zaman_alan.strip() == saat_dakika:
#                 sonuc.append(kayit)
#                 break

#     return sonuc


# def instagram_gonderi_yap(agent):
#     if not agent.image1:
#         print("❌ Görsel yok, gönderi atlanıyor.")
#         return

#     image_url = agent.image1.url  # Eğer dış erişime açık değilse, tam URL'ye çevir
#     if image_url.startswith("/"):
#         image_url = f"https://senin-site-adresin.com{image_url}"

#     caption_text = f"{agent.content}\n\n{agent.captions}\n\n{agent.hashtag}"

#     # Adım 1: Container oluştur
#     container_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
#     container_payload = {
#         "image_url": image_url,
#         "caption": caption_text,
#         "access_token": PAGE_ACCESS_TOKEN,
#     }
#     container_res = requests.post(container_url, data=container_payload).json()
#     print("📦 Container Yanıtı:", container_res)

#     if "id" not in container_res:
#         print("❌ Container oluşturulamadı.")
#         return

#     creation_id = container_res["id"]

#     # Adım 2: Paylaşım
#     publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
#     publish_payload = {
#         "creation_id": creation_id,
#         "access_token": PAGE_ACCESS_TOKEN,
#     }
#     publish_res = requests.post(publish_url, data=publish_payload).json()
#     print("✅ Yayın Yanıtı:", publish_res)

#     if "id" in publish_res:
#         print(f"✔ Başarıyla paylaşıldı: {publish_res['id']}")
#     else:
#         print("❌ Paylaşım başarısız.")


# def zamanlayici_fonksiyon():
#     while True:
#         print(f"🕒 Kontrol saati: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         gonderilecekler = zaman_uyumlu_kayitlari_getir()

#         if gonderilecekler:
#             print(f"🎯 {len(gonderilecekler)} içerik paylaşılacak.")
#             for agent in gonderilecekler:
#                 instagram_gonderi_yap(agent)
#         else:
#             print("🔍 Paylaşılacak içerik bulunamadı.")

#         time.sleep(60)  # Her 1 dakikada bir çalışır

# # Çalıştırmak için
# zamanlayici_fonksiyon()



import requests
import time
import google.generativeai as genai


import time
import requests
# Facebook API Access Token ve Kullanıcı ID'si
PAGE_ACCESS_TOKEN = "EAAJlO7ZAAo8YBOyo7HkCk0pz3Q9LNtnDIMCRUskbr9ZAm1wHI0TKJ0l0jVK2qQrCty0yItLBcBrQFXr52efqiFYX4iQ92J3ZBYaL21qykJwjy80UfOOGueDW6EW4CVOBe7D55056GX6I9k5Gjiwxb3VtetsvP9YSPFjqngww88H1s5lvfmFzt9BcZBbquDdFAwZDZD"
IG_USER_ID = "17841473186163452"
import re
from google import genai
from google.genai import types
client = genai.Client(api_key="AIzaSyDsUwQdKaXHs06fLsgwXVz70QEaDL7vD3E")

import time
MAX_COMMENT_LENGTH = 2100 
def reply_to_comment(comment_id, message):
    """Yoruma cevap ver."""
    # Yorumun uzunluğunu kontrol et
    if len(message) > MAX_COMMENT_LENGTH:
        print(f"⚠️ Yorum çok uzun! Yorum uzunluğu {len(message)} karakter. Yorum kısaltılıyor...")
        message = message[:MAX_COMMENT_LENGTH]  # Yorumun ilk kısmını al

    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    payload = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"✅ Yoruma cevap verildi: {message}")
    else:
        print("Cevap verirken hata:", response.text)

def get_posts():
    """Sayfada yayınlanan gönderileri çek."""
    url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print("Gönderileri çekerken hata:", response.text)
        return []

def get_post_details(post_id):
    """Bir gönderinin detayını (caption vs) çek."""
    url = f"https://graph.facebook.com/v18.0/{post_id}?fields=caption&access_token={PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Gönderi detaylarını çekerken hata:", response.text)
        return {}

def get_comments(post_id):
    """Seçilen gönderinin yorumlarını çek."""
    url = f"https://graph.facebook.com/v18.0/{post_id}/comments?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        print(f"Yorum verisi: {data}")  # Yorum verisini debug olarak yazdırıyoruz.
        return data
    else:
        print("Yorumları çekerken hata:", response.text)
        return []

def generate_ai_reply(comment_text):
    """AI cevabı üretir."""
    if client is None:
        print("AI istemcisi tanımlanmadı!")
        return "AI cevabı için istemci yapılandırılmalı."

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Sen bir iç mimarsın. Mekanları yalnızca estetik değil, aynı zamanda fonksiyonel, güvenli ve sürdürülebilir şekilde tasarlarsın. Elektrik, su, gaz tesisatları, oda kapıları, cam kapılar, pergole ve giyotin cam gibi unsurları göz önünde bulundurarak mekanların her bir detayını planlar, mekanik tesisatlar ve mobilya gruplarıyla uyumlu tasarımlar oluşturursun. Ayrıca seramik ve seramik işçiliği gibi ince işçilik gerektiren alanlarda da yüksek kaliteyi sağlarsın."),
        contents=comment_text
    )
    # Çıktıyı işleyin ve ** işaretlerini kaldırın
    response_text = re.sub(r"(\*|\*\*)", "", response.text)  # Gelen cevabı temizle
    return response_text.strip()
def main():
    # Sayfadaki gönderileri çek
    print("📋 Sayfadaki gönderiler çekiliyor...\n")
    posts = get_posts()

    if not posts:
        print("Hiç gönderi bulunamadı.")
        return

    print("Mevcut Gönderiler:\n")
    for idx, post in enumerate(posts):
        post_id = post['id']
        details = get_post_details(post_id)
        caption = details.get('caption', '[Açıklama Yok]')
        print(f"{idx + 1}. Post ID: {post_id} - Açıklama: {caption[:50]}...")

    try:
        selection = int(input("\nYorumlara cevap vermek istediğin gönderi numarasını gir: "))
        selected_post_id = posts[selection - 1]['id']
    except (ValueError, IndexError):
        print("Geçersiz seçim.")
        return

    print(f"\n🔎 Seçilen Gönderi ID: {selected_post_id}\n")
    conversation_history = []  # Sıralı şekilde kullanıcı ve AI hareketlerini tutacağız
    already_replied_comments = set()  # Aynı yoruma 2 kere cevap verilmemesi için

    while True:
        comments = get_comments(selected_post_id)
        print(f"📨 Çekilen yorum sayısı: {len(comments)}")

        if not comments:
            print("⚠️ Henüz yorum yok veya çekilemedi.")

        comments_sorted = sorted(comments, key=lambda x: x.get('timestamp', ''))  # Tarihe göre sırala (eğer varsa)
        
        for comment in comments_sorted:
            comment_id = comment['id']
            comment_text = comment.get('text')
            commenter_id = comment.get('from', {}).get('id')

            if not comment_text or not comment_text.strip():
                print(f"⚠️ Yorum ID {comment_id} mesaj içermiyor veya boş, atlanıyor.")
                continue

            if comment_id in already_replied_comments:
                continue

            # Konuşma geçmişinde son konuşan kim?
            last_speaker = conversation_history[-1][1] if conversation_history else None

            # Eğer son AI konuşmuşsa, ve şimdiki gelen de kullanıcıysa → cevap ver
            if last_speaker != 'user':
                print(f"🧠 AI cevap veriyor: {comment_text}")

                ai_reply = generate_ai_reply(comment_text)
                if not ai_reply:
                    print(f"⚠️ AI cevabı boş geldi, yorum atlanıyor.")
                    continue

                reply_to_comment(comment_id, ai_reply)

                conversation_history.append((commenter_id, 'user'))  # Önce kullanıcı yazdı
                conversation_history.append(('ai', 'ai'))            # Sonra AI cevapladı
                already_replied_comments.add(comment_id)

            else:
                print(f"➡️ Son yorumu kullanıcı yazmış, AI bekliyor.")
                conversation_history.append((commenter_id, 'user'))

        print("\n⏳ 1 dakika bekleniyor, yeni yorumlar kontrol edilecek...")
        time.sleep(60)

if __name__ == "__main__":
    main()