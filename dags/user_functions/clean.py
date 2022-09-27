import pandas


def to_clean():
    df = pandas.read_csv('~/Documents/data_for_tasks/763K_plus_IOS_Apps_Info.csv')
    df = df.replace(',', '', regex=True)
    df[['All_Genres', 'Languages']] = df[['All_Genres', 'Languages']].replace('[\[\]\']', '', regex=True)
    df = df.replace(' {2,}', ' ', regex=True)
    df = df.fillna('-')
    df = df.replace('\n', '', regex=True)
    df.to_csv('~/Documents/data_for_tasks/prep_data.csv', index=False)
    return

