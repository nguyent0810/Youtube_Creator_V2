"""Đường dẫn công cụ ngoài repo: một chỗ (factory/paths.py), ghi đè được bằng biến môi trường."""
import importlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_environment_overrides_every_tool_path(monkeypatch, tmp_path):
    from factory import paths
    for k in ("YF_CREDS_DIR", "YF_PY_TTS", "YF_PY_VID", "YF_FFMPEG_DIR"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("YF_TOOLS_DIR", str(tmp_path))
    try:
        importlib.reload(paths)
        assert paths.CREDS_DIR == tmp_path / "vietneu-tts" / ".youtube_channels"
        assert paths.PY_VID == tmp_path / "video-editor" / ".venv-video" / "Scripts" / "python.exe"
        monkeypatch.setenv("YF_FFMPEG_DIR", str(tmp_path / "ff"))
        monkeypatch.setenv("YF_CREDS_DIR", str(tmp_path / "creds"))
        importlib.reload(paths)
        assert paths.FFMPEG.startswith(str(tmp_path / "ff")) and paths.CREDS_DIR == tmp_path / "creds"
    finally:
        monkeypatch.undo()
        importlib.reload(paths)


def test_no_hard_coded_tool_path_outside_the_paths_module():
    """Bản cũ viết cứng C:\\Tools\\... ở sáu file: đổi máy là sửa sáu chỗ."""
    assign = re.compile(r"""=\s*(Path\()?r?["']C:\\""")
    bad = []
    for p in sorted(ROOT.glob("factory/**/*.py")) + sorted(ROOT.glob("scripts/**/*.py")) + sorted(ROOT.glob("motion/**/*.py")):
        if p.name == "paths.py":
            continue
        bad += [f"{p.relative_to(ROOT)}:{i}" for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
                if assign.search(line)]
    assert bad == []
