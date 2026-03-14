import altair as alt
import pandas as pd
import streamlit as st

data = './filtered_school_data.csv'
df = pd.read_csv(data)

st.markdown(
    "<h1 style='text-align: center;'>School Quality Reports Data For New York For 2022</h1>",
    unsafe_allow_html=True
)

st.write("Group Members: Divya Jain, Tejasri Joshi, Emily Chen, Peter Cheng,  Yujun Feng")
st.write("\n")
st.write("""
         Explore various metrics related to school performance by school type. 
         Use the dropdown menu to select a metric and visualize the distribution across different school types.
         """)

metric_names = df['Metric Display Name'].unique()
selected_metric = st.selectbox(
    "Select a Metric:",
    options=metric_names,
    index=6
)

filtered_df = df[df['Metric Display Name'] == selected_metric]

# bar chart
grouped_df = filtered_df.groupby('School Type').size().reset_index(name='Record Count')
bar_chart = alt.Chart(grouped_df).mark_bar().encode(
    x=alt.X('Record Count:Q', title='Number of Records'),
    y=alt.Y('School Type:N', title='School Type', sort='-x'),
    color=alt.Color('School Type:N', scale=alt.Scale(range=['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628'])),
    tooltip=['School Type:N', 'Record Count:Q']
).properties(
    title=f"Number of Records by School Type for {selected_metric}",
    width=600,
    height=250
)

st.header(f"Number of Records by School Type")
st.altair_chart(bar_chart, use_container_width=True)

st.write("""
         The bar chart shows the number of records for each school type based on the selected metric. 
         This helps you quickly compare how different school types contribute to the chosen performance metric.
         """)

# scatter plot
scatter_plot = alt.Chart(filtered_df).mark_point().encode(
    x=alt.X('Number of Students:Q', title='Number of Students'),
    y=alt.Y('Metric Value:Q', title='Metric Value'),
    color=alt.Color('School Type:N', scale=alt.Scale(range=['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628'])),
    tooltip=[
        alt.Tooltip('School Name:N', title='School Name'),
        alt.Tooltip('Number of Students:Q', title='Number of Students'),
        alt.Tooltip('Metric Value:Q', title='Metric Value'),
        alt.Tooltip('School Type:N', title='School Type')
    ]
).properties(
    width=600,
    height=400,
    title=f"Number of Students vs Metric Value for {selected_metric}"
).interactive()

st.header(f"Number of Students vs Metric Value")
st.altair_chart(scatter_plot, use_container_width=True)

st.write("""
         This scatter plot shows the relationship between the number of students and the metric value for the selected metric. 
         Each point represents a school, and the colors differentiate school types.
         """)

# stacked bar chart
filtered_df['Performance Category'] = filtered_df.apply(
    lambda row: 'Metric Value ≥ Comparison Group Average' if row['Metric Value'] >= row['Comparison Group Average']
    else 'Metric Value < Comparison Group Average',
    axis=1
)

agg_data = filtered_df.groupby(['School Type', 'Performance Category']).size().reset_index(name='Count')
horizontal_stacked_bar = alt.Chart(agg_data).mark_bar().encode(
    y=alt.Y('School Type:N', title='School Type', sort='-x'),
    x=alt.X('Count:Q', stack='normalize', title='Percentage'),
    color=alt.Color('Performance Category:N', title='Performance Category',
                    scale=alt.Scale(domain=['Metric Value ≥ Comparison Group Average', 'Metric Value < Comparison Group Average'],
                                    range=['#4CAF50', '#F44336'])),
    tooltip=['School Type:N', 'Performance Category:N', 'Count:Q']
).properties(
    width=600,
    height=300,
    title=f'Performance Distribution by School Type for {selected_metric}'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    titleFontSize=12,
    labelFontSize=12
)

st.header("Performance Distribution by School Type")
st.altair_chart(horizontal_stacked_bar, use_container_width=True)

st.write("""
         This stacked bar chart shows the performance distribution of each school type for the selected metric. 
         The chart indicates the proportion of schools performing above or below the comparison group average, with colors distinguishing the performance categories.
         """)

brush = alt.selection_interval(encodings=['x', 'y'])

# heatmap
heatmap = alt.Chart(filtered_df).mark_rect().encode(
    x=alt.X('Number of Students:Q', bin=alt.Bin(maxbins=30), title='Number of Students'),
    y=alt.Y('Metric Score:Q', bin=alt.Bin(maxbins=30), title='Metric Score'),
    color=alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'), title='Count of Records'),
    tooltip=[
        alt.Tooltip('Number of Students:Q', bin=alt.Bin(maxbins=30), title='Number of Students'),
        alt.Tooltip('Metric Score:Q', bin=alt.Bin(maxbins=30), title='Metric Score'),
        alt.Tooltip('count():Q', title='Count of Records')
    ]
).properties(
    width=200,
    height=200,
    title='Heatmap of Number of Students vs. Metric Score'
).add_params(
    brush
)

