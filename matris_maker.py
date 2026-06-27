import numpy as np
import pygame
import os
import sys

BOYUT = 16
HÜCRE_BOYUTU = 35
PENCERE_BOYUTU = BOYUT * HÜCRE_BOYUTU

# 'data' klasörünü kontrol et, yoksa oluştur
klasor_yolu = "data"
if not os.path.exists(klasor_yolu):
    os.makedirs(klasor_yolu)

cizim_alani = np.zeros((BOYUT, BOYUT), dtype=int)

pygame.init()
pencere = pygame.display.set_mode((PENCERE_BOYUTU, PENCERE_BOYUTU + 50))
pygame.display.set_caption("Şablon Üretici: Harfi Çizin")
font = pygame.font.SysFont("Arial", 14, bold=True)
calisiyor = True

while calisiyor:
    pencere.fill((200, 200, 200))
    for r in range(BOYUT):
        for c in range(BOYUT):
            renk = (0, 100, 200) if cizim_alani[r, c] == 1 else (255, 255, 255)
            pygame.draw.rect(pencere, renk, (c * HÜCRE_BOYUTU, r * HÜCRE_BOYUTU, HÜCRE_BOYUTU - 1, HÜCRE_BOYUTU - 1))
    buton_alani = pygame.Rect(10, PENCERE_BOYUTU + 10, PENCERE_BOYUTU - 20, 30)
    pygame.draw.rect(pencere, (200, 50, 50), buton_alani)
    yazi = font.render("ÇİZİMİ BİTİR VE VARYASYONLARI ÜRET", True, (255, 255, 255))
    pencere.blit(yazi, (PENCERE_BOYUTU // 2 - yazi.get_width() // 2, PENCERE_BOYUTU + 17))
    
    pygame.display.flip()
    
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif olay.type == pygame.MOUSEBUTTONDOWN or (olay.type == pygame.MOUSEMOTION and olay.buttons[0]):
            f_x, f_y = pygame.mouse.get_pos()
            if f_y < PENCERE_BOYUTU:
                c, r = f_x // HÜCRE_BOYUTU, f_y // HÜCRE_BOYUTU
                if olay.type == pygame.MOUSEBUTTONDOWN:
                    cizim_alani[r, c] = 1 - cizim_alani[r, c]
                else:
                    cizim_alani[r, c] = 1
            elif buton_alani.collidepoint(f_x, f_y) and olay.type == pygame.MOUSEBUTTONDOWN:
                calisiyor = False
pygame.quit()

# çizilen piksellerin koordinatlarını bul
aktif_pikseller = np.argwhere(cizim_alani == 1)

if len(aktif_pikseller) == 0:
    print("Hata: Hiçbir şey çizmediniz. Program sonlandırılıyor.")
    sys.exit()

# şeklin sınırları
min_y, min_x = aktif_pikseller.min(axis=0)
max_y, max_x = aktif_pikseller.max(axis=0)

# ana matristen sadece şeklin olduğu n x m boyutundaki kısmı kes
saf_sablon = cizim_alani[min_y:max_y+1, min_x:max_x+1]
N, M = saf_sablon.shape

print(f"\nÇizim Algılandı! Şeklin saf boyutu: {N} satır x {M} sütun.")

harf_etiketi = input("Bu şekil hangi karaktere ait? (Örn: S, F, A vb.): ").strip().upper()
dosya_yolu = os.path.join(klasor_yolu, f"{harf_etiketi}.txt")

kombinasyonlar = []

# şablonu 16x16'lık levha üzerinde gezdir (sonrasında bu durum değişebilir)
for i in range(BOYUT - N + 1):
    for j in range(BOYUT - M + 1):
        levha = np.zeros((BOYUT, BOYUT), dtype=int)
        levha[i:i+N, j:j+M] = saf_sablon
        kombinasyonlar.append(levha.flatten())

with open(dosya_yolu, 'a') as f:
    for satir in kombinasyonlar:
        metin = " ".join(map(str, satir))
        f.write(metin + "\n")

print("\n" + "="*50)
print(f"İŞLEM BAŞARILI!")
print(f"Şekil '{dosya_yolu}' dosyasına eklendi.")
print(f"Üretilen ve kaydedilen toplam varyasyon (kayma olasılığı): {len(kombinasyonlar)}")
