# Berat Ayazoğlu 2411081041 – Stok Yönetimi Sistemi

# 1. Projenin Amacı
Bu proje küçük ve orta ölçekli işletmelerin stok takibini dijital ortamda kullanıcı dostu bir arayüzle yapabilmelerini sağlamak amacıyla geliştirilmiştir. Manuel stok takibinin karmaşıklaştığı ve hatalara açık hale geldiği durumlarda bu sistem ürünlerin barkod, üretici, miktar gibi bilgileriyle kolayca izlenebilmesini sağlar.

# 2. Projenin Kapsamı ve Özellikleri
**Sistem Neler Yapabiliyor:**
- Kullanıcı kayıt ve giriş sistemi
- Admin girişi (sabit kullanıcı: admin@example.com/admin123)
- Ürün ekleme, düzenleme, silme
- Ürün arama ve filtreleme (Ürün adı, barkod, üretici vs)
- JSON formatında veri dışa aktarma
- Sade arayüz

**Kapsam Dışında Kalanlar:**
- Gerçek zamanlı bildirimler (Stok azaldığında)
- Geçmiş izleme


## 3. Kullanılan Teknolojiler
- **Programlama Dili:** Python, HTML, CSS, JavaScript
- **Framework:** Flask
- **Veritabanı:** SQLite
- **Araçlar / Kütüphaneler:**
  - Bootstrap 5 (arayüz tasarımı)
  - Jinja2 (şablon motoru)
  - Flask-SQLAlchemy (veritabanı işlemleri)
  - Flask-WTF (form işlemleri)
  - Flask-Login (giriş kontrolü)

## 4. Kurulum ve Çalıştırma Talimatları
1. Bu projeyi GitHub’dan klonlayın:
    ```bash
    git clone https://github.com/kullaniciadi/stok-yonetimi-sistemi.git
    cd stok-yonetimi-sistemi
    ```

2. Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3. Veritabanını oluşturun:
    ```bash
    python site_db.py
    ```

4. Uygulamayı çalıştırın:
    ```bash
    python app.py
    NOT: calistir.bat ile direk çalıştırılabilir 
    ```

5. Tarayıcınızdan `http://127.0.0.1:5000` adresini ziyaret edin.

---

## 5. Dosya Yapısı ve Açıklamaları

stokyonetimi/
├── instance/
| ├── site.db → Veritabanı
├── templates/
│ ├── base.html → Ortak şablon
│ ├── adminpanel.html → Admin Panel Formu
│ ├── dashboard.html → Kullanıcı Panel Fromı
│ ├── edit_stock.html → Düzenlenebilir stok formu
│ ├── edit_user.html → Düzenlenebilir kullanıcı formu
│ ├── login.html → Giriş formu
│ ├── stock_form.html → Stok Giriş formu
│ ├── register.html → Kayıt formu
│ ├── stokekle.html → Yeni ürün ekleme
│ ├── stokduzenle.html → Ürün düzenleme
├── static/
│ └── style.css → Özel stiller
├── app.py → Ana uygulama dosyası
├── data.json → Vei çıktı
├── calistir.bat → otomatik sunucu başlatma .bat
├── requirements.txt → Gereken kütüphaneler

## 6. Ekran Görselleri / Kısa Demo

### Görseller Ekran Görüntüleri png dosyası içeriğindedir:
    [stokyonetimi/png]


### JSON Veri Örneği:

    {
        "id": 8,
        "product_name": "Lego Blok Seti\t",
        "quantity": 50,
        "price": 215.0,
        "kdvli_fiyat": 253.7,
        "manufacturer": "MegaBlok",
        "category": "Oyuncak",
        "barcode": "8690002000001",
        "created_at": "2025-05-12 17:55:47"
    }

## 7. Zorluklar ve Öğrenilenler
Proje sürecinde özellikle Flask ta url_for request.args.get gibi fonksiyonların kullanımı başta karmaşık geldi. Ayrıca filtreleme işlemlerini yaparken veritabanı sorgularının doğru çalışması için birçok kez test yapmam gerekti. HTML ve Boostrap ile responsive arayüz geliştirmek de pratik kazandırdı. En önemlisi Flask içinde sayfa yönlendirme kullanıcı yönetimi gibi temel kavramları ögrendim.

## 8. Geliştirilebilir Yönler
Kullanıcı rollerine göre yetkilendirme (örneğin: depo çalışanı, yönetici)

Fatura  ekleme

İskont ekleme

PDF ve Excel dışa aktarma

Ürün görseli ekleme

Stok kritik seviyeleri için uyarı sistemi

E-posta entegrasyonu ile raporlama

Kdv değeri Değiştirme

Sanal Mağaza Bağlanıtısı(Site bağlantısı)

Fatura akratılması (Malkabul faturanın elle değil kesen firmanın otomatik olarak sisteme çekmesi veya aktarılması)

Kategorileri yönetme paneli (sabit kategori sistemi)

API desteği (mobil uygulama bağlantısı için)

Kategoriye göre grafiklerle stok analizi

Ciro ekleme

Günlük/Aylık/Yıllık Rapor Ciro (filtreleme dahil)

Bunun yanında verileri çekeceği bir satış arayüzü eklenebilir veya başka bir proje tasarlayarak birbirine entegre edilebilir 

Yardım Menüsü (Kullanıcının arayüzüne rehberlik için)

Stok Destek ekleme (Kullancı sikayet veya öneri için yada yaşadığı sorunu bildirmek için bir form ekranı eklenebilir adminveya yetkili oradan dönüş sağlayabilir)

Arayü Özelleştirme (kullanıcıların en çok kullandığı formları kendileri Dashboard da buton oalrak taşıma veya eklemesi için kullanım kolaylığı için bir eklenti eklenbilir (BİRAZ ABARTILI ama olabilir))

Yedekleme (Save dosyası oluşturularak her 1 saatte  bir veya 30 dk bir manuel de eklenebilir kullancı giridiiğin herhangi bir sorun a(Öreneğin: Elektirik veya donaım sorunu) karşı yedekleme böylece kullanıcı kaldığı yerden devam edebilir ve mağdur olmazmış olur.)

## 9. İletişim Bilgisi
GitHub: [github.com/kullaniciadi/stok-yonetimi-sistemi](https://github.com/BeratAyazoglu/final_projesi-/tree/main/stokyonetimi)
