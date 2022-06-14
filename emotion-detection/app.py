
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import keras
import numpy as np
import librosa
import os

class livePredictions:
    """
    Main class of the application.
    """

    def __init__(self, path):
        """
        Init method is used to initialize the main parameters.
        """
        self.path = path
        

    def load_model(self):
        """
        Method to load the chosen model.
        :param path: path to your h5 model.
        :return: summary of the model with the .summary() function.
        """
        self.loaded_model = keras.models.load_model(self.path)
        return self.loaded_model.summary()

    def makepredictions(self,file):
        """
        Method to process the files and create your features.
        """
        data, sampling_rate = librosa.load(file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predictions = np.argmax(self.loaded_model.predict(x), axis=-1)
        pred=self.convertclasstoemotion(predictions)
        print("Prediction is", " ", pred)
        return pred 

    @staticmethod
    def convertclasstoemotion(pred):
        """
        Method to convert the predictions (int) into human readable strings.
        """
        
        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if (int(key) == pred):
                label = value
        return label






pred = livePredictions(path='models/model_1.h5')
pred.load_model()
# Define a flask app
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
    
        # Get the file from post request
        print(request.files)
        f = request.files['voice']
      
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        # Make prediction
     
       
        result={}

        result['pred']=pred.makepredictions(file=file_path)
        return result
    return None
if __name__ == '__main__':
   app.run(debug=True)