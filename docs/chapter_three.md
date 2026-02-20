## CHAPTER THREE  
## METHODOLOGY  

### 3.0 Introduction  
This chapter presents the methodology adopted for developing an interpretable machine learning-based system for predicting student academic performance risk in Nigerian tertiary institutions. Consistent with the problem statement and theoretical framing in Chapters One and Two, the methodology follows an applied, quantitative approach in which institutional-style student records are prepared for supervised learning, two tree-based classification models are constructed (Random Forest and LightGBM), and an explainability layer is implemented using SHAP (SHapley Additive exPlanations). Emphasis is placed on transparent data preparation, reproducible model construction, class imbalance handling using SMOTE, and the generation of auditable outputs such as predictions, feature importance tables, and SHAP values and plots.

---

### 3.1 Research Design  
This study adopts an applied and quantitative research design, implemented as a supervised machine learning classification task. The research is implementation-oriented and consistent with an undergraduate computer science project in a Nigerian tertiary institution context, combining data-driven model development with explainable outputs suitable for academic decision support.

The target outcome is formulated as a binary classification label, `performance_risk`, where `0` denotes “not at risk” and `1` denotes “at risk”. The modeling workflow is designed to support valid model construction by separating data preparation from model fitting, applying class imbalance handling only to the training split, and saving all major artifacts (trained pipelines, prediction outputs, feature importance tables, and SHAP explanations) for verification and reporting.

---

### 3.2 Population of the Study  
The population of the study comprises undergraduate students enrolled in Nigerian tertiary institutions (Federal, State, and Private), whose institutional records capture academic history, engagement indicators, and relevant demographic/context variables. In operational terms, the population is represented as individual student-level records, where each record corresponds to a student and includes measured predictors together with the outcome label `performance_risk`.

The unit of analysis is a single student record. To support ethical considerations, direct identifiers are excluded from model predictors; where record tracking is required, an anonymised identifier (e.g., `student_id_hash`) is retained for dataset management but removed prior to modeling.

---

### 3.4 Sample and Sampling Procedure  
The sample used for implementation and experimentation is a structured dataset stored in CSV format at `data/raw/synthetic_student_dataset.csv`. The dataset is designed to reflect typical student record attributes in Nigerian tertiary institutions, incorporating mixed data types (numerical and categorical) consistent with administrative and academic information systems.

Sampling is operationalised as the selection of a fixed dataset of student records for model development and testing. The dataset is subsequently partitioned into training and test subsets using a hold-out split implemented with stratification on the target outcome where applicable. This procedure supports reproducibility and ensures that model construction is evaluated on unseen data, while preserving the original class proportions during splitting.

The dataset schema used in the study is documented in `docs/dataset_schema.md`. The schema groups predictors into academic variables (e.g., prior performance indicators such as GPA/CGPA, carryovers and failed courses), engagement/behavioural variables (e.g., attendance and assignment submission proxies), and demographic/context variables (e.g., institution type, faculty/department, age, sex, and state of origin). The target variable is `performance_risk` with two classes (`0` and `1`).

---

### 3.5 Instrument  
The primary instrument for this study is a structured student-record dataset designed according to the schema documented in `docs/dataset_schema.md`. The instrument is implemented as a tabular data file (CSV) with one row per student and columns corresponding to measured predictors and the outcome label.

In addition to the dataset file, the study employs an automated preprocessing and modeling pipeline as an instrument for transforming raw records into a model-ready representation. This pipeline provides a consistent mechanism for imputing missing values, encoding categorical variables, scaling numerical variables, and ensuring that the same transformations are applied during both training and prediction.

---

### 3.6 Methods  

#### Data Collection  
Data for the study is represented as a structured CSV dataset located at `data/raw/synthetic_student_dataset.csv`. The dataset follows the schema described in `docs/dataset_schema.md`, with mixed numerical and categorical variables reflecting student academic history, engagement proxies, and demographic/context information typically recorded in Nigerian tertiary institutions.

To support data understanding prior to modeling, an exploratory data analysis (EDA) script (`notebooks/01_eda_student_performance.py`) was used to generate descriptive summaries and diagnostic visualisations. The EDA procedure includes:

- descriptive statistics for numerical variables and frequency distributions for categorical variables;
- missing value analysis (counts and rates) with visualisation of missingness by feature;
- assessment of the target distribution (`performance_risk`) to verify the presence of class imbalance;
- correlation analysis among numeric predictors using Pearson correlation heatmaps.

The EDA stage provides descriptive evidence of dataset structure and quality, and it informs defensible preprocessing and class imbalance handling decisions.

