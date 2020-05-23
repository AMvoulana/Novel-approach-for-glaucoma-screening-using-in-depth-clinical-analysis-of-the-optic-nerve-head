#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Script permettant d'extraire les résultats obtenus de mesure dans un fichier CSV, et d'en tracer 
# les courbes


import numpy as np
import matplotlib.pyplot as plt
import csv

# Lecture des fichiers CSV des résultats
dossier_images = 'Courbes2/'

#resultats = np.zeros((52,13))
resultats = []

with open('resultats2.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    for i, row in enumerate(spamreader):
        if i == 0:
            titres = row[1:]
        else:
            resultats.append([float(n) for n in row[1:]])

            
            
tab =  [2,7,8,14,15,16,17,20,21,24,25,28,44,45,46,47,48,49]
tableau = [0,1,3,4,5,6,9,10,11,12,13,18,19,22,23,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]

x_normal = np.arange(0,18,1)
x_atteint = np.arange(19,51,1)

for i in range(0, len(resultats[0])):
    vecteur = [n[i] for n in resultats]
    print(vecteur)
    
    vecteur_normal = [vecteur[i] for i in tab]
    vecteur_atteint = [vecteur[i] for i in tableau]
    
    vecteur_normal.sort()
    vecteur_atteint.sort()
    
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(x_normal, vecteur_normal, 'gx')
    ax.plot(x_normal, vecteur_normal, 'g--')
    
    ax.plot(x_atteint, vecteur_atteint, 'ro')
    ax.plot(x_atteint, vecteur_atteint, 'r--')
    
    ax.axvline(x=18, color = 'k')
    if i == 12:
        ax.axhline(y=0.63)
    
    #ax.set_title(titres[i] + '- vert : patient normal, rouge : patient atteint')
    ax.set_xlabel('Images')
    ax.set_ylabel(titres[i])

    fig.savefig(dossier_images + titres[i] + '.png')
    
    mean_vecteur_normal, std_vecteur_normal = np.mean(vecteur_normal), np.std(vecteur_normal)
    mean_vecteur_atteint, std_vecteur_atteint = np.mean(vecteur_atteint), np.std(vecteur_atteint)
    
    fig2, ax2 = plt.subplots(figsize=(4,3))
    
    ax2.bar(0, [mean_vecteur_normal], [0.35], yerr = [std_vecteur_normal], color='g')
    ax2.bar(1, [mean_vecteur_atteint], [0.35], yerr = [std_vecteur_atteint], color='r')
    
    if titres[i] == 'ratio':
        print(mean_vecteur_normal)
        print(std_vecteur_normal)
        print(mean_vecteur_atteint)
        print(std_vecteur_atteint)

    ax2.set_title("Moyennes et écart-type - " + titres[i])
    ax2.set_ylabel("Moyennes et écart-type")
    plt.xticks(np.arange(2), ('C1', 'C2'))
    fig2.savefig(dossier_images + titres[i] + "_moy.png")


    
        