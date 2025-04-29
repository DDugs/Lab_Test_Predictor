import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
with open("lab_test_results.json") as f:
    data = json.load(f)

records = []
for report in data:
    for test in report.get('lab_test_data', []):
        records.append(test)

df = pd.DataFrame(records)

df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['bio_reference_range'] = pd.to_numeric(df['bio_reference_range'], errors='coerce')
df['lab_test_out_of_range'] = df['lab_test_out_of_range'].astype(int)
le = LabelEncoder()
df['test_name_encoded'] = le.fit_transform(df['test_name'].astype(str))
X = df[['test_name_encoded', 'value', 'bio_reference_range']].dropna()
y = df.loc[X.index, 'lab_test_out_of_range']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
joblib.dump(clf, "lab_test_model.pkl")
print("Model saved to lab_test_model.pkl")
