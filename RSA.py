import pandas as pd
import numpy as np

def convert_to_meters(distance):
    if '.+' in distance:
        km, m = distance.split('.+')
    elif '+.' in distance:
        km, m = distance.split('+.')
    elif '+' in distance:
        km, m = distance.split('+')
    elif '.' in distance:
        km, m = distance.split('.')

    km = int(km) * 1000
    m = int(m)
    total_meters = km + m
    return total_meters

def rsa_preprocess(excel_path, range_tuples):
    sheets = ['MCW LHS', 'MCW RHS', 'SRL', 'SRR', 'TL', 'IRL', 'IRR', 'TR', 'CR']
    
    all_data = []
    
    for sheet in sheets:
        df = pd.read_excel(excel_path, sheet_name=sheet, header=[9], usecols="A:J")
        df.columns = [i.lower().strip() for i in df.columns]

        print(sheet,df.shape)
        df.dropna(subset=['chainage'],inplace=True)
        df['chainage'] = df['chainage'].astype('str')

        if 'avenue/median/overhead' in df.columns:
            location_col = 'avenue/median/overhead'
        elif 'left/right/overhead' in df.columns:
            location_col = 'left/right/overhead'
        else:
            raise ValueError(f"Neither 'avenue/median/overhead' nor 'left/right/overhead' found in sheet: {sheet}")

        final_df = df[['chainage', 'type of sign board', location_col]]
        final_df.dropna(subset=['chainage'],inplace=True)
        
        final_df['chainage'] = final_df['chainage'].apply(convert_to_meters)


        def get_range(chainage):
            for start, end in range_tuples:
                if start <= chainage <= end:
                    return f"{start}-{end}"
            return None
        
        final_df['Chainage'] = final_df['chainage'].apply(get_range)
        
        grouped = final_df.groupby(['Chainage', 'type of sign board', location_col]).size().reset_index(name='count')
        grouped['Road Section'] = sheet
        all_data.append(grouped)
    
    # Combine all DataFrames into one
    combined_df = pd.concat(all_data, ignore_index=True)
    
    return combined_df

def rsa_process(excel_path, range):
    result = rsa_preprocess(excel_path, range)
    mapping = {
    'avenue': 'Avenue/Left',
    'left': 'Avenue/Left',
    'median': 'Median/Right',
    'right': 'Median/Right',
    'overhead': 'Avenue/Left'
    }

    # Apply the mapping to both columns
    result['avenue/median/overhead'] = result['avenue/median/overhead'].str.lower().str.strip().map(mapping).fillna(result['avenue/median/overhead'])
    result['left/right/overhead'] = result['left/right/overhead'].str.lower().str.strip().map(mapping).fillna(result['left/right/overhead'])

    # Combine the two columns into a single column (if needed)
    result['location'] = result['avenue/median/overhead'].combine_first(result['left/right/overhead'])

    # Drop the original columns if no longer needed
    result = result.drop(columns=['avenue/median/overhead', 'left/right/overhead'])

    sign_mapping = {
        'cautionary': 'Cautionary Warning Signs',
        'prohibitory': 'Prohibitory Mandatory Signs',
        'informatory': 'Informatory Signs',
        'chevron': 'Chevron',
        'hazard': 'Hazard'
    }

    def map_sign_type(value):
        value = value.lower().strip()
        for keyword, mapped_value in sign_mapping.items():
            if keyword in value:
                return mapped_value
        return value 

    result['type of sign board'] = result['type of sign board'].apply(map_sign_type)

    pivot_df = result.pivot_table(index=['Chainage','Road Section'], 
                                columns=['type of sign board', 'location'], 
                                values='count',
                                aggfunc='sum', 
                                fill_value=0)

    pivot_df.columns = [f'{col[0]} ({col[1]})' for col in pivot_df.columns]

    pivot_df.reset_index(inplace=True)

    # Step 1: Create a dictionary for the new column names
    columns_map = {
        'Chevron': ['Chevron (Avenue/Left)', 'Chevron (Median/Right)'],
        'Cautionary Warning Signs': ['Cautionary Warning Signs (Avenue/Left)', 'Cautionary Warning Signs (Median/Right)'],
        'Hazard': ['Hazard (Avenue/Left)', 'Hazard (Median/Right)'],
        'Prohibitory Mandatory Signs': ['Prohibitory Mandatory Signs (Avenue/Left)', 'Prohibitory Mandatory Signs (Median/Right)'],
        'Informatory Signs': ['Informatory Signs (Avenue/Left)', 'Informatory Signs (Median/Right)']
    }

    # Step 2: Convert relevant columns from string to numeric
    for col in pivot_df.columns:
        if col not in ['Chainage', 'Road Section']:
            pivot_df[col] = pd.to_numeric(pivot_df[col], errors='coerce')  # Convert to numeric, invalid parsing will be set as NaN

    # Step 3: Create a new DataFrame
    pivot_df_new = pd.DataFrame()

    # Copy unchanged columns first
    pivot_df_new[['Chainage', 'Road Section']] = pivot_df[['Chainage', 'Road Section']]

    # Step 4: Efficiently aggregate columns based on the `columns_map`
    for new_col, old_cols in columns_map.items():
        for col in old_cols:
            if col not in pivot_df.columns:
                pivot_df[old_cols] = np.nan
        pivot_df_new[new_col] = pivot_df[old_cols].sum(axis=1)

    return pivot_df, pivot_df_new