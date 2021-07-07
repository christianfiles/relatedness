#!/usr/bin/env python

"""
relatedness.py

Calculates whether the relationships between proband and parents are what is expected

"""


import pandas as pd
import warnings

def relatedness_test(ped, relatednessFile):

    """
    Open the ped and relatedness files
    Assigns appropriate variables to sampleID from ped file
    Removes NTC from relatedness file
    Compares the sampleID variables from ped against the values in the relatedness file
    
    """
    
    # Try opening the ped and relatedness files, otherwise output that the file could not be found
    try:
        pedFile = pd.read_csv(ped, delimiter = '\t', header = None)
        relateFile = pd.read_csv(relatednessFile, delimiter = '\t')
    except:
        fileP = open(ped + '.txt', 'w')
        fileP.write('Ped file could not be found- check file name')
        fileP.close()
        fileR = open(relatednessFile + '.txt', 'w')
        fileR.write('Relatedness file could not be found- check file name')
        fileR.close()
        return False, 'Either the pedigree file or relatedness file could not be found'

    # Check to see if there are the correct amount of columns in each file and if yes then rename column names in ped file
    if len(relateFile.columns) != 7:
        return False, 'There are the incorrect amount of columns within the relatedness file'
    else:
        pass

    #### This commented section creates a unique list of family IDs from the ped file, therefore it works with multiple families
    if len(pedFile.columns) != 6:
        return False, 'There are the incorrect amount of columns within the pedigree file'
    else:
        pedFile.columns = ['familyid', 'individualid', 'paternalid', 'maternalid', 'sex', 'phenotype']
    
    familyIdentifier = pedFile.familyid.unique().tolist()
    familyIdentifier.remove('0')

    # Creating an empty dictionary to store family identifiers and also their variables (key value pairs)
    familyID = {}

    for ID in familyIdentifier:
        familyID[ID] = {}

    #This will assign the mum for each ID! crack on with this tomorrow!
    for ID in familyIdentifier:                                                                      
       for x in pedFile.index:                                                                       
            if pedFile.paternalid[x] == '0' and pedFile.sex[x] == 2 and pedFile.familyid[x] == ID:
                familyID[ID]['mum'] = pedFile.individualid[x]
            elif pedFile.paternalid[x] == '0' and pedFile.sex[x] == 1 and pedFile.familyid[x] == ID:
                familyID[ID]['dad'] = pedFile.individualid[x]
            elif pedFile.paternalid[x] != '0' and pedFile.sex[x] != 0 and pedFile.familyid[x] == ID:
                familyID[ID]['proband'] = pedFile.individualid[x]
            if pedFile.sex[x] > 2 or pedFile.phenotype[x] > 2:
                return False


    # Getting rid of the NTCs in INDV columns
    noNTC = relateFile[relateFile['INDV1'] != 'NTC']
    relateFile = noNTC[noNTC['INDV2'] != 'NTC']


    for ID in familyIdentifier:
        for x in relateFile.index:
            if relateFile['INDV1'][x] == familyID[ID]['proband'] or relateFile['INDV2'][x] == familyID[ID]['proband']:
                if relateFile['INDV1'][x] == familyID[ID]['mum'] or relateFile['INDV1'][x] == familyID[ID]['dad'] or relateFile['INDV2'][x] == familyID[ID]['mum'] or relateFile['INDV2'][x] == familyID[ID]['dad']:
                    if relateFile['RELATEDNESS_PHI'][x] >= 0.2 and relateFile['RELATEDNESS_PHI'][x] <= 0.3:
                        pass
                    elif relateFile['RELATEDNESS_PHI'][x] < 0.2 or relateFile['RELATEDNESS_PHI'][x] > 0.3:
                        return False
            if relateFile['INDV1'][x] == familyID[ID]['mum'] and relateFile['INDV2'][x] == familyID[ID]['dad'] and relateFile['RELATEDNESS_PHI'][x] >= 0.04:
                return False, 'Looks like a possible problem. Check to see if parents are related'
        return True

if __name__ == '__main__':

    #result = relatedness_test('testData/210622_A00748_0110_AH5T3CDRXY.ped', 'testData/210622_A00748_0110_AH5T3CDRXYFAIL.relatedness2')
    result = relatedness_test('testData/201215_A00748_0068_AHT3FCDMXX_INCORRECT_NUMBER_OF_COLUMNS.ped', 'testData/201215_A00748_0068_AHT3FCDMXX.relatedness2')
    #result = relatedness_test('this_file_does_not_exist.ped', 'this_file_also_does_not_exist.relatedness2')
    print(result)






