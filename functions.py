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
    
    # Step 1: Create a dictionary for the new column names
    columns_map = {
        'Chevron': ['Chevron (Avenue/Left)', 'Chevron (Median/Right)'],
        'Cautionary Warning Signs': ['Cautionary Warning Signs (Avenue/Left)', 'Cautionary Warning Signs (Median/Right)'],
        'Hazard': ['Hazard (Avenue/Left)', 'Hazard (Median/Right)'],
        'Prohibitory Mandatory Signs': ['Prohibitory Mandatory Signs (Avenue/Left)', 'Prohibitory Mandatory Signs (Median/Right)'],
        'Informatory Signs': ['Informatory Signs (Avenue/Left)', 'Informatory Signs (Median/Right)']
    }

    # Step 2: Convert relevant columns from string to numeric
    for col in final_data.columns:
        if col not in ['Chainage', 'Road Section']:
            final_data[col] = pd.to_numeric(final_data[col], errors='coerce')  # Convert to numeric, invalid parsing will be set as NaN

    # Step 3: Create a new DataFrame
    final_data_new = pd.DataFrame()

    # Copy unchanged columns first
    final_data_new[['Chainage', 'Road Section']] = final_data[['Chainage', 'Road Section']]

    # Step 4: Efficiently aggregate columns based on the `columns_map`
    for new_col, old_cols in columns_map.items():
        final_data_new[new_col] = final_data[old_cols].sum(axis=1)

    # Display the final DataFrame
    print(final_data_new)





    return final_data,final_data_new


def preprocess_chainage(chainage_value):
    parts = chainage_value.replace(" ", "").split('-')
    parts.sort()
    return '-'.join(parts)

def preprocess_chainages(chainage_value):
    parts = chainage_value.replace(" ", "").split('-')
    return '-'.join(parts)

def get_text_position(value, max_value):
    # Use inside if the bar is too short
    if abs(value) < max_value * 0.3:  # Arbitrary threshold, 30% of the max value
        return 'inside'
    else:
        return 'outside'