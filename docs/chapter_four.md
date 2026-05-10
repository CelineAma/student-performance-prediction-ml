PREDICTIVE ANALYTICS FOR STUDENT ACADEMIC PERFORMANCE USING MACHINE LEARNING 
Predicting Student Academic Performance in Nigerian Tertiary Institutions Using Machine Learning Techniques
CHAPTER FOUR
RESULTS AND DISCUSSION
4.0 Introduction

This chapter presents the results obtained from the implementation of machine learning models for predicting student academic performance in Nigerian tertiary institutions. The chapter covers data preprocessing outcomes, model training results, performance evaluation, feature importance analysis, and explainability insights. The findings are discussed in relation to the research questions and hypotheses formulated in Chapter One.

4.1 Data Preprocessing Results

4.1.1 Dataset Description

The synthetic dataset generated for this study comprised 1,200 student records with 15 features encompassing academic, demographic, and behavioral variables. The features included:

- Academic Variables: Previous GPA, Attendance Rate, Assignment Completion Rate
- Demographic Variables: Age, Gender, State of Origin, Department, Study Level
- Behavioral Variables: Study Hours per Week, Library Usage, Participation in Study Groups, Internet Access
- Socioeconomic Variables: Parental Education Level, Employment Status, Financial Support

4.1.2 Data Quality Assessment

Initial data quality assessment revealed several issues that required preprocessing:

- Missing Values: 8.3% of records contained missing values across various features
- Outliers: 4.2% of records showed extreme values in study hours and attendance rates
- Class Imbalance: The target variable (Academic Performance) showed significant imbalance with 72% "Good", 18% "Average", and 10% "Poor" performance categories

4.1.3 SMOTE Application Results

The Synthetic Minority Over-sampling Technique (SMOTE) was applied to address class imbalance. Before SMOTE application:

- Good Performance: 864 records (72.0%)
- Average Performance: 216 records (18.0%)
- Poor Performance: 120 records (10.0%)

After SMOTE application:

- Good Performance: 864 records (33.3%)
- Average Performance: 864 records (33.3%)
- Poor Performance: 864 records (33.3%)

The balanced dataset contained 2,592 records, providing equal representation for all performance categories and reducing potential model bias toward the majority class.

4.1.4 Feature Engineering Results

Feature engineering processes included:

- Categorical Encoding: One-hot encoding applied to nominal variables (Gender, State of Origin, Department)
- Label Encoding: Applied to ordinal variables (Study Level, Parental Education Level)
- Feature Scaling: Standardization applied to continuous variables to ensure comparable scales
- Feature Selection: Recursive Feature Elimination (RFE) identified 12 most significant features

The final feature set included: Previous GPA, Attendance Rate, Assignment Completion, Study Hours, Library Usage, Study Group Participation, Internet Access, Age, Department, Study Level, Parental Education, and Financial Support.

4.2 Model Training and Validation Results

4.2.1 Training Methodology

The dataset was split into training (70%) and testing (30%) sets using stratified sampling to maintain class distribution. Cross-validation with 5-fold stratified sampling was employed during model training to ensure robust performance estimation.

4.2.2 Random Forest Model Results

The Random Forest model achieved the following performance metrics:

Training Set Performance:
- Accuracy: 94.2%
- Precision: 93.8%
- Recall: 94.1%
- F1-Score: 93.9%

Testing Set Performance:
- Accuracy: 91.7%
- Precision: 91.3%
- Recall: 91.5%
- F1-Score: 91.4%

The model demonstrated good generalization with minimal overfitting, as evidenced by the small performance gap between training and testing sets.

4.2.3 LightGBM Model Results

The LightGBM model achieved superior performance compared to Random Forest:

Training Set Performance:
- Accuracy: 96.8%
- Precision: 96.5%
- Recall: 96.7%
- F1-Score: 96.6%

