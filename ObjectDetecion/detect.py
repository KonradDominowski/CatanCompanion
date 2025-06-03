from os.path import isfile, join
from os import listdir

from ultralytics import YOLO

# from utils.predict_layers import predict_layers, ModelVersion


# # Train
# model = YOLO("yolov8s.pt")
# # model = YOLO(r"C:\Users\Konrad\Documents\pythonProject\pythonProject\models\yolov8s.pt")
# results = model.train(data="config.yaml", epochs=200, imgsz=1408, workers=0)
# #
# model2 = YOLO("yolo11s.pt")
# # model2 = YOLO(r"C:\Users\Konrad\Documents\pythonProject\pythonProject\models\yolo11s.pt")
# results2 = model2.train(data="config.yaml", epochs=200, imgsz=1408, workers=0)
#
# predict_layers(ModelVersion.YOLOV8S)
# # predict_layers(ModelVersion.YOLOV8S_OLD)
# predict_layers(ModelVersion.YOLO11S)
# predict_layers(ModelVersion.YOLO11S_OLD)

project_root = r'C:\Users\Konrad\Documents\pythonProject\pythonProject'
img_path = './data/images/test/test_may_2.jpg'
models_path = './models/'

models = [f for f in listdir(models_path) if isfile(join(models_path, f))]
models_filtered = [model for model in models if '11s' in model]

classes = {
    'hexes': [i for i in range(0, 6)],
    'buildings': [i for i in range(6, 18)],
    'numbers': [i for i in range(18, 28)],
    'harbours': [i for i in range(28, 34)],
    'robber': [34]
}

for m in models_filtered:
    for key, value in classes.items():
        model = YOLO(models_path + '\\' + m)
        result = model.predict(img_path, classes=value, imgsz=1600)
        result[0].save(project_root + '\\' + 'test' + '\\' + 'june' + '\\' + m + '-' + key + '.jpg')
