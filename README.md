# Raspberry Pi Robot Vacuum Cleaner Project

Bu proje, Raspberry Pi, Ultrasonik Sensörler, Motor Sürücü (L298) ve LCD ekran kullanılarak geliştirilen bir robot süpürge kontrol sistemini içerir.

## Kurulum

1. **Proteus Kütüphaneleri:**
   - `IDX` ve `LIB` dosyalarını `C:\Program Files (x86)\Labcenter Electronics\Proteus 8.13 Professional\DATA\LIBRARY` yoluna ekleyin.
   - `hcsr04sensor` klasörünü `C:\Program Files (x86)\Labcenter Electronics\Proteus 8.13 Professional\DATA\VSM Studio\drivers\RaspberryPi` yoluna ekleyin.

2. **Sensör Kullanımı:**
   - `hcsr04sensor` kütüphanesini kodunuzda şu şekilde çağırın: `import hcsr04sensor`

3. **Dokunmatik Sensör:**
   - Robot süpürgeyi başlatmak için dokunmatik sensöre bir sinyal gönderin.

## Sensör ve Robot Hareketleri

- Ultrasonik sensör, robot süpürgenin çevresindeki mesafeyi ölçer.
- Mesafe belirli bir sınırın altına düştüğünde, robot süpürge belirli bir hareket sergiler (örneğin, sağa döner).
- Robot süpürge belirli bir temizleme mantığına sahiptir (örneğin, U şeklinde hareket eder).

## Robot Hareket Mantığı

- Robot süpürge, belirli bir süre düz gider, ardından sağa döner, tekrar düz gider ve bu döngüyü devam ettirir.
- Sağa dönmek için sol motorun gücü kesilir, sola dönmek için sağ motorun gücü kesilir.

## Katkıda Bulunma

Eğer bu projeye katkıda bulunmak istiyorsanız, lütfen bir çekme isteği (pull request) göndermeden önce [Katkıda Bulunma Kılavuzu](CONTRIBUTING.md) dosyasını inceleyin.

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.
