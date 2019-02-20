import tensorflow as tf

x = tf.placeholder(tf.float32, shape=(1,2))
w1 = tf.Variable(tf.random_normal([2,3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3,1], stddev=1, seed=1))

a = tf.matmul(x,w1)
y = tf.matmul(a,w2)
print(y)

with tf.Session()  as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    print(sess.run(y,feed_dict={x:[[0.7,0.5]]}))

# async def init_session():
#     # 第一次请求获取params
#     async with aiohttp.request('GET',"https://manybooks.net") as r:
#         main_text = await r.text(encoding='utf-8')
#         # print(main_text)
#         main_html = etree.HTML(main_text)
#         params = {}
#         params['form_build_id'] = main_html.xpath("//input[@name='form_build_id']/@value")
#         params['form_id'] = main_html.xpath("//input[@name='form_id']/@value")
#         params['op'] = main_html.xpath("//button[@id='edit-submit']/@value")
#         params['ga_submit'] = main_html.xpath("//input[@name='ga_event']/@value")
#         for k,v in params.items():
#             if v:
#                 params[k] = v[0]
#             else:
#                 print('No params!')
#                 return
#         params['search'] = ''
#         # print(params)
#     session = aiohttp.ClientSession()
#     async with session.post('https://manybooks.net/search-book',data=params) as res:
#         print(res.status)