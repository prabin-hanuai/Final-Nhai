import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, gaussian_kde
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import plotly.graph_objects as go
import plotly.express as px


st.set_page_config(
    page_title="Analysis of Pavement and Furniture Reports",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def process_excel_file(excel_file):
    # Read the Excel file
    excel_file = pd.ExcelFile(excel_file)
    sheet_names = excel_file.sheet_names
    
    data = {}
    for sheet in sheet_names:
        try:
            # First read to find the column
            df = pd.read_excel(excel_file, sheet_name=sheet, header=None)
            target_col = None
            
            # Find the column containing "Existing Chainage (m)"
            for col in df.columns:
                if df[col].astype(str).str.contains('Existing Chainage \(m\)').any():
                    target_col = col
                    break
            
            if target_col is not None:
                # Read the entire sheet with multi-index header
                df_full = pd.read_excel(excel_file, 
                                      sheet_name=sheet,
                                      header=[4, 5])
                
                # Select the columns after reading
                selected_cols = df_full.columns[target_col:target_col + 11]
                df_final = df_full[selected_cols].copy()
                df_final.columns = ['Chainage From',
                                    'Chainage To',
                                    'Length (m)',
                                    'Cracking Area(Area in Sq m)',
                                    'Cracking Area (Area in %)',
                                    'Cracking Area(Rating)',
                                    'Cracking Area(Weighted Rating)',
                                    'Vinci Density',
                                    'drop',
                                    'RoadAthena detected',
                                    'Roadathena Density']
                df_final.dropna(subset=['Chainage From', 'Chainage To'], inplace=True)
                df_final['Type'] = sheet
                df_final.drop(columns=['drop'], inplace=True)
                df_final['Vinci Density'] = df_final['Vinci Density'] * 100
                df_final['Roadathena Density'] = df_final['Roadathena Density'] * 100
                data[sheet] = df_final
                
        except Exception as e:
            st.error(f"Error processing sheet {sheet}: {str(e)}")
    
    # Merge all DataFrames
    merged_df = pd.concat(data.values(), axis=0, ignore_index=True)
    
    # Add the new Chainage column
    merged_df['Chainage'] = merged_df['Chainage From'].astype(int).astype(str) + '-' + merged_df['Chainage To'].astype(int).astype(str)
    
    # Define columns to exclude from NaN filling
    exclude_cols = ['Chainage From', 'Chainage To', 'Length (m)', 'Type', 'Chainage']
    fill_cols = [col for col in merged_df.columns if col not in exclude_cols]
    
    # Fill NaN values with 0 only in specified columns
    merged_df[fill_cols] = merged_df[fill_cols].fillna(0)
    
    return merged_df

def show_developer_page():
    st.title("Developer Page")
    st.write("This page contains developer information and tools.")
    
    # Add developer page content here
    st.subheader("About")
    st.write("This application was developed to process and analyze Excel data.")
    
    st.subheader("Technical Details")
    st.write("- Built with Streamlit")
    st.write("- Uses Pandas for data processing")
    st.write("- Supports Excel file processing")

def calculate_metrics(df):
    try:
        # Handle division by zero in relative error calculation
        epsilon = 1e-10
        
        # Basic correlations
        pearson_corr = df['Vinci Density'].corr(df['Roadathena Density'], method='pearson')
        spearman_corr = df['Vinci Density'].corr(df['Roadathena Density'], method='spearman')
        
        # Error metrics
        mae = np.mean(np.abs(df['Vinci Density'] - df['Roadathena Density']))
        mse = np.mean((df['Vinci Density'] - df['Roadathena Density'])**2)
        rmse = np.sqrt(mse)
        
        # Relative error (avoiding infinity)
        relative_error = np.where(df['Vinci Density'] != 0,
                                abs(df['Vinci Density'] - df['Roadathena Density']) / (df['Vinci Density'] + epsilon) * 100,
                                0)
        mean_relative_error = np.mean(relative_error)
        
        # Calculate other metrics
        angles = np.degrees(np.arctan2(df['Roadathena Density'], df['Vinci Density']))
        zero_zero_mask = (df['Roadathena Density'] == 0) & (df['Vinci Density'] == 0)
        angle_mask = ((35 <= angles) & (angles <= 55)) | \
                     (np.isclose(angles, 35, rtol=1e-10)) | \
                     (np.isclose(angles, 55, rtol=1e-10))
        good_points = zero_zero_mask | angle_mask
        total_points = len(df)
        good_points_count = np.sum(good_points)
        agreement = good_points_count / total_points
        r_squared = r2_score(df['Vinci Density'], df['Roadathena Density'])
        
        return (pearson_corr, spearman_corr, mae, mse, rmse, mean_relative_error, 
                agreement, good_points_count, total_points, r_squared)
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return tuple([np.nan] * 10)  # Return NaN for all metrics

def show_main_page():
    st.title("Analysis of Pavement and Furniture Reports ")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])
    
    if uploaded_file is not None:
        try:
            # Process the file
            df = process_excel_file(uploaded_file)
            
            st.subheader("Filters")
            col1, col2, col3 = st.columns([1, 1, 1]) 
            
            with col1:
                chainage_options = ['All'] + list(df['Chainage'].unique())
                selected_chainage = st.selectbox('Select Chainage', chainage_options)
            
            with col2:
                type_options = ['All'] + list(df['Type'].unique())
                selected_type = st.selectbox('Select Type', type_options)
            

            filtered_df = df.copy()
            if selected_chainage != 'All':
                filtered_df = filtered_df[filtered_df['Chainage'] == selected_chainage]
            if selected_type != 'All':
                filtered_df = filtered_df[filtered_df['Type'] == selected_type]


            st.subheader("Processed Data")
            # filtered_df = filtered_df[(filtered_df["Vinci Density"] > 0) | (filtered_df["Roadathena Density"] > 0)]
            st.dataframe(filtered_df, use_container_width=True)


            # Add toggle for Chainage-wise comparison
            show_chainage_comparison = st.toggle('Show Chainage-wise Density Comparison', value=False)
            
            if show_chainage_comparison:
                st.subheader("Chainage-wise Density Comparison")
                st.write("""
                This scatter plot shows how density measurements vary along the data points:
                - Circle markers: Vinci measurements (blue)
                - X markers: Roadathena measurements (red)
                - Hover over points to see detailed information
                - Compare measurements at each chainage point
                """)

                # Interactive Line plot with enhanced hover info
                line_fig = go.Figure()
                line_fig.add_trace(go.Scatter(
                    x=list(range(len(filtered_df))),
                    y=filtered_df["Vinci Density"],
                    mode='markers',
                    name='Vinci Density (Expert)',
                    marker={
                        'symbol': 'circle',
                        'color': 'blue',
                        'size': 8
                    },
                    text=filtered_df.apply(
                        lambda row: f"Vinci (Expert):<br>"
                                  f"Type: {row['Type']}<br>"
                                  f"Chainage: {row['Chainage']}<br>"
                                  f"Density: {row['Vinci Density']:.2f}",
                        axis=1
                    ),
                    hoverinfo='text'
                ))
                line_fig.add_trace(go.Scatter(
                    x=list(range(len(filtered_df))),
                    y=filtered_df["Roadathena Density"],
                    mode='markers',
                    name='Roadathena Density (AI)',
                    marker={
                        'symbol': 'x',
                        'color': 'rgba(255, 0, 0, 0.7)',  # Red with some transparency
                        'size': 8,
                    },
                    text=filtered_df.apply(
                        lambda row: f"Roadathena (AI):<br>"
                                  f"Type: {row['Type']}<br>"
                                  f"Chainage: {row['Chainage']}<br>"
                                  f"Density: {row['Roadathena Density']:.2f}",
                        axis=1
                    ),
                    hoverinfo='text'
                ))

                line_fig.update_layout(
                    title='Comparison of Vinci and Roadathena Densities Over Data Points',
                    xaxis_title='Data Point Index',
                    yaxis_title='Density',
                    plot_bgcolor='white',
                    hovermode='closest',
                    showlegend=True,
                    legend={'orientation': 'h', 'y': -0.2},
                    margin={'b': 100},
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='lightgray'
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='lightgray'
                    )
                )
                st.plotly_chart(line_fig, use_container_width=True)

            # st.subheader('My graphs')
            # # Compute correlation
            # pearson_corr, _ = pearsonr(filtered_df["Vinci Density"], filtered_df["Roadathena Density"])
            # spearman_corr, _ = spearmanr(filtered_df["Vinci Density"], filtered_df["Roadathena Density"])

            # # Compute error metrics
            # mae = mean_absolute_error(filtered_df["Vinci Density"], filtered_df["Roadathena Density"])
            # mse = mean_squared_error(filtered_df["Vinci Density"], filtered_df["Roadathena Density"])
            # rmse = np.sqrt(mse)
            # r2 = r2_score(filtered_df["Vinci Density"], filtered_df["Roadathena Density"])

            # st.metric(f"Pearson Correlation: ",f"{pearson_corr:.4f}")
            # st.metric(f"Spearman Correlation: ",f"{spearman_corr:.4f}")
            # st.metric(f"Mean Absolute Error (MAE):",f" {mae:.6f}")
            # st.metric(f"Mean Squared Error (MSE): ",f"{mse:.6f}")
            # st.metric(f"Root Mean Squared Error (RMSE):",f" {rmse:.6f}")
            # st.metric(f"R-squared (R2):",f" {r2:.4f}")

            # # Interactive Scatter plot
            # scatter_fig = {
            #     'data': [{
            #         'x': filtered_df["Vinci Density"],
            #         'y': filtered_df["Roadathena Density"],
            #         'mode': 'markers',
            #         'type': 'scatter',
            #         'name': 'Density Points',
            #         'text': filtered_df.apply(
            #             lambda row: f"Type: {row['Type']}<br>Chainage: {row['Chainage']}<br>Vinci: {row['Vinci Density']:.2f}<br>Roadathena: {row['Roadathena Density']:.2f}",
            #             axis=1
            #         ),
            #         'hoverinfo': 'text',
            #         'marker': {'size': 8, 'opacity': 0.7}
            #     }],
            #     'layout': {
            #         'title': 'Scatter Plot of Vinci Density vs Roadathena Density',
            #         'xaxis': {'title': 'Vinci Density (Expert)', 'gridcolor': 'lightgray'},
            #         'yaxis': {'title': 'Roadathena Density (AI)', 'gridcolor': 'lightgray'},
            #         'plot_bgcolor': 'white'
            #     }
            # }
            # st.plotly_chart(scatter_fig, use_container_width=True)

            # # Interactive Box plot
            # box_fig = go.Figure()
            # for density_type in ['Vinci Density', 'Roadathena Density']:
            #     for type_val in filtered_df['Type'].unique():
            #         box_fig.add_trace(go.Box(
            #             y=filtered_df[filtered_df['Type'] == type_val][density_type],
            #             name=type_val,
            #             legendgroup=density_type,
            #             boxmean=True,
            #             legendgrouptitle_text=density_type
            #         ))

            # box_fig.update_layout(
            #     title='Box Plot of Vinci vs Roadathena Density by Type',
            #     yaxis_title='Density',
            #     boxmode='group',
            #     plot_bgcolor='white',
            #     showlegend=True
            # )
            # st.plotly_chart(box_fig, use_container_width=True)

            # # Residual plot to check errors visually
            residuals = filtered_df["Roadathena Density"] - filtered_df["Vinci Density"]
            # hist_fig = go.Figure()
            # hist_fig.add_trace(go.Histogram(
            #     x=residuals,
            #     name='Residuals',
            #     nbinsx=30,
            #     histnorm='probability density'
            # ))

            # # Add KDE as a line
            # kde = gaussian_kde(residuals)
            # x_range = np.linspace(residuals.min(), residuals.max(), 100)
            # hist_fig.add_trace(go.Scatter(
            #     x=x_range,
            #     y=kde(x_range),
            #     mode='lines',
            #     name='KDE',
            #     line={'color': 'red'}
            # ))

            # hist_fig.update_layout(
            #     title='Residual Distribution of AI vs Expert Densities',
            #     xaxis_title='Residuals (AI - Expert)',
            #     yaxis_title='Density',
            #     plot_bgcolor='white'
            # )
            # st.plotly_chart(hist_fig, use_container_width=True)

            

            # # Line plot of residuals vs index with hover details
            # fig = px.line(filtered_df, x=filtered_df.index, y=residuals, title="Residuals vs Index", 
            #             labels={"y": "Residuals (AI - Expert)", "x": "Index"},
            #             hover_data={"Type": True, "Chainage From": True, "Chainage To": True})
            # # fig.show()
            # st.plotly_chart(fig, use_container_width=True)




            
            # Add Density Analysis section with explanations
            st.subheader("Density Analysis")
            
            # Calculate metrics including point counts
            pearson_corr, spearman_corr, mae, mse, rmse, mean_relative_error, agreement, good_points_count, total_points, r_squared = calculate_metrics(filtered_df)
            
            # Display metrics with explanations
            st.write("### Statistical Metrics")
            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                st.metric("Pearson Correlation", f"{pearson_corr:.3f}")
                st.markdown("""
                **Formula:** r = Σ((x-μx)(y-μy)) / (σx σy)
                - Measures linear correlation
                - Sensitive to outliers
                - Range: [-1, 1]
                """)

            with metric_col2:
                st.metric("Spearman Correlation", f"{spearman_corr:.3f}")
                st.markdown("""
                **Formula:** ρ = 1 - (6Σd²)/(n(n²-1))
                - Rank-based correlation
                - Less sensitive to outliers
                - Range: [-1, 1]
                """)

            with metric_col3:
                st.metric("Mean Absolute Error", f"{mae:.3f}")
                st.markdown("""
                **Formula:** MAE = (1/n)Σ|yi - ŷi|
                - Average absolute differences
                - Same unit as measurements
                - Range: [0, ∞)
                """)

            st.write("### Error Metrics")
            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                st.metric("Mean Squared Error", f"{mse:.3f}")
                st.markdown("""
                **Formula:** MSE = (1/n)Σ(yi - ŷi)²
                - Penalizes larger errors
                - Squared unit
                - Range: [0, ∞)
                """)

            with metric_col2:
                st.metric("Root Mean Square Error", f"{rmse:.3f}")
                st.markdown("""
                **Formula:** RMSE = √((1/n)Σ(yi - ŷi)²)
                - Same unit as measurements
                - Range: [0, ∞)
                """)

            with metric_col3:
                st.metric("Mean Relative Error", f"{mean_relative_error:.2f}%")
                st.markdown("""
                **Formula:** MRE = (1/n)Σ|(yi - ŷi)/yi| × 100%
                - Percentage error
                - Range: [0, 100]
                """)

            st.write("### Model Fit Metrics")
            metric_col1, metric_col2 = st.columns(2)

            with metric_col1:
                st.metric("R² Score", f"{r_squared:.3f}")
                st.markdown("""
                **Formula:** R² = 1 - (Σ(yi - ŷi)²)/(Σ(yi - ȳ)²)
                - Coefficient of determination
                - Range: [0, 1]
                """)

            with metric_col2:
                st.metric("Agreement Ratio", f"{agreement:.2%}")
                st.markdown("""
                **Formula:** (Good Points / Total Points)
                - Points within 35-55° or at (0,0)
                - Range: [0, 1]
                """)

            # Overall Analysis Summary
            st.write("### Overall Analysis")
            
            # Dynamic analysis based on metrics
            analysis_points = []
            
            # Pearson correlation analysis
            if pearson_corr > 0.7:
                analysis_points.append("✅ Strong Pearson correlation (> 0.7) indicates reliable linear relationship between measurements.")
            elif pearson_corr > 0.3:
                analysis_points.append("⚠️ Moderate Pearson correlation (0.3-0.7) suggests some variability between systems.")
            else:
                analysis_points.append("❌ Weak Pearson correlation (< 0.3) indicates significant differences between systems.")
            
            # Spearman correlation analysis
            if spearman_corr > 0.7:
                analysis_points.append("✅ Strong Spearman correlation shows good rank-based relationship.")
            elif spearman_corr > 0.3:
                analysis_points.append("⚠️ Moderate Spearman correlation indicates some rank-order consistency.")
            else:
                analysis_points.append("❌ Weak Spearman correlation suggests poor rank-order alignment.")

            # Agreement ratio analysis
            if agreement > 0.8:
                analysis_points.append(f"✅ High agreement ratio ({agreement:.1%}) shows excellent consistency within 35-55° range.")
            elif agreement > 0.6:
                analysis_points.append(f"⚠️ Moderate agreement ratio ({agreement:.1%}) indicates acceptable but improvable consistency.")
            else:
                analysis_points.append(f"❌ Low agreement ratio ({agreement:.1%}) suggests systematic differences or calibration issues.")
            
            # MAE analysis
            if mae < 0.1:
                analysis_points.append(f"✅ Low Mean Absolute Error ({mae:.3f}) indicates good measurement alignment.")
            elif mae < 0.3:
                analysis_points.append(f"⚠️ Moderate Mean Absolute Error ({mae:.3f}) suggests some systematic variation.")
            else:
                analysis_points.append(f"❌ High Mean Absolute Error ({mae:.3f}) indicates significant measurement discrepancy.")

            # RMSE analysis
            if rmse < 0.15:
                analysis_points.append(f"✅ Low RMSE ({rmse:.3f}) shows good overall accuracy.")
            elif rmse < 0.4:
                analysis_points.append(f"⚠️ Moderate RMSE ({rmse:.3f}) indicates notable measurement variations.")
            else:
                analysis_points.append(f"❌ High RMSE ({rmse:.3f}) suggests substantial measurement differences.")

            # R-squared analysis
            if r_squared > 0.8:
                analysis_points.append(f"✅ High R² score ({r_squared:.3f}) indicates strong model fit.")
            elif r_squared > 0.6:
                analysis_points.append(f"⚠️ Moderate R² score ({r_squared:.3f}) suggests reasonable but improvable fit.")
            else:
                analysis_points.append(f"❌ Low R² score ({r_squared:.3f}) indicates poor model fit.")

            for point in analysis_points:
                st.write(point)
            
            # Visualization sections with explanations
            st.write("### Visualization Analysis")
            
            st.subheader("Density Comparison (Scatter Plot)")
            st.write(f"""
            This scatter plot shows the relationship between Vinci and Roadathena density measurements:
            - Green points: Measurements within 35-55 degree angle (good agreement)
            - Red points: Measurements outside ideal range
            - Points count: {good_points_count} good out of {total_points} total ({(good_points_count/total_points*100):.1f}%)
            - Perfect agreement would show points along a 45-degree line
            - Hover over points to see detailed information
            """)
            
            # Calculate angles and handle special cases
            angles = np.degrees(np.arctan2(filtered_df['Roadathena Density'], filtered_df['Vinci Density']))

            # Create a mask for (0,0) points
            zero_zero_mask = (filtered_df['Roadathena Density'] == 0) & (filtered_df['Vinci Density'] == 0)

            # Create mask for points within angle range or on boundary lines
            angle_mask = ((35 <= angles) & (angles <= 55)) | \
                        (np.isclose(angles, 35, rtol=1e-10)) | \
                        (np.isclose(angles, 55, rtol=1e-10))

            # Combine masks
            is_good_point = zero_zero_mask | angle_mask

            # Get the maximum value for both axes to set equal scale
            max_val = max(
                filtered_df['Vinci Density'].max(),
                filtered_df['Roadathena Density'].max()
            )

            # Add some padding to the max value (10% padding)
            padding = max_val * 0.001
            axis_max = max_val + padding

            # Calculate points for 35° and 55° lines
            # tan(35°) ≈ 0.700, tan(55°) ≈ 1.428
            x_values = np.linspace(0, axis_max, 100)
            y_35deg = 0.700 * x_values  # 35 degree line
            y_55deg = 1.428 * x_values  # 55 degree line
            
            # Modified scatter plot with square shape and all reference lines
            scatter_fig = {
                'data': [
                    # Green points (within 35-55 degrees or (0,0))
                    {
                        'x': filtered_df[is_good_point]['Vinci Density'],
                        'y': filtered_df[is_good_point]['Roadathena Density'],
                        'mode': 'markers',
                        'type': 'scatter',
                        'name': 'Within 35-55° or (0,0)',
                        'marker': {
                            'size': 8,
                            'opacity': 0.7,
                            'color': 'green'
                        },
                        'text': filtered_df[is_good_point].apply(
                            lambda row: f"Type: {row['Type']}<br>"
                                      f"Chainage: {row['Chainage']}<br>"
                                      f"Vinci: {row['Vinci Density']:.4f}<br>"
                                      f"Roadathena: {row['Roadathena Density']:.4f}",
                            axis=1
                        ),
                        'hoverinfo': 'text'
                    },
                    # Red points (outside 35-55 degrees and not (0,0))
                    {
                        'x': filtered_df[~is_good_point]['Vinci Density'],
                        'y': filtered_df[~is_good_point]['Roadathena Density'],
                        'mode': 'markers',
                        'type': 'scatter',
                        'name': 'Outside 35-55°',
                        'marker': {
                            'size': 7,
                            'opacity': 0.7,
                            'color': 'red'
                        },
                        'text': filtered_df[~is_good_point].apply(
                            lambda row: f"Type: {row['Type']}<br>"
                                      f"Chainage: {row['Chainage']}<br>"
                                      f"Vinci: {row['Vinci Density']:.4f}<br>"
                                      f"Roadathena: {row['Roadathena Density']:.4f}",
                            axis=1
                        ),
                        'hoverinfo': 'text'
                    },
                    # 45-degree reference line
                    {
                        'x': [0, axis_max],
                        'y': [0, axis_max],
                        'mode': 'lines',
                        'line': {
                            'color': 'black',
                            'dash': 'dash'
                        },
                        'name': '45° line'
                    },
                    # 35-degree reference line
                    {
                        'x': x_values,
                        'y': y_35deg,
                        'mode': 'lines',
                        'line': {
                            'color': 'grey',
                            'dash': 'dot'
                        },
                        'name': '35° line'
                    },
                    # 55-degree reference line
                    {
                        'x': x_values,
                        'y': y_55deg,
                        'mode': 'lines',
                        'line': {
                            'color': 'grey',
                            'dash': 'dot'
                        },
                        'name': '55° line'
                    }
                ],
                'layout': {
                    'xaxis': {
                        'title': 'Vinci Density',
                        'showgrid': True,
                        'gridcolor': 'lightgray',
                        'range': [0, axis_max],
                        # 'dtick': axis_max/10
                    },
                    'yaxis': {
                        'title': 'Roadathena Density',
                        'showgrid': True,
                        'gridcolor': 'lightgray',
                        'range': [0, axis_max],
                        'scaleanchor': 'x',
                        'scaleratio': 1,
                        # 'dtick': axis_max/10
                    },
                    'title': 'Vinci vs Roadathena Density',
                    'hovermode': 'closest',
                    'showlegend': True,
                    'width': 800,
                    'height': 800,
                    'plot_bgcolor': 'white'
                }
            }
            st.plotly_chart(scatter_fig, use_container_width=True)
            
            # Add metrics explanation specifically for point agreement
            st.markdown(f"""
            **Point Agreement Analysis:**
            - Total Points: {total_points}
            - Points in Agreement (35-55°): {good_points_count}
            - Agreement Percentage: {(good_points_count/total_points*100):.1f}%
            - This indicates how many measurements fall within the acceptable range of agreement
            """)

            # # Add Bland-Altman plot for agreement analysis
            # st.subheader("Bland-Altman Plot (Agreement Analysis)")
            # st.write("""
            # This plot helps assess systematic bias and agreement limits:
            # - X-axis: Average of Vinci and Roadathena measurements
            # - Y-axis: Difference between measurements (Roadathena - Vinci)
            # - Horizontal lines show mean difference and ±1.96 SD (95% limits of agreement)
            # - Points should be randomly scattered around mean difference line
            # """)

            # # Calculate Bland-Altman plot data
            # mean_density = (filtered_df['Vinci Density'] + filtered_df['Roadathena Density']) / 2
            # diff_density = filtered_df['Roadathena Density'] - filtered_df['Vinci Density']
            # mean_diff = diff_density.mean()
            # std_diff = diff_density.std()
            # limits_of_agreement = (mean_diff - 1.96 * std_diff, mean_diff + 1.96 * std_diff)

            # bland_altman_fig = {
            #     'data': [
            #         # Scatter points
            #         {
            #             'x': mean_density,
            #             'y': diff_density,
            #             'mode': 'markers',
            #             'name': 'Measurements',
            #             'marker': {
            #                 'color': 'blue',
            #                 'size': 8,
            #                 'opacity': 0.6
            #             },
            #             'text': filtered_df.apply(
            #                 lambda row: f"Type: {row['Type']}<br>"
            #                           f"Chainage: {row['Chainage']}<br>"
            #                           f"Vinci: {row['Vinci Density']:.4f}<br>"
            #                           f"Roadathena: {row['Roadathena Density']:.4f}",
            #                 axis=1
            #             ),
            #             'hoverinfo': 'text'
            #         },
            #         # Mean difference line
            #         {
            #             'x': [mean_density.min(), mean_density.max()],
            #             'y': [mean_diff, mean_diff],
            #             'mode': 'lines',
            #             'name': f'Mean difference ({mean_diff:.4f})',
            #             'line': {'color': 'red', 'dash': 'dash'}
            #         },
            #         # Upper limit of agreement
            #         {
            #             'x': [mean_density.min(), mean_density.max()],
            #             'y': [limits_of_agreement[1], limits_of_agreement[1]],
            #             'mode': 'lines',
            #             'name': f'+1.96 SD ({limits_of_agreement[1]:.4f})',
            #             'line': {'color': 'gray', 'dash': 'dot'}
            #         },
            #         # Lower limit of agreement
            #         {
            #             'x': [mean_density.min(), mean_density.max()],
            #             'y': [limits_of_agreement[0], limits_of_agreement[0]],
            #             'mode': 'lines',
            #             'name': f'-1.96 SD ({limits_of_agreement[0]:.4f})',
            #             'line': {'color': 'gray', 'dash': 'dot'}
            #         }
            #     ],
            #     'layout': {
            #         'xaxis': {
            #             'title': 'Mean of Vinci and Roadathena Density',
            #             'showgrid': True,
            #             'gridcolor': 'lightgray'
            #         },
            #         'yaxis': {
            #             'title': 'Difference (Roadathena - Vinci)',
            #             'showgrid': True,
            #             'gridcolor': 'lightgray',
            #             'zeroline': True,
            #             'zerolinecolor': 'lightgray',
            #             'zerolinewidth': 1
            #         },
            #         'title': 'Bland-Altman Plot',
            #         'showlegend': True,
            #         'plot_bgcolor': 'white',
            #         'hovermode': 'closest'
            #     }
            # }
            # st.plotly_chart(bland_altman_fig, use_container_width=True)

            # # Add interpretation of Bland-Altman results
            # st.markdown(f"""
            # **Bland-Altman Analysis Results:**
            # - Mean Difference: {mean_diff:.4f} (systematic bias)
            # - Standard Deviation: {std_diff:.4f}
            # - 95% Limits of Agreement: ({limits_of_agreement[0]:.4f}, {limits_of_agreement[1]:.4f})
            # """)

            # Add residuals vs index plot
            st.subheader("Residuals Plot")
            st.write("""
            This plot helps identify patterns in prediction errors:
            - Points above zero line: AI prediction higher than Expert
            - Points below zero line: AI prediction lower than Expert
            - Hover over points to see detailed information
            - Pattern in residuals may indicate systematic bias
            """)

            residuals = filtered_df["Roadathena Density"] - filtered_df["Vinci Density"]
            residuals_fig = px.line(
                filtered_df, 
                x=filtered_df.index, 
                y=residuals,
                title="Residuals vs Index",
                labels={
                    "y": "Residuals (AI - Expert)", 
                    "x": "Index"
                },
                hover_data={
                    "Type": True,
                    "Chainage From": True,
                    "Chainage To": True,
                    "Vinci Density": ":.2f",
                    "Roadathena Density": ":.2f"
                }
            )

            # Update layout for better appearance
            residuals_fig.update_layout(
                plot_bgcolor='white',
                hovermode='x unified',
                showlegend=True,
                xaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray',
                    zeroline=True,
                    zerolinecolor='red',
                    zerolinewidth=1
                )
            )

            # Add a horizontal line at y=0 for reference
            residuals_fig.add_hline(
                y=0, 
                line_dash="dash", 
                line_color="red", 
                annotation_text="Zero line",
                annotation_position="bottom right"
            )

            st.plotly_chart(residuals_fig, use_container_width=True)

            # # Add explanation for the residuals plot
            # st.markdown("""
            # **Residuals Plot Interpretation:**
            # - Points above zero line: AI prediction higher than Expert
            # - Points below zero line: AI prediction lower than Expert
            # - Hover over points to see detailed information
            # - Pattern in residuals may indicate systematic bias
            # """)

            # # Add recommendations based on analysis
            # st.write("### Recommendations")
            # if correlation < 0.7 or agreement < 0.6 or mean_abs_diff > 0.3:
            #     st.warning("""
            #     Based on the analysis, consider the following actions:
            #     1. Review measurement calibration for both systems
            #     2. Investigate chainages with significant differences
            #     3. Check for systematic errors in data collection
            #     4. Consider environmental factors that might affect measurements
            #     """)
            # else:
            #     st.success("""
            #     Measurements show good overall agreement. To maintain quality:
            #     1. Continue regular system calibration
            #     2. Monitor for any developing trends in differences
            #     3. Document conditions where best agreement is achieved
            #     """)

            # # Display basic information
            # st.subheader("Dataset Information")
            # info_col1, info_col2 = st.columns([1, 1])
            # with info_col1:
            #     st.write(f"Total rows: {filtered_df.shape[0]}")
            # with info_col2:
            #     st.write(f"Total columns: {filtered_df.shape[1]}")
            
            # # Add a download button for the filtered DataFrame
            # st.download_button(
            #     label="Download filtered data as CSV",
            #     data=filtered_df.to_csv(index=False).encode('utf-8'),
            #     file_name='processed_data.csv',
            #     mime='text/csv',
            # )
            
          
            
        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")

def main():
    # Add sidebar menu
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Select a page:", ["Main Page", "Developer Page"])
    
    # Display selected page
    if page == "Main Page":
        show_main_page()
    else:
        show_developer_page()

if __name__ == "__main__":
    main()