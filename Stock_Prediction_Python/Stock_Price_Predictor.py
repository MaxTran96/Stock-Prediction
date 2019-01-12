import tensorflow as tf
from Data_Handler import build_data_subsets

def measure_accuracy(actual, expected):
    num_correct = 0
    for i in range(len(actual)):
        actual_value = actual[i]
        expected_value = expected[i]
        if actual_value[0] >= actual_value[1] and expected_value[0] >= expected_value[1]:
            num_correct+=1
        elif  actual_value[0] <= actual_value[1] and expected_value[0] <= expected_value[1]:
            num_correct+=1
    return (num_correct /len(actual))*100

x_train, y_train = build_data_subsets('AAPL', '20180601', '20181125')
x_test, y_test = build_data_subsets('AAPL', '20181125', '20181205')


x_input = tf.placeholder(dtype=tf.float32, shape=[None, 5], name='x_input')
y_input = tf.placeholder(dtype=tf.float32, shape=[None, 2], name='y_input')

W = tf.Variable(initial_value=tf.ones(shape=[5,2]))
b = tf.Variable(initial_value=tf.ones(shape=[2]))
y_output = tf.add(tf.matmul(x_input, W), b, name='y_output')
loss = tf.reduce_sum(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_input, logits=y_output)))
optimizer = tf.train.AdamOptimizer(0.01).minimize(loss)

saver = tf.train.Saver()

session = tf.Session()
session.run(tf.global_variables_initializer())
tf.train.write_graph(session.graph_def, '.','stock_prediction.pbtxt', False)
saver.save(session, save_path='./stock_prediction.ckpt')

for _ in range(20000):
    session.run(optimizer, feed_dict={x_input:x_train , y_input:y_train})
print(measure_accuracy(session.run(y_output, feed_dict={x_input: x_train}), y_train))
print(measure_accuracy(session.run(y_output, feed_dict={x_input: x_test}), y_test))