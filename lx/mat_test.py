import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

pdf = PdfPages('des_file_name.pdf')

fig = plt.figure(figsize=(8.267,11.692),dpi=300)
ax = fig.add_axes([0,0,1,1])
ax.set_xlim(0,210)
ax.set_ylim(0,297)
ax.plot([0,105,47,198,209],[0,36,88,101,219])
ax.text(50,50,'abccc')
for i in range(10):
    ax.text(10*i,10*i,'aaaaa')
pdf.savefig()
plt.close()

fig = plt.figure(figsize=(8.267,11.692),dpi=300)
ax = fig.add_axes([0,0,1,1])
ax.set_xlim(0,210)
ax.set_ylim(0,297)
ax.plot([0,105,47,198,209],[0,36,88,101,219])
ax.text(50,50,'abccc')
pdf.savefig()
plt.close()


pdf.close()
##plt.savefig('text',dpi=300)
##plt.show()

#4、对图像进行放缩
##from scipy import misc
##lena_new_sz = misc.imresize(lena, 0.5) # 第二个参数如果是整数，则为百分比，如果是tuple，则为输出图像的尺寸
##plt.figure(num=4, figsize=(8,5),)
##plt.imshow(lena_new_sz)
##plt.title('The image title')
##plt.axis('off')
##plt.show()
