"""Health Endpoint 的基础回归测试。"""

from unittest import IsolatedAsyncioTestCase

from app.main import ServiceStatus, app, get_health


class HealthEndpointTest(IsolatedAsyncioTestCase):
    """验证 Health 路由函数和注册契约。"""

    async def test_get_health_returns_service_status(self) -> None:
        service_status = await get_health()

        self.assertIsInstance(service_status, ServiceStatus)
        self.assertEqual(service_status.name, "Jack AI Studio API")
        self.assertEqual(service_status.status, "foundation ready")
        self.assertGreaterEqual(len(service_status.planned_capabilities), 1)

    def test_get_health_route_is_registered(self) -> None:
        health_routes = [
            route
            for route in app.routes
            if getattr(route, "path", None) == "/health"
        ]

        self.assertEqual(len(health_routes), 1)
        self.assertIn("GET", health_routes[0].methods or set())
        self.assertIs(health_routes[0].response_model, ServiceStatus)
