# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/10_models.ipynb (unless otherwise specified).

__all__ = ['SimpleFeedForwardNetwork5', 'Simple1DConvNet']

# Cell

import tensorflow as tf

# Cell

class SimpleFeedForwardNetwork5(tf.keras.Model):
    def __init__(self, num_classes: int = 0, input_length: int = 0, **kwargs):
        if(num_classes == 0 or input_length == 0):
            raise Exception('ModelDimensionException')
        super(SimpleFeedForwardNetwork15, self).__init__(**kwargs)
        self.dense_1 = tf.keras.layers.Dense(input_length, activation='relu', name='layer1')
        self.dense_2 = tf.keras.layers.Dense(2048, activation='relu', name='layer2')
        self.dense_3 = tf.keras.layers.Dense(1024, activation='relu', name='layer3')
        self.dense_4 = tf.keras.layers.Dense(512, activation='relu', name='layer4')
        self.dense_5 = tf.keras.layers.Dense(num_classes, activation='softmax', name='layer5')

    def call(self, inputs):
        x = self.dense_1(inputs)
        x = self.dense_2(x)
        x = self.dense_3(x)
        x = self.dense_4(x)
        return self.dense_5(x)

class Simple1DConvNet(tf.keras.Model):
    def __init__(self, num_classes: int = 0, input_dimension=0,
                 conv_width: int = 32, batch_input_shape=0,
                 **kwargs):
        if(num_classes == 0 or input_dimension == 0):
            raise Exception('ModelDimensionException')
        super(Simple1DConvNet, self).__init__(**kwargs)
        self.conv_1 = tf.keras.layers.Conv1D(32, conv_width, padding='same',
                                             input_shape=input_dimension[1:],
                                             activation='relu', name='conv1')
        self.batch_norm_1 = tf.keras.layers.BatchNormalization(axis=1, name='batch_norm_1')
        self.max_pooling_1 = tf.keras.layers.MaxPooling1D(pool_size=(3,), name='max_pooling_1')
        self.dropout_1 = tf.keras.layers.Dropout(0.25, name='dropout_1')

        self.conv_2 = tf.keras.layers.Conv1D(64, conv_width, padding='same', activation='relu', name='conv2')
        self.batch_norm_2 = tf.keras.layers.BatchNormalization(axis=1, name='batch_norm_2')
        self.conv_3 = tf.keras.layers.Conv1D(64, conv_width, padding='same', activation='relu', name='conv3')
        self.batch_norm_3 = tf.keras.layers.BatchNormalization(axis=1, name='batch_norm_3')
        self.max_pooling_2 = tf.keras.layers.MaxPooling1D(pool_size=(2,), name='max_pooling_2')
        self.dropout_2 = tf.keras.layers.Dropout(0.25, name='dropout_2')

        #self.conv_4 = tf.keras.layers.Conv1D(128, conv_width, padding='same', activation='relu', name='conv4')
        #self.batch_norm_4 = tf.keras.layers.BatchNormalization(axis=1, name='batch_norm_4')
        #self.conv_5 = tf.keras.layers.Conv1D(128, conv_width, padding='same', activation='relu', name='conv5')
        #self.batch_norm_5 = tf.keras.layers.BatchNormalization(axis=1, name='batch_norm_5')
        #self.max_pooling_3 = tf.keras.layers.MaxPooling1D(pool_size=(2,), name='max_pooling_3')
        #self.dropout_3 = tf.keras.layers.Dropout(0.25, name='dropout_3')

        self.flatten_1 = tf.keras.layers.Flatten(name='flatten_1')

        self.dense_1 = tf.keras.layers.Dense(2048/2, activation='relu', name='dense_1')
        self.batch_norm_6 = tf.keras.layers.BatchNormalization(name='batch_norm_6')
        self.dropout_4 = tf.keras.layers.Dropout(0.5, name='dropout_4')

        self.dense_2 = tf.keras.layers.Dense(1024/2, activation='relu', name='dense_2')
        self.batch_norm_7 = tf.keras.layers.BatchNormalization(name='batch_norm_7')
        self.dropout_5 = tf.keras.layers.Dropout(0.5, name='dropout_5')

        self.dense_3 = tf.keras.layers.Dense(num_classes, activation='softmax', name='dense_3')

    def call(self, inputs):
        x = self.conv_1(inputs)
        x = self.batch_norm_1(x)
        x = self.max_pooling_1(x)
        x = self.dropout_1(x)

        x = self.conv_2(x)
        x = self.batch_norm_2(x)
        x = self.conv_3(x)
        x = self.batch_norm_3(x)
        x = self.max_pooling_2(x)
        x = self.dropout_2(x)

        #x = self.conv_4(x)
        #x = self.batch_norm_4(x)
        #x = self.conv_5(x)
        #x = self.batch_norm_5(x)
        #x = self.max_pooling_3(x)
        #x = self.dropout_3(x)

        x = self.flatten_1(x)

        x = self.dense_1(x)
        x = self.batch_norm_6(x)
        x = self.dropout_4(x)

        x = self.dense_2(x)
        x = self.batch_norm_7(x)
        x = self.dropout_5(x)

        x = self.dense_3(x)

        return x