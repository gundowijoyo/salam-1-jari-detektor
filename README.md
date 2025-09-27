# Salam 1 Jari Detektor 🤚🔊

Deteksi gestur tangan "salam 1 jari" (telunjuk terangkat) secara real-time menggunakan kamera, dan perkenalkan diri dengan suara Google TTS.

## 🎯 Fitur

- Deteksi tangan dan posisi jari menggunakan MediaPipe
- Deteksi gestur: **hanya telunjuk yang terangkat**
- Jika terdeteksi, program akan mengucapkan:
  > "Perkenalkan, nama saya Gundo"
- Cooldown agar suara tidak diulang terus-menerus
- Tampilan kamera real-time dengan OpenCV

## 🛠️ Instalasi

1. **Clone repository ini**

```bash
git clone https://github.com/gundowijoyo/salam-1-jari-detektor.git
cd salam-1-jari-detektor
````

2. **Install dependencies**

Disarankan pakai virtual environment (opsional):

```bash
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate di Windows
```

Install semua dependensi:

```bash
pip install -r requirements.txt
```

## ▶️ Menjalankan Program

Jalankan script utama:

```bash
python hand_one_finger_tts.py
```

* Kamera akan terbuka
* Arahkan tangan ke kamera dan tunjukkan **satu jari telunjuk**
* Jika terdeteksi, akan terdengar suara:

  > "Perkenalkan, nama saya Gundo"

Tekan **`q`** di jendela kamera untuk keluar.

## 📦 File & Struktur

```
salam-1-jari-detektor/
├── hand_one_finger_tts.py   # Script utama
├── requirements.txt         # Daftar dependensi
└── README.md                # Dokumentasi
```

## 📋 Ketergantungan

* Python 3.7 - 3.10
* OpenCV
* MediaPipe
* gTTS (Google Text-to-Speech)
* playsound (untuk memutar suara .mp3)

## ⚠️ Catatan

* Suara diputar melalui `playsound`. Jika tidak terdengar:

  * Pastikan volume aktif
  * Coba jalankan sebagai administrator (di Windows)
  * Atau ganti pemutar suara (hubungi saya untuk bantuannya)

## 📸 Screenshot

> (Tambahkan screenshot jika ingin, contoh gestur atau tampilan kamera)

## 🧠 Ide Pengembangan Lanjut

* Tambah lebih banyak gestur (contoh: salam dua jari)
* Gunakan model klasifikasi gestur lebih kompleks
* Integrasi dengan chatbot, animasi, atau kontrol robot

## 🙌 Kredit

Proyek oleh [Gundo Wijoyo]
Menggunakan MediaPipe oleh Google, gTTS, dan OpenCV

"Salam 1 jari, salam perkenalan!"
"Kalo ada error inpo-inpo"

MIT License bebas kalian gunakan :)
