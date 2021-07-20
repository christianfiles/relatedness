#!/usr/bin/env python

"""
relatedness.py

Calculates whether the relationships between proband and parents are what is expected

"""


import pandas as pd

def relatedness_test(ped, relatedness_file, min_relatedness, max_relatedness, max_parents_relatedness):

    """
    Open the ped and relatedness files
    Assigns appropriate variables to sampleID from ped file
    Removes NTC from relatedness file
    Compares the sampleID variables from ped against the values in the relatedness file
    
    """
    
    # Try opening the ped and relatedness files, otherwise output that the file could not be found
    try:
        ped_file = pd.read_csv(ped, delimiter = '\t', header = None)
        relate_file = pd.read_csv(relatedness_file, delimiter = '\t')
    except:
        return False, 'Either the pedigree file or relatedness file could not be found'

    # Check to see if there are the correct amount of columns in each file and if yes then rename column names in ped file
    if len(relate_file.columns) != 7:
        return False, 'There are the incorrect amount of columns within the relatedness file'

    # This section creates a unique list of family IDs from the ped file, therefore it works with multiple families
    if len(ped_file.columns) != 6:
        return False, 'There are the incorrect amount of columns within the pedigree file'
    else:
        ped_file.columns = ['family_id', 'individual_id', 'paternal_id', 'maternal_id', 'sex', 'phenotype']
    
    family_identifier = ped_file.family_id.unique().tolist()

    if '0' in family_identifier:

        family_identifier.remove('0')

    elif 0 in family_identifier:

        family_identifier.remove(0)

    # Checking that family_identifier is populated
    if family_identifier == []:
        return False, 'Looks like family ID in the pedigree file is incorrect'

    # Creating an empty dictionary to store family identifiers and also their variables (key value pairs)
    family_id = {}

    for ID in family_identifier:
        family_id[ID] = {}

    # This will assign the mum for each ID
    for ID in family_identifier:                                                                      
       for x in ped_file.index:                                                                       
            if ped_file.paternal_id[x] == '0' and ped_file.sex[x] == 2 and ped_file.family_id[x] == ID:
                family_id[ID]['mum'] = ped_file.individual_id[x]
            elif ped_file.paternal_id[x] == '0' and ped_file.sex[x] == 1 and ped_file.family_id[x] == ID:
                family_id[ID]['dad'] = ped_file.individual_id[x]
            elif ped_file.paternal_id[x] != '0' and ped_file.sex[x] != 0 and ped_file.family_id[x] == ID:
                family_id[ID]['proband'] = ped_file.individual_id[x]
            if ped_file.sex[x] > 2 or ped_file.phenotype[x] > 2:
                return False, 'Pedigree file does not look correct'


    # Getting rid of the NTCs in INDV columns
    no_ntc = relate_file[relate_file['INDV1'] != 'NTC']
    relate_file = no_ntc[no_ntc['INDV2'] != 'NTC']


    for ID in family_identifier:
        for x in relate_file.index:
            if relate_file['INDV1'][x] == family_id[ID]['proband'] or relate_file['INDV2'][x] == family_id[ID]['proband']:
                if relate_file['INDV1'][x] == family_id[ID]['mum'] or relate_file['INDV1'][x] == family_id[ID]['dad'] or relate_file['INDV2'][x] == family_id[ID]['mum'] or relate_file['INDV2'][x] == family_id[ID]['dad']:
                    if relate_file['RELATEDNESS_PHI'][x] >= min_relatedness and relate_file['RELATEDNESS_PHI'][x] <= max_relatedness:
                        pass
                    elif relate_file['RELATEDNESS_PHI'][x] < min_relatedness or relate_file['RELATEDNESS_PHI'][x] > max_relatedness:
                        return False, 'Relatedness error'
            if relate_file['INDV1'][x] == family_id[ID]['mum'] and relate_file['INDV2'][x] == family_id[ID]['dad'] and relate_file['RELATEDNESS_PHI'][x] >= max_parents_relatedness:
                return False, 'Looks like a possible problem. Check pedigree and relateness file'
        return True, 'Everything relatedness looks fine'

if __name__ == '__main__':

    #result = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXYFAIL.relatedness2')
    #result = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX.ped', 'testData/201215_A00748_0068_AHT3FCDMXX.relatedness2', 0.2, 0.3, 0.04)
    result = relatedness_test('testData/K00150_0149_AHG7YKBBXX.ped', 'testData/K00150_0149_AHG7YKBBXX.relatedness2', 0.2, 0.3, 0.04)
    #result = relatedness_test('this_file_does_not_exist.ped', 'this_file_also_does_not_exist.relatedness2')
    print(result)






