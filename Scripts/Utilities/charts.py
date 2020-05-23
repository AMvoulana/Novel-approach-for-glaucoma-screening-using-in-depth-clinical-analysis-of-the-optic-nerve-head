#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 00:51:57 2019

@author: amed
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

# Number of metrics to compute and plot
n_groups = 6

# Specify the reached values on each method: Article 1, CDR, ISNT, NRR and porposed method
cdr = (77.22, 77.14, 77.41, 88.52, 60, 82.44)
isnt = (67.33, 70, 61.29, 80.33, 47.5, 74.81)
nrr = (63.37, 68.57, 54.84, 77.41, 43.59, 92.54)
article1 = (83.16, 84.28, 80.65, 90.77, 69.44, 87.40)
proposed = (90.09, 90, 90.3, 95.45, 80, 92.64)


fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.15

opacity = 0.4
error_config = {'ecolor': '0.1'}


rects0 = ax.bar(index-bar_width, nrr, bar_width,
                alpha=opacity,
                label='NRR area')

rects1 = ax.bar(index, isnt, bar_width,
                alpha=opacity,
                label='ISNT rule')

rects2 = ax.bar(index + bar_width, cdr, bar_width,
                alpha=opacity,
                label='CDR')

rects3 = ax.bar(index + 2*bar_width, article1, bar_width,
                alpha=opacity,
                label='Method 1')

rects4 = ax.bar(index + 3*bar_width, proposed, bar_width,
                alpha=opacity,
                label='Proposed method')


ax.set_ylim(40,100)
#ax.set_xlabel('Metrics')
ax.set_ylabel('Scores')
ax.set_title('Scores on performed metrics for glaucoma screening')
ax.set_xticks(index + 2*bar_width/2)
ax.set_xticklabels(('Acc', 'Sen', 'Spe', 'PPV', 'NPV', 'F-score'))
ax.legend(loc="lower left")

fig.tight_layout()
plt.show()

fig.savefig('charts.png')
#plt.savefig(fig)