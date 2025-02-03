import streamlit as st
import pandas as pd
from functions import RA_preprocess, preprocess_chainage, get_text_position
from RSA import rsa_process
from download_functions import save_chart_to_image, create_word_doc,create_word_doc_new
import plotly.graph_objects as go
import shutil
import plotly.express as px
def main():
    activities = ["Home", "Old Template", "Devloper"]
    choice = st.sidebar.selectbox("Menu", activities)

    # if choice == 'Old Template':
    #     # Set up the title of the app
    #     st.title("Furniture Chainage Report")

    #     st.header("Upload PIU Excel File")
    #     type_a_file = st.file_uploader("Upload PIU Excel file", type=["xlsx", "xls"])

    #     if type_a_file is not None:
    #         try:
    #             type_a_df = pd.read_excel(type_a_file, header=[0, 1, 2, 3, 4])
    #             st.write("Data from PIU Excel file:")
    #             final_data1,final_data1_new = RA_preprocess(type_a_df)

    #             if 'Chainage' in final_data1.columns:
    #                 final_data1['Processed_Chainage'] = final_data1['Chainage'].apply(preprocess_chainage)
    #                 Chainage_values1 = final_data1['Processed_Chainage'].unique() 

    #                 Chainage_filter1 = st.selectbox("Select Chainage value to filter", ["All"] + list(Chainage_values1), key="chainage_filter1")
                    
    #                 if Chainage_filter1 != "All":
    #                     filtered_data1 = final_data1[final_data1['Processed_Chainage'] == Chainage_filter1]
    #                     filtered_data1 = filtered_data1.drop(columns=['Processed_Chainage'])
    #                     st.write(f"Filtered data for Chainage = {Chainage_filter1}:")
    #                     st.dataframe(filtered_data1, use_container_width=True)
    #                 else:
    #                     final_data1 = final_data1.drop(columns=['Processed_Chainage'])
    #                     st.write("Displaying whole data:")
    #                     st.dataframe(final_data1, use_container_width=True)

    #         except Exception as e:
    #             st.error(f"Error reading PIU Excel file: {e}")

    #     elif type_a_file is None:
    #         st.warning("Please upload a PIU Excel file.")

    #     st.header("Upload RA Excel File")
    #     type_b_file = st.file_uploader("Upload RA Excel file", type=["xlsx", "xls"])

    #     if type_b_file is not None:
    #         try:
    #             type_b_df = pd.read_excel(type_b_file, header=[0, 1, 2, 3, 4])
    #             st.write("Data from Type RA Excel file:")
    #             final_data2,final_data2_new = RA_preprocess(type_b_df)

    #             if 'Chainage' in final_data1.columns:
    #                 final_data2['Processed_Chainage'] = final_data2['Chainage'].apply(preprocess_chainage)
    #                 Chainage_values2 = final_data2['Processed_Chainage'].unique() 

    #                 Chainage_filter2 = st.selectbox("Select Chainage value to filter", ["All"] + list(Chainage_values2), key="chainage_filter2")
                    
    #                 if Chainage_filter2 != "All":
    #                     filtered_data2 = final_data2[final_data2['Processed_Chainage'] == Chainage_filter2]
    #                     filtered_data2 = filtered_data2.drop(columns=['Processed_Chainage'])
    #                     st.write(f"Filtered data for Chainage = {Chainage_filter2}:")
    #                     st.dataframe(filtered_data2, use_container_width=True)
    #                 else:
    #                     final_data2 = final_data2.drop(columns=['Processed_Chainage'])
    #                     st.write("Displaying whole data:")
    #                     st.dataframe(final_data1, use_container_width=True)
    #             else:
    #                 st.warning("The 'Chainage' column is not present in the RA Excel data.")

    #         except Exception as e:
    #             st.error(f"Error reading RA Excel file: {e}")

    #     elif type_b_file is None:
    #         st.warning("Please upload a RA Excel file.")

    #     st.header("Upload RSA Excel File")
    #     type_r_file = st.file_uploader("Upload RSA Excel file", type=["xlsx", "xls"])

    #     if type_r_file is not None and type_a_file is not None:
    #         with open('temp.xlsx', 'wb') as f:
    #                 # Write the uploaded file content to 'temp.xlsx'
    #                 shutil.copyfileobj(type_r_file, f)
    #         try:
    #             range_tuples = [(int(start.strip()), int(end.strip())) for r in Chainage_values1 for start, end in [r.split('-')]]
    #             rsa_df,rsa_df_new = rsa_process('temp.xlsx',range_tuples)
    #             st.write("Data from RSA Excel file:")


    #             if 'Chainage' in rsa_df.columns:
    #                 print('insode if')

    #                 rsa_df['Processed_Chainage'] = rsa_df['Chainage'].apply(preprocess_chainage)
    #                 Chainage_values_rsa = rsa_df['Processed_Chainage'].unique() 

    #                 Chainage_filter_rsa = st.selectbox("Select Chainage value to filter", ["All"] + list(Chainage_values_rsa), key="Chainage_filter_rsa")
                    
    #                 if Chainage_filter_rsa != "All":
    #                     filtered_rsa = rsa_df[rsa_df['Processed_Chainage'] == Chainage_filter_rsa]
    #                     filtered_rsa = filtered_rsa.drop(columns=['Processed_Chainage'])
    #                     st.write(f"Filtered data for Chainage = {Chainage_filter_rsa}:")
    #                     st.dataframe(filtered_rsa, use_container_width=True)
    #                 else:
    #                     rsa_df = rsa_df.drop(columns=['Processed_Chainage'])
    #                     st.write("Displaying whole data:")
    #                     st.dataframe(rsa_df, use_container_width=True)

    #         except Exception as e:
    #             st.error(f"Error reading RSA Excel file: {e}")

    #     elif type_r_file is None:
    #         st.warning("Please upload a RSA Excel file.")

    #     if type_a_file is not None and type_b_file is not None:
    #         st.header("Analyzed Data(Avenue & Median):")
    #         final_data1['Processed_Chainage'] = final_data1['Chainage'].apply(preprocess_chainage)
    #         final_data2['Processed_Chainage'] = final_data2['Chainage'].apply(preprocess_chainage)
    #         rsa_df['Processed_Chainage'] = rsa_df['Chainage'].apply(preprocess_chainage)
            
    #         Chainage_values3 = final_data1['Processed_Chainage'].unique() 
    #         Chainage_filter3 = st.selectbox("Select Chainage value to filter",["All"] + list(Chainage_values3), key="chainage_filter3")

    #         if Chainage_filter3 != "All":
    #             filtered_data1 = final_data1[final_data1['Processed_Chainage'] == Chainage_filter3]
    #             filtered_data2 = final_data2[final_data2['Processed_Chainage'] == Chainage_filter3]
    #             filtered_rsa_df = rsa_df[rsa_df['Processed_Chainage'] == Chainage_filter3]


    #             data1 = filtered_data1.copy()
    #             data2 = filtered_data2.copy()
    #             rsa_data = filtered_rsa_df.copy()

    #             data1 = data1.drop(columns=['Processed_Chainage','Road Section'])
    #             data2 = data2.drop(columns=['Processed_Chainage','Road Section'])
    #             rsa_data = rsa_data.drop(columns=['Processed_Chainage','Road Section'])



    #             # # Display the filtered data
    #             # st.write(f"Filtered Data from File 1 for Chainage = {Chainage_filter3}:")
    #             # st.dataframe(data1, use_container_width=True)
                
    #             # st.write(f"Filtered Data from File 2 for Chainage = {Chainage_filter3}:")
    #             # st.dataframe(data2, use_container_width=True)

    #             grouped_data1 = data1.groupby(['Chainage']).sum().reset_index()
    #             grouped_data2 = data2.groupby(['Chainage']).sum().reset_index()
    #             grouped_data3 = rsa_data.groupby(['Chainage']).sum().reset_index()

                

    #             transposed_data1 = grouped_data1.transpose()
    #             transposed_data2 = grouped_data2.transpose()
    #             transposed_data3 = grouped_data3.transpose()


    #             transposed_data1.columns = transposed_data1.iloc[0]
    #             transposed_data1 = transposed_data1.iloc[1:]

    #             transposed_data2.columns = transposed_data2.iloc[0]
    #             transposed_data2 = transposed_data2.iloc[1:]

    #             transposed_data3.columns = transposed_data3.iloc[0]
    #             transposed_data3 = transposed_data3.iloc[1:]

    #             transposed_data1['LHS+RHS'] = transposed_data1.sum(axis=1)
    #             transposed_data2['LHS+RHS'] = transposed_data2.sum(axis=1)
    #             transposed_data3['LHS+RHS'] = transposed_data3.sum(axis=1)


    #             gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)


    #             st.write(f"According to PIU Excel uploaded as per Approved road signage plan for Chainage = {Chainage_filter3}:")
    #             st.dataframe(transposed_data1, use_container_width=True)

    #             st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena for Chainage = {Chainage_filter3}:")
    #             st.dataframe(transposed_data2, use_container_width=True)

    #             st.write(f"GAP Analysis for Chainage = {Chainage_filter3}:")
    #             st.dataframe(gap_analysis, use_container_width=True)

    #             st.write(f"Signages according to RSA Excel uploaded for Chainage = {Chainage_filter3}:")
    #             st.dataframe(transposed_data3, use_container_width=True)

    #             #### Graphical Representation
    #             for i in range(len(transposed_data1.columns)):
    #                 combined_df = pd.DataFrame({
    #                     'PIU': transposed_data1[transposed_data1.columns[i]],
    #                     'RA': transposed_data2[transposed_data1.columns[i]],
    #                     'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                 })
    #                 combined_df = combined_df[(combined_df != 0).any(axis=1)]

    #                 if combined_df.empty:
    #                     height = 300

    #                     layout = go.Layout(
    #                         title=f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}",
    #                         barmode='group',
    #                         xaxis=dict(title='Values'),
    #                         yaxis=dict(title='Furniture Assets'),
    #                         height=height,
    #                         annotations=[
    #                             dict(
    #                                 x=0.5, y=0.5,
    #                                 xref='paper', yref='paper',
    #                                 text="There is no data to represent graphically",
    #                                 showarrow=False,
    #                                 font=dict(size=20, color='black'),
    #                                 align='center'
    #                             )
    #                         ],
    #                         bargap=0.3,
    #                     )
    #                     fig = go.Figure(data=[], layout=layout)
    #                     st.plotly_chart(fig)

    #                 else:
    #                     traces1 = []

    #                     traces1.append(go.Bar(
    #                         y=combined_df.index,
    #                         x=combined_df['Gap Analysis'],
    #                         name=f'Gap Analysis',
    #                         orientation='h',
    #                         marker=dict(color='red'),
    #                         text=combined_df['Gap Analysis'],
    #                         textposition='outside',
    #                     ))
    #                     traces1.append(go.Bar(
    #                         y=combined_df.index,
    #                         x=combined_df['RA'],
    #                         name=f'RA',
    #                         orientation='h',
    #                         marker=dict(color='green'),
    #                         text=combined_df['RA'],
    #                         textposition='outside',
    #                     ))
    #                     traces1.append(go.Bar(
    #                         y=combined_df.index,
    #                         x=combined_df['PIU'], 
    #                         name=f'PIU',
    #                         orientation='h',
    #                         marker=dict(color='blue'),
    #                         text=combined_df['PIU'],
    #                         textposition='outside',
    #                     ))



    #                     height = 300 if (len(combined_df) == 1) else len(combined_df) * 150

    #                     if i == 2:
    #                         title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[0]}(LHS + RHS)"
    #                     else:
    #                         title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}"

    #                     layout = go.Layout(
    #                         title= title,
    #                         barmode='group',
    #                         xaxis=dict(title='Values'),
    #                         yaxis=dict(title='Furniture Assets'),
    #                         height=height,
    #                         shapes=[
    #                             dict(
    #                                 type='line',
    #                                 x0=0, x1=0,
    #                                 y0=0, y1=1,
    #                                 xref='x', yref='paper',
    #                                 line=dict(
    #                                     color='black',
    #                                     width=2,
    #                                 ),
    #                             )
    #                         ],
    #                         bargap=0.4,
    #                     )
    #                     fig = go.Figure(data=traces1, layout=layout)
    #                     st.plotly_chart(fig)


    #         else:
    #             data1 = final_data1.copy()
    #             data2 = final_data2.copy()

    #             data1 = data1.drop(columns=['Chainage','Processed_Chainage','Road Section'])
    #             data2 = data2.drop(columns=['Chainage','Processed_Chainage','Road Section'])

    #             transposed_data1 = pd.DataFrame(data1.sum(axis=0))
    #             transposed_data2 = pd.DataFrame(data2.sum(axis=0))

    #             transposed_data1.columns = ['LHS + RHS']
    #             transposed_data2.columns = ['LHS + RHS']

    #             gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)

    #             st.write(f"According to PIU Excel uploaded in December 2024 as per Approved road signage plan for all Chainages")
    #             st.dataframe(transposed_data1, use_container_width=True)

    #             st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena in October 2024 for all Chainages")
    #             st.dataframe(transposed_data2, use_container_width=True)

    #             st.write(f"GAP Analysis for all Chainages")
    #             st.dataframe(gap_analysis, use_container_width=True)

    #             #### Graphical Representation
    #             for i in range(len(transposed_data1.columns)):
    #                 combined_df = pd.DataFrame({
    #                     'PIU': transposed_data1[transposed_data1.columns[i]],
    #                     'RA': transposed_data2[transposed_data1.columns[i]],
    #                     'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                 })
    #                 combined_df = combined_df[(combined_df != 0).any(axis=1)]

    #                 if combined_df.empty:
    #                     height = 300

    #                     layout = go.Layout(
    #                         title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                         barmode='group',
    #                         xaxis=dict(title='Values'),
    #                         yaxis=dict(title='Furniture Assets'),
    #                         height=height,
    #                         annotations=[
    #                             dict(
    #                                 x=0.5, y=0.5,
    #                                 xref='paper', yref='paper',
    #                                 text="There is no data to represent graphically",
    #                                 showarrow=False,
    #                                 font=dict(size=20, color='black'),
    #                                 align='center'
    #                             )
    #                         ],
    #                         bargap=0.3,
    #                     )
    #                     fig = go.Figure(data=[], layout=layout)
    #                     st.plotly_chart(fig)

    #                 else:
    #                     traces1 = []

    #                     traces1.append(go.Bar(
    #                         y=combined_df.index,
    #                         x=combined_df['Gap Analysis'],
    #                         name=f'Gap Analysis',
    #                         orientation='h',
    #                         marker=dict(color='red'),
    #                         text=combined_df['Gap Analysis'],
    #                         textposition='outside',
    #                         cliponaxis=False
    #                     ))
    #                     traces1.append(go.Bar(
    #                         y=combined_df.index,
    #                         x=combined_df['RA'],
    #                         name=f'RA',
    #                         orientation='h',
    #                         marker=dict(color='green'),
    #                         text=combined_df['RA'],
    #                         textposition='outside',
    #                         cliponaxis=False
    #                     ))
    #                     traces1.append(go.Bar(
    #                         y=combined_df.index,
    #                         x=combined_df['PIU'], 
    #                         name=f'PIU',
    #                         orientation='h',
    #                         marker=dict(color='blue'),
    #                         text=combined_df['PIU'],
    #                         textposition='outside',
    #                         cliponaxis=False
    #                     ))

    #                     height = 300 if (len(combined_df) == 1) else len(combined_df) * 150

    #                     layout = go.Layout(
    #                         title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                         barmode='group',
    #                         xaxis=dict(title='Values'),
    #                         yaxis=dict(title='Furniture Assets'),
    #                         height=height,
    #                         shapes=[
    #                             dict(
    #                                 type='line',
    #                                 x0=0, x1=0,
    #                                 y0=0, y1=1,
    #                                 xref='x', yref='paper',
    #                                 line=dict(
    #                                     color='black',
    #                                     width=2,
    #                                 ),
    #                             )
    #                         ],
    #                         bargap=0.4,
    #                     )
    #                     fig = go.Figure(data=traces1, layout=layout)
    #                     st.plotly_chart(fig)


    #         ##################### 
    #         ## Download as Word
    #         #####################
    #         if st.button('Generate Chainage Wise Report(Avenue & Median)'):
    #             with st.spinner('Generating Report...'):
    #                 data = {}
    #                 for Chainage_filter3 in ["All"] + list(Chainage_values3):
                            
    #                     if Chainage_filter3 != "All":
    #                         filtered_data1 = final_data1[final_data1['Processed_Chainage'] == Chainage_filter3]
    #                         filtered_data2 = final_data2[final_data2['Processed_Chainage'] == Chainage_filter3]

    #                         data1 = filtered_data1.copy()
    #                         data2 = filtered_data2.copy()

    #                         data1 = data1.drop(columns=['Processed_Chainage','Road Section'])
    #                         data2 = data2.drop(columns=['Processed_Chainage','Road Section'])


    #                         grouped_data1 = data1.groupby(['Chainage']).sum().reset_index()
    #                         grouped_data2 = data2.groupby(['Chainage']).sum().reset_index()

    #                         transposed_data1 = grouped_data1.transpose()
    #                         transposed_data2 = grouped_data2.transpose()

    #                         transposed_data1.columns = transposed_data1.iloc[0]
    #                         transposed_data1 = transposed_data1.iloc[1:]

    #                         transposed_data2.columns = transposed_data2.iloc[0]
    #                         transposed_data2 = transposed_data2.iloc[1:]

    #                         transposed_data1['LHS+RHS'] = transposed_data1.sum(axis=1)
    #                         transposed_data2['LHS+RHS'] = transposed_data2.sum(axis=1)

    #                         gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)

    #                         #### Graphical Representation
    #                         figs = []
    #                         for i in range(len(transposed_data1.columns)):
    #                             combined_df = pd.DataFrame({
    #                                 'PIU': transposed_data1[transposed_data1.columns[i]],
    #                                 'RA': transposed_data2[transposed_data1.columns[i]],
    #                                 'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                             })
    #                             combined_df = combined_df[(combined_df != 0).any(axis=1)]

    #                             if combined_df.empty:
    #                                 height = 300

    #                                 layout = go.Layout(
    #                                     title=f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}",
    #                                     barmode='group',
    #                                     xaxis=dict(title='Values'),
    #                                     yaxis=dict(title='Furniture Assets'),
    #                                     height=height,
    #                                     annotations=[
    #                                         dict(
    #                                             x=0.5, y=0.5,
    #                                             xref='paper', yref='paper',
    #                                             text="There is no data to represent graphically",
    #                                             showarrow=False,
    #                                             font=dict(size=20, color='black'),
    #                                             align='center'
    #                                         )
    #                                     ],
    #                                     bargap=0.2,
    #                                 )
    #                                 fig = go.Figure(data=[], layout=layout)
    #                                 figs.append(fig)

    #                             else:
    #                                 traces1 = []

    #                                 traces1.append(go.Bar(
    #                                     y=combined_df.index,
    #                                     x=combined_df['Gap Analysis'],
    #                                     name=f'Gap Analysis',
    #                                     orientation='h',
    #                                     marker=dict(color='red'),
    #                                     text=combined_df['Gap Analysis'],
    #                                     textposition='outside',
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     y=combined_df.index,
    #                                     x=combined_df['RA'],
    #                                     name=f'RA',
    #                                     orientation='h',
    #                                     marker=dict(color='green'),
    #                                     text=combined_df['RA'],
    #                                     textposition='outside',
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     y=combined_df.index,
    #                                     x=combined_df['PIU'], 
    #                                     name=f'PIU',
    #                                     orientation='h',
    #                                     marker=dict(color='blue'),
    #                                     text=combined_df['PIU'],
    #                                     textposition='outside',
    #                                 ))

                            

    #                                 height = 300 if (len(combined_df) == 1) else len(combined_df) * 120

    #                                 if i == 2:
    #                                     title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[0]}(LHS + RHS)"
    #                                 else:
    #                                     title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}"

    #                                 layout = go.Layout(
    #                                     title= title,
    #                                     barmode='group',
    #                                     xaxis=dict(title='Values'),
    #                                     yaxis=dict(title='Furniture Assets'),
    #                                     height=height,
    #                                     margin=dict(
    #                                         l=310,  # Left margin to give space for y-axis labels
    #                                     ),
    #                                     shapes=[
    #                                         dict(
    #                                             type='line',
    #                                             x0=0, x1=0,
    #                                             y0=0, y1=1,
    #                                             xref='x', yref='paper',
    #                                             line=dict(
    #                                                 color='black',
    #                                                 width=2,
    #                                             ),
    #                                         )
    #                                     ],
    #                                     bargap=0.2,
    #                                 )
    #                                 fig = go.Figure(data=traces1, layout=layout)
    #                                 figs.append(fig)

    #                         # Reset index for both DataFrames and assign a name to the new column
    #                         transposed_data1_reset = transposed_data1.reset_index()
    #                         transposed_data2_reset = transposed_data2.reset_index()
    #                         gap_analysis_reset = gap_analysis.reset_index()

    #                         # Optionally, rename the index column to 'Furniture Assets' or any other desired name
    #                         transposed_data1_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         transposed_data2_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         gap_analysis_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)

    #                         data[Chainage_filter3] = (transposed_data1_reset, transposed_data2_reset, gap_analysis_reset, fig)

    #                     else:
    #                         data1 = final_data1.copy()
    #                         data2 = final_data2.copy()

    #                         data1 = data1.drop(columns=['Chainage','Processed_Chainage','Road Section'])
    #                         data2 = data2.drop(columns=['Chainage','Processed_Chainage','Road Section'])

    #                         transposed_data1 = pd.DataFrame(data1.sum(axis=0))
    #                         transposed_data2 = pd.DataFrame(data2.sum(axis=0))

    #                         transposed_data1.columns = ['LHS + RHS']
    #                         transposed_data2.columns = ['LHS + RHS']



    #                         gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)

    #                         #### Graphical Representation
    #                         figs = []
    #                         for i in range(len(transposed_data1.columns)):
    #                             combined_df = pd.DataFrame({
    #                                 'PIU': transposed_data1[transposed_data1.columns[i]],
    #                                 'RA': transposed_data2[transposed_data1.columns[i]],
    #                                 'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                             })
    #                             combined_df = combined_df[(combined_df != 0).any(axis=1)]

    #                             if combined_df.empty:
    #                                 height = 300

    #                                 layout = go.Layout(
    #                                     title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                                     barmode='group',
    #                                     xaxis=dict(title='Values'),
    #                                     yaxis=dict(title='Furniture Assets'),
    #                                     height=height,
    #                                     margin=dict(
    #                                         l=310,
    #                                     ),
    #                                     annotations=[
    #                                         dict(
    #                                             x=0.5, y=0.5,
    #                                             xref='paper', yref='paper',
    #                                             text="There is no data to represent graphically",
    #                                             showarrow=False,
    #                                             font=dict(size=20, color='black'),
    #                                             align='center'
    #                                         )
    #                                     ],
    #                                     bargap=0.2,
    #                                 )
    #                                 fig = go.Figure(data=[], layout=layout)
    #                                 figs.append(fig)




    #                             else:
    #                                 traces1 = []

    #                                 traces1.append(go.Bar(
    #                                     y=combined_df.index,
    #                                     x=combined_df['Gap Analysis'],
    #                                     name=f'Gap Analysis',
    #                                     orientation='h',
    #                                     marker=dict(color='red'),
    #                                     text=combined_df['Gap Analysis'],
    #                                     textposition='outside',
    #                                     cliponaxis=False
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     y=combined_df.index,
    #                                     x=combined_df['RA'],
    #                                     name=f'RA',
    #                                     orientation='h',
    #                                     marker=dict(color='green'),
    #                                     text=combined_df['RA'],
    #                                     textposition='outside',
    #                                     cliponaxis=False
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     y=combined_df.index,
    #                                     x=combined_df['PIU'], 
    #                                     name=f'PIU',
    #                                     orientation='h',
    #                                     marker=dict(color='blue'),
    #                                     text=combined_df['PIU'],
    #                                     textposition='outside',
    #                                     cliponaxis=False
    #                                 ))

                            

    #                                 height = 300 if (len(combined_df) == 1) else len(combined_df) * 120

    #                                 layout = go.Layout(
    #                                     title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                                     barmode='group',
    #                                     xaxis=dict(title='Values'),
    #                                     yaxis=dict(title='           Furniture Assets           '),
    #                                     height=height,
    #                                     margin=dict(
    #                                         l=310,
    #                                     ),
    #                                     shapes=[
    #                                         dict(
    #                                             type='line',
    #                                             x0=0, x1=0,
    #                                             y0=0, y1=1,
    #                                             xref='x', yref='paper',
    #                                             line=dict(
    #                                                 color='black',
    #                                                 width=2,
    #                                             ),
    #                                         )
    #                                     ],
    #                                     bargap=0.2,
    #                                 )
    #                                 fig = go.Figure(data=traces1, layout=layout)

    #                                 figs.append(fig)
                        
    #                         # Reset index for both DataFrames and assign a name to the new column
    #                         transposed_data1_reset = transposed_data1.reset_index()
    #                         transposed_data2_reset = transposed_data2.reset_index()
    #                         gap_analysis_reset = gap_analysis.reset_index()

    #                         # Optionally, rename the index column to 'Furniture Assets' or any other desired name
    #                         transposed_data1_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         transposed_data2_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         gap_analysis_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)

    #                         data[Chainage_filter3] = (transposed_data1_reset, transposed_data2_reset, gap_analysis_reset, fig)

    #                 create_word_doc(data, file_name="Chainage_Wise_Analyzed_Data.docx")
    #                 st.success('Report generated successfully!')
    #                 with open("Chainage_Wise_Analyzed_Data.docx", "rb") as file:
    #                     st.download_button("Chainage_Wise_Analyzed_Data.docx", file, "Chainage_Wise_Analyzed_Data.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


    #     #################################################################################################################################################
    #     #################################################################################################################################################
    #     #################################################################################################################################################
    #     #################################################################################################################################################
    #     #################################################################################################################################################
    #     #################################################################################################################################################


    #         st.header("Analyzed Data(Furniture Assets):")
    #         final_data1_new['Processed_Chainage'] = final_data1_new['Chainage'].apply(preprocess_chainage)
    #         final_data2_new['Processed_Chainage'] = final_data2_new['Chainage'].apply(preprocess_chainage)
    #         Chainage_values4 = final_data1_new['Processed_Chainage'].unique() 
    #         Chainage_filter4 = st.selectbox("Select Chainage value to filter",["All"] + list(Chainage_values4), key="Chainage_filter4")

    #         if Chainage_filter4 != "All":
    #             filtered_data1 = final_data1_new[final_data1_new['Processed_Chainage'] == Chainage_filter4]
    #             filtered_data2 = final_data2_new[final_data2_new['Processed_Chainage'] == Chainage_filter4]

    #             data1 = filtered_data1.copy()
    #             data2 = filtered_data2.copy()

    #             data1 = data1.drop(columns=['Processed_Chainage','Road Section'])
    #             data2 = data2.drop(columns=['Processed_Chainage','Road Section'])



    #             # # Display the filtered data
    #             # st.write(f"Filtered Data from File 1 for Chainage = {Chainage_filter3}:")
    #             # st.dataframe(data1, use_container_width=True)
                
    #             # st.write(f"Filtered Data from File 2 for Chainage = {Chainage_filter3}:")
    #             # st.dataframe(data2, use_container_width=True)

    #             grouped_data1 = data1.groupby(['Chainage']).sum().reset_index()
    #             grouped_data2 = data2.groupby(['Chainage']).sum().reset_index()

    #             transposed_data1 = grouped_data1.transpose()
    #             transposed_data2 = grouped_data2.transpose()

    #             transposed_data1.columns = transposed_data1.iloc[0]
    #             transposed_data1 = transposed_data1.iloc[1:]

    #             transposed_data2.columns = transposed_data2.iloc[0]
    #             transposed_data2 = transposed_data2.iloc[1:]

    #             transposed_data1['LHS+RHS'] = transposed_data1.sum(axis=1)
    #             transposed_data2['LHS+RHS'] = transposed_data2.sum(axis=1)

    #             gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)


    #             st.write(f"According to PIU Excel uploaded in December 2024 as per Approved road signage plan for Chainage = {Chainage_filter4}:")
    #             st.dataframe(transposed_data1, use_container_width=True)

    #             st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena in October 2024 for Chainage = {Chainage_filter4}:")
    #             st.dataframe(transposed_data2, use_container_width=True)

    #             st.write(f"GAP Analysis for Chainage = {Chainage_filter4}:")
    #             st.dataframe(gap_analysis, use_container_width=True)

    #             #### Graphical Representation
    #             for i in range(len(transposed_data1.columns)):
    #                 combined_df = pd.DataFrame({
    #                     'PIU': transposed_data1[transposed_data1.columns[i]],
    #                     'RA': transposed_data2[transposed_data1.columns[i]],
    #                     'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                 })
    #                 combined_df = combined_df[(combined_df != 0).any(axis=1)]
    #                 x_labels = combined_df.index
    #                 index_map = {
    #                     'Chevron': 'Chevron',
    #                     'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
    #                     'Hazard': 'Hazard',
    #                     'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
    #                     'Informatory Signs': 'Informatory <br>Signs',
    #                 }

    #                 x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]
    #                 if combined_df.empty:
    #                     height = 300

    #                     layout = go.Layout(
    #                         title=f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}",
    #                         barmode='group',
    #                         xaxis=dict(
    #                             title='Furniture Assets',
    #                             tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                             ticktext=x_labels_with_br,  # Labels with line breaks
    #                             tickangle=0,  # Rotate labels for better visibility, if needed
    #                         ),
    #                         yaxis=dict(title='Values'),
    #                         # height=height,
    #                         annotations=[
    #                             dict(
    #                                 x=0.5, y=0.5,
    #                                 xref='paper', yref='paper',
    #                                 text="There is no data to represent graphically",
    #                                 showarrow=False,
    #                                 font=dict(size=20, color='black'),
    #                                 align='center'
    #                             )
    #                         ],
    #                         bargap=0.3,
    #                     )
    #                     fig = go.Figure(data=[], layout=layout)
    #                     st.plotly_chart(fig)

    #                 else:
    #                     traces1 = []
    #                     max_value = max(abs(combined_df['Gap Analysis'].max()), abs(combined_df['RA'].max()), abs(combined_df['PIU'].max()))

    #                     traces1.append(go.Bar(
    #                         x=combined_df.index,
    #                         y=combined_df['PIU'], 
    #                         name=f'PIU',
    #                         orientation='v',
    #                         marker=dict(color='blue'),
    #                         text=combined_df['PIU'],
    #                         textposition='outside',
    #                     ))
    #                     traces1.append(go.Bar(
    #                         x=combined_df.index,
    #                         y=combined_df['RA'],
    #                         name=f'RA',
    #                         orientation='v',
    #                         marker=dict(color='green'),
    #                         text=combined_df['RA'],
    #                         textposition='outside',
    #                     ))
    #                     traces1.append(go.Bar(
    #                         x=combined_df.index,
    #                         y=combined_df['Gap Analysis'],
    #                         name=f'Gap Analysis',
    #                         orientation='v',
    #                         marker=dict(color='red'),
    #                         text=combined_df['Gap Analysis'],
    #                         textposition='outside',
    #                     ))



    #                     height = 300 if (len(combined_df) == 1) else len(combined_df) * 150

    #                     if i == 2:
    #                         title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[0]}(LHS + RHS)"
    #                     else:
    #                         title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}"

    #                     layout = go.Layout(
    #                         title= title,
    #                         barmode='group',
    #                         xaxis=dict(
    #                             title='Furniture Assets',
    #                             tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                             ticktext=x_labels_with_br,  # Labels with line breaks
    #                             tickangle=0,  # Rotate labels for better visibility, if needed
    #                         ),
    #                         yaxis=dict(title='Values'),
    #                         # height=height,
    #                         shapes=[
    #                             dict(
    #                                 type='line',
    #                                 x0=0, x1=1,
    #                                 y0=0, y1=0,
    #                                 yref='y', xref='paper',
    #                                 line=dict(
    #                                     color='black',
    #                                     width=2,
    #                                 ),
    #                             )
    #                         ],
    #                         bargap=0.4,
    #                     )
    #                     fig = go.Figure(data=traces1, layout=layout)
    #                     st.plotly_chart(fig)


    #         else:
    #             data1 = final_data1_new.copy()
    #             data2 = final_data2_new.copy()

    #             data1 = data1.drop(columns=['Chainage','Processed_Chainage','Road Section'])
    #             data2 = data2.drop(columns=['Chainage','Processed_Chainage','Road Section'])

    #             transposed_data1 = pd.DataFrame(data1.sum(axis=0))
    #             transposed_data2 = pd.DataFrame(data2.sum(axis=0))

    #             transposed_data1.columns = ['LHS + RHS']
    #             transposed_data2.columns = ['LHS + RHS']

    #             gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)

    #             st.write(f"According to PIU Excel uploaded in December 2024 as per Approved road signage plan for all Chainages")
    #             st.dataframe(transposed_data1, use_container_width=True)

    #             st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena in October 2024 for all Chainages")
    #             st.dataframe(transposed_data2, use_container_width=True)

    #             st.write(f"GAP Analysis for all Chainages")
    #             st.dataframe(gap_analysis, use_container_width=True)

    #             #### Graphical Representation
    #             for i in range(len(transposed_data1.columns)):
    #                 combined_df = pd.DataFrame({
    #                     'PIU': transposed_data1[transposed_data1.columns[i]],
    #                     'RA': transposed_data2[transposed_data1.columns[i]],
    #                     'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                 })
    #                 combined_df = combined_df[(combined_df != 0).any(axis=1)]
    #                 x_labels = combined_df.index
    #                 index_map = {
    #                     'Chevron': 'Chevron',
    #                     'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
    #                     'Hazard': 'Hazard',
    #                     'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
    #                     'Informatory Signs': 'Informatory <br>Signs',
    #                 }

    #                 x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]

    #                 if combined_df.empty:
    #                     height = 300

    #                     layout = go.Layout(
    #                         title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                         barmode='group',
    #                         xaxis=dict(
    #                             title='Furniture Assets',
    #                             tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                             ticktext=x_labels_with_br,  # Labels with line breaks
    #                             tickangle=0,  # Rotate labels for better visibility, if needed
    #                         ),
    #                         yaxis=dict(title='Values'),
    #                         # height=height,
    #                         annotations=[
    #                             dict(
    #                                 x=0.5, y=0.5,
    #                                 xref='paper', yref='paper',
    #                                 text="There is no data to represent graphically",
    #                                 showarrow=False,
    #                                 font=dict(size=20, color='black'),
    #                                 align='center'
    #                             )
    #                         ],
    #                         bargap=0.3,
    #                     )
    #                     fig = go.Figure(data=[], layout=layout)
    #                     st.plotly_chart(fig)

    #                 else:
    #                     traces1 = []

    #                     traces1.append(go.Bar(
    #                         x=combined_df.index,
    #                         y=combined_df['PIU'], 
    #                         name=f'PIU',
    #                         orientation='v',
    #                         marker=dict(color='blue'),
    #                         text=combined_df['PIU'],
    #                         textposition='outside',
    #                         cliponaxis=False
    #                     ))
    #                     traces1.append(go.Bar(
    #                         x=combined_df.index,
    #                         y=combined_df['RA'],
    #                         name=f'RA',
    #                         orientation='v',
    #                         marker=dict(color='green'),
    #                         text=combined_df['RA'],
    #                         textposition='outside',
    #                         cliponaxis=False
    #                     ))
    #                     traces1.append(go.Bar(
    #                         x=combined_df.index,
    #                         y=combined_df['Gap Analysis'],
    #                         name=f'Gap Analysis',
    #                         orientation='v',
    #                         marker=dict(color='red'),
    #                         text=combined_df['Gap Analysis'],
    #                         textposition='outside',
    #                         cliponaxis=False
    #                     ))

    #                     height = 300 if (len(combined_df) == 1) else len(combined_df) * 150

    #                     layout = go.Layout(
    #                         title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                         barmode='group',
    #                         xaxis=dict(
    #                             title='Furniture Assets',
    #                             tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                             ticktext=x_labels_with_br,  # Labels with line breaks
    #                             tickangle=0,  # Rotate labels for better visibility, if needed
    #                         ),
    #                         yaxis=dict(title='Values'),
    #                         # height=height,
    #                         shapes=[
    #                             dict(
    #                                 type='line',
    #                                 x0=0, x1=1,
    #                                 y0=0, y1=0,
    #                                 yref='y', xref='paper',
    #                                 line=dict(
    #                                     color='black',
    #                                     width=2,
    #                                 ),
    #                             )
    #                         ],
    #                         bargap=0.4,
    #                     )
    #                     fig = go.Figure(data=traces1, layout=layout)
    #                     st.plotly_chart(fig)


    #         # ##################### 
    #         # ## Download as Word
    #         # #####################
    #         if st.button('Generate Chainage Wise Report(Furniture Assets)'):
    #             with st.spinner('Generating Report...'):
    #                 data = {}
    #                 for Chainage_filter4 in ["All"] + list(Chainage_values3):
                            
    #                     if Chainage_filter4 != "All":
    #                         filtered_data1 = final_data1_new[final_data1_new['Processed_Chainage'] == Chainage_filter4]
    #                         filtered_data2 = final_data2_new[final_data2_new['Processed_Chainage'] == Chainage_filter4]

    #                         data1 = filtered_data1.copy()
    #                         data2 = filtered_data2.copy()

    #                         data1 = data1.drop(columns=['Processed_Chainage','Road Section'])
    #                         data2 = data2.drop(columns=['Processed_Chainage','Road Section'])


    #                         grouped_data1 = data1.groupby(['Chainage']).sum().reset_index()
    #                         grouped_data2 = data2.groupby(['Chainage']).sum().reset_index()

    #                         transposed_data1 = grouped_data1.transpose()
    #                         transposed_data2 = grouped_data2.transpose()

    #                         transposed_data1.columns = transposed_data1.iloc[0]
    #                         transposed_data1 = transposed_data1.iloc[1:]

    #                         transposed_data2.columns = transposed_data2.iloc[0]
    #                         transposed_data2 = transposed_data2.iloc[1:]

    #                         transposed_data1['LHS+RHS'] = transposed_data1.sum(axis=1)
    #                         transposed_data2['LHS+RHS'] = transposed_data2.sum(axis=1)

    #                         gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)

    #                         #### Graphical Representation
    #                         figs = []
    #                         for i in range(len(transposed_data1.columns)):
    #                             combined_df = pd.DataFrame({
    #                                 'PIU': transposed_data1[transposed_data1.columns[i]],
    #                                 'RA': transposed_data2[transposed_data1.columns[i]],
    #                                 'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                             })
    #                             combined_df = combined_df[(combined_df != 0).any(axis=1)]
    #                             x_labels = combined_df.index
    #                             index_map = {
    #                                 'Chevron': 'Chevron',
    #                                 'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
    #                                 'Hazard': 'Hazard',
    #                                 'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
    #                                 'Informatory Signs': 'Informatory <br>Signs',
    #                             }

    #                             x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]


    #                             if combined_df.empty:
    #                                 height = 300

    #                                 layout = go.Layout(
    #                                     title=f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}",
    #                                     barmode='group',
    #                                     xaxis=dict(
    #                                         title='Furniture Assets',
    #                                         tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                                         ticktext=x_labels_with_br,  # Labels with line breaks
    #                                         tickangle=0,  # Rotate labels for better visibility, if needed
    #                                     ),
    #                                     yaxis=dict(title='Values'),
    #                                     # height=height,
    #                                     annotations=[
    #                                         dict(
    #                                             x=0.5, y=0.5,
    #                                             xref='paper', yref='paper',
    #                                             text="There is no data to represent graphically",
    #                                             showarrow=False,
    #                                             font=dict(size=20, color='black'),
    #                                             align='center'
    #                                         )
    #                                     ],
    #                                     bargap=0.3,
    #                                 )
    #                                 fig = go.Figure(data=[], layout=layout)
    #                                 figs.append(fig)

    #                             else:
    #                                 traces1 = []

    #                                 traces1.append(go.Bar(
    #                                     x=combined_df.index,
    #                                     y=combined_df['PIU'], 
    #                                     name=f'PIU',
    #                                     orientation='v',
    #                                     marker=dict(color='blue'),
    #                                     text=combined_df['PIU'],
    #                                     textposition='outside',
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     x=combined_df.index,
    #                                     y=combined_df['RA'],
    #                                     name=f'RA',
    #                                     orientation='v',
    #                                     marker=dict(color='green'),
    #                                     text=combined_df['RA'],
    #                                     textposition='outside',
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     x=combined_df.index,
    #                                     y=combined_df['Gap Analysis'],
    #                                     name=f'Gap Analysis',
    #                                     orientation='v',
    #                                     marker=dict(color='red'),
    #                                     text=combined_df['Gap Analysis'],
    #                                     textposition='outside',
    #                                 ))

                            

    #                                 height = 300 if (len(combined_df) == 1) else len(combined_df) * 120

    #                                 if i == 2:
    #                                     title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[0]}(LHS + RHS)"
    #                                 else:
    #                                     title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}"

    #                                 layout = go.Layout(
    #                                     title= title,
    #                                     barmode='group',
    #                                     xaxis=dict(
    #                                         title='Furniture Assets',
    #                                         tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                                         ticktext=x_labels_with_br,  # Labels with line breaks
    #                                         tickangle=0,  # Rotate labels for better visibility, if needed
    #                                     ),
    #                                     yaxis=dict(title='Values'),
    #                                     # height=height,
    #                                     # margin=dict(
    #                                     #     l=310,  # Left margin to give space for y-axis labels
    #                                     # ),
    #                                     shapes=[
    #                                         dict(
    #                                             type='line',
    #                                             x0=0, x1=1,
    #                                             y0=0, y1=0,
    #                                             yref='y', xref='paper',
    #                                             line=dict(
    #                                                 color='black',
    #                                                 width=2,
    #                                             ),
    #                                         )
    #                                     ],
    #                                     bargap=0.2,
    #                                 )
    #                                 fig = go.Figure(data=traces1, layout=layout)
    #                                 figs.append(fig)

    #                         # Reset index for both DataFrames and assign a name to the new column
    #                         transposed_data1_reset = transposed_data1.reset_index()
    #                         transposed_data2_reset = transposed_data2.reset_index()
    #                         gap_analysis_reset = gap_analysis.reset_index()

    #                         # Optionally, rename the index column to 'Furniture Assets' or any other desired name
    #                         transposed_data1_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         transposed_data2_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         gap_analysis_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)

    #                         data[Chainage_filter4] = (transposed_data1_reset, transposed_data2_reset, gap_analysis_reset, fig)

    #                     else:
    #                         data1 = final_data1_new.copy()
    #                         data2 = final_data2_new.copy()

    #                         data1 = data1.drop(columns=['Chainage','Processed_Chainage','Road Section'])
    #                         data2 = data2.drop(columns=['Chainage','Processed_Chainage','Road Section'])

    #                         transposed_data1 = pd.DataFrame(data1.sum(axis=0))
    #                         transposed_data2 = pd.DataFrame(data2.sum(axis=0))

    #                         transposed_data1.columns = ['LHS + RHS']
    #                         transposed_data2.columns = ['LHS + RHS']



    #                         gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)

    #                         #### Graphical Representation
    #                         figs = []
    #                         for i in range(len(transposed_data1.columns)):
    #                             combined_df = pd.DataFrame({
    #                                 'PIU': transposed_data1[transposed_data1.columns[i]],
    #                                 'RA': transposed_data2[transposed_data1.columns[i]],
    #                                 'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
    #                             })
    #                             combined_df = combined_df[(combined_df != 0).any(axis=1)]

    #                             x_labels = combined_df.index
    #                             index_map = {
    #                                 'Chevron': 'Chevron',
    #                                 'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
    #                                 'Hazard': 'Hazard',
    #                                 'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
    #                                 'Informatory Signs': 'Informatory <br>Signs',
    #                             }

    #                             x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]


    #                             if combined_df.empty:
    #                                 height = 300

    #                                 layout = go.Layout(
    #                                     title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                                     barmode='group',
    #                                     xaxis=dict(
    #                                         title='Furniture Assets',
    #                                         tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                                         ticktext=x_labels_with_br,  # Labels with line breaks
    #                                         tickangle=0,  # Rotate labels for better visibility, if needed
    #                                     ),
    #                                     yaxis=dict(title='Values'),
    #                                     # height=height,
    #                                     annotations=[
    #                                         dict(
    #                                             x=0.5, y=0.5,
    #                                             xref='paper', yref='paper',
    #                                             text="There is no data to represent graphically",
    #                                             showarrow=False,
    #                                             font=dict(size=20, color='black'),
    #                                             align='center'
    #                                         )
    #                                     ],
    #                                     bargap=0.3,
    #                                 )
    #                                 fig = go.Figure(data=[], layout=layout)
    #                                 figs.append(fig)




    #                             else:
    #                                 traces1 = []

    #                                 traces1.append(go.Bar(
    #                                     x=combined_df.index,
    #                                     y=combined_df['PIU'], 
    #                                     name=f'PIU',
    #                                     orientation='v',
    #                                     marker=dict(color='blue'),
    #                                     text=combined_df['PIU'],
    #                                     textposition='outside',
    #                                     cliponaxis=False
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     x=combined_df.index,
    #                                     y=combined_df['RA'],
    #                                     name=f'RA',
    #                                     orientation='v',
    #                                     marker=dict(color='green'),
    #                                     text=combined_df['RA'],
    #                                     textposition='outside',
    #                                     cliponaxis=False
    #                                 ))
    #                                 traces1.append(go.Bar(
    #                                     x=combined_df.index,
    #                                     y=combined_df['Gap Analysis'],
    #                                     name=f'Gap Analysis',
    #                                     orientation='v',
    #                                     marker=dict(color='red'),
    #                                     text=combined_df['Gap Analysis'],
    #                                     textposition='outside',
    #                                     cliponaxis=False
    #                                 ))

                            

    #                                 height = 300 if (len(combined_df) == 1) else len(combined_df) * 120

    #                                 layout = go.Layout(
    #                                     title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
    #                                     barmode='group',
    #                                     xaxis=dict(
    #                                         title='Furniture Assets',
    #                                         tickvals=combined_df.index,  # The positions of the ticks on the x-axis
    #                                         ticktext=x_labels_with_br,  # Labels with line breaks
    #                                         tickangle=0,  # Rotate labels for better visibility, if needed
    #                                     ),
    #                                     yaxis=dict(title='Values'),
    #                                     # height=height,
    #                                     # margin=dict(
    #                                     #     l=310,
    #                                     # ),
    #                                     shapes=[
    #                                         dict(
    #                                             type='line',
    #                                             x0=0, x1=1,
    #                                             y0=0, y1=0,
    #                                             yref='y', xref='paper',
    #                                             line=dict(
    #                                                 color='black',
    #                                                 width=2,
    #                                             ),
    #                                         )
    #                                     ],
    #                                     bargap=0.2,
    #                                 )
    #                                 fig = go.Figure(data=traces1, layout=layout)

    #                                 figs.append(fig)
                        
    #                         # Reset index for both DataFrames and assign a name to the new column
    #                         transposed_data1_reset = transposed_data1.reset_index()
    #                         transposed_data2_reset = transposed_data2.reset_index()
    #                         gap_analysis_reset = gap_analysis.reset_index()

    #                         # Optionally, rename the index column to 'Furniture Assets' or any other desired name
    #                         transposed_data1_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         transposed_data2_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)
    #                         gap_analysis_reset.rename(columns={'index': 'Furniture Assets'}, inplace=True)

    #                         data[Chainage_filter4] = (transposed_data1_reset, transposed_data2_reset, gap_analysis_reset, fig)

    #                 create_word_doc(data, file_name="Chainage_Wise_Analyzed_Data.docx")
    #                 st.success('Report generated successfully!')
    #                 with open("Chainage_Wise_Analyzed_Data.docx", "rb") as file:
    #                     st.download_button("Chainage_Wise_Analyzed_Data.docx", file, "Chainage_Wise_Analyzed_Data.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")



    if choice == 'Home':
        st.title("Furniture Chainage Report")

        st.header("Upload PIU Excel File")
        type_a_file = st.file_uploader("Upload PIU Excel file", type=["xlsx", "xls"])

        if type_a_file is not None:
            try:
                type_a_df = pd.read_excel(type_a_file, header=[0, 1, 2, 3, 4])
                st.write("Data from PIU Excel file:")
                final_data1,final_data1_new = RA_preprocess(type_a_df)

                if 'Chainage' in final_data1.columns:
                    final_data1['Processed_Chainage'] = final_data1['Chainage'].apply(preprocess_chainage)
                    Chainage_values1 = final_data1['Processed_Chainage'].unique() 

                    Chainage_filter1 = st.selectbox("Select Chainage value to filter", ["All"] + list(Chainage_values1), key="chainage_filter1")
                    
                    if Chainage_filter1 != "All":
                        filtered_data1 = final_data1[final_data1['Processed_Chainage'] == Chainage_filter1]
                        filtered_data1 = filtered_data1.drop(columns=['Processed_Chainage'])
                        st.write(f"Filtered data for Chainage = {Chainage_filter1}:")
                        st.dataframe(filtered_data1, use_container_width=True)
                    else:
                        final_data1 = final_data1.drop(columns=['Processed_Chainage'])
                        st.write("Displaying whole data:")
                        st.dataframe(final_data1, use_container_width=True)

            except Exception as e:
                st.error(f"Error reading PIU Excel file: {e}")

        elif type_a_file is None:
            st.warning("Please upload a PIU Excel file.")

        st.header("Upload RA Excel File")
        type_b_file = st.file_uploader("Upload RA Excel file", type=["xlsx", "xls"])

        if type_b_file is not None:
            try:
                type_b_df = pd.read_excel(type_b_file, header=[0, 1, 2, 3, 4])
                st.write("Data from Type RA Excel file:")
                final_data2,final_data2_new = RA_preprocess(type_b_df)

                if 'Chainage' in final_data1.columns:
                    final_data2['Processed_Chainage'] = final_data2['Chainage'].apply(preprocess_chainage)
                    Chainage_values2 = final_data2['Processed_Chainage'].unique() 

                    Chainage_filter2 = st.selectbox("Select Chainage value to filter", ["All"] + list(Chainage_values2), key="chainage_filter2")
                    
                    if Chainage_filter2 != "All":
                        filtered_data2 = final_data2[final_data2['Processed_Chainage'] == Chainage_filter2]
                        filtered_data2 = filtered_data2.drop(columns=['Processed_Chainage'])
                        st.write(f"Filtered data for Chainage = {Chainage_filter2}:")
                        st.dataframe(filtered_data2, use_container_width=True)
                    else:
                        final_data2 = final_data2.drop(columns=['Processed_Chainage'])
                        st.write("Displaying whole data:")
                        st.dataframe(final_data1, use_container_width=True)
                else:
                    st.warning("The 'Chainage' column is not present in the RA Excel data.")

            except Exception as e:
                st.error(f"Error reading RA Excel file: {e}")

        elif type_b_file is None:
            st.warning("Please upload a RA Excel file.")

        st.header("Upload RSA Excel File")
        type_r_file = st.file_uploader("Upload RSA Excel file", type=["xlsx", "xls"])
        

        if type_r_file is not None and type_a_file is not None:
            # with open('temp.xlsx', 'wb') as f:
            #         # Write the uploaded file content to 'temp.xlsx'
            #         shutil.copyfileobj(type_r_file, f)
            try:
                # range_tuples = [(int(start.strip()), int(end.strip())) for r in Chainage_values1 for start, end in [r.split('-')]]
                # rsa_df,rsa_df_new = rsa_process('temp.xlsx',range_tuples)
                range_tuples = [(int(start.strip()), int(end.strip())) for r in Chainage_values1 for start, end in [r.split('-')]]
                rsa_df,rsa_df_new = rsa_process(type_r_file,range_tuples)
                st.write("Data from RSA Excel file:")

                if 'Chainage' in rsa_df.columns:
                    print('inside if')

                    rsa_df['Processed_Chainage'] = rsa_df['Chainage'].apply(preprocess_chainage)
                    Chainage_values_rsa = rsa_df['Processed_Chainage'].unique() 

                    Chainage_filter_rsa = st.selectbox("Select Chainage value to filter", ["All"] + list(Chainage_values_rsa), key="Chainage_filter_rsa")
                    
                    if Chainage_filter_rsa != "All":
                        filtered_rsa = rsa_df[rsa_df['Processed_Chainage'] == Chainage_filter_rsa]
                        filtered_rsa = filtered_rsa.drop(columns=['Processed_Chainage'])
                        st.write(f"Filtered data for Chainage = {Chainage_filter_rsa}:")
                        st.dataframe(filtered_rsa, use_container_width=True)
                    else:
                        rsa_df = rsa_df.drop(columns=['Processed_Chainage'])
                        st.write("Displaying whole data:")
                        st.dataframe(rsa_df, use_container_width=True)

            except Exception as e:
                st.error(f"Error reading RSA Excel file: {e}")

        elif type_r_file is None:
            st.warning("Please upload a RSA Excel file.")

        if type_r_file is not None and type_a_file is not None and type_a_file is not None:
            st.header("Analyzed Data(Furniture Assets):")
            final_data1_new['Processed_Chainage'] = final_data1_new['Chainage'].apply(preprocess_chainage)
            final_data2_new['Processed_Chainage'] = final_data2_new['Chainage'].apply(preprocess_chainage)
            rsa_df_new['Processed_Chainage'] = rsa_df_new['Chainage'].apply(preprocess_chainage)

            Chainage_values4 = final_data1_new['Processed_Chainage'].unique() 
            Chainage_filter4 = st.selectbox("Select Chainage value to filter",["All"] + list(Chainage_values4), key="Chainage_filter4")

            if Chainage_filter4 != "All":
                filtered_data1 = final_data1_new[final_data1_new['Processed_Chainage'] == Chainage_filter4]
                filtered_data2 = final_data2_new[final_data2_new['Processed_Chainage'] == Chainage_filter4]
                filtered_data3 = rsa_df_new[rsa_df_new['Processed_Chainage'] == Chainage_filter4]


                data1 = filtered_data1.copy()
                data2 = filtered_data2.copy()
                data3 = filtered_data3.copy()


                data1 = data1.drop(columns=['Processed_Chainage','Road Section'])
                data2 = data2.drop(columns=['Processed_Chainage','Road Section'])
                data3 = data3.drop(columns=['Processed_Chainage','Road Section'])




                # # Display the filtered data
                # st.write(f"Filtered Data from File 1 for Chainage = {Chainage_filter3}:")
                # st.dataframe(data1, use_container_width=True)
                
                # st.write(f"Filtered Data from File 2 for Chainage = {Chainage_filter3}:")
                # st.dataframe(data2, use_container_width=True)

                grouped_data1 = data1.groupby(['Chainage']).sum().reset_index()
                grouped_data2 = data2.groupby(['Chainage']).sum().reset_index()
                grouped_data3 = data3.groupby(['Chainage']).sum().reset_index()


                transposed_data1 = grouped_data1.transpose()
                transposed_data2 = grouped_data2.transpose()
                transposed_data3 = grouped_data3.transpose()


                transposed_data1.columns = transposed_data1.iloc[0]
                transposed_data1 = transposed_data1.iloc[1:]

                transposed_data2.columns = transposed_data2.iloc[0]
                transposed_data2 = transposed_data2.iloc[1:]

                transposed_data3.columns = transposed_data3.iloc[0]
                transposed_data3 = transposed_data3.iloc[1:]

                transposed_data1['NHAI'] = transposed_data1.sum(axis=1)
                transposed_data2['AI'] = transposed_data2.sum(axis=1)
                transposed_data3['RSA'] = transposed_data3.sum(axis=1)+transposed_data2['AI']

                transposed_data1 = pd.DataFrame(transposed_data1['NHAI'])
                transposed_data2 = pd.DataFrame(transposed_data2['AI'])
                transposed_data3 = pd.DataFrame(transposed_data3['RSA'])



                gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)
                gap_analysis['NHAI(Gap Analysis)'] = gap_analysis.sum(axis=1)
                gap_analysis = pd.DataFrame(gap_analysis['NHAI(Gap Analysis)'])

                gap_analysis2 = transposed_data3.subtract(transposed_data2, fill_value=0)
                gap_analysis2['RSA(Gap Analysis)'] = gap_analysis2.sum(axis=1)
                gap_analysis2 = pd.DataFrame(gap_analysis2['RSA(Gap Analysis)'])

                final_df = pd.concat([transposed_data1, transposed_data2,transposed_data3, gap_analysis,gap_analysis2], axis=1)

                # st.write(f"According to PIU Excel uploaded in December 2024 as per Approved road signage plan for Chainage = {Chainage_filter4}:")
                # st.dataframe(transposed_data1, use_container_width=True)

                # st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena in October 2024 for Chainage = {Chainage_filter4}:")
                # st.dataframe(transposed_data2, use_container_width=True)

                # st.write(f"GAP Analysis for Chainage = {Chainage_filter4}:")
                # st.dataframe(gap_analysis, use_container_width=True)

                st.write(f"Data for Chainage = {Chainage_filter4}:")
                st.dataframe(final_df, use_container_width=True)

                #### Graphical Representation
                for i in range(len(transposed_data1.columns)):
                    combined_df = pd.DataFrame({
                        'NHAI': transposed_data1[transposed_data1.columns[i]],
                        'AI': transposed_data2[transposed_data2.columns[i]],
                        'RSA': transposed_data3[transposed_data3.columns[i]],
                        'Gap Analysis': gap_analysis[gap_analysis.columns[i]],
                        'Gap Analysis2': gap_analysis2[gap_analysis2.columns[i]],

                    })
                    combined_df = combined_df[(combined_df != 0).any(axis=1)]
                    excess_shortfall = combined_df['Gap Analysis'].to_list()
                    excess_shortfall_colours = ['green' if diff > 0 else 'red' for diff in excess_shortfall]
                    excess_shortfall2 = combined_df['Gap Analysis2'].to_list()
                    x_labels = combined_df.index
                    index_map = {
                        'Chevron': 'Chevron',
                        'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
                        'Hazard': 'Hazard',
                        'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
                        'Informatory Signs': 'Informatory <br>Signs',
                    }

                    x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]
                    if combined_df.empty:
                        height = 300

                        layout = go.Layout(
                            title=f"Graphical Representation of Analyzed Data for Chainage = {Chainage_filter4}",
                            barmode='group',
                            xaxis=dict(
                                title='Furniture Assets',
                                tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                ticktext=x_labels_with_br,  # Labels with line breaks
                                tickangle=0,  # Rotate labels for better visibility, if needed
                            ),
                            yaxis=dict(title='Values'),
                            height=height,
                            annotations=[
                                dict(
                                    x=0.5, y=0.5,
                                    xref='paper', yref='paper',
                                    text="There is no data to represent graphically",
                                    showarrow=False,
                                    font=dict(size=20, color='black'),
                                    align='center'
                                )
                            ],
                            bargap=0.3,
                        )
                        fig = go.Figure(data=[], layout=layout)
                        st.plotly_chart(fig)

                    else:
                        traces1 = []
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=combined_df['NHAI'], 
                            name=f'NHAI',
                            marker=dict(color='#CC0505'),
                            text=combined_df['NHAI'],
                            textposition='outside',
                            cliponaxis=False,
                            offsetgroup=0
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=combined_df['AI'],
                            name=f'AI',
                            marker=dict(color='#05BCFE'),
                            text=combined_df['AI'],
                            textposition='outside',
                            cliponaxis=False,
                            offsetgroup=1
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=combined_df['RSA'],
                            name=f'RSA',
                            marker=dict(color='green'),
                            text=combined_df['RSA'],
                            textposition='outside',
                            cliponaxis=False,
                            offsetgroup=2
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=[max(0, diff) for diff in excess_shortfall],
                            name=f'Shortfall(NHAI)',
                            base=combined_df['AI'],
                            marker=dict(color='#d66565'),
                            # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                            # textposition='inside',
                            cliponaxis=False,
                            offsetgroup=0
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=[min(0, diff) for diff in excess_shortfall],
                            name=f'Excess(NHAI)',
                            base=combined_df['AI'],
                            marker=dict(color='#66CCFF'),
                            # text=['{}'.format(int(diff)) if diff < 0 else '' for diff in excess_shortfall],
                            # textposition='inside',
                            cliponaxis=False,
                            offsetgroup=1
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=[max(0, diff) for diff in excess_shortfall2],
                            name=f'Shortfall(RSA)',
                            base=combined_df['AI'],
                            marker=dict(color='lightgreen'),
                            # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                            # textposition='inside',
                            cliponaxis=False,
                            offsetgroup=2
                        ))
                        # traces1.append(go.Bar(
                        #     x=combined_df.index,
                        #     y=[min(0, diff) for diff in excess_shortfall2],
                        #     name=f'Excess',
                        #     base=combined_df['RA'],
                        #     marker=dict(color='#66CCFF'),
                        #     # text=['{}'.format(int(diff)) if diff < 0 else '' for diff in excess_shortfall],
                        #     # textposition='inside',
                        #     offsetgroup=1
                        # ))

                        # annotations = []
                        # # Loop to create annotations for each bar's text
                        # for i, (piu, ra, shortfall, excess,shortfall2, excess2) in enumerate(zip(combined_df['PIU'], combined_df['RA'], excess_shortfall, excess_shortfall,excess_shortfall2,excess_shortfall2)):
                        #     # For Shortfall (positive values)
                        #     if shortfall > 0:
                        #         annotations.append(dict(
                        #             x=i - 0.35,
                        #             y=ra + shortfall/2,
                        #             text=f'+{int(shortfall)}',
                        #             textangle = 90,
                        #             showarrow=False,
                        #             font=dict(size=12, color='black'),
                        #             align='left',
                        #         ))

                        #     # For Excess (negative values)
                        #     if excess < 0:
                        #         annotations.append(dict(
                        #             x=i - 0.15,
                        #             y=ra + excess/2,
                        #             text=f'{int(excess)}',
                        #             textangle = 90,
                        #             showarrow=False,
                        #             font=dict(size=12, color='black'),
                        #             align='left',
                        #         ))
                        #     if shortfall2 > 0:
                        #         annotations.append(dict(
                        #             x=i + 0.35,
                        #             y=ra + shortfall2/2,
                        #             text=f'+{int(shortfall2)}',
                        #             textangle = 90,
                        #             showarrow=False,
                        #             font=dict(size=12, color='black'),
                        #             align='left',
                        #         ))

                        #     # For Excess (negative values)
                        #     if excess2 < 0:
                        #         annotations.append(dict(
                        #             x=i + 0.35,
                        #             y=ra + excess2/2,
                        #             text=f'{int(excess2)}',
                        #             textangle = 90,
                        #             showarrow=False,
                        #             font=dict(size=12, color='black'),
                        #             align='left',
                        #         ))

                        height = 300 if (len(combined_df) == 1) else len(combined_df) * 150
                        if i < len(transposed_data1.columns):
                            if i == 2:
                                title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[0]}(LHS + RHS)"
                            else:
                                title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}"
                        else:
                            title = f"Graphical Representation of Analyzed Data for all Chainages ({Chainage_filter4})"

                        
                        layout = go.Layout(
                            title= title,
                            barmode='group',
                            xaxis=dict(
                                title='Furniture Assets',
                                tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                ticktext=x_labels_with_br,  # Labels with line breaks
                                tickangle=0,  # Rotate labels for better visibility, if needed
                            ),
                            yaxis=dict(title='Values'),
                            # height=height,
                            shapes=[
                                dict(
                                    type='line',
                                    x0=0, x1=1,
                                    y0=0, y1=0,
                                    yref='y', xref='paper',
                                    line=dict(
                                        color='black',
                                        width=2,
                                    ),
                                )
                            ],
                            # annotations=annotations,
                            bargap=0.4,
                        )
                        fig = go.Figure(data=traces1, layout=layout)
                        st.plotly_chart(fig)


            else:
                data1 = final_data1_new.copy()
                data2 = final_data2_new.copy()
                data3 = rsa_df_new.copy()


                data1 = data1.drop(columns=['Chainage','Processed_Chainage','Road Section'])
                data2 = data2.drop(columns=['Chainage','Processed_Chainage','Road Section'])
                data3 = data3.drop(columns=['Chainage','Processed_Chainage','Road Section'])


                transposed_data1 = pd.DataFrame(data1.sum(axis=0))
                transposed_data2 = pd.DataFrame(data2.sum(axis=0))
                transposed_data3 = pd.DataFrame(data3.sum(axis=0))


                transposed_data1['NHAI'] = data1.sum(axis=0)
                transposed_data2['AI'] = data2.sum(axis=0)
                transposed_data3['RSA'] = data3.sum(axis=0)+transposed_data2['AI']

                transposed_data1 = pd.DataFrame(transposed_data1['NHAI'])
                transposed_data2 = pd.DataFrame(transposed_data2['AI'])
                transposed_data3 = pd.DataFrame(transposed_data3['RSA'])



                gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)
                gap_analysis['NHAI(Gap Analysis)'] = gap_analysis.sum(axis=1)
                gap_analysis = pd.DataFrame(gap_analysis['NHAI(Gap Analysis)'])

                gap_analysis2 = transposed_data3.subtract(transposed_data2, fill_value=0)
                gap_analysis2['RSA(Gap Analysis)'] = gap_analysis2.sum(axis=1)
                gap_analysis2 = pd.DataFrame(gap_analysis2['RSA(Gap Analysis)'])

                final_df = pd.concat([transposed_data1, transposed_data2,transposed_data3, gap_analysis,gap_analysis2], axis=1)
                # st.write(f"According to PIU Excel uploaded in December 2024 as per Approved road signage plan for all Chainages")
                # st.dataframe(transposed_data1, use_container_width=True)

                # st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena in October 2024 for all Chainages")
                # st.dataframe(transposed_data2, use_container_width=True)

                # st.write(f"GAP Analysis for all Chainages")
                # st.dataframe(gap_analysis, use_container_width=True)

                st.write(f"GAP Analysis for all Chainages")
                st.dataframe(final_df, use_container_width=True)

                #### Graphical Representation
                for i in range(len(transposed_data1.columns)):
                    combined_df = pd.DataFrame({
                        'NHAI': transposed_data1[transposed_data1.columns[i]],
                        'AI': transposed_data2[transposed_data2.columns[i]],
                        'RSA': transposed_data3[transposed_data3.columns[i]],
                        'Gap Analysis': gap_analysis[gap_analysis.columns[i]],
                        'Gap Analysis2': gap_analysis2[gap_analysis2.columns[i]],
                    })
                    combined_df = combined_df[(combined_df != 0).any(axis=1)]
                    excess_shortfall = combined_df['Gap Analysis'].to_list()
                    excess_shortfall2 = combined_df['Gap Analysis2'].to_list()
                    excess_shortfall_colours = ['green' if diff > 0 else 'red' for diff in excess_shortfall]
                    x_labels = combined_df.index
                    index_map = {
                        'Chevron': 'Chevron',
                        'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
                        'Hazard': 'Hazard',
                        'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
                        'Informatory Signs': 'Informatory <br>Signs',
                    }

                    x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]

                    if combined_df.empty:
                        height = 300

                        layout = go.Layout(
                            title=f"Graphical Representation of Analyzed Data for all Chainages ({Chainage_filter4})",
                            barmode='group',
                            xaxis=dict(
                                title='Furniture Assets',
                                tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                ticktext=x_labels_with_br,  # Labels with line breaks
                                tickangle=0,  # Rotate labels for better visibility, if needed
                            ),
                            yaxis=dict(title='Values'),
                            # height=height,
                            annotations=[
                                dict(
                                    x=0.5, y=0.5,
                                    xref='paper', yref='paper',
                                    text="There is no data to represent graphically",
                                    showarrow=False,
                                    font=dict(size=20, color='black'),
                                    align='center'
                                )
                            ],
                            bargap=0.3,
                        )
                        fig = go.Figure(data=[], layout=layout)
                        st.plotly_chart(fig)

                    else:
                        traces1 = []

                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=combined_df['NHAI'], 
                            name=f'NHAI',
                            marker=dict(color='#CC0505'),
                            text=combined_df['NHAI'],
                            textposition='outside',
                            cliponaxis=False,
                            offsetgroup=0
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=combined_df['AI'],
                            name=f'AI',
                            marker=dict(color='#05BCFE'),
                            text=combined_df['AI'],
                            textposition='outside',
                            cliponaxis=False,
                            offsetgroup=1
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=combined_df['RSA'],
                            name=f'RSA',
                            marker=dict(color='green'),
                            text=combined_df['RSA'],
                            textposition='outside',
                            cliponaxis=False,
                            offsetgroup=2
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=[max(0, diff) for diff in excess_shortfall],
                            name=f'Shortfall(NHAI)',
                            base=combined_df['AI'],
                            marker=dict(color='#d66565'),
                            # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                            # textposition='inside',
                            cliponaxis=False,
                            offsetgroup=0
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=[min(0, diff) for diff in excess_shortfall],
                            name=f'Excess(NHAI)',
                            base=combined_df['AI'],
                            marker=dict(color='#66CCFF'),
                            # text=['{}'.format(int(diff)) if diff < 0 else '' for diff in excess_shortfall],
                            # textposition='inside',
                            cliponaxis=False,
                            offsetgroup=1
                        ))
                        traces1.append(go.Bar(
                            x=combined_df.index,
                            y=[max(0, diff) for diff in excess_shortfall2],
                            name=f'Shortfall(RSA)',
                            base=combined_df['AI'],
                            marker=dict(color='lightgreen'),
                            # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                            # textposition='inside',
                            cliponaxis=False,
                            offsetgroup=2
                        ))


                        # annotations = []
                        # # Loop to create annotations for each bar's text
                        # for i, (piu, ra, shortfall, excess) in enumerate(zip(combined_df['PIU'], combined_df['RA'], excess_shortfall, excess_shortfall)):
                        #     # For Shortfall (positive values)
                        #     if shortfall > 0:
                        #         annotations.append(dict(
                        #             x=i + 0.35,
                        #             y=ra + shortfall/2,
                        #             text=f'+{int(shortfall)}(shortfall)',
                        #             textangle = 90,
                        #             showarrow=False,
                        #             font=dict(size=12, color='black'),
                        #             align='left',
                        #         ))

                        #     # For Excess (negative values)
                        #     if excess < 0:
                        #         annotations.append(dict(
                        #             x=i + 0.35,
                        #             y=ra + excess/2,
                        #             text=f'{int(excess)}(excess)',
                        #             textangle = 90,
                        #             showarrow=False,
                        #             font=dict(size=12, color='black'),
                        #             align='left',
                        #         ))

                        height = 300 if (len(combined_df) == 1) else len(combined_df) * 150

                        if i < len(transposed_data1.columns):
                            title = f"Graphical Representation of Analyzed Data for all Chainages ({Chainage_filter4})"
                        else:
                            title = f"Graphical Representation of Analyzed Data for all Chainages ({Chainage_filter4})"

                        layout = go.Layout(
                            title=title,
                            barmode='group',
                            xaxis=dict(
                                title='Furniture Assets',
                                tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                ticktext=x_labels_with_br,  # Labels with line breaks
                                tickangle=0,  # Rotate labels for better visibility, if needed
                            ),
                            yaxis=dict(title='Counts'),
                            # height=height,
                            shapes=[
                                dict(
                                    type='line',
                                    x0=0, x1=1,
                                    y0=0, y1=0,
                                    yref='y', xref='paper',
                                    line=dict(
                                        color='black',
                                        width=2,
                                    ),
                                )
                            ],
                            bargap=0.4,
                            # annotations=annotations,
                        )
                        fig = go.Figure(data=traces1, layout=layout)
                        st.plotly_chart(fig)

            # ##################### 
            # ## Download as Word
            # #####################
            if st.button('Generate Chainage Wise Report(Furniture Assets)'):
                with st.spinner('Generating Report...'):
                    data = {}
                    moretables = {}
                    morecharts = []
                    three_tables = []
                    for Chainage_filter4 in ["All"] + list(Chainage_values4):
                        
                            
                        if Chainage_filter4 != "All":
                            filtered_data1 = final_data1_new[final_data1_new['Processed_Chainage'] == Chainage_filter4]
                            filtered_data2 = final_data2_new[final_data2_new['Processed_Chainage'] == Chainage_filter4]
                            filtered_data3 = rsa_df_new[rsa_df_new['Processed_Chainage'] == Chainage_filter4]


                            data1 = filtered_data1.copy()
                            data2 = filtered_data2.copy()
                            data3 = filtered_data3.copy()


                            data1 = data1.drop(columns=['Processed_Chainage','Road Section'])
                            data2 = data2.drop(columns=['Processed_Chainage','Road Section'])
                            data3 = data3.drop(columns=['Processed_Chainage','Road Section'])


                            grouped_data1 = data1.groupby(['Chainage']).sum().reset_index()
                            grouped_data2 = data2.groupby(['Chainage']).sum().reset_index()
                            grouped_data3 = data3.groupby(['Chainage']).sum().reset_index()


                            transposed_data1 = grouped_data1.transpose()
                            transposed_data2 = grouped_data2.transpose()
                            transposed_data3 = grouped_data3.transpose()


                            transposed_data1.columns = transposed_data1.iloc[0]
                            transposed_data1 = transposed_data1.iloc[1:]

                            transposed_data2.columns = transposed_data2.iloc[0]
                            transposed_data2 = transposed_data2.iloc[1:]

                            transposed_data3.columns = transposed_data3.iloc[0]
                            transposed_data3 = transposed_data3.iloc[1:]

                            transposed_data1['NHAI'] = transposed_data1.sum(axis=1)
                            transposed_data2['AI'] = transposed_data2.sum(axis=1)
                            transposed_data3['RSA'] = transposed_data3.sum(axis=1)+transposed_data2['AI']

                            transposed_data1 = pd.DataFrame(transposed_data1['NHAI'])
                            transposed_data2 = pd.DataFrame(transposed_data2['AI'])
                            transposed_data3 = pd.DataFrame(transposed_data3['RSA'])

                            gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)
                            gap_analysis['NHAI(Gap Analysis)'] = gap_analysis.sum(axis=1)
                            gap_analysis = pd.DataFrame(gap_analysis['NHAI(Gap Analysis)'])

                            gap_analysis2 = transposed_data3.subtract(transposed_data2, fill_value=0)
                            gap_analysis2['RSA(Gap Analysis)'] = gap_analysis2.sum(axis=1)
                            gap_analysis2 = pd.DataFrame(gap_analysis2['RSA(Gap Analysis)'])

                            final_df = pd.concat([transposed_data1, transposed_data2,transposed_data3, gap_analysis,gap_analysis2], axis=1)

                            #### Graphical Representation
                            figs = []
                            for i in range(len(transposed_data1.columns)):
                                combined_df = pd.DataFrame({
                                    'NHAI': transposed_data1[transposed_data1.columns[i]],
                                    'AI': transposed_data2[transposed_data2.columns[i]],
                                    'RSA': transposed_data3[transposed_data3.columns[i]],
                                    'Gap Analysis': gap_analysis[gap_analysis.columns[i]],
                                    'Gap Analysis2': gap_analysis2[gap_analysis2.columns[i]],

                                })
                                combined_df = combined_df[(combined_df != 0).any(axis=1)]
                                excess_shortfall = combined_df['Gap Analysis'].to_list()
                                excess_shortfall_colours = ['green' if diff > 0 else 'red' for diff in excess_shortfall]
                                excess_shortfall2 = combined_df['Gap Analysis2'].to_list()
                                x_labels = combined_df.index
                                index_map = {
                                    'Chevron': 'Chevron',
                                    'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
                                    'Hazard': 'Hazard',
                                    'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
                                    'Informatory Signs': 'Informatory <br>Signs',
                                }

                                x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]


                                if combined_df.empty:
                                    height = 300

                                    layout = go.Layout(
                                        title=f"Graphical Representation of Analyzed Data for Chainage = {Chainage_filter4}",
                                        barmode='group',
                                        xaxis=dict(
                                            title='Category of Signages',
                                            tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                            ticktext=x_labels_with_br,  # Labels with line breaks
                                            tickangle=0,  # Rotate labels for better visibility, if needed
                                        ),
                                        yaxis=dict(title='Values'),
                                        # height=height,
                                        annotations=[
                                            dict(
                                                x=0.5, y=0.5,
                                                xref='paper', yref='paper',
                                                text="There is no data to represent graphically",
                                                showarrow=False,
                                                font=dict(size=20, color='black'),
                                                align='center'
                                            )
                                        ],
                                        bargap=0.3,
                                    )
                                    fig = go.Figure(data=[], layout=layout)
                                    figs.append(fig)

                                else:
                                    traces1 = []
                                    traces1.append(go.Bar(
                                        x=combined_df.index,
                                        y=combined_df['NHAI'], 
                                        name=f'NHAI Record',
                                        marker=dict(color='#fc8403'),
                                        text=combined_df['NHAI'],
                                        textposition='outside',
                                        cliponaxis=False,
                                        offsetgroup=0
                                    ))
                                    traces1.append(go.Bar(
                                        x=combined_df.index,
                                        y=combined_df['AI'],
                                        name=f'AI Survey',
                                        marker=dict(color='#037ffc'),
                                        text=combined_df['AI'],
                                        textposition='outside',
                                        cliponaxis=False,
                                        offsetgroup=1
                                    ))
                                    traces1.append(go.Bar(
                                        x=combined_df.index,
                                        y=combined_df['RSA'],
                                        name=f'RSA Recommendations',
                                        marker=dict(color='#1f8f17'),
                                        text=combined_df['RSA'],
                                        textposition='outside',
                                        cliponaxis=False,
                                        offsetgroup=2
                                    ))
                                    # traces1.append(go.Bar(
                                    #     x=combined_df.index,
                                    #     y=[max(0, diff) for diff in excess_shortfall],
                                    #     name=f'Shortfall(NHAI)',
                                    #     base=combined_df['AI'],
                                    #     marker=dict(color='#d66565'),
                                    #     # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                                    #     # textposition='inside',
                                    #     cliponaxis=False,
                                    #     offsetgroup=0
                                    # ))
                                    # traces1.append(go.Bar(
                                    #     x=combined_df.index,
                                    #     y=[min(0, diff) for diff in excess_shortfall],
                                    #     name=f'Excess(NHAI)',
                                    #     base=combined_df['AI'],
                                    #     marker=dict(color='#66CCFF'),
                                    #     # text=['{}'.format(int(diff)) if diff < 0 else '' for diff in excess_shortfall],
                                    #     # textposition='inside',
                                    #     cliponaxis=False,
                                    #     offsetgroup=1
                                    # ))
                                    # traces1.append(go.Bar(
                                    #     x=combined_df.index,
                                    #     y=[max(0, diff) for diff in excess_shortfall2],
                                    #     name=f'δRSA Recommendations',
                                    #     base=combined_df['AI'],
                                    #     marker=dict(color='lightgreen'),
                                    #     # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                                    #     # textposition='inside',
                                    #     cliponaxis=False,
                                    #     offsetgroup=2
                                    # ))

                            

                                    height = 300 if (len(combined_df) == 1) else len(combined_df) * 120

                                    if i == 2:
                                        title = f"Graphical Representation of Analyzed Data for Chainage = {Chainage_filter4}"
                                    else:
                                        title = f"Graphical Representation of Analyzed Data for Chainage = {Chainage_filter4}"

                                    layout = go.Layout(
                                        title= title,
                                        barmode='group',
                                        xaxis=dict(
                                            title='Category of Signages',
                                            tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                            ticktext=x_labels_with_br,  # Labels with line breaks
                                            tickangle=0,  # Rotate labels for better visibility, if needed
                                        ),
                                        yaxis=dict(title='Values'),
                                        # height=height,
                                        # margin=dict(
                                        #     l=310,  # Left margin to give space for y-axis labels
                                        # ),
                                        shapes=[
                                            dict(
                                                type='line',
                                                x0=0, x1=1,
                                                y0=0, y1=0,
                                                yref='y', xref='paper',
                                                line=dict(
                                                    color='black',
                                                    width=2,
                                                ),
                                            )
                                        ],
                                        bargap=0.2,
                                    )
                                    fig = go.Figure(data=traces1, layout=layout)
                                    figs.append(fig)

                            # Reset index for both DataFrames and assign a name to the new column
                            transposed_data1_reset = transposed_data1.reset_index()
                            transposed_data2_reset = transposed_data2.reset_index()
                            gap_analysis_reset = gap_analysis.reset_index()
                            final_df.columns = ['Nos. of Signages As per NHAI record', 'Nos. of Signages Based on the AI Survey', 'Total signages required including Existing and RSA recommendation (AI + Δ RSA)', 'Gap Based on NHAI record , (-) represents excess signs boards w.r.t NHAI record', 'Gap Based on RSA recommendation']
                            column_sum_all = final_df.sum()
                            final_df.loc['Total'] = column_sum_all
                            final_df_reset = final_df.reset_index()

                            # Optionally, rename the index column to 'Furniture Assets' or any other desired name
                            transposed_data1_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            transposed_data2_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            gap_analysis_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            final_df_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)

                            data[Chainage_filter4] = (final_df_reset, fig)

                        else:
                            data1 = final_data1_new.copy()
                            data2 = final_data2_new.copy()
                            data3 = rsa_df_new.copy()


                            data1 = data1.drop(columns=['Chainage','Processed_Chainage','Road Section'])
                            data2 = data2.drop(columns=['Chainage','Processed_Chainage','Road Section'])
                            data3 = data3.drop(columns=['Chainage','Processed_Chainage','Road Section'])


                            transposed_data1 = pd.DataFrame(data1.sum(axis=0))
                            transposed_data2 = pd.DataFrame(data2.sum(axis=0))
                            transposed_data3 = pd.DataFrame(data3.sum(axis=0))


                            transposed_data1['NHAI'] = data1.sum(axis=0)
                            transposed_data2['AI'] = data2.sum(axis=0)
                            transposed_data3['RSA'] = data3.sum(axis=0)+transposed_data2['AI']

                            transposed_data1 = pd.DataFrame(transposed_data1['NHAI'])
                            transposed_data2 = pd.DataFrame(transposed_data2['AI'])
                            transposed_data3 = pd.DataFrame(transposed_data3['RSA'])
                            whole_nhai = transposed_data1.copy()
                            whole_ai = transposed_data2.copy()

                            whole_nhai.columns = ['Nos. of Signages As per NHAI record']
                            whole_ai.columns = ['Nos. of Signages Based on the AI Survey'] 

                            whole_nhai.loc['Total'] = whole_nhai.sum()
                            whole_ai.loc['Total'] = whole_ai.sum()

                            # Reset index and name the new column
                            whole_nhai.reset_index(inplace=True)
                            whole_ai.reset_index(inplace=True)

                            # Rename the new index column
                            whole_nhai.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            whole_ai.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            moretables['Road Signage Inventory (as provided by NHAI)'] = whole_nhai
                            moretables['Road Signage Inventory based on AI Survey Data (conducted by IIITD)'] = whole_ai
                            three_tables.append(whole_nhai)
                            three_tables.append(whole_ai)

                            gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)
                            gap_analysis['NHAI(Gap Analysis)'] = gap_analysis.sum(axis=1)
                            gap_analysis = pd.DataFrame(gap_analysis['NHAI(Gap Analysis)'])

                            gap_analysis2 = transposed_data3.subtract(transposed_data2, fill_value=0)
                            gap_analysis2['RSA(Gap Analysis)'] = gap_analysis2.sum(axis=1)
                            gap_analysis2 = pd.DataFrame(gap_analysis2['RSA(Gap Analysis)'])

                            final_df = pd.concat([transposed_data1, transposed_data2,transposed_data3, gap_analysis,gap_analysis2], axis=1)

                            nhai_ai = pd.concat([transposed_data1, transposed_data2, gap_analysis], axis=1)
                            nhai_ai.columns = ['Nos. of Signages As per NHAI record', 'Nos. of Signages Based on the AI Survey', 'Gap Analysis']
                            column_sum = nhai_ai.sum()
                            nhai_ai.loc['Total'] = column_sum
                            nhai_ai.reset_index(inplace=True)

                            nhai_ai_graph = pd.concat([transposed_data1, transposed_data2], axis=1)
                            nhai_ai_graph.columns = ['NHAI record', 'AI Survey']
                            column_sum_nhai_ai = nhai_ai_graph.sum()
                            nhai_ai_graph.loc['Total'] = column_sum_nhai_ai
                            total_row = nhai_ai_graph.loc['Total']
                            total_row = total_row.astype(int)

                            total_graph = pd.concat([transposed_data1, transposed_data2,transposed_data3], axis=1)
                            total_graph.columns = ['NHAI record', 'AI Survey', 'RSA Recommendations']
                            column_sum_all = total_graph.sum()
                            total_graph.loc['Total'] = column_sum_all
                            total_rows = total_graph.loc['Total']
                            total_rows = total_rows.astype(int)

                            fig = go.Figure()
                            colors = ['#fc8403', '#037ffc', '#1f8f17']

                            # Add a bar for each column in the 'Total' row
                            for i, column in enumerate(total_row.index):
                                fig.add_trace(go.Bar(
                                    x=[column],  # Use column name as the x-axis value
                                    y=[total_row[column]],  # Use the value of the "Total" row for that column
                                    name=column,
                                    marker=dict(color=colors[i]),  # Cycle through the color list
                                    text=[total_row[column]],
                                    textposition='outside',
                                    cliponaxis=False,
                                ))

                            # Update layout
                            fig.update_layout(
                                title="Graphical Representation of Gap study based on NHAI data",
                                xaxis=dict(title=' '),
                                yaxis=dict(title='Values'),
                                barmode='group',
                                height=400,
                                bargap=0.3,  # Space between bars
                            )
                            morecharts.append(fig)
                            # Display the plot in Streamlit
                            st.plotly_chart(fig)


                            fig = go.Figure()
                            colors = ['#fc8403', '#037ffc', '#1f8f17']

                            # Add a bar for each column in the 'Total' row
                            for i, column in enumerate(total_rows.index):
                                fig.add_trace(go.Bar(
                                    x=[column],  # Use column name as the x-axis value
                                    y=[total_rows[column]],  # Use the value of the "Total" row for that column
                                    name=column,
                                    marker=dict(color=colors[i]),  # Cycle through the color list
                                    text=[total_rows[column]],
                                    textposition='outside',
                                    cliponaxis=False,
                                ))

                            # Update layout
                            fig.update_layout(
                                title="Graphical Representation of Gap study",
                                xaxis=dict(title=' '),
                                yaxis=dict(title='Values'),
                                barmode='group',
                                height=400,
                                bargap=0.3,  # Space between bars
                            )
                            morecharts.append(fig)
                            # Display the plot in Streamlit
                            st.plotly_chart(fig)

                            # Rename the new index column
                            nhai_ai.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            moretables['Gap study based on NHAI data'] = nhai_ai
                            three_tables.append(nhai_ai)


                            #### Graphical Representation
                            figs = []
                            for i in range(len(transposed_data1.columns)):
                                combined_df = pd.DataFrame({
                                    'NHAI': transposed_data1[transposed_data1.columns[i]],
                                    'AI': transposed_data2[transposed_data2.columns[i]],
                                    'RSA': transposed_data3[transposed_data3.columns[i]],
                                    'Gap Analysis': gap_analysis[gap_analysis.columns[i]],
                                    'Gap Analysis2': gap_analysis2[gap_analysis2.columns[i]],
                                })
                                combined_df = combined_df[(combined_df != 0).any(axis=1)]
                                excess_shortfall = combined_df['Gap Analysis'].to_list()
                                excess_shortfall2 = combined_df['Gap Analysis2'].to_list()
                                excess_shortfall_colours = ['green' if diff > 0 else 'red' for diff in excess_shortfall]
                                x_labels = combined_df.index
                                index_map = {
                                    'Chevron': 'Chevron',
                                    'Cautionary Warning Signs': 'Cautionary <br>Warning Signs',
                                    'Hazard': 'Hazard',
                                    'Prohibitory Mandatory Signs': 'Prohibitory <br>Mandatory Signs',
                                    'Informatory Signs': 'Informatory <br>Signs',
                                }

                                x_labels_with_br = [index_map.get(label, label) for label in combined_df.index]


                                if combined_df.empty:
                                    height = 300

                                    layout = go.Layout(
                                        title=f"Graphical Representation of Analyzed Data for all Chainages",
                                        barmode='group',
                                        xaxis=dict(
                                            title='Category of Signages',
                                            tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                            ticktext=x_labels_with_br,  # Labels with line breaks
                                            tickangle=0,  # Rotate labels for better visibility, if needed
                                        ),
                                        yaxis=dict(title='Values'),
                                        # height=height,
                                        annotations=[
                                            dict(
                                                x=0.5, y=0.5,
                                                xref='paper', yref='paper',
                                                text="There is no data to represent graphically",
                                                showarrow=False,
                                                font=dict(size=20, color='black'),
                                                align='center'
                                            )
                                        ],
                                        bargap=0.3,
                                    )
                                    fig = go.Figure(data=[], layout=layout)
                                    figs.append(fig)




                                else:
                                    traces1 = []

                                    traces1.append(go.Bar(
                                        x=combined_df.index,
                                        y=combined_df['NHAI'], 
                                        name=f'NHAI Record',
                                        marker=dict(color='#fc8403'),
                                        text=combined_df['NHAI'],
                                        textposition='outside',
                                        cliponaxis=False,
                                        offsetgroup=0
                                    ))
                                    traces1.append(go.Bar(
                                        x=combined_df.index,
                                        y=combined_df['AI'],
                                        name=f'AI Survey',
                                        marker=dict(color='#037ffc'),
                                        text=combined_df['AI'],
                                        textposition='outside',
                                        cliponaxis=False,
                                        offsetgroup=1
                                    ))
                                    traces1.append(go.Bar(
                                        x=combined_df.index,
                                        y=combined_df['RSA'],
                                        name=f'RSA Recommendations',
                                        marker=dict(color='#1f8f17'),
                                        text=combined_df['RSA'],
                                        textposition='outside',
                                        cliponaxis=False,
                                        offsetgroup=2
                                    ))
                                    # traces1.append(go.Bar(
                                    #     x=combined_df.index,
                                    #     y=[max(0, diff) for diff in excess_shortfall],
                                    #     name=f'Shortfall(NHAI)',
                                    #     base=combined_df['AI'],
                                    #     marker=dict(color='#de7c7c'),
                                    #     # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                                    #     # textposition='inside',
                                    #     cliponaxis=False,
                                    #     offsetgroup=0
                                    # ))
                                    # traces1.append(go.Bar(
                                    #     x=combined_df.index,
                                    #     y=[min(0, diff) for diff in excess_shortfall],
                                    #     name=f'Excess(NHAI)',
                                    #     base=combined_df['AI'],
                                    #     marker=dict(color='#84cff5'),
                                    #     # text=['{}'.format(int(diff)) if diff < 0 else '' for diff in excess_shortfall],
                                    #     # textposition='inside',
                                    #     cliponaxis=False,
                                    #     offsetgroup=1
                                    # ))
                                    # traces1.append(go.Bar(
                                    #     x=combined_df.index,
                                    #     y=[max(0, diff) for diff in excess_shortfall2],
                                    #     name=f'δRSA Recommendations',
                                    #     base=combined_df['AI'],
                                    #     marker=dict(color='#4bad51'),
                                    #     # text=['+{}'.format(int(diff)) if diff > 0 else '' for diff in excess_shortfall],
                                    #     # textposition='inside',
                                    #     cliponaxis=False,
                                    #     offsetgroup=2
                                    # ))


                            

                                    height = 300 if (len(combined_df) == 1) else len(combined_df) * 120

                                    layout = go.Layout(
                                        title=f"Graphical Representation of Analyzed Data for all Chainages",
                                        barmode='group',
                                        xaxis=dict(
                                            title='Category of Signages',
                                            tickvals=combined_df.index,  # The positions of the ticks on the x-axis
                                            ticktext=x_labels_with_br,  # Labels with line breaks
                                            tickangle=0,  # Rotate labels for better visibility, if needed
                                        ),
                                        yaxis=dict(title='Values'),
                                        # height=height,
                                        # margin=dict(
                                        #     l=310,
                                        # ),
                                        shapes=[
                                            dict(
                                                type='line',
                                                x0=0, x1=1,
                                                y0=0, y1=0,
                                                yref='y', xref='paper',
                                                line=dict(
                                                    color='black',
                                                    width=2,
                                                ),
                                            )
                                        ],
                                        bargap=0.2,
                                    )
                                    fig = go.Figure(data=traces1, layout=layout)

                                    figs.append(fig)
                        
                            # Reset index for both DataFrames and assign a name to the new column
                            transposed_data1_reset = transposed_data1.reset_index()
                            transposed_data2_reset = transposed_data2.reset_index()
                            gap_analysis_reset = gap_analysis.reset_index()
                            final_df.columns = ['Nos. of Signages As per NHAI record', 'Nos. of Signages Based on the AI Survey', 'Total signages required including Existing and RSA recommendation (AI + Δ RSA)', 'Gap Based on NHAI record , (-) represents excess signs boards w.r.t NHAI record', 'Gap Based on RSA recommendation']
                            column_sum_all = final_df.sum()
                            final_df.loc['Total'] = column_sum_all
                            final_df_reset = final_df.reset_index()

                            # Optionally, rename the index column to 'Furniture Assets' or any other desired name
                            transposed_data1_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            transposed_data2_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            gap_analysis_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            final_df_reset.rename(columns={'index': 'Category of Signages'}, inplace=True)
                            Gap_study_report  = final_df_reset.copy()


                            data[Chainage_filter4] = (final_df_reset, fig)

                    doc_stream = create_word_doc_new(three_tables,Gap_study_report,moretables,morecharts, data, file_name="Chainage_Wise_Analyzed_Data.docx")
                    st.success('Report generated successfully!')
                    st.download_button("Chainage_Wise_Analyzed_Data.docx", doc_stream, "Chainage_Wise_Analyzed_Data.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")




if __name__ == "__main__":
    main()
