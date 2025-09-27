import cv2
import mediapipe as mp
import time
from gtts import gTTS
from playsound import playsound
import threading
import tempfile
import os

# ----- Pengaturan -----
TTS_TEXT = "Perkenalkan, nama saya Gundo"
COOLDOWN_SECONDS = 5.0  # jeda antar deteksi suara agar tidak spam
CAMERA_ID = 0           # ganti jika perlu (0,1,...)

# ----- Inisialisasi MediaPipe -----
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5
)

# ----- Fungsi TTS + pemutar (jalan di thread supaya tidak block) -----
def play_tts(text):
    try:
        # buat file mp3 sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
            tmp_path = tf.name
        tts = gTTS(text, lang="id")  # bahasa Indonesia
        tts.save(tmp_path)
        # putar audio (blocking di thread ini saja)
        playsound(tmp_path)
    except Exception as e:
        print("Error play_tts:", e)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

# ----- Utility: cek jari terangkat -----
# Landmark index:
# 4: thumb_tip, 8: index_tip, 12: middle_tip, 16: ring_tip, 20: pinky_tip
# Untuk menentukan "up" vs "down" kita bandingkan y tip dengan y pip (pakaian 6,10,14,18)
TIP_IDS = [4, 8, 12, 16, 20]
PIP_IDS = [3, 6, 10, 14, 18]  # pip untuk thumb gunakan 3 sebagai pendekatan

def fingers_status(hand_landmarks):
    """
    Mengembalikan list boolean panjang 5: True = finger up, False = down.
    Asumsi kamera upright, koordinat y lebih kecil = lebih atas di gambar.
    """
    status = []
    lm = hand_landmarks.landmark
    # Thumb: periksa perbandingan x relatif (karena thumb bergerak lateral)
    # Jika tangan kanan, thumb tip x > ip x => terbuka. Namun ini sederhana — kita abaikan thumb detail.
    # Untuk aplikasi satu jari (index) kita fokus ke index, middle, ring, pinky.
    # Thumb: gunakan perbandingan x relatif ke pip untuk mencoba mendeteksi
    try:
        # thumb
        status.append(lm[TIP_IDS[0]].x > lm[PIP_IDS[0]].x)  # simple heuristic
    except:
        status.append(False)

    # index .. pinky berdasarkan y (tip lebih atas dari pip => up)
    for i in range(1,5):
        try:
            tip_y = lm[TIP_IDS[i]].y
            pip_y = lm[PIP_IDS[i]].y
            status.append(tip_y < pip_y)
        except:
            status.append(False)
    return status  # [thumb, index, middle, ring, pinky]

# ----- Main loop kamera -----
cap = cv2.VideoCapture(CAMERA_ID)
if not cap.isOpened():
    print("Gagal membuka kamera. Pastikan camera id benar dan tidak sedang dipakai.")
    exit(1)

last_tts_time = 0

print("Tekan 'q' untuk keluar.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Tidak dapat membaca frame dari kamera.")
        break

    # Flip horizontally untuk efek mirror (opsional)
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert BGR ke RGB untuk mediapipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    detected_one_finger = False

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # gambar landmark
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # cek status jari
            status = fingers_status(hand_landmarks)
            thumb_up, index_up, middle_up, ring_up, pinky_up = status

            # Kita definisikan "salam 1 jari" sebagai: index up, dan middle/ring/pinky down
            if index_up and (not middle_up) and (not ring_up) and (not pinky_up):
                detected_one_finger = True
                # beri label di frame
                cx = int(hand_landmarks.landmark[8].x * w)
                cy = int(hand_landmarks.landmark[8].y * h)
                cv2.putText(frame, "Salam 1 jari terdeteksi", (cx - 100, cy - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2, cv2.LINE_AA)

    # jika terdeteksi, dan cooldown sudah lewat -> mainkan TTS
    now = time.time()
    if detected_one_finger and (now - last_tts_time) > COOLDOWN_SECONDS:
        last_tts_time = now
        # jalankan tts di thread supaya tidak memblok loop utama
        threading.Thread(target=play_tts, args=(TTS_TEXT,), daemon=True).start()

    # tampilkan info cooldown
    cooldown_remaining = max(0, COOLDOWN_SECONDS - (now - last_tts_time))
    cv2.putText(frame, f"Cooldown: {cooldown_remaining:.1f}s", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 2, cv2.LINE_AA)

    cv2.imshow("Camera - Salam 1 Jari Detector", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
