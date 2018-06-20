import unittest
import base64
import ocr_service as ocr


class TestOcrService(unittest.TestCase):
    def setUp(self):
        pass

    def test_ocr(self):
        INPUT_FILE = 'Data/input/pic/t7.jpg'
        with open(INPUT_FILE, "rb") as image_file:
            encoded_string = base64.b64encode((image_file.read()))
        result = ocr.ocr_jpg(base64.b64decode(encoded_string), 0)
        self.assertIsNotNone(result, "OCR WORKS")


if __name__ == '__main__':
    unittest.main()
