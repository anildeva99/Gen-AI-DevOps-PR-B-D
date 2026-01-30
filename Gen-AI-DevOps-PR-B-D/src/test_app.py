import unittest
from  import handler

class TestHandler(unittest.TestCase):
    def test_create(self):
        event = {"action": "create"}
        result = handler(event, None)
        self.assertEqual(result["status"], "done")

if  == "__main__":
    unittest.main()
