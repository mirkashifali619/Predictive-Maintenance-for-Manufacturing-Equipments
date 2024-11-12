# This Code needs to be runned on the PowerBI Dashboard PowerQuery Script

import pickle
import pandas as pd

# Load the dataset from Power BI
equipment_data = dataset  # 'dataset' is the default input data in Power BI for Python scripts

# Load the model
with open('predictive_maintenance_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the PredictiveMaintenanceRecommender class
class PredictiveMaintenanceRecommender:
    def __init__(self, model, healthy_threshold=80):
        self.model = model
        self.healthy_threshold = healthy_threshold

    def predict_machine_condition(self, equipment_data):
        failure_probability = self.model.predict_proba(equipment_data)[:, 1]
        equipment_data['machine_condition(%)'] = (1 - failure_probability)*100
        return equipment_data

    def recommend_maintenance_schedule(self, equipment_data):
        equipment_data = self.predict_machine_condition(equipment_data)
        recommendations = equipment_data.copy()
        recommendations['recommended_maintenance'] = recommendations['machine_condition(%)'] < self.healthy_threshold
        return recommendations

# Instantiate the class and make recommendations
recommender = PredictiveMaintenanceRecommender(model)
recommendations = recommender.recommend_maintenance_schedule(equipment_data)

# Output the result to Power BI
result = recommendations
