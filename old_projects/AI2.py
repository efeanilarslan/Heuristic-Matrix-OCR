import numpy as np
import matplotlib.pyplot as plt
import pygame
#matrisler.txt aynı dizinde olmalıdır!
toplam_matris = None
with open('matrisler.txt', 'r') as f:
    for satir in f:
        veri_matrisi = np.array([int(x) for x in satir.split()])
        if toplam_matris is None:
            toplam_matris = veri_matrisi
        else:
            toplam_matris += veri_matrisi

temiz_toplam_matris = toplam_matris.copy().astype(float)
it = np.nditer(temiz_toplam_matris, op_flags=['readwrite'])
for f in it:
    if f == 0:
        f[...] = -50
    elif 1 <= f <= 4:
        f[...] = -24 * (1 / f)

eleman_sayisi = len(temiz_toplam_matris)
boyut = int(np.sqrt(eleman_sayisi))
hafiza_resmi = temiz_toplam_matris.reshape((boyut, boyut))
plt.figure(figsize=(6, 6))
plt.title(f"Karakter Şablonu Isı Haritası ({boyut}x{boyut})")
plt.imshow(hafiza_resmi, cmap='hot')
plt.colorbar(label='Piksel Ağırlık Puanı')
plt.show()

with open('matrisler.txt', 'r') as f:
    satir_no = 1
    for satir in f:
        sinav_matrisi = np.array([int(x) for x in satir.split()])
        skor = np.sum(sinav_matrisi * temiz_toplam_matris)
        print(f"Örnek {satir_no} Skoru: {skor}")
        satir_no += 1

cizim_alani = np.zeros((boyut, boyut), dtype=int)
HÜCRE_BOYUTU = 35
PENCERE_BOYUTU = boyut * HÜCRE_BOYUTU
pygame.init()
pencere = pygame.display.set_mode((PENCERE_BOYUTU, PENCERE_BOYUTU + 40))#buton için +40
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
yeni_skor = np.sum(test_matrisi * temiz_toplam_matris)

print(f"\n[ANALİZ SONUCU]")
print(f"Çizdiğiniz matrisin benzerlik skoru: {yeni_skor}")