#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script permettant de faire la segmentation du OC et du OD pour le diagnostic de glaucome grâce au CDR

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.measure import label, regionprops
from scipy.spatial import distance as dis
import scipy.ndimage.measurements as snm
import csv

# import xlsxwriter module 
import xlsxwriter 


""" ----------------------------------------------------------------------------- """

input_folder = '../OC_OD_segmentation/'

# --- Folders of the computed segmentations --- 

oc_folder = input_folder + 'oc_results/'
oc_list = os.listdir(oc_folder)
oc_list.sort()

od_folder = input_folder + 'od_results/'
od_list = os.listdir(od_folder)
od_list.sort()

# --- Folders of the ground-truth segmentations --- 

oc_gt_folder = input_folder + 'Ground_truth/processed_oc_gt/'
oc_gt_list = os.listdir(oc_gt_folder)
oc_list.sort()

od_gt_folder = input_folder + 'Ground_truth/processed_od_gt/'
od_gt_list = os.listdir(od_gt_folder)
od_gt_list.sort()


""" ----------------------------------------------------------------------------- """

# Compute the vertical diameter of a convex region (OC or OD) 
    
def vertical_diameter(binary_image):
    
    label_image = label(binary_image)
    
    # Compute the boundary box of each connected component in the label image
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        
    vertical = maxr - minr
    horizontal = maxc - minc
            
    return vertical, horizontal


# Compute the location (x,y) of the four quadrants points of a convex region (OC or OD)
    
def quadrants(binary_image):
    
    label_image = label(binary_image)
    
    # Compute the boundary box of each connected component in the label image
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        
    inferior = (maxr, minc + int((maxc - minc)/2))
    superior = (minr, minc + int((maxc - minc)/2))
    
    nasal = (minr + int((maxr - minr)/2), minc)
    temporal = (minr + int((maxc - minr)/2), maxc)
    
    return inferior, superior, nasal, temporal


def sectors(inferior_oc, superior_oc, nasal_oc, temporal_oc, inferior_od, superior_od, nasal_od, temporal_od):
    
    inf_sector = inferior_od[0] - inferior_oc[0]
    sup_sector = superior_oc[0] - superior_od[0]
    
    nasal_sector = nasal_oc[1] - nasal_od[1]
    temporal_sector = temporal_od[1] - temporal_oc[1]
    
    return inf_sector, sup_sector, nasal_sector, temporal_sector

    
def nrr_area(oc_image, od_image):
    
    oc_area = len(oc_image[oc_image != 0])
    od_area = len(od_image[od_image != 0])
    cdr_area = oc_area/od_area
    
    #print(oc_area)
    #print(od_area)
    
    rim_area = od_area - oc_area
    
    return rim_area, cdr_area
    

def onh_areas(oc_image, od_image):
    
    oc_area = len(oc_image[oc_image != 0])
    od_area = len(od_image[od_image != 0])
    #cdr_area = oc_area/od_area
    
    #print(oc_area)
    #print(od_area)
    
    #rim_area = od_area - oc_area
    
    return oc_area, od_area

"""
oc = cv2.imread(oc_folder + 'drishtiGS_002.png')

oc_image = cv2.imread(oc_folder + 'drishtiGS_002.png', 0)
od_image = cv2.imread(od_folder + 'drishtiGS_002.png', 0)

vertical_oc, horizontal_oc = vertical_diameter(oc_image)
vertical_od, horizontal_od = vertical_diameter(od_image)

cdr = vertical_oc/vertical_od

inferior_oc, superior_oc, nasal_oc, temporal_oc = quadrants(oc_image)
inferior_od, superior_od, nasal_od, temporal_od = quadrants(od_image)

notch = notching(inferior_oc, superior_oc, nasal_oc, temporal_oc, inferior_od, superior_od, nasal_od, temporal_od)

rim_area = nrr_area(oc_image, od_image)
"""



""" ---------------------------------------------------------------------------------------------- """


measures = [['image', 'Vertical CDR', 'inf_sector', 'Sup_sector', 'Nasal_sector', 'Temporal_sector', 'NRR area']]

diagnosis = [['image', 'Vertical CDR', 'Notching', 'NRR area', 'Diagnosis by major voting']]

onh_areas = [['image', 'oc_area', 'od_area']]


