import redis
import pickle
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def sohbete_katil(user_id, chat_id):
    r.sadd(f"aktif_sohbetler:{user_id}", chat_id)
    r.sadd("aktif_kullanicilar", user_id)

def mesaj_birak(alici_id, gonderen_id, icerik):
    if r.get(f"baglantida_mi:{alici_id}") == b'true':
        return False

    mesaj = {
        "gonderen": gonderen_id,
        "icerik": icerik,
        "timestamp": time.time(),
        "read_by": []
    }

    key = f"offline_mesajlar:{alici_id}"
    r.rpush(key, pickle.dumps(mesaj))
    return True

def mesajlari_oku(chat_id, okuyan_id):
    key = f"sohbet:{chat_id}"
    mesajlar = r.lrange(key, 0, -1)
    guncellenen = []

    for m in mesajlar:
        mesaj = pickle.loads(m)
        if okuyan_id != mesaj["gonderen"] and okuyan_id not in mesaj.get("read_by", []):
            mesaj["read_by"].append(okuyan_id)
        guncellenen.append(pickle.dumps(mesaj))

    if guncellenen:
        r.delete(key)
        r.rpush(key, *guncellenen)

    return [pickle.loads(m) for m in guncellenen]

def sohbetten_cik(user_id, chat_id):
    r.srem(f"aktif_sohbetler:{user_id}", chat_id)
    r.srem(f"sohbet_katilim:{chat_id}", user_id)
    if r.scard(f"sohbet_katilim:{chat_id}") == 0:
        r.delete(f"sohbet:{chat_id}")

def offline_mesajlari_getir(user_id):
    key = f"offline_mesajlar:{user_id}"
    mesajlar = r.lrange(key, 0, -1)
    r.delete(key)
    return [pickle.loads(m) for m in mesajlar]

def kullanici_baglandi(user_id):
    r.set(f"baglantida_mi:{user_id}", "true")

def kullanici_kapatti(user_id):
    r.set(f"baglantida_mi:{user_id}", "false")

def mesajlari_sil(chat_id):
    r.delete(f"sohbet:{chat_id}")

def sohbet_sil_if_herkes_cikti(chat_id, user1, user2):
    aktif1 = r.sismember(f"aktif_sohbetler:{user1}", chat_id)
    aktif2 = r.sismember(f"aktif_sohbetler:{user2}", chat_id)
    if not aktif1 and not aktif2:
        r.delete(f"sohbet:{chat_id}")