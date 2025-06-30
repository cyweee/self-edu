import unittest
from app.logic.todo import add_task, get_all_tasks, delete_task
from app.database.connection import get_connection

class TestDatabasePersistence(unittest.TestCase):

    def test_task_persistence(self):
        # Добавляем тестовую задачу
        task_text = "Тестовая задача для проверки"
        task_id = add_task(task_text)

        # Читаем все задачи
        tasks = get_all_tasks()
        found = any(t['id'] == task_id and t['task'] == task_text for t in tasks)
        self.assertTrue(found, "Задача не найдена после добавления")

        # Удаляем тестовую задачу
        delete_task(task_id)

        # Проверяем, что задача удалена
        tasks_after = get_all_tasks()
        found_after = any(t['id'] == task_id for t in tasks_after)
        self.assertFalse(found_after, "Задача не удалена")

if __name__ == '__main__':
    unittest.main()
