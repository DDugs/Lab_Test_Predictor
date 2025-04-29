
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import joblib
from extractor import extract_lab_data_from_image
from sklearn.preprocessing import LabelEncoder
import numpy as np

model = joblib.load('lab_test_model.pkl')
test_names = ["HEMOGLOBIN", "RBC", "WBC", "PLATELET COUNT", "MCV", "MCH", "MCHC", "NEUTROPHILS"]
le = LabelEncoder()
le.fit(test_names)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:

        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        lab_tests = extract_lab_data_from_image(file_location)
        os.remove(file_location)
        for test in lab_tests:
            try:
                test_name = test.get("test_name", "")
                value = float(test.get("value", None))
                reference = float(test.get("bio_reference_range", None))

                test_encoded = le.transform([test_name])[0] if test_name in le.classes_ else 0
                feature = np.array([[test_encoded, value, reference]])
                prediction = model.predict(feature)
                test["lab_test_out_of_range"] = bool(prediction[0])
            except:
                test["lab_test_out_of_range"] = None

        return JSONResponse(content={
            "is_success": True,
            "lab_test_data": lab_tests
        })

    except Exception as e:
        return JSONResponse(content={
            "is_success": False,
            "error": str(e)
        }, status_code=500)
