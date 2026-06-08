import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn import datasets

# Configuración visual
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('tab10')
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['font.size'] = 12

print('✅ Librerías cargadas correctamente')
print(f'   NumPy     {np.__version__}')
print(f'   Pandas    {pd.__version__}')
import sklearn; print(f'   Sklearn   {sklearn.__version__}')