# Gömülü Oyun İçi Mağaza Altyapısı

**mmorpg_store** — Chromium tabanlı, bağımsız çalışan ve herhangi bir masaüstü oyununa entegre edilebilir oyun içi mağaza modülü.

---

## Proje Hakkında

Modern çok oyunculu masaüstü oyunlarında mağaza sistemi genellikle şu şekilde çalışır: oyuncu arayüz içindeki bir butona basar, oyunun üzerine bir Chromium penceresi açılır ve bu pencere üzerinden item satın alınır, bakiye kullanılır, envanter güncellenir.

Bu proje tam olarak o altyapıyı bağımsız bir modül olarak sunar. Herhangi bir oyuna veya uygulamaya entegre etmeye hazır, kendi başına da eksiksiz çalışan bir sistemdir.

Şu an bir oyuna bağlı değildir. Veri tabanı, API ve arayüz tamamen işlevseldir; ileride bir oyun motoruna bağlanmak istendiğinde yalnızca backend katmanının güncellenmesi yeterlidir.

---

## Ne Yapar

- Oyuncu bakiyesi üzerinden item satın alma
- Satın alınan itemların envantere eklenmesi, aynı itemi tekrar alınca adet artması
- Item listesi, kategori filtresi ve arama
- İndirim ve popüler ürün etiketleri
- Nadirlik sistemi: Legendary, Epic, Rare, Common
- Chromium tabanlı arayüz — HTML/CSS/JS ile tam kontrol
- Tek komutla başlatma: `python launcher.py`

---

## Teknolojiler

**Backend**

- Python 3.11
- FastAPI — REST API
- Uvicorn — ASGI sunucusu
- Motor — Asenkron MongoDB sürücüsü
- MongoDB — Oyuncu, item ve satın alım verileri

**Frontend**

- HTML5 / CSS3 / Vanilla JS
- Google Fonts — Ma Shan Zheng, Noto Serif SC
- Chromium tabanlı render

**Masaüstü Katmanı**

- PyQt6 — Ana pencere yönetimi
- PyQt6-WebEngine (QtWebEngine / Chromium) — Arayüz render motoru

---

## Kurulum

Gereksinimler: Python 3.11+, MongoDB

```bash
# Bağımlılıkları kur
pip install -r requirements.txt

# MongoDB başlat (Docker)
docker run -d -p 27017:27017 mongo:7

# İlk çalıştırmada DB'yi sıfırlamak istersen
python reset_db.py

# Uygulamayı başlat
python launcher.py
```

`launcher.py` çalıştırıldığında FastAPI sunucusu otomatik olarak arka planda başlatılır. Ayrı terminal açmak gerekmez.

---

## API

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/player/{player_id}` | Oyuncu bilgisi ve bakiye |
| GET | `/api/items?category=...` | Mağaza itemları, isteğe bağlı kategori filtresi |
| GET | `/api/purchases/{player_id}` | Satın alınan itemlar (envanter) |
| POST | `/api/buy` | Item satın al, bakiyeyi düş |
| GET | `/api/categories` | Mevcut kategoriler |
| GET | `/health` | Sunucu durum kontrolü |

---

## Oyuna Entegrasyon

Modül, ileride bir oyuna gömülmek üzere katmanlı tasarlanmıştır.

- `launcher.py` içindeki `StoreWindow` sınıfı PyQt6 overlay olarak oyun penceresinin üzerine konumlandırılabilir.
- `backend/main.py` içindeki MongoDB bağlantısı oyunun kendi veri tabanıyla değiştirilebilir.
- `POST /api/buy` endpoint'i oyunun envanter sistemine bağlanacak şekilde genişletilebilir.
- PyQt6 `QWebChannel` ile JS ve Python arasında çift yönlü köprü kurulabilir.

---

## PNG İkon Ekleme

Item ikonları şu an emoji ile temsil edilmektedir. Kendi görsellerini eklemek için `frontend/images/` klasörüne PNG dosyalarını koy ve `index.html` içindeki `ICONS` nesnesini güncelle:

```javascript
sword_fire: '<img src="images/sword_fire.png" style="width:40px;height:40px;object-fit:contain">',
```

---

## Lisans

MIT
