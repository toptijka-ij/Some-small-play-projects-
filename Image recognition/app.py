import os

from imageai.Detection import ObjectDetection

current_dir = os.getcwd()
recognizer = ObjectDetection()
recognizer.setModelTypeAsRetinaNet()
recognizer.setModelPath(os.path.join(current_dir, 'st_m.h5'))
recognizer.loadModel()
found_objects = recognizer.detectObjectsFromImage(input_image=os.path.join(current_dir, 'before.jpg'),
                                                  output_image_path=os.path.join(current_dir, 'after.jpg'))
for obj in found_objects:
    print(obj['name'], ' : ', obj['percentage_probability'])
