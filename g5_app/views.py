from django.core.files.storage import FileSystemStorage

import joblib
import tensorflow.keras as keras
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import CsvFileUpload
from .forms import CsvForm
import xgboost as xgb
from django.contrib import messages
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler, MaxAbsScaler, LabelEncoder, \
    StandardScaler
import os
import json
import pandas as pd

module_dir = os.path.dirname(__file__)
xgb_file_path = os.path.join(module_dir, 'static/ml_models/xgb_model_heart.plk')
svm_file_path = os.path.join(module_dir, 'static/ml_models/svm_model_heart.plk')
ranf_file_path = os.path.join(module_dir, 'static/ml_models/ranf_model_heart.plk')
mlp_file_path = os.path.join(module_dir, 'static/ml_models/mlp_model_heart.h5')
svm_loaded_module = joblib.load(open(svm_file_path, 'rb'))
xgb_loaded_module = joblib.load(open(xgb_file_path, 'rb'))
ranf_loaded_module = joblib.load(open(ranf_file_path, 'rb'))
mlp_loaded_module = keras.models.load_model(mlp_file_path)

def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "upload.html", {
            "image_url": image_url
        })
    return render(request, "upload.html")

def Home(request):
    return render(request, 'generator/home.html')


class Charts(TemplateView):
    template_name = 'generator/charts.html'

    def get(self, request):
        return render(request, self.template_name)


class Tables(TemplateView):
    template_name = 'generator/tables.html'

    def get(self, request):
        return render(request, self.template_name)

class CsvFormView(TemplateView):
    template_name = 'get_csv.html'

    def get(self, request):
        form = CsvForm()
        files = CsvFileUpload.objects.all()
        args = {'form': form, 'files': files}

        return render(request, self.template_name, args)

    def post(self, request):
        data_frame = {}

        if request.method == 'POST':
            form = CsvForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                data = pd.read_csv(csv_file)
                df = pd.DataFrame(data)

                #df.to_csv('csv_data.csv', index=False)
                # Predict by using the imported cancer SVM model
                #normalized_dataset = normalize_csv_input_data_svm(data)
                prediction = svm_loaded_module.predict(data)
                probability = svm_loaded_module.predict_proba(data)

                xgb_prediction = xgb_loaded_module.predict(data)
                xgb_probability = xgb_loaded_module.predict_proba(data)

                ranf_prediction = ranf_loaded_module.predict(data)
                ranf_probability = ranf_loaded_module.predict_proba(data)

                mlp_prediction = mlp_loaded_module.predict(data)

                data['the_diagnosis'] = prediction
                data['svm_probability_false'] = probability[0][0]
                data['svm_probability_true'] = probability[0][1]

                data['xgb_diagnosis'] = xgb_prediction
                data['xgb_probability_false'] = xgb_probability[0][0]
                data['xgb_probability_true'] = xgb_probability[0][1]

                data['ranf_diagnosis'] = ranf_prediction
                data['ranf_probability_true'] = ranf_probability[0][1]

                data['mlp_diagnosis'] = mlp_prediction


                json_records = data.reset_index().to_json(orient='records')
                the_data = json.loads(json_records)
                data_frame = {'d': the_data}

                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'No es un CSV')
                    return redirect('upload_csv')

        return render(request, 'generator/diagnosis.html', data_frame)