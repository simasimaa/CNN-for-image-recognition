import numpy as np
import matplotlib.pylab as plt
import chainer
import chainer.links as L
import chainer.functions as F
from chainer import Chain, optimizers, Variable, serializers
import recognition
import cv2
import os

x_train=[]
x_test=[]
t_train=[]
t_test=[]
recognition_dict=recognition.detection_words

for word in recognition_dict:
    path=recognition.image_folder_name+'/'+str(recognition_dict[word])
    imgList=os.listdir(path)
    img_num=len(imgList)
    train_num=int(img_num/4*3)
    for j in range(img_num):
        imgSrc=cv2.imread(path+"/"+imgList[j])
        if imgSrc is None:continue
    
        #imgSrcを(3,32,32)にサイズ変更
        imgSrc=cv2.resize(imgSrc,(32,32))
        if j<train_num:
            x_train.append(imgSrc)
            t_train.append(recognition_dict[word])
        else:
            x_test.append(imgSrc)
            t_test.append(recognition_dict[word])
    
    if j==img_num-1:
        plt.imshow(imgSrc[:,:,1])
        plt.show()
        plt.imshow(imgSrc[:,:,0])
        plt.show()
        plt.imshow(imgSrc[:,:,2])
        plt.show()
    
    
x_train=np.array(x_train).astype(np.float32).reshape((len(x_train),3,32,32))/255
t_train = np.array(t_train).astype(np.int32)
x_test = np.array(x_test).astype(np.float32).reshape((len(x_test),3,32,32))/255
t_test = np.array(t_test).astype(np.int32)

class CNN(Chain):
    def __init__(self):
        super(CNN, self).__init__(
            conv1 = L.Convolution2D(3, 20, 5), # filter 5
            conv2 = L.Convolution2D(20, 50, 5), # filter 5
            l1 = L.Linear(1250, 500),
            l2 = L.Linear(500, 500),
            l3 = L.Linear(500, len(recognition_dict), initialW=np.zeros((len(recognition_dict), 500), dtype=np.float32))
        )
    def forward(self, x):
        h = F.max_pooling_2d(F.relu(self.conv1(x)), 2)
        h = F.max_pooling_2d(F.relu(self.conv2(h)), 2)
        h = F.relu(self.l1(h))
        h = F.relu(self.l2(h))
        h = self.l3(h)
        return h
 
model = CNN()
optimizer = optimizers.Adam()
optimizer.setup(model)
 
n_epoch = 50
batch_size = 15
N=len(t_train)

accuracy_histry=[]
loss_histry=[]
for epoch in range(n_epoch):
    #train
    sum_loss = 0
    sum_accuracy = 0
    
    perm = np.random.permutation(N)
    for i in range(0, N, batch_size):
        x = Variable(x_train[perm[i:i+batch_size]])
        t = Variable(t_train[perm[i:i+batch_size]])
        y = model.forward(x)
        model.zerograds()
        loss = F.softmax_cross_entropy(y, t)
        acc = F.accuracy(y, t)
        loss.backward()
        optimizer.update()
        sum_loss += loss.data*batch_size
        sum_accuracy += acc.data*batch_size
    accuracy_histry.append(sum_accuracy/N)
    loss_histry.append(sum_loss/N)
    print("epoch: {}, mean loss: {}, mean accuracy: {}".format(epoch, sum_loss/N, sum_accuracy/N))

#グラフ化    
X_axis=np.arange(n_epoch)    
plt.plot(X_axis,accuracy_histry,label="mean-accuracy")
plt.plot(X_axis,loss_histry,label="mean-loss")
plt.xlabel("epoch")
plt.title("accuracy,loss-epoch")
plt.legend()
plt.show()

    
    
cnt = 0
testsize=len(t_test)
count={}
for i in range(testsize):
    x = Variable(np.array([x_test[i]], dtype=np.float32))
    t = t_test[i]
    y = model.forward(x)
    y = np.argmax(y.data[0])
    
    try:
        count[t]
    except:
        count[t]=[0,0]
    if t == y:
        cnt += 1
        #それぞれのラベルの正解数をカウント
        count[t][0]+=1
    #それぞれのラベルの合計数をカウント
    count[t][1]+=1         
    #print(t,y)
print("accuracy: {}".format(cnt/testsize))
#それぞれのラベルの正解数
for i in count:
    for word in recognition.detection_words:
        if recognition.detection_words[word]==i:
            print("{}の正当数:{}、誤答数{}、正解率{}".format(word,count[i][0],count[i][1]-count[i][0],count[i][0]/count[i][1]))
    