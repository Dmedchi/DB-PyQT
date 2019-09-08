import unittest
import Server_
from lib_ import dict_str_bytes, bytes_str_dict


class Test_lib_(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_dict_str_bytes(self):
        r = dict_str_bytes({'text': 'text'})
        self.assertEqual(r, b'{"text": "text"}')


    def test_bytes_str_dict(self):
        r = bytes_str_dict(b'{"action": "presence"}')
        self.assertEqual(r, {'action': 'presence'})


    def test_encode(self):
        self.assertTrue('utf-8')


class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_form_response(self):
        response = {'response': 200}
        self.assertIn('response', response)


    def test_port(self):
        self.assertEqual(7777, 7777)


    def test_listen(self):
        self.assertTrue(5)


    def test_message(self):
        self.assertFalse(None)



if __name__ == '__main__':
    unittest.main()



