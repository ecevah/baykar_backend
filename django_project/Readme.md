# Django IHA Kiralama Sistemi

Bu proje, kullanıcılara IHA (İnsansız Hava Aracı) kiralama hizmeti sunan bir web uygulamasıdır. Django ve PostgreSQL kullanılarak geliştirilmiştir. Uygulama, IHA, Customer ve Reservation olmak üzere üç ana tablodan oluşur.

## Teknolojiler

- Django
- PostgreSQL
- JWT (JSON Web Token) için djangorestframework-simplejwt

## Veritabanı Modeli

- `IHA`: Marka, model, ağırlık, saatlik fiyat, kategori ve resim içerir.
- `Customer`: İsim, soyisim, kullanıcı adı ve şifreden oluşur.
- `Reservation`: Müşteri ve IHA arasında many-to-one ilişki kurar. Başlangıç ve bitiş tarihleri, toplam fiyat ve rezervasyon numarası içerir.

## Özellikler

- CRUD işlemleri: Her tablo için oluşturma, silme, güncelleme ve tüm parametreleri getiren işlevler.
- Özelleştirilmiş sorgular: `get_specific` fonksiyonları ile tablolarda bir veya birden fazla değere göre sorgulama.
- Kullanıcı girişi ve JWT token ile yetkilendirme.
- Rezervasyon kaydında toplam fiyatın dinamik olarak hesaplanması.

## Başlarken

### Önkoşullar

- Python (3.8 veya daha yeni)
- PostgreSQL
- Pipenv veya virtualenv (opsiyonel)

### Kurulum

1. Projeyi klonlayın ve proje dizinine gidin.

   ```bash
   git clone https://yourrepository.com/django_iha_kiralama.git
   cd django_iha_kiralama
   ```

2. Bağımlılıkları yükleyin. (Not: `requirements.txt` dosyası eklenmelidir)

   ```bash
   pip install -r requirements.txt
   ```

3. PostgreSQL veritabanını yapılandırın ve `settings.py` dosyasında gerekli değişiklikleri yapın.

4. Veritabanı migrasyonlarını uygulayın.

   ```bash
   python manage.py migrate
   ```

5. Geliştirme sunucusunu başlatın.
   ```bash
   python manage.py runserver
   ```

### API Yolları

- `/v1/`: Admin işlemleri için.
- `/api/`: Kullanıcı işlemleri için. Middleware üzerinden erişim sağlanır.

# Django IHA Kiralama Sistemi API Kullanımı

Bu belge, Django IHA Kiralama Sistemi'nin API endpoint'leri için detaylı kullanım örnekleri sunmaktadır. Her bir istek için gerekli `Authorization` başlığı ve POST istekleri için gerekli olan istek gövdesi dahil edilmiştir. `/v1/` yalnızca admin erişimi için ayrılmışken, `/api/` yalnızca müşteri kullanımı için belirlenmiştir.

## IHA İşlemleri

### 1. Tüm IHAları Listeleme

- **Endpoint:** `GET /api/ihas`
- **Header:** `Authorization: [your_token_here]`
- **Başarılı Yanıt:** List of IHAs
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`

### 2. Yeni IHA Oluşturma

- **Endpoint:** `POST /v1/iha/create`
- **Header:** `Content-Type: application/json` ve `Authorization: [your_token_here]`
- **Body:**
  ```json
  {
    "brand": "IHA Brand",
    "model": "Model",
    "weight": "Weight",
    "category": "Category",
    "price": "Price",
    "image": "Optional image file"
  }
  ```
- **Başarılı Yanıt:**
  ```json
  {
    "status": true,
    "message": "IHA creation successful.",
    "data": {
        "id": "IHA ID",
        "brand": "IHA Brand",
        "model": "Model",
        ...
    }
  }
  ```
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`

### 3. IHA Silme

- **Endpoint:** `DELETE /v1/iha/delete/[iha_id]`
- **Header:** `Authorization: [your_token_here]`
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`

### 4. IHA Güncelleme

- **Endpoint:** `PUT /v1/iha/update/[iha_id]`
- **Header:** `Authorization: [your_token_here]`
- **Body:** Yeni IHA detayları
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`

### 5. Özel IHA Arama

- **Endpoint:** `GET /api/iha/find?brand=[brand]&model=[model]&...`
- **Header:** `Authorization: [your_token_here]`
- **Başarılı Yanıt:** İstenen özelliklere göre filtrelendiğinde bulunan IHAların listesi
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`

## Müşteri İşlemleri

(Müşteri ile ilgili API endpoint'leri ve örnekleri)

### 1. Tüm Müşterileri Listeleme

- **Endpoint:** `GET /api/customers`
- **Header:** `Authorization: [your_token_here]`
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`

### 2. Müşteri Oluşturma

- **Endpoint:** `POST /api/customer/create`
- **Header:** `Authorization: [your_token_here]`
- **Body:** Müşteri detayları
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`

## Rezervasyon İşlemleri

(Rezervasyon ile ilgili API endpoint'leri ve örnekleri)

### 1. Tüm Rezervasyonları Listeleme

- **Endpoint:** `GET /api/reservations`
- **Header:** `Authorization: [your_token_here]`
- **Hata Yanıtı:** `{"status": false, "message": "Error message"}`
