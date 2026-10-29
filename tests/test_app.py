"""Contracts for the standalone, synthetic demo application."""
import importlib.util
import unittest


class ApplicationTests(unittest.TestCase):
    def test_home_identifies_its_source_and_demo_data(self):
        self.assertIsNotNone(importlib.util.find_spec("app"), "The demo app is not implemented")
        from app import app
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Demo Metrics", response.data)
        self.assertIn(b"metrics", response.data)
        self.assertIn(b"fictives", response.data)

    def test_health_exposes_only_demo_identity(self):
        from app import app
        response = app.test_client().get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok", "source": "metrics", "version": "1.0.1", "synthetic": True})

    def test_assets_and_health_links_follow_the_wsgi_mount(self):
        from app import app
        prefix = "/example/demo/test"
        client = app.test_client()
        response = client.get("/", environ_overrides={"SCRIPT_NAME": prefix})
        self.assertEqual(response.status_code, 200)
        self.assertIn((prefix + "/static/style.css").encode(), response.data)
        self.assertIn((prefix + "/healthz").encode(), response.data)
        with client.get("/static/style.css") as css:
            self.assertEqual(css.status_code, 200)

    def test_favicon_does_not_escape_the_application_mount(self):
        from app import app
        response = app.test_client().get("/")
        self.assertIn(b'<link rel="icon" href="data:image/svg+xml;base64,', response.data)

    def test_no_write_endpoint_is_exposed(self):
        from app import app
        client = app.test_client()
        self.assertEqual(client.post("/").status_code, 405)
        self.assertEqual(client.get("/missing").status_code, 404)


if __name__ == "__main__":
    unittest.main()
