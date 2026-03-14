# NYC School Performance Analytics Dashboard

## Live Dashboard

Explore the interactive dashboard here:

https://huggingface.co/spaces/tajoshi2/nyc-school-performance-dashboard

---

## Overview

This project is an interactive analytics dashboard built using the **School Quality Reports Data for New York City (2022)** from NYC OpenData.

The dashboard enables users to explore school performance metrics across different school types through multiple visualizations. It supports dynamic metric selection and provides insights into the relationship between school size, performance, and distribution patterns across the NYC school system.

## Dataset

The dataset used in this project comes from **NYC OpenData – School Quality Reports**.

To ensure the analysis reflects the most recent available information, the data was filtered to include **only records from 2022**.

---

## Key Visualizations

### 1. School Type Distribution
A bar chart showing the number of records for each school type based on the selected metric.

### 2. Number of Students vs Metric Value
A scatter plot showing the relationship between school size and the selected performance metric.

### 3. Performance Distribution by School Type
A stacked bar chart showing the proportion of schools performing above or below the comparison group average.

### 4. Heatmap and School Type Distribution
An interactive heatmap visualizing the relationship between number of students and metric score, with a linked bar chart for school type distribution.

### 5. Average Metric Score vs Number of Students
A line chart showing how average metric values vary across schools with different student population sizes.

---

## Key Insights

- Smaller schools show higher variability in performance metrics, likely due to lower student counts and greater sensitivity to individual outcomes.
- Larger schools tend to demonstrate more stable and slightly higher average metric scores.
- Most schools perform at or above their comparison group averages across many metrics.
- Certain metrics apply specifically to certain school types, reflecting the different goals and evaluation criteria across school categories.

---

## Data Processing Pipeline

1. School Quality Reports data was retrieved from NYC OpenData.
2. The dataset was filtered to include only records from 2022.
3. Relevant performance metrics were cleaned and prepared for analysis.
4. Interactive visualizations were built to explore relationships between school size, school type, and metric values.
5. The dashboard was deployed as an interactive application on Hugging Face Spaces.

---

## Technologies Used

- Python
- Data visualization libraries
- Interactive dashboard framework
- Hugging Face Spaces
- NYC OpenData

---
---

## Data Source

**NYC OpenData – School Quality Reports**

---

## Portfolio Relevance

This project demonstrates skills in:
- dashboard design
- exploratory data analysis
- interactive data visualization
- education data analytics
- communicating insights through visual storytelling
