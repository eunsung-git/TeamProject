from django.conf import settings
import pandas as pd
import random
import os

def tip_link(item, gender):
    df = pd.read_excel(os.path.join(settings.BASE_DIR, 'tip.xlsx'))
    
    youtube = df.loc[(df['category']==item) & (df['gender']==gender), ['url','image_url','title']]
    youtube = youtube.values.tolist()
    youtube  = random.choice(youtube)
    
#     tip_link = youtube[0]
#     tip_thumbnail = youtube[1]
#     tip_title = youtube[2]

    
    return youtube