#### Data Preprocessing  
Data preprocessing was implemented using reproducible pipeline components defined in `backend/python/src/preprocessing.py`, primarily with scikit-learn’s `ColumnTransformer` and `Pipeline`. The dataset contains mixed feature types; therefore, preprocessing is executed separately for numerical and categorical predictors.

The preprocessing approach comprises the following steps:

- **Feature type identification:** numerical and categorical features are inferred from the dataset after excluding the target column.
- **Missing value treatment:** numerical features are imputed using the median (`SimpleImputer(strategy="median")`), while categorical features are imputed using the most frequent category (`SimpleImputer(strategy="most_frequent")`).
- **Categorical encoding:** categorical variables are converted to a numeric form through one-hot encoding using `OneHotEncoder(handle_unknown="ignore")`, which supports stable inference when unseen categories appear during deployment.
- **Feature scaling:** numerical features are standardised using `StandardScaler()` to ensure consistent scaling across numeric predictors.

To support reproducibility and prevent leakage, the dataset is partitioned into training and test sets using a hold-out split (`train_test_split`) with stratification on `performance_risk` when the outcome contains more than one class. All preprocessing components are fit on the training partition and subsequently applied to the test partition and any future inference data.

In addition, a minimal feature engineering step is applied consistently during training and explanation: a “missing value count” feature is computed per record using `BasicFeatureEngineer(add_missing_count=True)` to provide a transparent proxy for data completeness without introducing complex derived variables.

Generated preprocessing-related outputs include:

- transformed feature matrices produced by the fitted preprocessor;
- post-transformation feature names (where available) obtained using `get_feature_names_out()` for auditing feature importance and SHAP attributions.

#### Handling Class Imbalance (SMOTE)  
The target variable `performance_risk` is treated as an imbalanced outcome consistent with real-world academic risk settings, where the at-risk class is typically a minority. To address this, the Synthetic Minority Over-sampling Technique (SMOTE) is employed using `imblearn.over_sampling.SMOTE`.

The operational procedure for SMOTE is implemented in `backend/python/apply_smote.py` and follows a leakage-aware design:

- the data is split into training and test sets prior to any resampling;
- preprocessing is fitted on the training data only and used to transform the training predictors;
- SMOTE is applied only to the transformed training set (`fit_resample`) to generate synthetic minority examples.

For auditability, the SMOTE script reports class distributions before and after resampling and saves resampled training data to `artifacts/smote/` as:

- `X_train_smote.csv`
- `y_train_smote.csv`

These outputs support transparent reporting and enable verification of the resampling procedure.

#### Model Development  
Model development was implemented in Python using scikit-learn, imbalanced-learn, and LightGBM. Two tree-based classifiers were constructed under a consistent pipeline design to ensure that preprocessing and resampling steps are applied identically during training and prediction.

The core design is an imbalanced-learn pipeline (`imblearn.pipeline.Pipeline`) with the following ordered stages:

- `preprocessor`: imputes missing values, encodes categorical variables, and scales numeric variables;
- `smote`: applies SMOTE within the training procedure;
- `model`: the classifier (Random Forest or LightGBM).

Hyperparameter selection is conducted using `GridSearchCV` with five-fold cross-validation, using a small and defensible grid suitable for an undergraduate scope and computational constraints. The scoring function used for search is `f1_macro` to provide an evaluation criterion that does not depend solely on the majority class.

Model outputs generated by the training scripts include:

- a saved fitted pipeline (for reuse in deployment and explanation);
- a metrics payload saved as JSON (including chosen hyperparameters and evaluation metrics, without interpretive claims in the methodology);
- a feature importance table saved as CSV, computed in the post-preprocessing feature space.

##### Random Forest  
The Random Forest model is implemented in `backend/python/train_random_forest.py` using `sklearn.ensemble.RandomForestClassifier`. The classifier is trained within the pipeline described above and configured with reproducible settings (`random_state`) and parallel execution (`n_jobs=-1`).

Hyperparameter tuning is performed using a grid search over key Random Forest parameters, including the number of trees (`n_estimators`), tree depth (`max_depth`), split and leaf constraints (`min_samples_split`, `min_samples_leaf`), and the feature sampling strategy (`max_features`).

The script generates and saves the following outputs under `artifacts/random_forest/`:

- `random_forest_pipeline.joblib` (trained end-to-end pipeline)
- `metrics.json` (training configuration and reported metrics)
- `feature_importance.csv` (model-based feature importance values aligned to transformed feature names)

##### LightGBM  
The LightGBM model is implemented in `backend/python/train_lightgbm.py` using `lightgbm.LGBMClassifier` with a binary objective. The model is trained in the same pipeline structure (preprocessing → SMOTE → classifier) and uses reproducible controls (`random_state`) and parallelism (`n_jobs=-1`).

