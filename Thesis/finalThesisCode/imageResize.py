import matplotlib.pyplot as plt
from PIL import Image
import dlib
import os
import pandas as pd
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from skimage.io import imread
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from skimage.transform import resize
from IPython.display import display
from sklearn.svm import SVR

datadir = "/Users/sabrinasimkhovich/Desktop/Thesis/all_Emotion_Images"
emotions = ["Neutral", "Happy", "Sad"
    , "Surprise", "Anger", "Disgust", "Fear"]
# flat_data_arr = []
# target_arr = []
detector = dlib.get_frontal_face_detector()
flat_file = open("flat_data_arr_fl", 'rb')
flat_data_arr = pickle.load(flat_file)
tar_file = open("target_arr_fl", 'rb')
target_arr = pickle.load(tar_file)

# SVM variables
param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [0.0001, 0.001, 0.1, 1], 'kernel': ['rbf', 'poly']}
svc = svm.SVC(probability=True)
#
# for i in emotions:
#     print(f'loading... category : {i}')
#     path = os.path.join(datadir, i)
#     for img in os.listdir(path):
#         if not img.startswith('.') and os.path.isfile(os.path.join(path, img)):
#             img_array = imread(os.path.join(path, img))
#             while (True):
#                 faces = detector(img_array)
#                 for face in faces:
#                     x1 = face.left()
#                     y1 = face.top()
#                     x2 = face.right()
#                     y2 = face.bottom()
#                 x, y = x1, y1
#                 width, height = x2, y2
#                 area = (x, y, width, height)
#                 image = Image.fromarray(img_array, 'RGB')
#                 break
#             cropped_img = image.crop(area)
#             imgARR = np.array(cropped_img)
#             graying = np.mean(imgARR, axis=2)
#             img_resized = resize(graying, (150, 150, 3))
#             flat_data_arr.append(img_resized.flatten())
#             target_arr.append(emotions.index(i))
#     print(f'loaded category:{i} successfully')

# with open("flat_data_arr_fl", 'wb') as fi:
#     pickle.dump(flat_data_arr, fi)
# with open("target_arr_fl", 'wb') as fi:
#     pickle.dump(target_arr, fi)


print("Graphing data")
# creates a plotted graph of data
df = pd.DataFrame(flat_data_arr)
df['Target'] = target_arr

print("---------------------------------------------")
# setting x and y variables to a certain data point --> pretty sure its the end
x = df.iloc[:, :-1]
y = df.iloc[:, -1]

# randomly splits data frame into train and test splits
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=77, stratify=y)

# trains the model and creates a prediction variable
print("The training of the model is started, please wait for while as it may take few minutes to complete")
print("---------------------------------------------")
model = GridSearchCV(svc, param_grid)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
np.array(y_test)
print(f"The model is {accuracy_score(y_pred, y_test) * 100}% accurate")
print("---------------------------------------------")
pickle.dump(model, open('img_model.p', 'wb'))


while(True):
    model = pickle.load(open("img_model.p", "rb"))# model is loaded
    print("model loaded")
    y_pred = model.predict(x_test) # a new predicition value is created for another subset array
    url = input('Enter URL of Image') # user input is prompted
    img = imread(url) # the url is read
    while (True):# facial detection code detects face and cropps the image just as it did earlier
        faces = detector(img)
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
        x, y = x1, y1
        width, height = x2, y2
        area = (x, y, width, height)
        image = Image.fromarray(img, 'RGB')
        break
    cropped_img = image.crop(area) # the same image processing is done where it is cropped, turned into an array, into a gray array and the transformed again to a set size
    croppedImgArr = np.array(cropped_img)
    grayomginput = np.mean(croppedImgArr, axis=2)
    inputRES = resize(grayomginput, (150, 150, 3))# probably messing up the resize becuase addimg more area. but probably not gonna fix it
    plt.imshow(inputRES)
    plt.show()
    l = [inputRES.flatten()] # the image data is flattened
    probability = model.predict_proba(l) # computer proboably outcomes of the flatteneed image
    print(f"The model is {accuracy_score(y_pred, y_test) * 100}% accurate") # outputs an accuracy score
    print("The predicted image is : " + emotions[model.predict(l)[0]]) # a predicted emotion
    print(f'Is the image a {emotions[model.predict(l)[0]]} ?(y/n)') # and then asks user weather that emotion is correct or not
    while (True):
        b = input()
        if (b == "y" or b == "n"):
            break
        print("please enter either y or n")
    # if answer is "n" or NO, the image is re trained with the new data
    if (b == 'n'):
        print("What is the image?") # if the asnwer is no, program asks for the correct image
        for i in range(len(emotions)):
            print(f"Enter {i} for {emotions[i]}")
        k = int(input())
        while (k < 0 or k >= len(emotions)):
            print(f"Please enter a valid number between 0-{len(emotions) - 1}")
            k = int(input())
        print("Please wait for a while for the model to learn from this image :)") # the program begins the retraining process of the model
        flat_arr = flat_data_arr.copy()
        tar_arr = target_arr.copy()
        tar_arr = np.append(tar_arr, k)
        flat_arr.extend(l)
        tar_arr = np.array(tar_arr)
        flat_df = np.array(flat_arr)
        df1 = pd.DataFrame(flat_df)
        df1['Target'] = tar_arr
        model1 = GridSearchCV(svc, param_grid)
        x1 = df1.iloc[:, :-1]
        y1 = df1.iloc[:, -1]
        x_train1, x_test1, y_train1, y_test1 = train_test_split(x1, y1, test_size=0.20, random_state=77, stratify=y1)
        d = {}
        for i in model.best_params_:
            d[i] = [model.best_params_[i]]
        model1 = GridSearchCV(svc, d)
        model1.fit(x_train1, y_train1)
        y_pred1 = model.predict(x_test1)
        print(f"The model is now {accuracy_score(y_pred1, y_test1) * 100}% accurate")
        # all updated variables are saved to file for safety

    with open('img_model.p', "wb") as model_file:
        pickle.dump(model1, model_file)
    print("Model saved")
    model_file.close()
    print("File closed")
    print("-----------------------------")
    with open("flat_data_arr_fl", "ab") as flat_file:
        pickle.dump(flat_arr, flat_file)
    print("flat data saved")
    flat_file.close()
    print("File closed")
    print("-----------------------------")
    with open("target_arr_fl", "ab") as tar_file:
        pickle.dump(tar_arr, tar_file)
    print("target data saved")
    tar_file.close()
    print("File closed ")
    print("-----------------------------")
    print("all files updated")



# interogating the data
