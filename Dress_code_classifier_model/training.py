from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import Adam
import keras,os
import numpy as np
import matplotlib.pyplot as plt

h = 300
w = 150
    
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=( h, w,1)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# model.add(Conv2D(64, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.2))

model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(2,activation='softmax'))

# model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])


# opt = Adam(lr=0.005)
model.compile(optimizer="adam", loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])

batch_size = 10


train_datagen = ImageDataGenerator(horizontal_flip=True,brightness_range=[0.3,1.0],width_shift_range=[-10,10],height_shift_range=[0,20])
test_datagen = ImageDataGenerator(horizontal_flip=True,brightness_range=[0.3,1.0],width_shift_range=[-10,10],height_shift_range=[0,20])


train_generator = train_datagen.flow_from_directory('croped/train', target_size=(h, w),batch_size=batch_size,color_mode="grayscale") 
validation_generator = test_datagen.flow_from_directory('croped/test',target_size=(h, w),batch_size=batch_size,color_mode="grayscale")

print(train_generator.samples)
print(validation_generator.samples)
print(train_generator.class_indices)
history = model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=2,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // batch_size)


model.save('version4.h5')  # always save your weights after training or during trainin

print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
