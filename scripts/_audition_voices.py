"""Nghe thử giọng: cùng một đoạn, nhiều giọng, nối thành một file.

Tôi không nghe được audio nên không thẩm định được giọng nào "ấm" hay "già
dặn". Cách đúng là render cùng một đoạn qua các ứng viên rồi để người nghe
chọn -- mất vài phút, dùng được nhiều năm.

Chọn ứng viên theo đúng mô tả: nam Bắc trầm già dặn, và nữ Nam ấm áp.
Ưu tiên "phong cách kể chuyện" thay vì "tin tức" -- tin tức nhịp nhanh và
phẳng, không hợp nội dung phong thuỷ.
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import speak  # noqa: E402

CANDIDATES = [
    ("Anh Khôi",      "Nam · Bắc · kể chuyện"),
    ("Thiền Tâm Đức", "Nam · Bắc · kể chuyện"),
    ("Thục Đoan",     "Nữ · Nam · kể chuyện"),
    ("Mỹ Duyên",      "Nữ · Nam · đọc truyện"),
]

TEXT = ("Hướng nhà đẹp mà bếp đặt sai thì vẫn chưa ổn. "
        "Người xưa xem bếp là nơi giữ lửa, nên vị trí của nó được coi trọng hơn cả cửa chính.")

out_dir = ROOT / "output" / "_audition"
out_dir.mkdir(parents=True, exist_ok=True)

engine = speak._load_engine()
gap = np.zeros(int(speak.SAMPLE_RATE * 0.8), dtype=np.float32)
pieces = []

for voice, desc in CANDIDATES:
    print(f"  {voice:16s} ({desc})...", flush=True)
    audio = engine.infer(TEXT, voice=voice)
    sf.write(str(out_dir / f"{voice}.wav"), audio, speak.SAMPLE_RATE)
    pieces += [np.asarray(audio, dtype=np.float32), gap]

combined = out_dir / "nghe-thu-4-giong.wav"
sf.write(str(combined), np.concatenate(pieces), speak.SAMPLE_RATE)
print("\nFile nghe lien tiep:", combined)
print("Thu tu:", " -> ".join(v for v, _ in CANDIDATES))