for i, fichier in enumerate(oc_gt_list):
    
    #if(i != 21):
    print("Processing sur l'image %d" % (i+1))
    
    oc_image = cv2.imread(oc_folder + fichier, 0)
    
    od_image = cv2.imread(od_folder + fichier, 0)
    
    vertical_oc, horizontal_oc = vertical_diameter(oc_image)
    vertical_od, horizontal_od = vertical_diameter(od_image)
    
    """---------------- Measurements -------------------"""
    
    cdr = vertical_oc/vertical_od
    
    inferior_oc, superior_oc, nasal_oc, temporal_oc = quadrants(oc_image)
    inferior_od, superior_od, nasal_od, temporal_od = quadrants(od_image)
    
    inf_sector, sup_sector, nasal_sector, temporal_sector = sectors(inferior_oc, superior_oc, nasal_oc, temporal_oc, inferior_od, superior_od, nasal_od, temporal_od)
        
    rim_area, cdr_area = nrr_area(oc_image, od_image)
    
    oc_area, od_area = onh_areas()
    
    measure = [[fichier, cdr, inf_sector, sup_sector, nasal_sector, temporal_sector, cdr_area]]
    
    measures = np.concatenate((measures, measure))
    
    
    """---------------- Diagnosis in accordance with the measurements -------------------"""
    """
    if cdr < 0.6:
        diag_cdr = 'Negative'
    else:
        diag_cdr = 'Positive'
        
    #notch = notching(inf_sector, sup_sector, nasal_sector, temporal_sector)
    
    #if notch == 'True':
        #diag_notch = 'Positive'
    #else:
        #diag_notch = 'Negative'
        
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
    
    diag = [[fichier, diag_cdr, diag_notch, diag_nrr, final_diag]]
    
    diagnosis = np.concatenate((diagnosis, diag))
    """
    
    
workbook = xlsxwriter.Workbook('../OC_OD_segmentation/measures_areas.xlsx') 
  
# By default worksheet names in the spreadsheet will be Sheet1, Sheet2 etc., but we can also specify a name. 
worksheet = workbook.add_worksheet("My sheet") 
  
# Start from the first cell. Rows and columns are zero indexed. 
row = 0
col = 0
  
# Iterate over the data and write it out row by row. 
for image, cdr, inf_sector, sup_sector, nasal_sector, temporal_sector, cdr_area in (measures): 
    
    worksheet.write(row, col, image) 
    worksheet.write(row, col + 1, cdr)
    worksheet.write(row, col + 2, inf_sector)
    worksheet.write(row, col + 3, sup_sector)
    worksheet.write(row, col + 4, nasal_sector)
    worksheet.write(row, col + 5, temporal_sector)
    worksheet.write(row, col + 6, cdr_area)
    row += 1
  
workbook.close() 
    

workbook = xlsxwriter.Workbook('../diagnosis.xlsx') 
  
worksheet = workbook.add_worksheet("Measures") 
  
# Start from the first cell. Rows and columns are zero indexed. 
row = 0
col = 0
  
# Iterate over the data and write it out row by row. 
for image, cdr, inf_sector, sup_sector, nasal_sector, temporal_sector, rim_area in (measures): 
    
    worksheet.write(row, col, image) 
    worksheet.write(row, col + 1, cdr)
    worksheet.write(row, col + 2, inf_sector)
    worksheet.write(row, col + 3, sup_sector)
    worksheet.write(row, col + 4, nasal_sector)
    worksheet.write(row, col + 5, temporal_sector)
    worksheet.write(row, col + 6, rim_area)
    row += 1
    
"""    
# By default worksheet names in the spreadsheet will be Sheet1, Sheet2 etc., but we can also specify a name. 
worksheet = workbook.add_worksheet("Diagnosis") 

# Start from the first cell. Rows and columns are zero indexed. 
row = 0
col = 0
  
# Iterate over the data and write it out row by row. 
for image, diag_cdr, diag_notch, diag_nrr, final_diag in (diagnosis): 
    
    worksheet.write(row, col, image)
    worksheet.write(row, col + 1, diag_cdr)
    worksheet.write(row, col + 2, diag_notch)
    worksheet.write(row, col + 3, diag_nrr)
    worksheet.write(row, col + 4, final_diag)
    row += 1
  
workbook.close() 
""" 
    
    
#cv2.circle(oc,(temporal[1], temporal[0]), 5, (0,0,255), -1)

#plt.imshow(oc)
#plt.imshow(od_image)
#plt.show()


"""
# Fonction faisant le calcul de l'aire d'une image binaire
def calcul_aire(binary_image):
    
    binary_image = binary_image[binary_image != 0]
    aire = len(binary_image)
    
    return aire


# Fonction établissant le diagnostic en fonction du ratio
def diagnostic(ratio):
    
    if ratio < 0.64:
        diag = 'Normal'
        
    elif 0.64 < ratio and ratio <= 1.0:
        diag = 'Glaucomatous'
    
    else:
        diag = 'Erreur de calcul'

    return diag
"""