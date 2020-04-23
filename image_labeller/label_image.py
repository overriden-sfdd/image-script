import json
import cv2
from PIL import Image


class BboxDrawer:
    '''
    Pay attention please that in image_labeller lies image based
    on the last json file (which was deleted to hide tokens and other info) 
    we get in pdf task guidance  i copied it on my local machine 
    to understand the structure better and thus apply this BboxDrawer.
    Hence it doesn't represent objects in any of my images in ../images dir
    it just contains an example of how my dirty BboxDrawer works.
    '''
    def __init__(self, bbox_color:tuple, label_color:tuple, font_size:float, json_object, alpha=0.3): 
        self.alpha = alpha
        self.bbox_color = bbox_color
        self.label_color = label_color
        self.font_size = font_size
        self.json_object = json_object
        self.image_path, self.image = None, None        # very dumb and ugly way
        self.num_objects, self.image_dict = None, None  # made for simplicity 

    def draw_bbox(self, w, h, x, y, label):
        overlay = self.image.copy()
        cv2.rectangle(self.image, (x, y), (x+w, y+h), self.bbox_color, 2)
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, self.font_size, 2)
        yLeftBottom = max(y, labelSize[1])
        cv2.rectangle(self.image, (x, yLeftBottom - labelSize[1]),
                                (x + labelSize[0], yLeftBottom + baseLine),
                                (255, 255, 255,), cv2.FILLED) # white color on the label background
        cv2.putText(self.image, label, (x, yLeftBottom),
                    cv2.FONT_HERSHEY_SIMPLEX, self.font_size, (0, 0, 0)) # black color on the label text
        cv2.addWeighted(overlay, self.alpha, self.image, 1 - self.alpha, 0, self.image)

    def get_img_data(self, idx):        
        idt = self.image_dict[idx]
        return (idt['width'], idt['height'], idt['x'], idt['y'], idt['label'])
       
    def label_and_bound(self):
        self.init_nones()
        for idx in range(self.num_objects):
            w, h, x, y, label = self.get_img_data(idx)
            self.draw_bbox(w, h, x, y, label)
            if idx == self.num_objects - 1: self.save_image() # very ugly but works 

    def save_image(self):
        img = Image.fromarray(self.image).convert('RGB')
        img.save(self.image_path)

    def init_nones(self):  # init our Nones in __init__ (dealing with opening image times
        img_dct = self.read_json()  # how many detected objects we have in image)
        self.image_dict = img_dct['session']['stillages'][0]['shelves'][0]['positions'][:-1]
        self.image_path = img[dct]['session']['imageParts']['path']
        self.image = cv2.imread(self.image_path)
        self.num_objects = len(self.image_dict)

    def read_json(self):  # get json data about image or in practice server response
        if isinstance(self.json_object, str):
            with open(self.json_object, 'r') as f: 
                return json.load(f)
        else: 
            return json.load(json_object)


# bd = BboxDrawer((255, 0, 0), (0, 255, 0), 1.5, 'img_js.json')
bd.label_and_bound()