Hyperparameter tuning is performed using a grid search across boosting configuration parameters, including the number of estimators (`n_estimators`), learning rate (`learning_rate`), leaf complexity (`num_leaves`), tree depth (`max_depth`), and subsampling controls (`subsample`, `colsample_bytree`).

The script generates and saves the following outputs under `artifacts/lightgbm/`:

- `lightgbm_pipeline.joblib` (trained end-to-end pipeline)
- `metrics.json` (training configuration and reported metrics)
- `feature_importance.csv` (model-based feature importance values aligned to transformed feature names)

#### Explainable AI Layer (SHAP)  
To satisfy the interpretability requirement stated in Chapters One and Two, an explainable AI layer is implemented using SHAP (SHapley Additive exPlanations). The SHAP utilities are implemented in `backend/python/src/explainability.py` and applied through `backend/python/explain_best_model.py`.

Given that both Random Forest and LightGBM are tree-based models, SHAP explanations are computed using `shap.TreeExplainer`. Explanations are generated in the post-preprocessing feature space by transforming input records using the fitted `preprocessor` contained within the trained pipeline.

Two categories of SHAP outputs are produced:

- **Global explanations:** a SHAP summary plot showing the overall influence of features across the dataset.
- **Local explanations:** a SHAP waterfall plot for a single student instance (selected from records predicted as at risk), showing how individual features contribute positively or negatively to that specific prediction.

The explainability script saves outputs under `artifacts/shap/`, including:

- `shap_global_summary.png` (global summary plot)
- `shap_local_waterfall_at_risk.png` (local waterfall plot)
- `local_explanation_summary.json` (top positive and negative feature contributions for the explained instance)
- `educator_friendly_interpretation.txt` (a concise narrative intended for non-technical educational stakeholders)

These outputs provide an auditable explanation layer that complements the predictive component, enabling reporting of feature attributions (SHAP values) alongside model predictions.

#### Analysis of Existing System Data  
The analysis of existing system data is conducted through an exploratory data analysis (EDA) workflow implemented in `notebooks/01_eda_student_performance.py`. This procedure examines the structure, completeness, and distributional properties of the student-record dataset to inform defensible preprocessing and modeling decisions. The EDA includes descriptive statistics for numerical and categorical variables, missing value analysis with visualisation, assessment of target class distribution to identify class imbalance, and correlation analysis among numeric predictors. The outcomes of this analysis provide descriptive evidence of dataset quality, guide the choice of imputation and encoding strategies, and justify the application of class imbalance handling techniques during model development.

#### System Design  
The proposed system is designed as a two-tier architecture that separates machine learning inference from web-facing request handling. The design consists of (i) a Python machine learning inference and explainability service, and (ii) a Node.js backend API. The Python service loads the trained pipeline, applies the fitted preprocessing steps, generates predictions, and computes SHAP-based explanations. The Node.js backend provides HTTP endpoints, validates input payloads, forwards requests to the Python service, and formats responses for users. This separation improves maintainability, ensures consistent preprocessing between training and deployment, and supports auditable generation of prediction and explanation outputs. The design aligns with the project’s interpretability requirement and with the need for a lightweight, extensible web interface for educational decision support.

#### System Programming/Construction  
System construction follows a modular implementation approach. The machine learning components are implemented in Python using scikit-learn, imbalanced-learn, LightGBM, and SHAP, with preprocessing and model training encapsulated in reproducible pipelines. The web backend is implemented in Node.js, handling request routing, validation, and response formatting. Communication between tiers is conducted via a well-defined interface (REST API) within a trusted network boundary. All major artifacts—trained pipelines, metrics, feature importance tables, and SHAP explanations—are saved to an `artifacts/` directory structure to support traceability and reporting. The implementation uses version-controlled code and deterministic random states to ensure reproducibility across training, evaluation, and deployment stages.

#### System Testing  
System testing is performed to verify that the end-to-end workflow operates correctly and that outputs are reproducible. Testing includes (i) unit and integration testing of preprocessing and model pipelines to confirm that transformations are applied consistently during training and inference; (ii) validation of SMOTE application to confirm that resampling occurs only on the training split and that class distributions are as expected; (iii) functional testing of the Python inference service to confirm that predictions and SHAP explanations are generated correctly for new records; (iv) API testing of the Node.js backend to ensure request validation, error handling, and response formatting behave as specified; and (v) end-to-end testing of the prediction and explanation flow from user input through to final output. Test cases are documented and, where applicable, saved as artifacts to support auditability and to demonstrate that the system satisfies the methodological requirements stated in this chapter.
