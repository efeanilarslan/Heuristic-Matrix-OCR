import numpy as np
import os

def veri_seti_olustur(sablon, K, dosya_adi='matrisler3.txt'):
    """
    sablon: N x M boyutunda numpy array (Şeklin kendisi)
    K: Levhanın boyutu (K x K kare alan)
    """
    N, M = sablon.shape  # Şeklin boyutlarını al (N: Yükseklik, M: Genişlik)
    kombinasyonlar = []

    # Şablonun KxK alana sığıp sığmadığını kontrol et
    if N > K or M > K:
        print(f"Hata: {N}x{M} boyutundaki şekil {K}x{K} alana sığmaz!")
        return

    # Kaydıran Pencere (Sliding Window) Algoritması
    # Dikeyde (K - N + 1), Yatayda (K - M + 1) kadar farklı pozisyon vardır.
    for i in range(K - N + 1):
        for j in range(K - M + 1):
            # 1. K x K boyutunda boş (0) bir levha oluştur
            levha = np.zeros((K, K), dtype=int)
            
            # 2. Şablonu (i, j) koordinatından başlayarak levhaya yerleştir
            levha[i:i+N, j:j+M] = sablon
            
            # 3. Levhayı tek bir satır (K*K eleman) haline getir ve listeye ekle
            kombinasyonlar.append(levha.flatten())

    # Sonuçları dosyaya yaz
    with open(dosya_adi, 'w') as f:
        for satir in kombinasyonlar:
            # Listeyi boşluklu metne çevir: "0 0 1 0..."
            metin = " ".join(map(str, satir))
            f.write(metin + "\n")

    print(f"İşlem Tamam!")
    print(f"Şekil Boyutu: {N}x{M}")
    print(f"Levha Boyutu: {K}x{K}")
    print(f"Toplam Üretilen Varyasyon: {len(kombinasyonlar)}")
    print(f"Dosya: {os.path.abspath(dosya_adi)}")

# --- AYARLAR VE ÇALIŞTIRMA ---

# 1. Şablonu Belirle (N x M)
# İstediğin şekli buraya istediğin boyutta girebilirsin.
# Örnek: 3x5 boyutunda bir 'S' harfi
ssekil = np.array([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# 2. Büyük Levha Boyutunu Belirle (K x K)
K_DEGERI = 16

# 3. Fonksiyonu Çalıştır
veri_seti_olustur(ssekil, K_DEGERI)