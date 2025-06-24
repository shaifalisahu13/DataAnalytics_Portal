import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# App Configuration
st.set_page_config(page_title='Data Analytics Portal', page_icon='📊', layout='wide')

# Title and Header
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':grey[Explore data with ease.]', divider='rainbow')

# File Upload
file = st.file_uploader('Upload a CSV or Excel file', type=['csv', 'xlsx'])

if file:
    try:
        data = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        st.success('File uploaded successfully ✅')
        st.dataframe(data)

        # Dataset Overview
        st.subheader(':rainbow[Basic Dataset Information]', divider='rainbow')
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Summary', 'Top & Bottom Rows', 'Data Types', 'Columns', 'Missing Values'])

        with tab1:
            st.write(f'Total Rows: {data.shape[0]}, Total Columns: {data.shape[1]}')
            st.subheader('📊 Statistical Summary')
            st.dataframe(data.describe())

        with tab2:
            num = st.slider('Number of rows to display', 1, min(50, data.shape[0]), value=5)
            st.write('🔼 Top Rows')
            st.dataframe(data.head(num))
            st.write('🔽 Bottom Rows')
            st.dataframe(data.tail(num))

        with tab3:
            st.write('🧬 Column Data Types')
            st.dataframe(data.dtypes)

        with tab4:
            st.write('📌 Column Names')
            st.write(list(data.columns))

        with tab5:
            st.write('🧩 Missing Values Count')
            st.dataframe(data.isnull().sum())

        # Value Counts
        st.subheader(':rainbow[Column Value Distribution]', divider='rainbow')
        with st.expander('🔢 Value Counts'):
            col1, col2 = st.columns(2)
            with col1:
                selected_col = st.selectbox('Select column for counting values', options=data.columns)
            with col2:
                top_n = st.number_input('Top N rows', min_value=1, value=5, step=1)

            if st.button('Show Counts'):
                value_counts = data[selected_col].value_counts().reset_index().head(top_n)
                value_counts.columns = [selected_col, 'Count']
                st.dataframe(value_counts)

                st.subheader('📈 Visualizations', divider='grey')
                st.plotly_chart(px.bar(value_counts, x=selected_col, y='Count', text='Count'))
                st.plotly_chart(px.line(value_counts, x=selected_col, y='Count', markers=True))
                st.plotly_chart(px.pie(value_counts, names=selected_col, values='Count'))

        # Group By
        st.subheader(':rainbow[GroupBy Summary]', divider='rainbow')
        with st.expander('🔍 Group & Aggregate'):
            col1, col2, col3 = st.columns(3)
            with col1:
                groupby_cols = st.multiselect('Select columns to group by', options=data.columns)
            with col2:
                operation_col = st.selectbox('Select column to aggregate', options=data.select_dtypes(include='number').columns)
            with col3:
                operation = st.selectbox('Select operation', ['sum', 'mean', 'min', 'max', 'count', 'median'])

            if groupby_cols:
                try:
                    agg_result = data.groupby(groupby_cols).agg({operation_col: operation}).reset_index()
                    agg_col_name = f'{operation_col}_{operation}'
                    agg_result.columns = groupby_cols + [agg_col_name]
                    st.dataframe(agg_result)

                    # Download Button
                    csv = agg_result.to_csv(index=False).encode('utf-8')
                    st.download_button('📥 Download Grouped Data', data=csv, file_name='grouped_data.csv', mime='text/csv')

                    # Visualize Grouped Data
                    st.subheader('📊 Visualization', divider='grey')
                    graph_type = st.selectbox('Choose Graph Type', ['Line', 'Bar', 'Scatter', 'Pie', 'Sunburst'])

                    if graph_type == 'Line':
                        fig = px.line(agg_result, x=groupby_cols[0], y=agg_col_name, markers=True, color=groupby_cols[0])
                    elif graph_type == 'Bar':
                        fig = px.bar(agg_result, x=groupby_cols[0], y=agg_col_name, color=groupby_cols[0])
                    elif graph_type == 'Scatter':
                        fig = px.scatter(agg_result, x=groupby_cols[0], y=agg_col_name, size=agg_col_name, color=groupby_cols[0])
                    elif graph_type == 'Pie':
                        fig = px.pie(agg_result, values=agg_col_name, names=groupby_cols[0])
                    elif graph_type == 'Sunburst':
                        fig = px.sunburst(agg_result, path=groupby_cols, values=agg_col_name)

                    st.plotly_chart(fig)

                except Exception as e:
                    st.error(f"Error: {e}")

        # Correlation Heatmap
        st.subheader(':rainbow[Correlation Heatmap]', divider='rainbow')
        with st.expander('📌 Show Correlation Heatmap'):
            numeric_data = data.select_dtypes(include='number')
            if not numeric_data.empty:
                fig, ax = plt.subplots()
                sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
                st.pyplot(fig)
            else:
                st.warning('No numeric columns to compute correlation.')

    except Exception as e:
        st.error(f"File loading failed. Details: {e}")
else:
    st.info('Please upload a valid CSV or Excel file to continue.', icon='📎')
