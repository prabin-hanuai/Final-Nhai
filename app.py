import streamlit as st
import pandas as pd
from functions import RA_preprocess, preprocess_chainage
import plotly.graph_objects as go


# Set up the title of the app
st.title("Furniture Chainage Report")

st.header("Upload PIU Excel File")
type_a_file = st.file_uploader("Upload PIU Excel file", type=["xlsx", "xls"])

if type_a_file is not None:
    try:
        type_a_df = pd.read_excel(type_a_file, header=[0, 1, 2, 3, 4])
        st.write("Data from PIU Excel file:")
        final_data1 = RA_preprocess(type_a_df)

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
        final_data2 = RA_preprocess(type_b_df)

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

if type_a_file is not None and type_b_file is not None:
    st.header("Analyzed Data:")
    final_data1['Processed_Chainage'] = final_data1['Chainage'].apply(preprocess_chainage)
    final_data2['Processed_Chainage'] = final_data2['Chainage'].apply(preprocess_chainage)
    Chainage_values3 = final_data1['Processed_Chainage'].unique() 
    Chainage_filter3 = st.selectbox("Select Chainage value to filter",["All"] + list(Chainage_values3), key="chainage_filter3")

    if Chainage_filter3 != "All":
        filtered_data1 = final_data1[final_data1['Processed_Chainage'] == Chainage_filter3]
        filtered_data2 = final_data2[final_data2['Processed_Chainage'] == Chainage_filter3]

        data1 = filtered_data1.copy()
        data2 = filtered_data2.copy()

        data1 = data1.drop(columns=['Processed_Chainage','Road Section'])
        data2 = data2.drop(columns=['Processed_Chainage','Road Section'])



        # # Display the filtered data
        # st.write(f"Filtered Data from File 1 for Chainage = {Chainage_filter3}:")
        # st.dataframe(data1, use_container_width=True)
        
        # st.write(f"Filtered Data from File 2 for Chainage = {Chainage_filter3}:")
        # st.dataframe(data2, use_container_width=True)

        grouped_data1 = data1.groupby(['Chainage']).sum().reset_index()
        grouped_data2 = data2.groupby(['Chainage']).sum().reset_index()

        transposed_data1 = grouped_data1.transpose()
        transposed_data2 = grouped_data2.transpose()

        transposed_data1.columns = transposed_data1.iloc[0]
        transposed_data1 = transposed_data1.iloc[1:]

        transposed_data2.columns = transposed_data2.iloc[0]
        transposed_data2 = transposed_data2.iloc[1:]

        transposed_data1['LHS+RHS'] = transposed_data1.sum(axis=1)
        transposed_data2['LHS+RHS'] = transposed_data2.sum(axis=1)

        gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)


        st.write(f"According to PIU Excel uploaded in December 2024 as per Approved road signage plan for Chainage = {Chainage_filter3}:")
        st.dataframe(transposed_data1, use_container_width=True)

        st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena in October 2024 for Chainage = {Chainage_filter3}:")
        st.dataframe(transposed_data2, use_container_width=True)

        st.write(f"GAP Analysis for Chainage = {Chainage_filter3}:")
        st.dataframe(gap_analysis, use_container_width=True)

        #### Graphical Representation
        for i in range(len(transposed_data1.columns)):
            combined_df = pd.DataFrame({
                'PIU': transposed_data1[transposed_data1.columns[i]],
                'RA': transposed_data2[transposed_data1.columns[i]],
                'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
            })
            combined_df = combined_df[(combined_df != 0).any(axis=1)]

            if combined_df.empty:
                height = 300

                layout = go.Layout(
                    title=f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}",
                    barmode='group',
                    xaxis=dict(title='Values'),
                    yaxis=dict(title='Furniture Assets'),
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
                    y=combined_df.index,
                    x=combined_df['Gap Analysis'],
                    name=f'Gap Analysis',
                    orientation='h',
                    marker=dict(color='red'),
                    text=combined_df['Gap Analysis'],
                    textposition='outside',
                ))
                traces1.append(go.Bar(
                    y=combined_df.index,
                    x=combined_df['RA'],
                    name=f'RA',
                    orientation='h',
                    marker=dict(color='green'),
                    text=combined_df['RA'],
                    textposition='outside',
                ))
                traces1.append(go.Bar(
                    y=combined_df.index,
                    x=combined_df['PIU'], 
                    name=f'PIU',
                    orientation='h',
                    marker=dict(color='blue'),
                    text=combined_df['PIU'],
                    textposition='outside',
                ))

        

                height = 300 if (len(combined_df) == 1) else len(combined_df) * 150

                if i == 2:
                    title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[0]}(LHS + RHS)"
                else:
                    title = f"Graphical Representation of Analyzed Data for Chainage = {transposed_data1.columns[i]}"

                layout = go.Layout(
                    title= title,
                    barmode='group',
                    xaxis=dict(title='Values'),
                    yaxis=dict(title='Furniture Assets'),
                    height=height,
                    shapes=[
                        dict(
                            type='line',
                            x0=0, x1=0,
                            y0=0, y1=1,
                            xref='x', yref='paper',
                            line=dict(
                                color='black',
                                width=2,
                            ),
                        )
                    ],
                    bargap=0.4,
                )
                fig = go.Figure(data=traces1, layout=layout)
                st.plotly_chart(fig)
    else:
        data1 = final_data1.copy()
        data2 = final_data2.copy()

        data1 = data1.drop(columns=['Chainage','Processed_Chainage','Road Section'])
        data2 = data2.drop(columns=['Chainage','Processed_Chainage','Road Section'])

        transposed_data1 = pd.DataFrame(data1.sum(axis=0))
        transposed_data2 = pd.DataFrame(data2.sum(axis=0))

        transposed_data1.columns = ['LHS + RHS']
        transposed_data2.columns = ['LHS + RHS']



        gap_analysis = transposed_data1.subtract(transposed_data2, fill_value=0)

        st.write(f"According to PIU Excel uploaded in December 2024 as per Approved road signage plan for all Chainages")
        st.dataframe(transposed_data1, use_container_width=True)

        st.write(f"Signages according to AI Survey undertaken by IIIT-D RoadAthena in October 2024 for all Chainages")
        st.dataframe(transposed_data2, use_container_width=True)

        st.write(f"GAP Analysis for all Chainages")
        st.dataframe(gap_analysis, use_container_width=True)

        #### Graphical Representation
        for i in range(len(transposed_data1.columns)):
            combined_df = pd.DataFrame({
                'PIU': transposed_data1[transposed_data1.columns[i]],
                'RA': transposed_data2[transposed_data1.columns[i]],
                'Gap Analysis': gap_analysis[transposed_data1.columns[i]],
            })
            combined_df = combined_df[(combined_df != 0).any(axis=1)]

            if combined_df.empty:
                height = 300

                layout = go.Layout(
                    title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
                    barmode='group',
                    xaxis=dict(title='Values'),
                    yaxis=dict(title='Furniture Assets'),
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
                    y=combined_df.index,
                    x=combined_df['Gap Analysis'],
                    name=f'Gap Analysis',
                    orientation='h',
                    marker=dict(color='red'),
                    text=combined_df['Gap Analysis'],
                    textposition='outside',
                ))
                traces1.append(go.Bar(
                    y=combined_df.index,
                    x=combined_df['RA'],
                    name=f'RA',
                    orientation='h',
                    marker=dict(color='green'),
                    text=combined_df['RA'],
                    textposition='outside',
                ))
                traces1.append(go.Bar(
                    y=combined_df.index,
                    x=combined_df['PIU'], 
                    name=f'PIU',
                    orientation='h',
                    marker=dict(color='blue'),
                    text=combined_df['PIU'],
                    textposition='outside',
                ))

        

                height = 300 if (len(combined_df) == 1) else len(combined_df) * 150

                layout = go.Layout(
                    title=f"Graphical Representation of Analyzed Data for all Chainages ({transposed_data1.columns[i]})",
                    barmode='group',
                    xaxis=dict(title='Values'),
                    yaxis=dict(title='Furniture Assets'),
                    height=height,
                    shapes=[
                        dict(
                            type='line',
                            x0=0, x1=0,
                            y0=0, y1=1,
                            xref='x', yref='paper',
                            line=dict(
                                color='black',
                                width=2,
                            ),
                        )
                    ],
                    bargap=0.4,
                )
                fig = go.Figure(data=traces1, layout=layout)
                st.plotly_chart(fig)





        
