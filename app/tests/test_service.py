from unittest.mock import Mock

from coin_bot.Coin_bot.app.service import is_add_category_command, is_add_subcategory_command, \
    is_show_categories_command, is_delete_subcategory_command, is_show_statistic_command, is_delete_category_command, \
    is_draw_pipe_command

import unittest


class TestIsAddCategoryCommand(unittest.TestCase):
    def test_valid_input(self):
        message = Mock()
        message.text = 'Add category food as spends'
        self.assertTrue(is_add_category_command(message))

    def test_invalid_input(self):
        message = Mock()
        message.text = 'add category food as budget'
        self.assertFalse(is_add_category_command(message))

    def test_invalid_input_not_enough_args(self):
        message = Mock()
        message.text = 'add category food'
        self.assertFalse(is_add_category_command(message))

    def test_invalid_input_not_alpha(self):
        message = Mock()
        message.text = 'add category 123 as incomes'
        self.assertFalse(is_add_category_command(message))


class TestIsAddSubcategoryCommand(unittest.TestCase):

    def test_valid_input(self):
        message = Mock()
        message.text = 'add subcategory fastfood in food'
        self.assertTrue(is_add_subcategory_command(message))

    def test_invalid_input(self):
        message = Mock()
        message.text = 'add subcategoryfood in food'
        self.assertFalse(is_add_subcategory_command(message))

    def test_invalid_input2(self):
        message = Mock()
        message.text = 'food'
        self.assertFalse(is_add_subcategory_command(message))

    def test_invalid_input_not_enough_args(self):
        message = Mock()
        message.text = 'add subcategory fastfood in food taste'
        self.assertFalse(is_add_subcategory_command(message))

    def test_valid_different_letter_size(self):
        message = Mock()
        message.text = 'Add SubcatEgory fasTfood In food'
        self.assertTrue(is_add_subcategory_command(message))


class TestIsShowCategoriesCommand(unittest.TestCase):

    def test_valid_input(self):
        message = Mock()
        message.text = 'show subcategories'
        self.assertTrue(is_show_categories_command(message))

    def test_valid_input2(self):
        message = Mock()
        message.text = 'show categories'
        self.assertTrue(is_show_categories_command(message))

    def test_invalid_input_not_enough_args(self):
        message = Mock()
        message.text = 'show'
        self.assertFalse(is_show_categories_command(message))

    def test_valid_different_letter_size(self):
        message = Mock()
        message.text = 'ShOw cAteGories'
        self.assertTrue(is_show_categories_command(message))


class TestIsDeleteCategoryCommand(unittest.TestCase):
    def test_valid_input(self):
        message = Mock()
        message.text = 'delete categroy one'
        self.assertTrue(is_delete_category_command(message))

    def test_valid_input2(self):
        message = Mock()
        message.text = 'delete category two'
        self.assertTrue(is_delete_category_command(message))

    def test_invalid_input_not_enough_args(self):
        message = Mock()
        message.text = 'delete'
        self.assertFalse(is_delete_category_command(message))

    def test_valid_different_letter_size(self):
        message = Mock()
        message.text = 'DElete caTegory 2314 '
        self.assertTrue(is_delete_category_command(message))


class TestIsShowStatisticCommand(unittest.TestCase):

    def test_valid_input(self):
        message = Mock()
        message.text = 'show statistic for 7 days'
        self.assertTrue(is_show_statistic_command(message))

    def test_valid_input2(self):
        message = Mock()
        message.text = 'show statistic for 7 days in products'
        self.assertTrue(is_show_statistic_command(message))

    def test_invalid_input_not_enough_args(self):
        message = Mock()
        message.text = 'show'
        self.assertFalse(is_show_statistic_command(message))

    def test_valid_different_letter_size(self):
        message = Mock()
        message.text = 'ShOw staTistic for 1 day '
        self.assertTrue(is_show_statistic_command(message))


class TestIsDrawPipeCommand(unittest.TestCase):

    def test_valid_input(self):
        message = Mock()
        message.text = 'Draw pipe in products for 7 days'
        self.assertTrue(is_draw_pipe_command(message))

    def test_valid_input2(self):
        message = Mock()
        message.text = 'Draw piPe in produCts for 732 day'
        self.assertTrue(is_draw_pipe_command(message))

    def test_invalid_input_not_enough_args(self):
        message = Mock()
        message.text = 'piPe'
        self.assertFalse(is_draw_pipe_command(message))

    def test_valid_different_letter_size(self):
        message = Mock()
        message.text = 'Draw piPe in produCts for 732     day'
        self.assertTrue(is_draw_pipe_command(message))