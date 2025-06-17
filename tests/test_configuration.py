import sys  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402

from modules.configuration import Configuration  # noqa: E402


def test_multiple_writes_preserve_configuration(tmp_path):
    config_file = tmp_path / "config.json"
    cfg = Configuration(config_file)
    cfg.write(["section", "item1"], 1)
    cfg.write(["section", "item2"], 2)
    assert cfg.config == {"section": {"item1": 1, "item2": 2}}
    assert cfg.read(["section", "item1"]) == 1
    assert cfg.read(["section", "item2"]) == 2


def test_write_with_mixed_keys(tmp_path):
    config_file = tmp_path / "config.json"
    cfg = Configuration(config_file)
    cfg.write("root", "value")
    cfg.write(["nested", "key"], "value2")
    assert cfg.config == {"root": "value", "nested": {"key": "value2"}}
    assert cfg.read(["nested", "key"]) == "value2"
