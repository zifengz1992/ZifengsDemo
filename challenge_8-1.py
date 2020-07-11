import pandas as pd
import numpy

def clean():

    df = pd.read_csv("http://labfile.oss.aliyuncs.com/courses/1176/earthquake.csv")

    df_1 = pd.DataFrame(data=df, columns=['time', 'latitude', 'longitude', 'depth', 'mag'])
    df_region = df['place'].str.rsplit(",", 1, expand=True)
    df_region.fillna(df_region[0], inplace=True)
    
    df_clean = pd.concat([df_1, df_region[1]], axis=1).dropna().drop_duplicates()
    df_clean.columns=['time', 'latitude', 'longitude', 'depth', 'mag', 'region']

    return df_clean

def mag_region():

    df_clean = clean()

    sc_list = ['micro', 'light', 'strong', 'major', 'great']

    df_clean['scale'] = pd.cut(df_clean.mag, bins=[0, 2, 5, 7, 9, 12], right=False, labels=sc_list)

    df_count = df_clean.groupby(by=['scale', 'region']).count()

    fr_list = []
        
    for n in range(len(sc_list)):
        try:
            fr_list.append(int(df_count.loc[df_count.index.get_level_values('scale')==sc_list[n]].max()['time']))
        except:
            fr_list.append(numpy.nan)

    rg_list = []

    for n in range(len(sc_list)):
        try:
            rg_list.append(df_count.query('scale=="%s"' % (sc_list[n])).loc[df_count['time']==fr_list[n]].index[0][1])
        except:
            rg_list.append(numpy.nan)

    # print(sc_list)
    # print(fr_list)
    # print(rg_list)

    df_final = pd.DataFrame({'region': rg_list, 'times': fr_list}, index=sc_list).dropna()
    df_final.index.name = 'mag'

    print(df_final)
    return df_final

if __name__ == "__main__":

    mag_region()