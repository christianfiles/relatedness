#!/usr/bin/env python

from relatedness2 import relatedness_test

import unittest

class TestRelatedness(unittest.TestCase):

	def test_function_with_one_family(self):
		result = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXY.relatedness2')
		self.assertEqual(result, True)

	def test_ped_with_parent_not_related(self):
		result = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXYFAIL.relatedness2')
		self.assertEqual(result, False)

	def test_ped_file_is_fail(self):
		result = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXYFAIL.ped', 'testData/210622_A00748_0110_AH5T3CDRXY.relatedness2')
		self.assertEqual(result, False)

	def test_parents_related(self):
		result, comment = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXYPR.relatedness2')
		self.assertEqual(result, False)

	def test_function_with_multiple_families(self):
		result = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX.ped', 'testData/201215_A00748_0068_AHT3FCDMXX.relatedness2')
		self.assertEqual(result, True)

	def test_either_ped_or_relatedness_file_not_found(self):
		result, comment = relatedness_test('this_file_does_not_exist.ped', 'this_file_also_does_not_exist.relatedness2')
		self.assertEqual(result, False)

	def test_ped_file_with_incorrect_number_of_columns(self):
		result, comment = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX_INCORRECT_NUMBER_OF_COLUMNS.ped', 'testData/201215_A00748_0068_AHT3FCDMXX.relatedness2')
		self.assertEqual(result, False)

	def test_relatedness_file_with_incorrect_number_of_columns(self):
		result, comment = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX.ped', 'testData/201215_A00748_0068_AHT3FCDMXX_INCORRECT_NUMBER_OF_COLUMNS.relatedness2')
		self.assertEqual(result, False)

if __name__ == '__main__':
	unittest.main()

