# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:56:07 2019

@author: mvoulana
"""

import xlrd
import numpy as np

# import xlsxwriter module 
import xlsxwriter 


""" ----------------------------------------------------------------------------- """

input_folder = '../OC_OD_segmentation/'

myBook = xlrd.open_workbook(input_folder + 'measures1.xlsx')
sheet = myBook.sheet_by_index(0)

measures = [sheet.row_values(0,0)[0:7]]

for i in range(1, sheet.nrows):
    
    arrayofvalues = sheet.row_values(i,0)
    arrayofvalues = [arrayofvalues[0:7]]
    
    measures = np.concatenate((measures, arrayofvalues))
  
images = measures[:,0]
measures = [x.astype(np.float) for x in measures[1:,1:]]


# Notching function: if true, the ISNT is not respected and the optic nerve head potentially suffers from glaucoma
    
def notching(inf_sector, sup_sector, nasal_sector, temporal_sector):
    
    if ((inf_sector < sup_sector < nasal_sector) and (inf_sector < sup_sector < temporal_sector)):
        return True
    else:
        return False
    
    
diagnosis = [['Vertical CDR', 'Notching', 'NRR area', 'Diagnosis by major voting']]
    
    
for cdr, inf_sector, sup_sector, nasal_sector, temporal_sector, rim_area in (measures):
    
    if cdr < 0.6:
        diag_cdr = 'Negative'
    else:
        diag_cdr = 'Positive'
        
    notch = notching(inf_sector, sup_sector, nasal_sector, temporal_sector)
    
    if notch == 'True':
        diag_notch = 'Positive'
    else:
        diag_notch = 'Negative'
        
    if rim_area > 10000:
        diag_nrr = 'Negative'
    else:
        diag_nrr = 'Positive'
            
    # Dignosis with the major voting
    diag_vector = [diag_cdr, diag_notch, diag_nrr]
    
    if diag_vector.count('Negative') >= 2:
        final_diag = 'Negative'
    else:
        final_diag = 'Positive'
    
    diag = [[diag_cdr, diag_notch, diag_nrr, final_diag]]
    
    diagnosis = np.concatenate((diagnosis, diag))
    
    
workbook = xlsxwriter.Workbook('../OC_OD_segmentation/measures1.xlsx')

# By default worksheet names in the spreadsheet will be Sheet1, Sheet2 etc., but we can also specify a name. 
worksheet = workbook.add_worksheet("Diagnosis") 

cell_format_image = workbook.add_format({'bg_color': '#F6879F'})
cell_format_cdr = workbook.add_format({'bg_color': '#DBE7F8'})
cell_format_isnt = workbook.add_format({'bg_color': '#B3ECAE'})
cell_format_rim = workbook.add_format({'bg_color': '#F2BD8C'})
                                       
# Start from the first cell. Rows and columns are zero indexed. 
row = 0
col = 0
  
# Iterate over the data and write it out row by row. 

for image in (images):
    worksheet.write(row, col, image)
    row += 1

# Start from the first cell. Rows and columns are zero indexed. 
row = 0
col = 0

for diag_cdr, diag_notch, diag_nrr, final_diag in (diagnosis): 
    
    worksheet.write(row, col + 1, diag_cdr)
    worksheet.write(row, col + 2, diag_notch)
    worksheet.write(row, col + 3, diag_nrr)
    worksheet.write(row, col + 4, final_diag)
    row += 1
  
workbook.close() 
        

    
