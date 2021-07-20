#!/usr/bin/env python

from relatedness2 import relatedness_test

import unittest

class TestRelatedness(unittest.TestCase):

	def test_function_with_one_family(self):
		result, comment = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXY.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, True)

	def test_ped_with_parent_not_related(self):
		result, comment = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXYFAIL.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_ped_file_is_fail(self):
		result, comment = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXYFAIL.ped', 'testData/210622_A00748_0110_AH5T3CDRXY.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_parents_related(self):
		result, comment = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXYPR.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_function_with_multiple_families(self):
		result, comment = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX.ped', 'testData/201215_A00748_0068_AHT3FCDMXX.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, True)

	def test_either_ped_or_relatedness_file_not_found(self):
		result, comment = relatedness_test('this_file_does_not_exist.ped', 'this_file_also_does_not_exist.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_ped_file_with_incorrect_number_of_columns(self):
		result, comment = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX_INCORRECT_NUMBER_OF_COLUMNS.ped', 'testData/201215_A00748_0068_AHT3FCDMXX.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_relatedness_file_with_incorrect_number_of_columns(self):
		result, comment = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX.ped', 'testData/201215_A00748_0068_AHT3FCDMXX_INCORRECT_NUMBER_OF_COLUMNS.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_tso_no_one_related(self):
		result, comment = relatedness_test('testData/210709_NB551319_0232_AHF2JFBGXJ.ped', 'testData/210709_NB551319_0232_AHF2JFBGXJ.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_tso_no_one_related_unexpected_related(self):

		# relatedness between 18M01316	21M11357 is 0.2
		result, comment = relatedness_test('testData/210709_NB551319_0232_AHF2JFBGXJ.ped', 'testData/210709_NB551319_0232_AHF2JFBGXJ_2.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_big_genome_run(self):

		# Test run with 5 correct trios
		result, comment = relatedness_test('testData/K00150_0149_AHG7YKBBXX.ped', 'testData/K00150_0149_AHG7YKBBXX.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, True)

	def test_duplicate_sample1(self):

		# test correct wings run with same sample repeated

		result, comment = relatedness_test('testData/210604_A00748_0108_AHWVTGDMXX.ped', 'testData/210604_A00748_0108_AHWVTGDMXX.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)

	def test_tso_no_one_related_unexpected_related(self):

		# relatedness a duplicate sample - 18M01316	21M10702
		result, comment = relatedness_test('testData/210709_NB551319_0232_AHF2JFBGXJ.ped', 'testData/210709_NB551319_0232_AHF2JFBGXJ_duplicate.relatedness2', 0.2, 0.3, 0.04)
		self.assertEqual(result, False)




if __name__ == '__main__':
	unittest.main()

