import unittest
from main import NotBash

class TestNotBash(unittest.TestCase):
    def setUp(self):
        self.not_bash = NotBash()

    # --- Тесты для команды ls ---
    
    def test_ls_normal(self):
        """Тест команды ls в нормальных условиях"""
        result = self.not_bash._ls()
        self.assertIn("home", result)
        self.assertIn("etc", result)

    def test_ls_empty(self):
        """Тест команды ls на пустой директории"""
        self.not_bash._cd("empty")
        result = self.not_bash._ls()
        self.assertEqual("", result)

    def test_ls_wich_pash(self):
        """Тест команды ls с указанием пути"""
        result = self.not_bash._ls("home/user")
        self.assertIn("file.txt", result)
        self.assertIn("file2.txt", result)

    # --- Тесты для команды cd ---

    def test_cd_valid(self):
        """Тест команды cd с корректным переходом в директорию"""
        self.not_bash._cd("empty")
        self.assertEqual(self.not_bash.path, "./file_system/empty/")

    def test_cd_invalid(self):
        """Тест команды cd с несуществующей директорией"""
        result = self.not_bash._cd("invalid_dir")
        self.assertEqual(result, "No such directory")

    def test_cd_to_root(self):
        """Тест команды cd с переходом в корень"""
        self.not_bash.path = "./file_system/home/user/"
        self.not_bash._cd("/")
        self.assertEqual(self.not_bash.path, "./file_system/")

    # --- Тесты для команды tail ---

    def test_tail_normal(self):
        """Тест команды tail без параметров"""
        self.not_bash._cd("/home/user")
        result = self.not_bash._tail("file.txt")
        self.assertEqual(result, "Строка 1\nСтрока 2\nСтрока 3")

    def test_tail_params(self):
        """Тест команды tail с параметрами"""
        result = self.not_bash._tail("home/user/file.txt")
        self.assertEqual(result, "Строка 1\nСтрока 2\nСтрока 3")

    def test_tail_invalid(self):
        """Тест команды tail с несуществующим файлом"""
        result = self.not_bash._tail("invalid_file")
        self.assertEqual(result, "No such file")

    # --- Тесты для команды du ---

    def test_du_normal(self):
        """Тест команды du без параметров"""
        result = self.not_bash._du("")
        self.assertEqual(
            "373\t/etc/passwd\n44\t/home/user/file.txt\n22\t/home/user/file2.txt\nTotal size: 439 bytes", 
            result)
        
    def test_du_params(self):
        """Тест команды du с параметрами"""
        result = self.not_bash._du("home/user")
        self.assertEqual("44\t/home/user/file.txt\n22\t/home/user/file2.txt\nTotal size: 66 bytes", result)

    def test_du_empty(self):
        """Тест команды du на пустой директории"""
        self.not_bash._cd("empty")
        result = self.not_bash._du("")
        self.assertEqual("Total size: 0 bytes", result)

    # --- Тесты для других методов ---

    def test_get_path_relative(self):
        """Тест метода get_path с относительным путем"""
        self.not_bash._cd("empty")
        result = self.not_bash.get_path("../home/user")
        self.assertEqual(result, "./file_system/home/user/")

    def test_get_path_absolute(self):
        """Тест метода get_path с абсолютным путем"""
        self.not_bash._cd("empty")
        result = self.not_bash.get_path("/home/user")
        self.assertEqual(result, "./file_system/home/user/")

if __name__ == "__main__":
    unittest.main()