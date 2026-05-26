import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class CollegeMLSystem:
    def __init__(self):
        self.course_model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.admission_model = LogisticRegression()
        self.le_group = LabelEncoder()
        self.train_models()

    def generate_dummy_data(self):
        groups = ['Maths', 'Biology', 'Commerce'] * 50
        marks = np.random.randint(60, 100, 150)
        courses = ['CS Engineering' if g=='Maths' and m>80 else 'Mechanical Engineering' if g=='Maths' else 'MBBS' if g=='Biology' and m>85 else 'BSc Biotechnology' if g=='Biology' else 'BCom Finance' for g, m in zip(groups, marks)]
        self.df_courses = pd.DataFrame({'Group': groups, 'Marks': marks, 'Recommended_Course': courses})
        
        categories = ['General', 'OBC', 'SC/ST'] * 50
        admitted = [1 if (m > 75 and c == 'General') or (m > 65 and c != 'General') else 0 for m, c in zip(marks, categories)]
        self.df_admissions = pd.DataFrame({'Marks': marks, 'Category': categories, 'Admitted': admitted})

    def train_models(self):
        self.generate_dummy_data()
        self.df_courses['Group_Encoded'] = self.le_group.fit_transform(self.df_courses['Group'])
        self.course_model.fit(self.df_courses[['Group_Encoded', 'Marks']], self.df_courses['Recommended_Course'])
        self.admission_model.fit(self.df_admissions[['Marks']], self.df_admissions['Admitted'])

    def predict_course(self, group, marks):
        group_enc = self.le_group.transform([group])[0]
        prediction = self.course_model.predict([[group_enc, marks]])[0]
        return [prediction, "BSc General", "Diploma in Tech"]

    def predict_admission(self, marks):
        prob = self.admission_model.predict_proba([[marks]])[0][1]
        return round(prob * 100, 2)
