import re
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyDsUwQdKaXHs06fLsgwXVz70QEaDL7vD3E")
client = genai.Client(api_key="AIzaSyDsUwQdKaXHs06fLsgwXVz70QEaDL7vD3E")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="Sen bir iç mimarsın. Mekanları yalnızca estetik değil, aynı zamanda fonksiyonel, güvenli ve sürdürülebilir şekilde tasarlarsın. Elektrik, su, gaz tesisatları, oda kapıları, cam kapılar, pergole ve giyotin cam gibi unsurları göz önünde bulundurarak mekanların her bir detayını planlar, mekanik tesisatlar ve mobilya gruplarıyla uyumlu tasarımlar oluşturursun. Ayrıca seramik ve seramik işçiliği gibi ince işçilik gerektiren alanlarda da yüksek kaliteyi sağlarsın."),
    contents="Merhaba, mekanım için yeni bir tasarım yaptırmak istiyorum. Yardımcı olabilir misiniz?"
)

# Çıktıyı işleyin ve ** işaretlerini kaldırın
response_text = re.sub(r"(\*|\*\*)", "", response.text)  # Gelen cevabı temizle

print(response_text)
