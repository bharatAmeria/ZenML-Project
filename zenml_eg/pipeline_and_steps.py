import numpy as np

from typing import Tuple

from zenml import step, pipeline

# Create steps for a simple ML workflow
@step
def get_data() -> Tuple[np.ndarray, np.ndarray]:
    # Generate some synthetic data
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 1, 0, 1])
    return X, y

@step
def process_data(data: Tuple[np.ndarray, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    X, y = data
    # Apply a simple transformation
    X_processed = X * 2
    return X_processed, y

@step
def train_and_evaluate(processed_data: Tuple[np.ndarray, np.ndarray]) -> float:
    X, y = processed_data
    # Simplistic "training" - just compute accuracy based on a rule
    predictions = [1 if sum(sample) > 10 else 0 for sample in X]
    accuracy = sum(p == actual for p, actual in zip(predictions, y)) / len(y)
    return accuracy

# Create a pipeline that combines these steps
@pipeline
def simple_example_pipeline():
    raw_data = get_data()
    processed_data = process_data(raw_data)
    accuracy = train_and_evaluate(processed_data)
    print(f"Model accuracy: {accuracy}")

# Run the pipeline
if __name__ == "__main__":
    simple_example_pipeline()
