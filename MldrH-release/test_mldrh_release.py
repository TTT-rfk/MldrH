import importlib.util
import sys
from pathlib import Path

from prompt_toolkit.keys import Keys


MODULE_PATH = Path(__file__).with_name("MldrH.py")
SPEC = importlib.util.spec_from_file_location("mldrh_release", MODULE_PATH)
mldrh = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mldrh
SPEC.loader.exec_module(mldrh)


def test_parse_command_supports_advertised_suggest_and_top_controls():
    assert mldrh.parse_command("/suggest") == ("suggest", "")
    assert mldrh.parse_command("/top 12") == ("top", 12)
    assert mldrh.parse_command("/top 0") == ("error", "Use /top N where N is an integer from 1 to 32.")


def test_input_session_binds_clear_and_think_shortcuts(monkeypatch):
    captured = {}

    def prompt_session(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(mldrh, "PromptSession", prompt_session)
    mldrh.create_input_session()

    assert captured["key_bindings"].get_bindings_for_keys((Keys.ControlL,))
    assert captured["key_bindings"].get_bindings_for_keys((Keys.ControlT,))


def test_relative_config_paths_resolve_from_release_root(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        '{"embedding_base_model":"assets\\\\BAAI-bge-m3","generation_base_model":"assets\\\\Qwen2.5-3B-Instruct","retrieval_adapter":"adapters\\\\Mdlr-theory-embed-v1","think_adapter":"adapters\\\\Mdlr1.1-think","database_path":"knowledge_db_theory_v1"}',
        encoding="utf-8",
    )
    monkeypatch.setattr(mldrh, "ROOT", tmp_path)
    monkeypatch.setattr(mldrh, "CONFIG_PATH", config_path)

    paths = mldrh.asset_paths(mldrh.config())

    assert paths["generation_base_model"] == tmp_path / "assets" / "Qwen2.5-3B-Instruct"
    assert paths["database_path"] == tmp_path / "knowledge_db_theory_v1"
