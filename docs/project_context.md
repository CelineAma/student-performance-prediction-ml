# Project Context

## Background
Student academic performance in Nigerian tertiary institutions is shaped by interacting academic, socio-economic, and institutional factors. In practice, early identification of students at risk of poor performance is often constrained by limited staff capacity, delayed reporting cycles, and variability in record-keeping across departments. Predictive analytics offers a structured way to use available student-related data to support timely, evidence-informed academic advising and targeted interventions. However, for such systems to be accepted in educational settings, the underlying models must be both empirically reliable and interpretable to non-technical stakeholders.

## Aim
To develop an interpretable machine learning-based web application that predicts student academic performance in Nigerian tertiary institutions and provides explainable insights to support academic decision-making.

## Objectives
- To review relevant literature on student performance prediction and interpretable machine learning in educational contexts.
- To collect, describe, and prepare a dataset representative of a Nigerian tertiary institution setting, including handling missing values and mixed data types.
- To design a preprocessing and feature engineering pipeline suitable for structured student data.
- To address class imbalance using the Synthetic Minority Over-sampling Technique (SMOTE) on the training data.
- To train and compare Random Forest and LightGBM classifiers using appropriate evaluation metrics.
- To integrate SHAP-based explainability to provide feature-level contributions for individual and aggregate predictions.
- To deploy the trained model(s) within a web application architecture that supports practical use and future extension.

## Scope
This project focuses on supervised machine learning for predicting a defined academic outcome (e.g., pass/fail, degree classification category, or risk level) from structured student data. The scope includes data preprocessing, model training, evaluation, and explainability, as well as integration into a web application for demonstration purposes. The work does not aim to establish causal relationships, replace institutional grading policies, or serve as a standalone decision authority; rather, it provides a decision-support tool whose outputs should be interpreted alongside professional academic judgment and established institutional processes.
