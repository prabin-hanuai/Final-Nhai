import pandas as pd

def RA_preprocess(temp):
    Furniture_Chainage_Report = {}
    chaing = temp['Furniture Chainage Report']['Chainage']
    chaing.iloc[:, 0] = chaing.iloc[:, 0].fillna(method='ffill')
    Chainage = chaing[chaing.columns[0]].to_list()
    Chainage_from = chaing[chaing.columns[1]].to_list()
    Chainage_to = chaing[chaing.columns[2]].to_list()
    r_section = temp['Furniture Chainage Report']['Road Section']
    road_section = r_section[r_section.columns[0]].to_list()
    Furniture_Chainage_Report['Chainage'] = Chainage
    Furniture_Chainage_Report['Road Section'] = road_section
    # Furniture_Chainage_Report['Chainage (From)'] = Chainage_from
    # Furniture_Chainage_Report['Chainage (To)'] = Chainage_to
    furniture_assets = ['Chevron','Cautionary Warning Signs','Hazard','Prohibitory Mandatory Signs','Informatory Signs']
    overhead = []
    for type in furniture_assets:
        try:
            _data = temp['Furniture Chainage Report']['Furniture Assets'][type]
            for column in _data.columns:
                if True in ['Overhead' in i for i in column]:
                    Furniture_Chainage_Report[f'{type} (Overhead)'] = _data[column].to_list()
                    overhead.append(type)
                if True in ['Avenue' in i or 'Left' in i for i in column]:
                    Furniture_Chainage_Report[f'{type} (Avenue/Left)'] = _data[column].to_list()
                if True in ['Median' in i or 'Right' in i for i in column]:
                    Furniture_Chainage_Report[f'{type} (Median/Right)'] = _data[column].to_list()
        except:
            continue
    
    
    final_data = pd.DataFrame(Furniture_Chainage_Report)
    final_data.dropna(subset=['Road Section'], inplace=True)
    final_data.replace('NONE', pd.NA, inplace=True)
    final_data.fillna(0,inplace = True)
    while overhead:
        _  = overhead.pop()
        avenue_left_col = f'{_} (Avenue/Left)'
        overhead_col = f'{_} (Overhead)'
        final_data[avenue_left_col].astype('int')
        final_data[overhead_col].astype('int')
        final_data[f'{_} (Avenue/Left)'] = final_data[avenue_left_col] + final_data[overhead_col]
        final_data.drop(columns = [overhead_col],inplace = True)
    final_data['Chainage'] = final_data['Chainage'].apply(preprocess_chainages)
    return final_data


def preprocess_chainage(chainage_value):
    parts = chainage_value.replace(" ", "").split('-')
    parts.sort()
    return '-'.join(parts)

def preprocess_chainages(chainage_value):
    parts = chainage_value.replace(" ", "").split('-')
    return '-'.join(parts)