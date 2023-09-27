insta_df_train = pd.read_csv('./train.csv')
print(insta_df_train.info())
insta_df_test = pd.read_csv("./test.csv")

X_train = insta_df_train.drop(columns = ['fake'])
y_train = insta_df_train['fake']

X_test = insta_df_test.drop(columns = ['fake'])
  y_test = insta_df_test['fake']

  scaler_x = StandardScaler()
  X_train = scaler_x.fit_transform(X_train)
  X_test = scaler_x.transform(X_test)

  y_train = tf.keras.utils.to_categorical(y_train, num_classes = 2)
  y_test = tf.keras.utils.to_categorical(y_test, num_classes = 2)

  model = Sequential()
  model.add(Dense(50, input_dim=7, activation='relu'))
  model.add(Dense(150, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(150, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(25, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(2,activation='softmax'))

  model.summary()

  model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
  epochs_hist = model.fit(X_train, y_train, epochs = 50,verbose = 1, validation_split = 0.1)

  predicted = model.predict(X_test)
  ans = predicted[-1]

  array = np.array(ans)
  integer_array = np.round(array).astype(int)
  integer_array = integer_array[1:]

  if(integer_array == 0):
    check = 'real'
  else:
    check = 'fake'