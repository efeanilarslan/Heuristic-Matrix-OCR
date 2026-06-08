import numpy as np
import matplotlib.pyplot as plt
import pygame
import sys
import glob

dosya_listesi = glob.glob("data/*.txt")
if not dosya_listesi:
    print("Hata: Bulunulan klasörde hiç .txt dosyası bulunamadı!")
    sys.exit()
sablonlar = {}
boyut = None
print(f"Sistemde tespit edilen dosyalar: {dosya_listesi}")
for dosya in dosya_listesi:
    print(f"\n{dosya}")
    toplam_matris = None
    with open(dosya, 'r') as f:
        for satir in f:
            veri_matrisi = np.array([int(x) for x in satir.split()])
            if toplam_matris is None:
                toplam_matris = veri_matrisi
            else:
                if len(veri_matrisi) == len(toplam_matris):
                    toplam_matris += veri_matrisi
    toplam_matris = toplam_matris - np.min(toplam_matris)
    temiz_toplam_matris = toplam_matris.copy().astype(float)
    it = np.nditer(temiz_toplam_matris, op_flags=['readwrite'])
    for f_val in it:
        if f_val == 0:
            f_val[...] = -50
        elif 1 <= f_val <= 4:
            f_val[...] = -24 * (1 / f_val)
    eleman_sayisi = len(temiz_toplam_matris)
    boyut = int(np.sqrt(eleman_sayisi))
    sablonlar[dosya] = temiz_toplam_matris
    hafiza_resmi = temiz_toplam_matris.reshape((boyut, boyut))
    plt.figure(figsize=(6, 6))
    plt.title(f"Şablon Isı Haritası: {dosya} ({boyut}x{boyut})")
    plt.imshow(hafiza_resmi, cmap='hot')
    plt.colorbar(label='Piksel Ağırlık Puanı')
    plt.show()

    print(f"[{dosya} SKOR ANALİZİ]")
    with open(dosya, 'r') as f:
        satir_no = 1
        for satir in f:
            elemanlar = satir.split()
            if not elemanlar: continue
            try:
                sinav_matrisi = np.array([int(x) for x in elemanlar])
                if len(sinav_matrisi) == eleman_sayisi:
                    skor = np.sum(sinav_matrisi * temiz_toplam_matris)
                    print(f"Örnek {satir_no} Skoru: {skor}")
                    satir_no += 1
            except ValueError:
                continue
if not sablonlar:
    print("Geçerli hiçbir şablon oluşturulamadı. Program sonlandırılıyor.")
    sys.exit()
cizim_alani = np.zeros((boyut, boyut), dtype=int)
HÜCRE_BOYUTU = 35
PENCERE_BOYUTU = boyut * HÜCRE_BOYUTU
pygame.init()
pencere = pygame.display.set_mode((PENCERE_BOYUTU, PENCERE_BOYUTU + 40))
pygame.display.set_caption(f"Karakter Çizim Paneli ({boyut}x{boyut})")
font = pygame.font.SysFont("Arial", 14, bold=True)
calisiyor = True
while calisiyor:
    for r in range(boyut):
        for c in range(boyut):
            if cizim_alani[r, c] == 1 :
                renk = (0, 100, 200)
            else:
                renk = (255, 255, 255)
            pygame.draw.rect(pencere, renk, (c * HÜCRE_BOYUTU, r * HÜCRE_BOYUTU, HÜCRE_BOYUTU - 1, HÜCRE_BOYUTU - 1))
    buton_alani = pygame.Rect(10, PENCERE_BOYUTU + 5, PENCERE_BOYUTU - 20, 30)
    pygame.draw.rect(pencere, (34, 139, 34), buton_alani)
    yazi = font.render("MATRİSİ GÖNDER", True, (255, 255, 255))
    pencere.blit(yazi, (PENCERE_BOYUTU // 2 - yazi.get_width() // 2, PENCERE_BOYUTU + 12))
    pygame.display.flip()

    for olay in pygame.get_event_loop() if hasattr(pygame, 'get_event_loop') else pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False
            pygame.quit()
            sys.exit()
        elif olay.type == pygame.MOUSEBUTTONDOWN or (olay.type == pygame.MOUSEMOTION and olay.buttons[0]):
            f_x, f_y = pygame.mouse.get_pos()
            if f_y < PENCERE_BOYUTU:
                c = f_x // HÜCRE_BOYUTU
                r = f_y // HÜCRE_BOYUTU
                if olay.type == pygame.MOUSEBUTTONDOWN:
                    cizim_alani[r, c] = 1 - cizim_alani[r, c]
                else:
                    cizim_alani[r, c] = 1
            elif buton_alani.collidepoint(f_x, f_y) and olay.type == pygame.MOUSEBUTTONDOWN:
                calisiyor = False
pygame.quit()
test_matrisi = cizim_alani.flatten()
print(f"\n[NİHAİ ANALİZ SONUÇLARI]")
#sözlükte tuttuğumuz her dosya ismi ve onun şablonu için kıyaslama yapıyoruz
for dosya_ismi, sablon_matrisi in sablonlar.items():
    yeni_skor = np.sum(test_matrisi * sablon_matrisi)
    print(f"Çizdilen matrisin {dosya_ismi} şablonuna göre benzerlik skoru: {yeni_skor}")