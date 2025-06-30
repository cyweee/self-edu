import unittest
import os
from app.database.path import get_db_path

class DatabasePathTest(unittest.TestCase):
    def test_db_path_exists_after_call(self):
        db_path = get_db_path()
        # Проверяем, что путь к базе не пустой строкой
        self.assertTrue(isinstance(db_path, str))
        self.assertNotEqual(db_path, "")

        # Проверяем, что директория для базы действительно существует
        dir_path = os.path.dirname(db_path)
        self.assertTrue(os.path.exists(dir_path))
        self.assertTrue(os.path.isdir(dir_path))

        # Проверяем, что файл не обязательно существует (может быть создан позже)
        # Но если он есть — проверим, что это файл
        if os.path.exists(db_path):
            self.assertTrue(os.path.isfile(db_path))

if __name__ == '__main__':
    unittest.main()
