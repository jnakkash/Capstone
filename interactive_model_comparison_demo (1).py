import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Data for the models
data = {
    'Model': ['Logistic Regression', 'SVM', 'Decision Tree', 'K-Nearest Neighbors'],
    'Accuracy': [0.83, 0.85, 0.79, 0.81],
    'Precision': [0.85, 0.87, 0.80, 0.82],
    'Recall': [0.82, 0.84, 0.79, 0.81],
    'F1-Score': [0.83, 0.85, 0.79, 0.81]
}

df = pd.DataFrame(data)

def main():
    st.title("SpaceX Falcon 9 First Stage Landing Prediction")
    st.subheader("Model Performance Comparison")

    # Display the dataframe
    st.dataframe(df.style.highlight_max(axis=0, color='lightgreen'))

    # Metric selection
    metric = st.selectbox("Choose a metric to visualize:", ['Accuracy', 'Precision', 'Recall', 'F1-Score'])

    # Bar chart
    fig = px.bar(df, x='Model', y=metric, text=metric, 
                 title=f'{metric} Comparison Across Models',
                 color='Model', 
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)

    # Radar chart
    st.subheader("Model Performance Radar Chart")
    model = st.selectbox("Choose a model to visualize:", df['Model'])

    categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    fig = go.Figure()

    model_data = df[df['Model'] == model].iloc[0]
    fig.add_trace(go.Scatterpolar(
        r=[model_data['Accuracy'], model_data['Precision'], 
           model_data['Recall'], model_data['F1-Score']],
        theta=categories,
        fill='toself',
        name=model
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False
    )
    st.plotly_chart(fig)

    # Model description
    st.subheader("Model Descriptions")
    model_descriptions = {
        'Logistic Regression': "A statistical method for predicting binary outcomes. It's simple, interpretable, and works well for linearly separable classes.",
        'SVM': "Support Vector Machine finds the hyperplane that best separates classes. It's effective in high-dimensional spaces and versatile through the use of different kernels.",
        'Decision Tree': "A tree-like model of decisions. It's easy to understand and visualize, but can be prone to overfitting.",
        'K-Nearest Neighbors': "A simple, instance-based learning algorithm. It classifies a data point based on how its neighbors are classified. It's easy to implement but can be computationally expensive."
    }
    selected_model = st.selectbox("Select a model to learn more:", list(model_descriptions.keys()))
    st.write(model_descriptions[selected_model])

    # Conclusion
    st.subheader("Conclusion")
    st.write("""
    Based on the performance metrics, the SVM (Support Vector Machine) model appears to be the best performing model for this task, with the highest accuracy, precision, recall, and F1-score.
    However, the choice of the best model may also depend on other factors such as interpretability, computational efficiency, and specific requirements of the project.
    """)

if __name__ == "__main__":
    main()