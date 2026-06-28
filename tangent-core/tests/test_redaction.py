import importlib.util
import unittest


def load_engine():
    spec = importlib.util.spec_from_file_location("tangent_core", "tangent-core/tangent_core.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load tangent_core module")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TangentEngine()



class TestRedaction(unittest.TestCase):
    def test_assignment_redaction_no_duplicate_key(self):
        engine = load_engine()
        out, changed = engine.redact_line("SECRET_KEY=my-super-secret-key-123456")
        self.assertTrue(changed)
        self.assertEqual(out, "SECRET_KEY=[REDACTED]")

    def test_home_path_redaction(self):
        engine = load_engine()
        out, changed = engine.redact_line("HOME=/home/raymond")
        self.assertTrue(changed)
        self.assertEqual(out, "HOME=[REDACTED]")


if __name__ == "__main__":
    unittest.main()

