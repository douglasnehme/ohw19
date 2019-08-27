import pandas as pd
import matplotlib.pyplot as plt


# import cartopy.crs as ccrs
# from palettable.cmocean.sequential import Thermal_20

##############################################################################
url = ("https://raw.githubusercontent.com/ocefpaf/"
       "2018-Jun-SWC-Floripa/master/data")

fname = "dados_pirata.csv"
df = pd.read_csv(
    f"{url}/{fname}",
    index_col='datahora',
    parse_dates=True,
    na_values=-99999,
)


df.drop('Unnamed: 0', axis=1, inplace=True)
df.columns = ['{0:0>3}'.format(col.split('_')[1]) for
              col in df.columns]

df.sort_index(axis=1, inplace=True)
##############################################################################


fig, ax = plt.subplots()

# df.iloc[:, -1].plot(ax=ax)
ax = df.iloc[:, -1].plot()

##############################################################################
fig, ax = plt.subplots()

plot = {"marker": ".", "linestyle": "none", "figsize": (11, 3)}
# This command is telling to te interpolating function that it is just to be
# applied in gaps limited to 10 values, that in this df is in hours.
interp = {"method": "time", "limit": 10}

df["001"].plot(**plot);
df["001"].interpolate(**interp).plot(alpha=0.65);


plt.show()