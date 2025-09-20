# Crosshair X Clone (Python)

Bu Python uygulaması, **oyunlarda veya ekran üzerinde ortalanmış crosshair** göstermek için geliştirilmiş basit ve özelleştirilebilir bir araçtır.  

## Özellikler

- **Overlay Crosshair**  
  - +, X, Daire, Nokta ve özel PNG seçenekleri
  - Boyut, kalınlık, renk ve aralık ayarlanabilir
  - Şeffaf arka plan (arka plan görünmez)

- **Kara Tema Ayarlar Penceresi**  
  - Modern TTK bileşenleri kullanılmıştır
  - Boyut, renk, şekil ve gap kolayca değiştirilebilir
  - PNG desteği ile özel crosshair eklenebilir

- **Hotkey Desteği**  
  - `F8` → Crosshair göster/gizle  
  - `F9` → Ayarları varsayılana sıfırla

- **Config Dosyası**  
  - Ayarlar JSON formatında `%TEMP%\crosshair_config.json` içine kaydedilir  
  - Program kapatılsa bile ayarlar korunur

- **Bağımsız Overlay**  
  - Tk ana penceresi gizlidir, crosshair ekranın ortasında bağımsız olarak çalışır

## Kurulum

1. Python 3.10+ yüklü olmalıdır.
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
3. Programı çalıştırın:
   `python crosshair.py`
## Gereksinimler
- Python 3.10+
- Pillow
- keyboard
- pywin32
## Kullanım
- Program açıldığında crosshair overlay ekranın ortasında belirir.
- Ayarlar penceresi ile renk, boyut, şekil ve kalınlığı değiştirebilirsiniz.
- Hotkey'ler ile overlay'i gizleyip gösterebilir veya ayarları sıfırlayabilirsiniz.