# bar chart
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('School Type:N', title='School Type'),
    y=alt.Y('count():Q', title='Count of Records'),
    color=alt.Color('School Type:N', scale=alt.Scale(range=['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628'])),
    tooltip=[
        alt.Tooltip('School Type:N', title='School Type'),
        alt.Tooltip('count():Q', title='Count of Records')
    ]
).transform_filter(
    brush
).properties(
    width=200,
    height=200,
    title='Distribution of School Types for Selected Data'
)

combined_chart = alt.hconcat(heatmap, bar_chart).configure_title(
    fontSize=16,
    anchor='start'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    titleFontSize=12,
    labelFontSize=12
)

st.header("Heatmap and School Type Distribution")
st.altair_chart(combined_chart, use_container_width=True)

st.write("""
         This interactive heatmap visualizes the relationship between the number of students and the metric score. 
         Each cell represents a count of records within specific ranges of these two variables. 
         The bar chart to the right dynamically updates to show the distribution of school types for the data selected in the heatmap. 
         Use the brush tool (click and drag) on the heatmap to filter the data and explore how school types vary in the selected range.
         """)

# line chart
interval_size = 100
df['Student Group'] = (df['Number of Students'] // interval_size) * interval_size
df['Student Range'] = df['Student Group'].astype(str) + " - " + (df['Student Group'] + interval_size).astype(str)

grouped_data = df.groupby(['Student Group', 'Student Range']).agg(
    Avg_Metric_Score=('Metric Score', 'mean'),
    Student_Count=('Number of Students', 'count')
).reset_index()

line_chart = alt.Chart(grouped_data).mark_line(interpolate='monotone', strokeWidth=2).encode(
    x=alt.X('Student Group:Q', title='Number of Students', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Avg_Metric_Score:Q', title='Average Metric Score'),
    tooltip=[
        alt.Tooltip('Student Range:N', title='Number of Students (Range)'),
        alt.Tooltip('Avg_Metric_Score:Q', title='Average Metric Score'),
        alt.Tooltip('Student_Count:Q', title='Number of Records')
    ]
).properties(
    title="Average Metric Score vs Number of Students",
    width=700,
    height=400
)

points = alt.Chart(grouped_data).mark_point(size=50, color='red').encode(
    x='Student Group:Q',
    y='Avg_Metric_Score:Q',
    tooltip=[
        alt.Tooltip('Student Range:N', title='Number of Students (Range)'),
        alt.Tooltip('Avg_Metric_Score:Q', title='Average Metric Score')
    ]
)

combined_chart = (line_chart + points).interactive()

st.header("Average Metric Score vs Number of Students")
st.altair_chart(combined_chart, use_container_width=True)

st.write("""
         This line chart shows the relationship between the number of students and the average metric scores, 
         aggregated across all metrics and all school types. Each red point highlights the average metric score 
         for schools with a specific number of students, providing a clearer view of the trend within the range.
         """)

st.header("Analysis and Insights")
st.write("""
The School Quality Reports Data for New York City (2022), retrieved from NYC OpenData, provides valuable insights into school performance across various metrics and school types. The analysis reveals notable trends, variability, and unique patterns that help us better understand the factors influencing student outcomes.

We decided to subset the data to only include the year 2022. This was the latest year available, and we wanted to ensure that our analysis was based on the most up-to-date data, as it reflects the current state of the schools' performance.

Smaller schools with a lower number of students show a high degree of variability in their performance metrics. This is evident in both the scatter plot and heatmap, where smaller schools not only have a larger count of records but also exhibit considerable fluctuations in their metric scores. Such variability may stem from limited resources, smaller sample sizes, or greater sensitivity to individual student performance.

In contrast, schools with a larger number of students tend to display higher and more stable average metric scores, as observed in the Average Metric Score vs Number of Students line chart. Despite occasional fluctuations, the overall trend indicates an upward movement, suggesting that larger schools may benefit from better infrastructure, experienced staff, and established programs that contribute to more consistent performance. This trend highlights the potential advantages of scale in school systems.

The analysis of performance distribution shows that for most metrics, schools generally perform equal to or above the comparison group average. This consistent trend reflects a positive aspect of NYC schools, suggesting that their performance is competitive when compared to similar groups.

One key observation is the overlap and concentration of schools across different types in the scatter plot. While schools of various types often form dense clusters with similar performance metrics, their outliers stand out. For example, specific metrics like the Transfer School Graduation Rate apply exclusively to High School Transfer schools. Such school-type-specific metrics highlight how performance evaluation is tailored to meet the unique goals and challenges of each school category.

In conclusion, the data highlights clear patterns in school performance. Larger schools demonstrate higher stability and stronger average performance, while smaller schools show greater variability. Metrics tailored to specific school types reflect the unique contexts and challenges they address. By understanding these trends, stakeholders can better target resources and interventions to improve outcomes across the NYC school system.

---

**Sources:**  

[School Quality Reports Data - NYC OpenData](https://data.cityofnewyork.us/Education/School-Quality-Reports-Data/dnpx-dfnc)

""")