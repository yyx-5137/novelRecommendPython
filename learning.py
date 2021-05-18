import pandas as pd
import numpy as np
import tensorflow as tf


def normalizeRatings(rating, record):
    m, n = rating.shape
    rating_mean = np.zeros((m, 1))
    rating_norm = np.zeros((m, n))
    for i in range(m):
        idx = record[i, :] !=0
        rating_mean[i] = np.mean(rating[i, idx])
        rating_norm[i, idx] -= rating_mean[i]
    return rating_norm, rating_mean

def learning():
	ratings_df = pd.read_csv('ml-latest-small/ratings.csv')
	novels_df = pd.read_csv('ml-latest-small/novels.csv')

	novels_df['novelRow'] = novels_df.index

	novels_df = novels_df[['novelRow', 'novelId', 'title']]
	novels_df.to_csv('novelsProcessed.csv', index=False, header=True, encoding='utf-8')

	ratings_df = pd.merge(ratings_df, novels_df, on='novelId')

	ratings_df = ratings_df[['userId', 'novelRow', 'rating']]
	ratings_df.to_csv('ratingsProcessed.csv', index = False, header=True, encoding='utf-8')
	pd.read_csv('ml-latest-small/novels.csv')
	userNo = ratings_df['userId'].max()+1
	novelNo = ratings_df['novelRow'].max()+1

	rating = np.zeros((novelNo, userNo))

	flag = 0
	ratings_df_length = np.shape(ratings_df)[0]

	for index, row in ratings_df.iterrows():
		rating[int(row['novelRow']), int(row['userId'])] = row['rating']
		flag += 1
		if flag % 5000 == 0:
			print('processed %d, %d left' % (flag, ratings_df_length-flag))

	record = rating>0

	record = np.array(record, dtype=int)


	rating_norm, rating_mean = normalizeRatings(rating, record)

	rating_norm = np.nan_to_num(rating_norm)

	rating_mean = np.nan_to_num(rating_mean)

	num_features = 10
	X_parameters = tf.Variable(tf.random_normal([novelNo, num_features], stddev=0.35))
	Theta_paramters = tf.Variable(tf.random_normal([userNo, num_features], stddev=0.35))
	loss = 1/2 * tf.reduce_sum(((tf.matmul(X_parameters, Theta_paramters, transpose_b=True) - rating_norm)*record)**2) + \
		1/2 * (tf.reduce_sum(X_parameters**2) + tf.reduce_sum(Theta_paramters**2))
	optimizer = tf.train.AdamOptimizer()
	train = optimizer.minimize(loss)

	tf.summary.scalar('loss', loss)
	summaryMerged = tf.summary.merge_all()
	filename = './novel_tensorboard'
	# writer = tf.summary.FileWriter(filename)

	sess = tf.Session()
	init = tf.global_variables_initializer()
	sess.run(init)

	penalty = novelNo*userNo

	for i in range(3000):
		l, _, novel_summary = sess.run([loss, train, summaryMerged])
		if i%100 == 0:
			Current_X_parameters, Current_Theta_parameters = sess.run([X_parameters, Theta_paramters])
			predicts = np.dot(Current_X_parameters,Current_Theta_parameters.T) + rating_mean
			errors = np.mean((predicts - rating)**2)
			print('step:', i, ' train loss:%.5f' % (l/penalty), ' test loss:%.5f' % errors)
		# writer.add_summary(novel_summary, i)

	Current_X_parameters, Current_Theta_parameters = sess.run([X_parameters, Theta_paramters])
	predicts = np.dot(Current_X_parameters,Current_Theta_parameters.T) + rating_mean
	errors = np.mean((predicts - rating)**2)
	return predicts
	# user_id = userid

	# sortedResult = predicts[:, int(user_id)].argsort()[::-1]
	# idx = 0
	# print('为该用户推荐的评分最高的20部电影是：'.center(80, '='))
	# for i in sortedResult:
		# print('评分：%.2f, 电影名：%s' % (predicts[i, int(user_id)], novels_df.iloc[i]['title']))#novelId
	# 	idx += 1
	# 	if idx == 20: break
		
		
		