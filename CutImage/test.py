import tensorflow as tf
import numpy as np
# np.set_printoptions(threshold=np.inf) #全部输出
SEED = 23455

rdm = np.random.RandomState(SEED)#基于seed产生随机数
#随机数返回32行2列的矩阵 表示32组
X = rdm.rand(32,2)

with tf.Session() as sess:#计算
    init_op = tf.global_variables_initializer()#初始化
    sess.run(init_op)#初始化
    print(rdm)#打印
    # print(X)#打印