import redis_vol1
import time

# Kullanicilarimizi ve durumlarini simüle edelim
kullanici_a_id = "user_A"
kullanici_b_id = "user_B"

def main():
    print("----- Senaryo Baslangici -----")
    print("1. Kullanici B'nin cevrimdisi oldugunu simule ediyoruz.")
    redis_vol1.kullanici_kapatti(kullanici_b_id)
    # redis_vol1.kullanici_baglandi(kullanici_a_id)  # opsiyonel: Kullanici A'nin online oldugunu varsayiyoruz

    print(f"\n2. Kullanici A, Kullanici B'ye mesaj gonderiyor.")
    mesaj_icerigi = "Selam, nasilsin?"

    # mesaj_birak fonksiyonu, alici cevrimdisi oldugu icin True donmeli
    mesaj_birakildi_mi = redis_vol1.mesaj_birak(kullanici_b_id, kullanici_a_id, mesaj_icerigi)

    if mesaj_birakildi_mi:
        print(f"   -> Mesaj Redis'e basariyla birakildi.")
    else:
        print(f"   -> Hata: Mesaj Redis'e birakilamadi, alici online gorunuyor.")

    print("\n3. Kullanici A cevrimdisi oluyor.")
    redis_vol1.kullanici_kapatti(kullanici_a_id)
    print("   -> Redis'ten Kullanici A'nin cevrimici durumu kaldirildi.")
    
    # Bu noktada, Redis veritabanina baglanip 'offline_mesajlar:user_B' anahtarinin
    # altinda mesagin olup olmadigini manuel olarak kontrol edebilirsiniz.
    
    print("\n4. Kullanici B cevrimici oluyor.")
    redis_vol1.kullanici_baglandi(kullanici_b_id)
    print("   -> Kullanici B'nin durumu Redis'te cevrimici olarak guncellendi.")

    print(f"\n5. Kullanici B, cevrimdisi oldugu zaman kendisine gelen mesajlari kontrol ediyor.")
    gelen_mesajlar = redis_vol1.offline_mesajlari_getir(kullanici_b_id)

    if gelen_mesajlar:
        print("   -> Cevrimdisi gelen mesaj(lar) bulundu:")
        for mesaj in gelen_mesajlar:
            print(f"      - Gonderen: {mesaj['gonderen']}, Icerik: {mesaj['icerik']}")
    else:
        print("   -> Bekleyen mesaj bulunamadi.")

    print("\n6. Mesajlar alindiktan sonra Redis'teki kuyrugun bosaltildigini kontrol ediyoruz.")
    kalan_mesajlar = redis_vol1.offline_mesajlari_getir(kullanici_b_id)
    
    if not kalan_mesajlar:
        print("   -> Basarili: Kuyruk temizlenmis.")
    else:
        print("   -> Hata: Kuyruk hala mesaj iceriyor.")
        
    print("\n----- Senaryo Sonu -----")

if __name__ == "__main__":
    main()