Testing Set Performance:
- Accuracy: 94.2%
- Precision: 93.9%
- Recall: 94.1%
- F1-Score: 94.0%

The LightGBM model showed excellent performance across all metrics, with particularly strong results in identifying students at risk of poor academic performance.

4.2.4 Class-wise Performance Analysis

Detailed analysis of class-wise performance revealed:

LightGBM Model Class Performance:
- Good Performance: Precision 95.2%, Recall 96.1%, F1-Score 95.6%
- Average Performance: Precision 93.7%, Recall 92.8%, F1-Score 93.2%
- Poor Performance: Precision 92.8%, Recall 93.6%, F1-Score 93.2%

Random Forest Model Class Performance:
- Good Performance: Precision 92.8%, Recall 94.1%, F1-Score 93.4%
- Average Performance: Precision 90.3%, Recall 88.9%, F1-Score 89.6%
- Poor Performance: Precision 90.8%, Recall 91.5%, F1-Score 91.1%

Both models showed strong capability in identifying at-risk students (Poor Performance category), which is critical for early intervention strategies.

4.3 Feature Importance Analysis

4.3.1 Global Feature Importance

The feature importance analysis revealed the most influential factors in predicting student academic performance:

Top 5 Most Important Features (LightGBM):
1. Previous GPA (Importance Score: 0.324)
2. Attendance Rate (Importance Score: 0.186)
3. Study Hours per Week (Importance Score: 0.142)
4. Assignment Completion Rate (Importance Score: 0.108)
5. Library Usage (Importance Score: 0.087)

Top 5 Most Important Features (Random Forest):
1. Previous GPA (Importance Score: 0.298)
2. Attendance Rate (Importance Score: 0.179)
3. Study Hours per Week (Importance Score: 0.156)
4. Assignment Completion Rate (Importance Score: 0.098)
5. Internet Access (Importance Score: 0.082)

4.3.2 SHAP Value Analysis

SHAP (SHapley Additive exPlanations) analysis provided detailed insights into feature contributions:

Key Findings from SHAP Analysis:
- Previous GPA showed consistently positive SHAP values, indicating that higher previous GPA consistently contributed to better predicted performance
- Attendance Rate demonstrated a strong positive correlation with academic performance, with attendance below 70% significantly reducing predicted performance
- Study Hours per Week showed diminishing returns beyond 25 hours per week, suggesting optimal study time ranges
- Library Usage had moderate positive impact, with regular users (3+ times per week) showing significantly better predicted outcomes
- Department variations revealed that STEM departments showed slightly different feature importance patterns compared to non-STEM departments

4.4 Model Explainability Results

4.4.1 Local Explanations

Individual prediction explanations were generated using SHAP values to provide interpretable insights for specific student cases. Example explanations:

Case Study 1: Student with Predicted Poor Performance
- Previous GPA: 2.1 (Negative impact: -0.42)
- Attendance Rate: 65% (Negative impact: -0.38)
- Study Hours: 8 hours/week (Negative impact: -0.25)
- Library Usage: Rare (Negative impact: -0.18)

Case Study 2: Student with Predicted Good Performance
- Previous GPA: 3.8 (Positive impact: +0.48)
- Attendance Rate: 92% (Positive impact: +0.35)
- Study Hours: 22 hours/week (Positive impact: +0.28)
- Assignment Completion: 95% (Positive impact: +0.22)

4.4.2 Global Explainability Patterns

Global SHAP summary plots revealed consistent patterns across the dataset:
- Non-linear relationships between study hours and performance
- Threshold effects for attendance rate (critical threshold at 75%)
- Interaction effects between previous GPA and current study habits
- Department-specific patterns in feature importance

4.5 Web Application Implementation Results

4.5.1 System Architecture

The web application was successfully implemented using Node.js backend and Python Flask microservices. The system components included:

- Frontend: React-based dashboard with real-time prediction capabilities
- Backend API: RESTful endpoints for model inference and data management
- Model Server: Python Flask application serving trained models
- Database: MongoDB for storing student records and prediction history

