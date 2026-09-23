
import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Early Wake-Up & Health Analytics",
    page_icon="🌅",
    layout="wide",
)

DATA_PATHS = [
    "data/early_wakeup_health_dataset.csv",
    "early_wakeup_health_dataset.csv",
]

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

def find_dataset():
    for path in DATA_PATHS:
        if os.path.exists(path):
            return path
    return None

st.title("🌅 Early Wake-Up & Health Analytics")
st.caption("Interactive exploratory analysis of sleep, exercise, lifestyle and wellness patterns.")

path = find_dataset()

if path is None:
    st.error("Dataset not found in the repository.")
    uploaded = st.file_uploader(
        "Upload early_wakeup_health_dataset.csv",
        type=["csv"],
    )
    if uploaded is None:
        st.stop()
    df = pd.read_csv(uploaded)
else:
    df = load_data(path)

# Keep the same basic cleaning approach used in the notebook:
# remove rows with missing values before the visual analysis.
df = df.dropna().copy()

st.sidebar.header("Filters")

genders = sorted(df["Gender"].dropna().unique().tolist())
selected_gender = st.sidebar.multiselect("Gender", genders, default=genders)

occupations = sorted(df["Occupation"].dropna().unique().tolist())
selected_occupation = st.sidebar.multiselect(
    "Occupation", occupations, default=occupations
)

early_values = sorted(df["Early_Waker"].dropna().unique().tolist())
selected_early = st.sidebar.multiselect(
    "Early Waker", early_values, default=early_values
)

filtered = df[
    df["Gender"].isin(selected_gender)
    & df["Occupation"].isin(selected_occupation)
    & df["Early_Waker"].isin(selected_early)
].copy()

st.sidebar.markdown("---")
st.sidebar.write(f"Filtered records: **{len(filtered):,}**")

# KPI row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Records", f"{len(filtered):,}")
c2.metric("Avg Health Score", f"{filtered['Health_Score'].mean():.1f}")
c3.metric("Avg Sleep", f"{filtered['Sleep_Duration_Hours'].mean():.2f} h")
c4.metric("Avg BMI", f"{filtered['BMI'].mean():.2f}")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Sleep & Energy", "Exercise & Lifestyle", "Data Explorer"]
)

with tab1:
    st.subheader("Population overview")

    left, right = st.columns(2)

    with left:
        gender_counts = filtered["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig = px.pie(
            gender_counts,
            names="Gender",
            values="Count",
            title="Gender Distribution",
            hole=0.35,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        occ = (
            filtered.groupby("Occupation", as_index=False)["Health_Score"]
            .mean()
            .sort_values("Health_Score", ascending=False)
        )
        fig = px.bar(
            occ,
            x="Occupation",
            y="Health_Score",
            title="Average Health Score by Occupation",
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("BMI distribution")
    fig = px.box(filtered, y="BMI", points=False, title="BMI Distribution")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Sleep and energy")

    left, right = st.columns(2)

    with left:
        fig = px.scatter(
            filtered,
            x="Sleep_Duration_Hours",
            y="Energy_Level_Score",
            color="Early_Waker",
            hover_data=["Age", "Gender", "Health_Score"],
            title="Sleep Duration vs Energy Level",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.histogram(
            filtered,
            x="Sugary_Drinks_Per_Week",
            nbins=15,
            title="Sugary Drinks per Week",
        )
        st.plotly_chart(fig, use_container_width=True)

    early_summary = (
        filtered.groupby("Early_Waker")[
            ["Sleep_Duration_Hours", "Sleep_Quality_Score", "Energy_Level_Score", "Health_Score"]
        ]
        .mean()
        .round(2)
        .reset_index()
    )
    st.dataframe(early_summary, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Exercise and lifestyle")

    left, right = st.columns(2)

    with left:
        exercise_counts = filtered["Exercise_Type"].value_counts().reset_index()
        exercise_counts.columns = ["Exercise_Type", "Count"]
        fig = px.pie(
            exercise_counts,
            names="Exercise_Type",
            values="Count",
            title="Exercise Type Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        steps = (
            filtered.groupby("Gender", as_index=False)["Daily_Steps"]
            .mean()
            .sort_values("Daily_Steps", ascending=False)
        )
        fig = px.bar(
            steps,
            x="Gender",
            y="Daily_Steps",
            title="Average Daily Steps by Gender",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Selected numeric relationships with BMI")
    numeric_cols = filtered.select_dtypes(include="number").columns
    corr = (
        filtered[numeric_cols]
        .corr(numeric_only=True)["BMI"]
        .drop("BMI")
        .sort_values(key=lambda s: s.abs(), ascending=False)
        .head(10)
        .reset_index()
    )
    corr.columns = ["Feature", "Correlation with BMI"]
    st.dataframe(corr.round(3), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Filtered dataset")
    st.dataframe(filtered, use_container_width=True, height=520)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        data=csv,
        file_name="filtered_early_wakeup_health_data.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption(
    "This dashboard is for exploratory data analysis only. Associations in the dataset "
    "should not be interpreted as medical diagnoses or causal effects."
)
