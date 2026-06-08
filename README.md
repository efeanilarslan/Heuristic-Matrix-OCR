# Karakter Tanıma Sistemi (Heuristic Matrix OCR)

Bu proje, Python ve NumPy kullanarak basit matrisler üzerinden karakter tanıma gerçekleştiren bir görüntü işleme uygulamasıdır. Geleneksel yapay sinir ağları yerine, sezgisel bir ağırlık haritalama ve nokta çarpımı benzerliği yöntemi kullanır.

## Proje Yapısı
- **`AI3.py`**: Uygulamanın en güncel ve kararlı ana çalışma dosyası.
- **`data/`**: Karakter şablonlarını içeren matris dosyaları (`.txt`).
- **`old_projects/`**: Geliştirme sürecindeki eski sürümler ve denemeler.
- **`matris_maker.py`**: Yeni karakter matrisleri oluşturmak için yardımcı araç.

## Kurulum
Öncelikle gerekli kütüphaneleri kurun:
```bash
pip install -r requirements.txt
```

## Kullanım
Programı ana dizinden şu komutla çalıştırabilirsiniz:
```bash
python AI3.py
```

## Çalışma Mantığı (Heuristic Approach)
Sistem, `data/` klasöründeki şablonları analiz ederek her karakter için bir "frekans haritası" oluşturur. Kullanıcının çizdiği yeni matris ile bu haritalar arasında nokta çarpımı (dot product) yaparak bir benzerlik skoru üretir. Boş hücreler ve az kullanılan pikseller için sezgisel cezalandırma puanları uygulayarak doğruluğu artırır.