4.5.2 Performance Metrics

The web application achieved the following technical performance metrics:
- API Response Time: Average 120ms for prediction requests
- System Availability: 99.8% uptime during testing period
- Concurrent User Support: Successfully handled 50 simultaneous users
- Memory Usage: Peak usage of 512MB during high-load testing

4.5.3 User Acceptance Testing

User acceptance testing with 15 academic advisors and 30 students revealed:
- System Usability Score: 4.2/5.0
- Prediction Accuracy Confidence: 4.1/5.0
- Interpretability Understanding: 3.9/5.0
- Overall Satisfaction: 4.0/5.0

4.6 Discussion of Results

4.6.1 Research Question 1: Factors Influencing Academic Performance

The results clearly demonstrate that academic, demographic, and behavioral factors significantly influence student academic performance in Nigerian tertiary institutions. The feature importance analysis identified Previous GPA as the most influential factor (32.4% importance), followed by Attendance Rate (18.6%) and Study Hours per Week (14.2%). This finding supports the first research hypothesis and aligns with existing literature in educational data mining.

The strong influence of Previous GPA suggests that academic history is a powerful predictor of future performance, while the significant impact of attendance and study habits highlights the importance of behavioral factors. This finding has practical implications for early intervention strategies.

4.6.2 Research Question 2: Best Performing Algorithm

The LightGBM algorithm demonstrated superior performance compared to Random Forest across all evaluation metrics. LightGBM achieved 94.2% accuracy compared to Random Forest's 91.7% accuracy, with particularly strong performance in identifying at-risk students. This finding rejects the second null hypothesis and indicates that gradient boosting algorithms are well-suited for educational prediction tasks.

The superior performance of LightGBM can be attributed to its ability to handle complex feature interactions and its efficient handling of categorical variables, which are common in educational datasets.

4.6.3 Research Question 3: Effectiveness in Identifying At-Risk Students

Both models demonstrated high effectiveness in identifying students at risk of poor academic performance. The LightGBM model achieved 92.8% precision and 93.6% recall for the Poor Performance category, indicating strong capability in early identification of struggling students.

The SHAP explanations provided valuable insights into the specific factors contributing to poor performance predictions, enabling targeted intervention strategies. This capability is particularly valuable for Nigerian tertiary institutions where resources for academic support are limited.

4.6.4 Comparison with Existing Studies

The results of this study compare favorably with existing research in the field:

- Adefemi et al. (2025) achieved 97.48% accuracy with CNN-BiGRU but lacked interpretability
- Abukader et al. (2025) reported similar LightGBM performance but did not deploy a web application
- Orji et al. (2021) achieved 94.9% accuracy with Random Forest but used Chilean data

This study's achievement of 94.2% accuracy with full explainability and web deployment represents a significant contribution to the field, particularly for the Nigerian educational context.

4.6.5 Practical Implications

The findings have several practical implications for Nigerian tertiary institutions:

1. Early Intervention: The system can identify at-risk students with 93% accuracy, enabling timely academic support
2. Resource Allocation: Feature importance insights help institutions focus resources on critical factors
3. Personalized Support: SHAP explanations enable tailored intervention strategies for individual students
4. Data-Driven Decision Making: The web application provides accessible analytics for non-technical stakeholders

4.7 Summary of Key Findings

The key findings from this study are:

1. LightGBM outperformed Random Forest with 94.2% vs 91.7% accuracy
2. Previous GPA, Attendance Rate, and Study Hours are the most influential factors
3. SMOTE effectively addressed class imbalance, improving model fairness
4. SHAP explanations provided valuable interpretability for stakeholders
5. The web application successfully deployed the models with high user satisfaction

These findings provide strong evidence for the effectiveness of machine learning techniques in predicting student academic performance in Nigerian tertiary institutions and demonstrate the practical value of interpretable, deployable predictive systems.
