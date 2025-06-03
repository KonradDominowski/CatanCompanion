import os
from ultralytics import YOLO

# project_root = r'C:\Users\Konrad\Documents\pythonProject\pythonProject'
img_path = './images/test_may_2.jpg'
model = './model.pt'

classes = {
    'hexes': [i for i in range(0, 6)],
    'buildings': [i for i in range(6, 18)],
    'numbers': [i for i in range(18, 28)],
    'harbours': [i for i in range(28, 34)],
    'robber': [34]
}

for key, value in classes.items():
    model = YOLO(model)
    result = model.predict(img_path, classes=value, imgsz=1600)
    result[0].save('./test' + os.sep + key + '.jpg')
