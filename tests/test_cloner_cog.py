import os
import sys
import types
import asyncio
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

dummy_main = types.SimpleNamespace(
    name_syntax="%original%",
    clear_guild=True,
    clone_icon=True,
    clone_banner=True,
    clone_roles=True,
    clone_channels=True,
    clone_emojis=True,
    clone_stickers=True,
    clone_messages_enabled=True,
    live_update_enabled=True,
    process_new_messages_enabled=True,
    clone_delay=1.0,
    messages_delay=0.1,
    clone_oldest_first=True,
    messages_limit=1,
    messages_webhook_clear=True,
    logger=types.SimpleNamespace(error=lambda *a, **k: None),
)
sys.modules.setdefault("main", dummy_main)

from cogs.cloner_cog import ClonerCog


class DummyLogger:
    def __init__(self):
        self.messages = []

    def info(self, msg):
        self.messages.append(msg)


class DummyCloner:
    def __init__(self, last_method):
        self.args = {
            "clear_guild": True,
            "clone_icon": True,
            "clone_banner": True,
            "clone_roles": True,
            "clone_channels": True,
            "clone_emojis": True,
            "clone_stickers": True,
            "clone_messages": True,
        }
        self.last_executed_method = last_method
        self.logger = DummyLogger()
        self.executed = []

    async def prepare_server(self):
        self.executed.append("prepare_server")

    async def clone_icon(self):
        self.executed.append("clone_icon")

    async def clone_banner(self):
        self.executed.append("clone_banner")

    async def clone_roles(self):
        self.executed.append("clone_roles")

    async def clone_categories(self):
        self.executed.append("clone_categories")

    async def clone_channels(self):
        self.executed.append("clone_channels")

    async def clone_emojis(self):
        self.executed.append("clone_emojis")

    async def clone_stickers(self):
        self.executed.append("clone_stickers")

    async def clone_messages(self):
        self.executed.append("clone_messages")

    def save_state(self):
        pass

    def load_state(self):
        pass


class DummyCtx:
    def __init__(self):
        self.message = self

    async def delete(self):
        pass


@pytest.mark.asyncio
async def test_process_start_respects_last_method(monkeypatch):
    cog = ClonerCog(bot=None)
    dummy = DummyCloner(last_method="clone_icon")
    cog.cloners.append(dummy)

    import cogs.cloner_cog as cc
    monkeypatch.setattr(cc, "cloner", dummy, raising=False)
    monkeypatch.setattr(cc, "logger", dummy.logger, raising=False)

    ctx = DummyCtx()
    await ClonerCog.process.callback(cog, ctx, args_str="start=true save=false")

    assert "clone_icon" not in dummy.executed
    expected = [
        "prepare_server",
        "clone_banner",
        "clone_roles",
        "clone_categories",
        "clone_channels",
        "clone_emojis",
        "clone_stickers",
        "clone_messages",
    ]
    assert dummy.executed == expected
