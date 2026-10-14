"""Offline regression checks for regional X50 discovery and capability loading."""
import ast
import base64
import copy
import importlib.util
import json
import logging
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from typing import Any
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components/dreame_vacuum"
MARKER = "# BEGIN REGIONAL X50 SUPPORT"


def decode_registry(source, original=None):
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.AnnAssign)
                and isinstance(n.target, ast.Name) and n.target.id == "DEVICE_INFO")
    scope = {"DEVICE_INFO": ast.literal_eval(node.value)}
    if original is not None:
        scope["DEVICE_INFO"] = base64.b64encode(zlib.compress(json.dumps(original).encode())).decode()
    if MARKER in source:
        exec(source[source.index(MARKER):], scope)
    return json.loads(zlib.decompress(base64.b64decode(scope["DEVICE_INFO"]), 47))


def current_registry():
    return decode_registry((COMPONENT / "dreame/const.py").read_text())


def discover(data, model):
    tree = ast.parse((COMPONENT / "dreame/protocol.py").read_text())
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
                  and n.name == "get_supported_devices"
                  and "response['page']['records']" in ast.unparse(n))
    scope = {"Any": Any, "copy": copy, "_LOGGER": logging.getLogger("offline-test")}
    exec(compile(ast.Module(body=[method], type_ignores=[]), "upstream-discovery", "exec"), scope)
    device = {"model": model, "customName": "Test vacuum",
              "deviceInfo": {"displayName": "X50 Ultra Complete"}}
    class Cloud:
        def get_devices(self):
            return {"page": {"records": [device.copy()]}}
    models = {f"dreame.vacuum.{k}": data[0][v][1]
              for k, v in data[3].items() if data[0][v][0] == 0}
    return scope["get_supported_devices"](Cloud(), models)


def load_capability(data, model):
    spec = importlib.util.spec_from_file_location("offline_dreame_types", COMPONENT / "dreame/types.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    class Device:
        info = SimpleNamespace(model=model, version=3684)
        status = SimpleNamespace(current_segments=None, current_map=None, selected_map=None, fill_light=None)
        _map_manager = None
        def get_property(self, prop):
            # No cloud calls: absent properties remain absent rather than fabricating capabilities.
            return None
    capability = module.DreameVacuumDeviceCapability(Device())
    capability.load(data)
    return capability


class RegionalModelTest(unittest.TestCase):
    def test_regional_model_is_discovered_with_its_real_identity(self):
        supported, rejected = discover(current_registry(), "dreame.vacuum.r9446j")
        self.assertEqual(len(supported), 1)
        self.assertEqual(rejected, [])
        self.assertEqual(supported[0]["model"], "dreame.vacuum.r9446j")

    def test_regional_runtime_capabilities_load(self):
        try:
            capability = load_capability(current_registry(), "dreame.vacuum.r9446j")
        except Exception as error:
            self.fail(f"Runtime rejected regional model: {error}")
        self.assertTrue(capability.loaded)
        self.assertTrue(capability.video_dynamic_vendor)
        self.assertTrue(capability.stream_tx)
        self.assertTrue(capability.key)

    def test_existing_model_remains_supported(self):
        supported, rejected = discover(current_registry(), "dreame.vacuum.r9446k")
        self.assertEqual(len(supported), 1)
        self.assertEqual(rejected, [])

    def test_unrelated_unknown_model_stays_rejected(self):
        supported, rejected = discover(current_registry(), "dreame.vacuum.unknown_test")
        self.assertEqual(supported, [])
        self.assertEqual(len(rejected), 1)

    def test_upstream_entries_capabilities_and_keys_are_preserved(self):
        source = subprocess.check_output(["git", "show", "v2.0.2:custom_components/dreame_vacuum/dreame/const.py"], cwd=ROOT, text=True)
        original = decode_registry(source)
        patched = current_registry()
        patched[3].pop("r9446j", None)
        self.assertEqual(patched, original)

    def test_future_native_model_support_is_preserved(self):
        source = (COMPONENT / "dreame/const.py").read_text()
        future = current_registry()
        future[3]["r9446j"] = future[3]["r9446b"]
        self.assertEqual(decode_registry(source, original=future), future)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()
