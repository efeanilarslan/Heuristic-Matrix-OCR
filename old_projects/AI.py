import numpy as np
toplam_matris = None
#matrisler.txt deki matris satırları toplanır, aynı dizinde olması önemlidir!
with open('matrisler.txt', 'r') as f:
    for satir in f:
        veri_matrisi = np.array([int(x) for x in satir.split()])
        if toplam_matris is None:
            toplam_matris = veri_matrisi
        else:
            toplam_matris += veri_matrisi
#sıfıra kaydırma yapılır, matristeki en düşük sayı sıfıra gelene kadar sayılar küçülür
temiz_toplam_matris = toplam_matris - np.min(toplam_matris)
print(temiz_toplam_matris)
with open('matrisler.txt', 'r') as f:
    satir_no = 1
    for satir in f:
        sinav_matrisi = np.array([int(x) for x in satir.split()])
        skor = np.sum(sinav_matrisi * temiz_toplam_matris)
        print(f"Örnek {satir_no} Skoru: {skor}")
        satir_no += 1
#matrisler.txt dosyasındaki matrisleri, temiz_toplam_matris ile çarparak her birinin skoru hesaplanır
kullanici_girdisi = input(f"Aralarinda boşluk birakarak matris girin:\n")
try:
    test_matrisi = np.array([int(x) for x in kullanici_girdisi.split()])
    if len(test_matrisi) != len(temiz_toplam_matris):
        print(f"Hata: Tam olarak {len(temiz_toplam_matris)} adet değer girmelisiniz!")
    else:
        yeni_skor = np.sum(test_matrisi * temiz_toplam_matris)
        print(f"Girdiğiniz matrisin skoru: {yeni_skor}")
except ValueError:
    print("Hata: Sadece sayı (0 veya 1) girmelisiniz!")