"""Short tự chạy qa_blank + contact sheet sau khi dựng (retro 2 mục 12: trước đây PM soát tay, ảnh X-4 ghi sai nơi chụp lọt
tới bước duyệt). Không chặn: chỉ in cảnh báo."""
import inspect
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "stier"), str(ROOT / "motion"), str(ROOT)]
import build as B  # noqa: E402


def test_build_runs_qa_after_every_final():
    src = inspect.getsource(B.build)
    assert src.index("qa_short(final)") > src.index("mux hỏng")


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="cần ffmpeg trong PATH")
def test_qa_short_reports_blank_and_writes_sheet(tmp_path):
    v = tmp_path / "final.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=216x384:d=2:r=10",
                    "-f", "lavfi", "-i", "testsrc=s=216x384:d=2:r=10", "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]",
                    "-map", "[v]", str(v)], check=True)
    out = B.qa_short(v, ffmpeg="ffmpeg")
    assert out[0].startswith("QA final.mp4: 1 đoạn trống") and "WARNING" in out[0]
    assert (tmp_path / "final_sheet.jpg").exists() and out[-1].startswith("contact sheet:")


def test_qa_short_never_raises(tmp_path):
    out = B.qa_short(tmp_path / "missing.mp4", ffmpeg="ffmpeg-does-not-exist")
    assert all("WARNING" in m for m in out)
