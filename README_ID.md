
# 🕹️ Game 3D Menyeberang Jalan dengan Kontrol Gestur Tangan

Sebuah game 3D sederhana ala **Frogger**, tapi dengan tampilan **side-scrolling** dan kontrol unik lewat **gestur tangan** menggunakan **OpenCV** dan **MediaPipe**. Dibuat menggunakan [Ursina Engine](https://www.ursinaengine.org/).

---

## 🎮 Fitur-Fitur

- Jalan 3D dengan mobil-mobil yang datang dari kejauhan
- Kamera mengikuti karakter dari samping
- Karakter bisa dikendalikan dengan gestur tangan lewat webcam:
  - 👉 Tunjuk kanan → Jalan maju
  - 👈 Tunjuk kiri → Jalan mundur
  - ✋ Telapak tangan terbuka → Berhenti
- Versi game alternatif dengan kontrol keyboard biasa
- Tes deteksi gestur secara real-time

---

## 📁 Struktur Proyek

| File                   | Fungsi                                             |
|------------------------|----------------------------------------------------|
| `game.py`              | Game utama dengan kontrol gestur                  |
| `test_game.py`         | Versi game tanpa gestur, pakai keyboard saja      |
| `gesture_worker.py`    | Proses pendeteksi gestur berbasis webcam          |
| `test_recogniser.py`   | Menjalankan tes kamera dan deteksi gestur langsung|
| `gestures/recogniser.py` | Logika utama pengenalan gestur pakai MediaPipe |
| `requirements.txt`     | Semua dependensi Python yang dibutuhkan           |

---

## 🚀 Cara Menjalankan Game

### 1. Install Python

Pastikan kamu sudah menginstall **Python 3.8–3.11**.  
Kalau belum, bisa unduh di: https://www.python.org/downloads/

### 2. Clone Repositori Ini

```bash
git clone https://github.com/nama-kamu/nama-repo.git
cd nama-repo
```

### 3. Install Semua Dependensi

```bash
pip install -r requirements.txt
```

> Ini akan meng-install `ursina`, `opencv-python`, `mediapipe`, `pyautogui`, dll.

---

## 🎮 Menjalankan Game

### 🖐️ Mode Gestur (kontrol tangan via webcam)

```bash
python game.py
```

- Pastikan webcam aktif dan ruangan cukup terang
- Arahkan tangan ke kamera untuk mulai menggerakkan karakter

### ⌨️ Mode Keyboard (tanpa webcam)

```bash
python test_game.py
```

Gunakan tombol:
- `W` → Maju
- `S` → Mundur
- `A` → Pindah kiri
- `D` → Pindah kanan

### 👀 Tes Pendeteksi Gestur

```bash
python test_recogniser.py
```

- Akan membuka jendela webcam dan menampilkan gestur yang terdeteksi secara real-time

---

## ✋ Daftar Gestur

| Gestur             | Fungsi                        |
|--------------------|-------------------------------|
| 👉 Tunjuk ke kanan | Jalan maju ke kanan           |
| 👈 Tunjuk ke kiri  | Jalan mundur ke kiri          |
| ✋ Telapak terbuka | Berhenti (tidak bergerak)     |

---

## 💻 Kompatibilitas Platform

- ✅ Windows
- ✅ Linux
- ✅ macOS *(MediaPipe butuh penyesuaian lebih lanjut)*

---

## ⚙️ Syarat & Tips

- Butuh webcam yang aktif
- Pastikan tangan terlihat jelas di kamera
- Usahakan pencahayaan cukup agar deteksi lebih akurat

---

## 📄 Lisensi

Proyek ini menggunakan lisensi **MIT**.  
Bebas digunakan, dimodifikasi, dan dibagikan.
