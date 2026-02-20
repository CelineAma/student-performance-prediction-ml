PREDICTIVE ANALYTICS FOR STUDENT ACADEMIC PERFORMANCE USING MACHINE LEARNING 
Predicting Student Academic Performance in Nigerian Tertiary Institutions Using Machine Learning Techniques
CHAPTER ONE
INTRODUCTION
1.0 Background of the Study

Academic performance is a critical measure of the success of educational systems and an important determinant of students’ future academic and career opportunities. In tertiary institutions, students’ academic outcomes influence graduation rates, employability prospects, institutional ranking, and overall national human capital development. Consequently, improving academic performance remains a major priority for higher education stakeholders.

In Nigerian tertiary institutions, monitoring and evaluating student academic performance is traditionally carried out using manual and descriptive approaches, such as examination scores and grade point averages. These approaches are largely reactive, as academic interventions are often implemented only after students have already performed poorly or failed courses. Such late interventions reduce the chances of recovery and increase the likelihood of dropout, delayed graduation, and low academic morale.

The increasing availability of educational data, such as students’ academic records, attendance information, demographic characteristics, and study-related behaviors, has created new opportunities for data-driven decision-making in education. Predictive analytics, particularly through machine learning techniques, has emerged as a powerful approach for analyzing large and complex educational datasets to uncover patterns and predict future academic outcomes.

Machine learning models such as Random Forest, Support Vector Machines, Gradient Boosting, and deep learning architectures have been shown to outperform traditional statistical methods in predicting student academic performance. These models can identify at-risk students early, allowing institutions to provide timely academic support and personalized interventions.

However, despite the growing body of research in this area, most existing studies are based on datasets from developed regions such as Europe, Asia, and North America. There is limited empirical evidence focusing on Nigerian tertiary institutions, where distinct socioeconomic, infrastructural, and behavioral factors influence academic performance. This raises concerns about the applicability and generalizability of existing predictive models to the Nigerian educational context.

This study, therefore, focuses on applying machine learning techniques to predict student academic performance in Nigerian tertiary institutions, using relevant academic, demographic, and behavioral variables to support early academic intervention and informed decision-making.

1.1 Statement of the Problem

Poor academic performance among students in Nigerian tertiary institutions remains a persistent challenge, often resulting in course failures, extended study duration, student dropout, and reduced employability after graduation. In many institutions, academic monitoring systems are limited to reporting past performance without providing insight into future academic risks.

Current evaluation methods are largely manual and lack predictive capability, making it difficult for educators and administrators to identify struggling students early enough for effective intervention. As a result, academic support measures are frequently delayed and less effective.

Although several studies have applied machine learning techniques to predict student academic performance, most rely on foreign datasets and do not adequately reflect the realities of Nigerian tertiary institutions. There is, therefore, a gap in the development of predictive models that are tailored to the Nigerian educational environment.

The absence of such predictive systems limits the ability of institutions to leverage student data for proactive academic planning. Furthermore, even when models are developed, they often remain as offline scripts that are inaccessible to academic advisors. There is a significant lack of integrated web-based platforms that provide real-time, interpretable predictions to non-technical stakeholders. This study seeks to address this gap by developing an interpretable machine learning-based web application for student academic performance in Nigerian tertiary institutions.

1.2 Aim of the Study

The aim of this study is to develop an interpretable machine learning-based web application for forecasting student academic performance in Nigerian tertiary institutions.

1.3 Objectives of the Study

The specific objectives of the study are to:

Identify key academic, demographic, and behavioral factors that influence student academic performance.
Design and preprocess a dataset using SMOTE (Synthetic Minority Over-sampling Technique) to address inherent class imbalances.
Develop and train selected machine learning models (Random Forest and LightGBM) for academic outcomes.
Implement an Explainable AI (XAI) layer using SHAP (SHapley Additive exPlanations) to interpret model predictions.
Determine the most influential factors affecting student academic performance using feature importance techniques.
To develop a web-based dashboard using Node.js and Python for the visualization of predictive insights.

1.4 Research Questions

The study seeks to answer the following research questions:

What factors significantly influence student academic performance in Nigerian tertiary institutions?
Which machine learning algorithm provides the most accurate prediction of student academic performance?
How effective are machine learning models in identifying students at risk of poor academic performance?

1.5 Research Hypotheses

The following null hypotheses were formulated for the study:

H₀₁: Academic, demographic, and behavioral factors do not significantly influence student academic performance.
H₀₂: There is no significant difference in the predictive performance of the selected machine learning algorithms.

1.6 Significance / Justification of the Study

This study is significant in the following ways:

Educational Institutions: It provides a data-driven tool for early identification of at-risk students, enabling timely academic interventions.
Students: It supports improved academic outcomes through proactive monitoring and support.
Researchers: It contributes empirical evidence and insights specific to Nigerian tertiary institutions.
Policy Makers: It supports informed educational planning and policy formulation based on predictive analytics.

1.7 Scope of the Study

The study focuses on undergraduate students in Nigerian tertiary institutions. It utilizes historical student data, including academic records, attendance information, and demographic characteristics. The study applies supervised machine learning techniques to predict academic performance and does not include real-time data integration or postgraduate student analysis.

1.8 Limitations of the Study

The study is subject to certain limitations, including limited access to large-scale Nigerian student datasets, potential data imbalance, and constraints related to computational resources. Additionally, the findings may not be fully generalizable beyond the selected institutions or datasets.

1.9 Definition of Terms

Machine Learning: A subset of artificial intelligence that enables systems to learn patterns from data and make predictions.
Predictive Analytics: The use of data analysis techniques to forecast future outcomes.
Academic Performance: A measure of a student’s academic achievement, often expressed through grades, GPA, or CGPA.
Dataset: A structured collection of data used for analysis and model training.
Feature Importance: A technique used to identify variables that most influence model predictions.
Explainable AI (XAI): A set of tools and frameworks that help humans understand and interpret the decision-making process of machine learning models.
SHAP (SHapley Additive exPlanations): A mathematical method used to explain the output of any machine learning model by assigning each feature an importance value for a particular prediction.
SMOTE: An over-sampling technique that generates synthetic samples for the minority class (e.g., at-risk students) to improve model fairness and accuracy.
