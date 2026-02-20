CHAPTER TWO
LITERATURE REVIEW
2.0 Introduction

This chapter reviews existing literature related to student academic performance prediction using machine learning techniques. It examines relevant concepts, theoretical foundations, empirical studies, and related works to identify gaps that justify the current study.

2.1 Conceptual Framework

The conceptual framework for this study is based on the relationship between student-related factors and academic performance. Input variables such as academic history, attendance, demographic characteristics, and study behavior are processed using machine learning algorithms to produce predicted academic outcomes. The output of the system is the predicted student performance category, which can be used for early academic intervention.

2.2 Theoretical Framework

This study is grounded in Educational Data Mining (EDM) and Learning Analytics theories. Educational Data Mining focuses on applying data mining and machine learning techniques to educational data to understand learning processes and improve educational outcomes. Learning Analytics emphasizes the measurement, collection, and analysis of learner data for the purpose of enhancing learning environments and decision-making.

Statistical Learning Theory also underpins this study by providing a foundation for understanding how machine learning models generalize from training data to unseen data.

This study is also grounded in the CRISP-DM (Cross-Industry Standard Process for Data Mining) framework. This theoretical model provides a structured approach to the project lifecycle, spanning Business (Educational) Understanding, Data Preparation, Modeling, Evaluation, and Deployment.

2.3 Empirical Framework

Empirical studies have demonstrated the effectiveness of machine learning techniques in predicting student academic performance. These studies commonly follow a methodology involving data collection, preprocessing, feature selection, model training, and evaluation using performance metrics such as accuracy, precision, recall, and F1-score.

2.4 Review of Related Works

Several studies have explored machine learning approaches to student academic performance prediction.

Adefemi et al. (2025) proposed a hybrid CNN-BiGRU deep learning model for predicting student academic performance. The model achieved 97.48% accuracy but required significant computational resources and lacked interpretability.

Abukader et al. (2025) introduced an optimized LightGBM model enhanced with metaheuristic algorithms and introduced SHAP values to improve transparency, demonstrating improved prediction accuracy compared to baseline models. Their work proved that behavioral metrics combined with explainability provide a superior tool for intervention.

Rohani et al. (2024) applied the CatBoost algorithm to large-scale clickstream educational data, showing its effectiveness in handling categorical variables (like State of Origin or Department) and large datasets without extensive manual encoding, which is vital for diverse Nigerian datasets.

Orji et al. (2021) applied Random Forest, K-Nearest Neighbors, and Decision Tree algorithms to predict student academic performance based on motivational and study strategy factors, achieving prediction accuracy of up to 94.9%. Their study highlighted the importance of behavioral and psychological variables.

Zhu et al. (2020) employed Random Forest models to predict student grades using academic and engagement data. The study reported moderate predictive performance and emphasized the role of previous academic results.



Kalita et al. (2022) investigated Bi-LSTM models for sequential academic performance prediction, identifying prior GPA and reading habits as key predictors.

Other related studies have explored Logistic Regression, Support Vector Machines, and ensemble models, with varying levels of success depending on dataset size, feature quality, and preprocessing techniques.

2.5 Research Gap

Despite extensive research on student academic performance prediction, there is limited focus on Nigerian tertiary institutions. Additionally, many existing studies prioritize "Black Box" predictive accuracy over interpretability. Most importantly, there is a gap in the literature regarding the deployment of these models into usable web interfaces for local institutional use. This study addresses these gaps by implementing interpretable models (via SHAP) and deploying them through a dedicated web application built for the Nigerian academic environment.

2.6 Summary Table of Reference Citations

S/N
Author & Year
Methodology
Findings
Limitations
Gap to be filled
1
Rohani (2024)
CatBoost
Tree-based models handle categorical data best.
Focused on middle schools, and not 
Tertiary level.
Applies to Nigerian Tertiary level.
2
Adefemi (2025)
CNN-BiGRU
High accuracy (97.48%).
Black-box nature; complex.
Adds Explainability (SHAP).
3
Abukader (2025)
LightGBM + SHAP
Improved transparency and increased user trust.
No web-based/deployment interface.
Develops a Node.js Web App for users.
4
Orji (2022)
Random Forest
Motivation is a key feature.
Uses Chilean dataset.
Uses Nigerian student data.
5
Kalita (2025)
Bi-LSTM
Sequential data improves results.
Small dataset size.
Uses SMOTE for data balancing.




































