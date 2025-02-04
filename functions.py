import pandas as pd
import streamlit as st

def RA_preprocess(temp):
    Furniture_Chainage_Report = {}
    first_level_header = temp.columns.get_level_values(0).unique()[0]  # Fetch the first unique header
    print("First level header:", first_level_header)
    chaing = temp[first_level_header]['Chainage']
    chaing.iloc[:, 0] = chaing.iloc[:, 0].fillna(method='ffill')
    Chainage = chaing[chaing.columns[0]].to_list()
    Chainage_from = chaing[chaing.columns[1]].to_list()
    Chainage_to = chaing[chaing.columns[2]].to_list()
    r_section = temp[first_level_header]['Road Section']
    road_section = r_section[r_section.columns[0]].to_list()
    Furniture_Chainage_Report['Chainage'] = Chainage
    Furniture_Chainage_Report['Road Section'] = road_section
    # Furniture_Chainage_Report['Chainage (From)'] = Chainage_from
    # Furniture_Chainage_Report['Chainage (To)'] = Chainage_to
    furniture_assets = ['Chevron','Cautionary Warning Signs','Hazard','Prohibitory Mandatory Signs','Informatory Signs','CHEVRON','CAUTIONARY WARNING SIGNS','HAZARD','PROHIBITORY MANDATORY SIGNS','INFORMATORY SIGNS','Chevron ','Cautionary Warning Signs ','Hazard ','Prohibitory Mandatory Signs ','Informatory Signs ']
    overhead = []
    st.dataframe(temp[first_level_header]['Furniture Assets'], use_container_width=True)
    for type in furniture_assets:
        
        try:
            _data = temp[first_level_header]['Furniture Assets'][type]
            type = type.strip().lower().title()
            for column in _data.columns:
                if True in ['overhead' in i.lower() for i in column]:
                    Furniture_Chainage_Report[f'{type} (Overhead)'] = _data[column].to_list()
                    overhead.append(type)
                if True in ['avenue' in i.lower() or 'left' in i.lower() for i in column]:
                    Furniture_Chainage_Report[f'{type} (Avenue/Left)'] = _data[column].to_list()
                if True in ['median' in i.lower() or 'right' in i.lower() for i in column]:
                    Furniture_Chainage_Report[f'{type} (Median/Right)'] = _data[column].to_list()
        except:
            continue

    final_data = pd.DataFrame(Furniture_Chainage_Report)

    for col in final_data.columns:
        if col not in ['Chainage', 'Road Section']:
            final_data[col] = pd.to_numeric(final_data[col], errors='coerce') 
    
    na_data = final_data[final_data['Road Section'].isna()].copy()
    na_data = na_data.drop(columns = ['Road Section','Chainage'])
    # na_data = na_data.astype('str')
    # na_data = na_data.replace('NIL',pd.NA)
    # na_data = na_data.replace('nan',pd.NA)
    # na_data = na_data.replace('NONE',pd.NA)

    total_sum = na_data.fillna(0)
    rows_with_data = na_data[na_data.sum(axis=1) != 0] 
    rows_with_data_indices = rows_with_data.index.tolist()
    total_sum = na_data.sum().sum()
    if total_sum != 0:
        st.write('Data is not in the correct format, check row with missing Road Section, their sum is ',total_sum)
        st.write('Rows with data present (non-zero) are at indices:', rows_with_data_indices)

    final_data.dropna(subset=['Road Section'], inplace=True)
    # final_data.replace('NONE', pd.NA, inplace=True)
    # final_data.replace('NIL', pd.NA, inplace=True)
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