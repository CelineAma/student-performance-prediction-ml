# Test script to verify all required packages are installed correctly
import sys

print("Python version:", sys.version)
print("\nTesting package imports...")

try:
    import fastapi
    print("✓ FastAPI:", fastapi.__version__)
except ImportError as e:
    print("✗ FastAPI:", e)

try:
    import uvicorn
    print("✓ Uvicorn:", uvicorn.__version__)
except ImportError as e:
    print("✗ Uvicorn:", e)

try:
    import pydantic
    print("✓ Pydantic:", pydantic.__version__)
except ImportError as e:
    print("✗ Pydantic:", e)

try:
    import numpy
    print("✓ NumPy:", numpy.__version__)
except ImportError as e:
    print("✗ NumPy:", e)

try:
    import pandas
    print("✓ Pandas:", pandas.__version__)
except ImportError as e:
    print("✗ Pandas:", e)

try:
    import sklearn
    print("✓ Scikit-learn:", sklearn.__version__)
except ImportError as e:
    print("✗ Scikit-learn:", e)

try:
    import imblearn
    print("✓ Imbalanced-learn:", imblearn.__version__)
except ImportError as e:
    print("✗ Imbalanced-learn:", e)

try:
    import joblib
    print("✓ Joblib:", joblib.__version__)
except ImportError as e:
    print("✗ Joblib:", e)

print("\nAll imports completed successfully!")
