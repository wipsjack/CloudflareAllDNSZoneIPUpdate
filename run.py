import CloudFlare

# Kullanıcının dil seçimini isteme işlemi
while True:
    lang = input("Select your language (TR/EN/DE/FR/IT): ").upper()
    if lang in ['TR', 'EN', 'DE', 'FR', 'IT']:
        break
    else:
        print("Geçersiz giriş yaptınız. Lütfen yeniden deneyin." if lang == 'TR' else "Invalid input. Please try again.")

# Cloudflare API anahtarınızı ve e-posta adresinizi girin.
cf = CloudFlare.CloudFlare(email='email_adresiniz@example.com', token='api_anahtarınız')

# Eski IP adresini girin
old_ip = "eski_ip_adresi"

# Yeni IP adresini girin
new_ip = "yeni_ip_adresi"

# Tüm zone'ların listelenmesi
zones = cf.zones.get()

# Değiştirilecek kayıtların topluca saklanması için bir liste oluşturulması
records_to_update = []

# Her zone için kayıtların listelenmesi ve IP adreslerinin güncellenmesi
for zone in zones:
    zone_id = zone['id']
    dns_records = cf.zones.dns_records.get(zone_id)
    for record in dns_records:
        record_id = record['id']
        record_type = record['type']
        content = record['content']

        # Dil çevirisi
        if lang == 'TR':
            if record_type == 'A':
                content = "Alan adı"
            elif record_type == 'CNAME':
                content = "Alternatif alan adı (CNAME)"
            elif record_type == 'MX':
                content = "E-posta sunucusu"
            elif record_type == 'TXT':
                content = "Metin"
            else:
                content = "Bilinmeyen tip"

        elif lang == 'DE':
            if record_type == 'A':
                content = "Domain-Name"
            elif record_type == 'CNAME':
                content = "Alternativer Domain-Name (CNAME)"
            elif record_type == 'MX':
                content = "E-Mail-Server"
            elif record_type == 'TXT':
                content = "Text"
            else:
                content = "Unbekannter Typ"

        elif lang == 'FR':
            if record_type == 'A':
                content = "Nom de domaine"
            elif record_type == 'CNAME':
                content = "Nom de domaine alternatif (CNAME)"
            elif record_type == 'MX':
                content = "Serveur de messagerie électronique"
            elif record_type == 'TXT':
                content = "Texte"
            else:
                content = "Type inconnu"

        elif lang == 'IT':
            if record_type == 'A':
                content = "Nome di dominio"
            elif record_type == 'CNAME':
                content = "Nome di dominio alternativo (CNAME)"
            elif record_type == 'MX':
                content = "Server di posta elettronica"
            elif record_type == 'TXT':
                content = "Testo"
            else:
                content = "Tipo sconosciuto"

        if old_ip in content:
            print(f"{content} ({record_type})" if lang == 'EN' else f"{content} ({record_type}) bulundu.")
            
            new_content = content.replace(old_ip, new_ip)
            record['content'] = new_content
            records_to_update.append((zone_id, record_id, record, f"{content} ({record_type}) {zone['name']} alan adında bulundu ve IP adresi güncellendi."))

# Toplu kayıt güncelleme işlemi
if records_to_update:
    while True:
        answer = input(f"{len(records_to_update)} kaydı güncellemek istediğinizden emin misiniz? (E/H)").upper()
        if answer == 'E':
            for zone_id, record_id, record, message in records_to_update:
                r = cf.zones.dns_records.put(zone_id, record_id, data=record)

                if lang == 'EN':
                    print(f"{message} New IP: {r['content']}")
                else:
                    print(f"{message} Yeni IP: {r['content']}")

            break
        elif answer == 'H':
            print("İşlem iptal edildi." if lang == 'TR' else "Process cancelled.")
            break
        else:
            print("Lütfen 'E' veya 'H' girin." if lang == 'TR' else "Please enter 'Y' or 'N'.")

else:
    if lang == 'EN':
        print("No matching DNS records found.")
    elif lang == 'TR':
        print("Eşleşen DNS kaydı bulunamadı.")
    elif lang == 'DE':
        print("Keine passenden DNS-Einträge gefunden.")
    elif lang == 'FR':
        print("Aucun enregistrement DNS correspondant trouvé.")
    elif lang == 'IT':
        print("Nessuna corrispondenza trovata per il record DNS.")
