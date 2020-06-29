import pandas as pd

def tip_link(item, gender):
    path = r'E:\\study\\project\\team\\clothes'

    df =  pd.read_excel(path+'\\팁.xlsx')
    df = df[['category', 'gender', 'url','image_url']] 
    
    youtube = df.loc[(df['category']==item) & (df['gender']==gender), ['url','image_url']]
    youtube = youtube.values.tolist()[0]
    
#     tip_link = youtube[0]
#     tip_thumbnail = youtube[1]
    
    return youtube