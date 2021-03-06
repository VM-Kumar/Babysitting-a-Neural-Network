
#import necessary libraries
import sys
import cv2
import numpy as np
import random
from matplotlib import pyplot
#from keras.datasets import cifar10
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.regularizers import l2
from keras.callbacks import LearningRateScheduler
from keras.preprocessing.image import ImageDataGenerator

# define cnn model
def define_model(W,L):
  model = Sequential()
  model.add(Flatten(input_shape=(20,20,3)))
  model.add(Dense(20, activation='relu', kernel_initializer='he_uniform', kernel_regularizer=l2(W)))
  model.add(Dense(2, activation='softmax'))
  # compile model
  opt = SGD(learning_rate=L, momentum=0.9)
  model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
  return model

# obtaining the dataset
trainsize=1000
testsize=100

############insert path of the dataset folder containing 4 folders dataset_face_train,dataset_nonface_train,dataset_face_test,dataset_nonface_test containing 1000,1000,100,100 images resply
path=r'/content/drive/My Drive/dataset/......'
img_face_train=[]
for i in range(trainsize//2):
    pat= path + 'dataset_face_train/im{}.jpg'.format(i+1)
    image=cv2.imread(pat)
    img_face_train.append(image)
img_face_train=np.array(img_face_train)    


img_face_test=[]
for i in range(testsize//2):
    pat= path + 'dataset_face_test/im{}.jpg'.format(i+1)
    image=cv2.imread(pat)
    img_face_test.append(image)
img_face_test=np.array(img_face_test)


img_nonface_train=[]
for i in range(trainsize//2):
    pat= path + 'dataset_nonface_train/im{}.jpg'.format(i+1)
    image=cv2.imread(pat)
    img_nonface_train.append(image)
img_nonface_train=np.array(img_nonface_train)


img_nonface_test=[]
for i in range(testsize//2):
    pat= path + 'dataset_nonface_test/im{}.jpg'.format(i+1)
    image=cv2.imread(pat)
    img_nonface_test.append(image)
img_nonface_test=np.array(img_nonface_test)

trainY=np.array([[0]]*(trainsize//2) + [[1]]*(trainsize//2))
testY=np.array([[0]]*(testsize//2) + [[1]]*(testsize//2))
trainY = to_categorical(trainY)
testY = to_categorical(testY)
trainX=np.append(img_face_train,img_nonface_train,axis=0)
testX=np.append(img_face_test,img_nonface_test,axis=0)
print(trainX.shape,type(trainX),testX.shape,type(testX))

# convert from integers to floats
train_norm = trainX.astype('float32')
test_norm = testX.astype('float32')

# normalize to range 0-1
trainX = train_norm / 255.0
testX = test_norm / 255.0

#Normalization
trainX-=np.mean(trainX,axis=0)
trainX/=np.std(trainX,axis=0)
testX-=np.mean(testX,axis=0)
testX/=np.std(testX,axis=0)
batch_size=64

# Common Training module with normalized data and data augmentation
Weight_Decay=1e-6 ;Learning_Rate=0.00001
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))

#train to overfit
Weight_Decay=1e-6 ;Learning_Rate=0.01
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=100,
                    verbose=1,validation_data=(testX,testY))

#4.	Sanity Check:Keep constant learning rate=0.001 and increase regularization
#(i) Regularization= 0 (no regularization)
Weight_Decay=0 ;Learning_Rate=0.001
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))
#(ii) Regularization= 1000 (no regularization)
Weight_Decay=1000 ;Learning_Rate=0.001
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))
#(iii) Regularization= 10000 (no regularization)
Weight_Decay=10000 ;Learning_Rate=0.001
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))

#5.	Sanity Check 2:For a constant Regularization=0.001 and change Learning 
#(i) Learning Rate=1e-6 
Weight_Decay=0.001 ;Learning_Rate=1e-6
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))


#(i) Learning Rate=1e-3
Weight_Decay=0.001 ;Learning_Rate=1e-3
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))

#(i) Learning Rate=1e1    
Weight_Decay=0.001 ;Learning_Rate=1e1
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))

#Hyperparameter Tuning
max_count=10
for count in range(max_count):
  REG=10**random.uniform(-6,0)
  LR=10**random.uniform(-6,-1)  
  model = define_model(REG,LR)
  print('Regularization=',REG,'Learning Rate=',LR)
  datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
  datagen.fit(trainX)
  model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                      steps_per_epoch=trainX.shape[0] // batch_size,epochs=5,
                      verbose=1,validation_data=(testX,testY))

# Train for most suitable value Regularization= 0.02597090269567742 Learning Rate= 0.05210002876562015
Weight_Decay=0.02597090269567742 ;Learning_Rate=0.05210002876562015
model = define_model(Weight_Decay,Learning_Rate)
datagen = ImageDataGenerator(rotation_range=15,width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True,)
datagen.fit(trainX)
model.fit_generator(datagen.flow(trainX,trainY, batch_size=64),
                    steps_per_epoch=trainX.shape[0] // batch_size,epochs=10,
                    verbose=1,validation_data=(testX,testY))

# evaluate model
_, acc = model.evaluate(testX, testY, verbose=0)
print('> %.3f' % (acc * 100.0))
# learning curves
summarize_diagnostics(history)
