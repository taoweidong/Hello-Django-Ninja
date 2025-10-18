from datetime import datetime

from django.test import SimpleTestCase

from app.api.schemas import ApiResponse
from app.common.api_response import success, error, not_found, unauthorized, forbidden


class TestApiResponse(SimpleTestCase):
    def test_success_response(self):
        """测试成功响应功能"""
        # 测试带数据的成功响应
        data = {"test": "data"}
        result = success(data=data, message="Success", code=200)

        self.assertIsInstance(result, ApiResponse)
        self.assertEqual(result.code, 200)
        self.assertEqual(result.message, "Success")
        self.assertEqual(result.data, data)
        self.assertIsInstance(result.timestamp, datetime)

        # 测试不带数据的成功响应
        result_no_data = success()
        self.assertIsNone(result_no_data.data)

    def test_error_response(self):
        """测试错误响应功能"""
        result = error(message="Error", code=400, data={"error": "details"})

        self.assertIsInstance(result, ApiResponse)
        self.assertEqual(result.code, 400)
        self.assertEqual(result.message, "Error")
        self.assertEqual(result.data, {"error": "details"})
        self.assertIsInstance(result.timestamp, datetime)

    def test_not_found_response(self):
        """测试未找到响应功能"""
        result = not_found(message="Not Found", code=404)

        self.assertIsInstance(result, ApiResponse)
        self.assertEqual(result.code, 404)
        self.assertEqual(result.message, "Not Found")
        self.assertIsNone(result.data)
        self.assertIsInstance(result.timestamp, datetime)

    def test_unauthorized_response(self):
        """测试未授权响应功能"""
        result = unauthorized(message="Unauthorized", code=401)

        self.assertIsInstance(result, ApiResponse)
        self.assertEqual(result.code, 401)
        self.assertEqual(result.message, "Unauthorized")
        self.assertIsNone(result.data)
        self.assertIsInstance(result.timestamp, datetime)

    def test_forbidden_response(self):
        """测试禁止访问响应功能"""
        result = forbidden(message="Forbidden", code=403)

        self.assertIsInstance(result, ApiResponse)
        self.assertEqual(result.code, 403)
        self.assertEqual(result.message, "Forbidden")
        self.assertIsNone(result.data)
        self.assertIsInstance(result.timestamp, datetime)
