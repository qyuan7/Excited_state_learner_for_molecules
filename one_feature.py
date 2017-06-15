#Mean featured logistic regression

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from sklearn import linear_model,svm
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
#import data and normalization
data = genfromtxt('training_log.csv',delimiter=',')
X = data[:,:2]
Y = data[:,-1]
avg = np.mean(X,axis=0)
dev = np.std(X,axis=0)
X_normal = (X-avg)/dev
#X_normal = scaler.fit_transform(X)
test_data = genfromtxt('test_log.csv',delimiter=',')
X_test = test_data[:,:2]
X_test_normal = (X_test-avg)/dev
#X_test_normal = scaler.transform(X_test)
X_test1 = X_test_normal[:,0]
X_test2 = X_test_normal[:,1]
Y2 = test_data[:,-1]
h=0.02 # stepsize in the mesh
X_train = X_normal[:,0]
logreg = linear_model.LogisticRegression(C=1)
svmreg = svm.SVC(kernel='rbf',C=1.8,gamma=7).fit(X_train.reshape(len(X_train),1),Y)
#svmreg = svm.SVC(kernel='rbf', C=0.5,gamma=2)

# we create an instance of Neighbours Classifier and fit the data
#logreg.fit(X_train.reshape(len(X_train),1), Y)
#svmreg.fit(X_train.reshape(len(X_train),1), Y)

# Plot decision boundary. Assign each point in the mesh [x_min,xmax]*[y_min,y_max]
x_min, x_max = X_normal[:, 0].min() - .5, X_normal[:, 0].max() + .5
y_min, y_max = X_normal[:, 1].min() - .5, X_normal[:, 1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min,x_max,h), np.arange(y_min,y_max,h))
Z = svmreg.predict(np.c_[xx.ravel()].reshape(len(np.c_[xx.ravel()]),1))
#Z = svmreg.predict(np.c_[xx.ravel(), yy.ravel()])
# Put result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1, figsize=(4,3))
plt.pcolormesh(xx,yy,Z,cmap=plt.cm.Paired)

#Predict on test set
Z1 = svmreg.predict(X_normal[:,0].reshape(len(X_normal[:,0]),1))
Z2 = svmreg.predict(X_test_normal[:,0].reshape(len(X_test_normal[:,0]),1))

#Calculate accuracy, precision, recall
train_result = (Z1-Y).tolist()
train_result2 = (Z1+Y).tolist()
test_result = (Z2-Y2).tolist()
test_result2 = (Z2+Y2).tolist()
train_tp,train_tn = train_result2.count(2),train_result2.count(0)
train_fp,train_fn = train_result.count(1),train_result.count(-1)
test_tp,test_tn = test_result2.count(2),test_result2.count(0)
test_fp,test_fn = test_result.count(1),test_result.count(-1)
train_acc = float(train_tp+train_tn)/len(Z1)
train_pre = float(train_tp)/(train_tp+train_fp)
train_rec = float(train_tp)/(train_tp+train_fn)
test_acc = float(test_tp+test_tn)/len(Z2)
test_pre = float(test_tp)/(test_tp+test_fp)
test_rec = float(test_tp)/(test_tp+test_fn)
 
print 'training set: accuracy %10.2f, precision %10.2f, recall %10.2f' % (train_acc,train_pre,train_rec)
print 'test set: accuracy %10.2f, precision %10.2f, recall %10.2f' % (test_acc, test_pre,test_rec)

#Plot training or test set
#plt.scatter(X_test1[Y2 == 1], X_test2[Y2 == 1], c='b', s = 50, marker = '^',label='Unstable')
#plt.scatter(X_test1[Y2 == 0], X_test2[Y2 == 0], c='r', s = 50, marker = 's',label='Stable')
plt.scatter(X_normal[:,0][Y == 1], X_normal[:,1][Y == 1], c='b',s=50, marker = '^',label='Unstable')
plt.scatter(X_normal[:,0][Y == 0], X_normal[:,1][Y == 0], c='r',s=50, marker = 's',label='Stable')
leg = plt.legend(loc = 'upper right',fancybox=True,fontsize='x-small')
leg.get_frame().set_alpha(0.5)
#plt.scatter(X_normal[:,0],X_normal[:,1], c=Y,s=40, edgecolors='k',cmap=plt.cm.Paired)
plt.xlim(xx.min(),xx.max())
plt.ylim(yy.min(),yy.max())
plt.xlabel('Normalized Energy')
plt.ylabel('Normalized Strength')
plt.title('Training set')
#plt.savefig('Test_trans.png',bbox_inches='tight',transparent= True)
plt.show()
