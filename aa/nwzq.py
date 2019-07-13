import time
print("五目並べへようこそ!!!")
time.sleep(2)


def pt(message,zikan):
    print(message)
    time.sleep(zikan)

from IPython.display import Image,display


# url1 = "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1380645979,3378769833&fm=26&gp=0.jpg"
urlastarts = ['./1.jpg',
	'./2.jpg',
	'./3.jpg',
	'./4.jpg']
urlbstarts = ['./5.jpg',
	".6.jpg"]

print("ゲームが始める前に,まず過程を知る")

for url in urlastarts:
	display(Image(url))
	time.sleep(2)

print("さて、二人、準備できた？")
time.sleep(1)

print("では、ささっと対戦を始めましょう！")
time.sleep(2)

infos = ("基盤！！！！！","黒と白")
for info,url in zip(infos, urlbstarts):
	print(info)
	display(Image(url))
	time.sleep(2)

#创建棋盘的程序
def initBoard():
	global board	#调用全局的board
	board=[None]*16
	for i in range(len(board)):
		board[i]=["+"]*20

#打印棋盘的程序
def printBoard():
	global board
	for i in range(len(board)):
		for j in range(len(board[i])):
			print(board[i][j],end="")
		print()

#开始下棋的程序
def startGame():
	global board
	player=0
	while isGameContinue():
		if player%2==0:
			#黑方下棋
			print("==>黒の番")
			if not playChess("•"):
				continue
		else:
			#白方下棋
			print("==>白の番")
			if not playChess("○"):
				continue
		player+=1

def get_xy(info, error_info, max):
	while True:
		try:
			x = int(input(info))
			if 0 < x <= max:
				x -= 1
				return x
			else:
				print('请输入正确的落子{}！'.format(error_info))
		except:
			print('请输入正确的落子{}！'.format(error_info))


def playChess(chess):
	#获取位置
	x = get_xy("==> X=", '列数', len(board[0]))
	y = get_xy("==> Y=", '行数', len(board))	
	if board[x][y]=="+":
		board[x][y]=chess
		printBoard()
		return True	#落子成功
	else:
		print("ヤバ==> 改めて置こう")
		printBoard()
		return False#落子失败

def isGameContinue():
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j]!="+ ":
				#横向
				if j<=11:
					if board[i][j]==board[i][j+1]==board[i][j+2]==board[i][j+3]==board[i][j+4] and board[i][j] != '+':
						whoWin(i,j)
						return False
				#竖向
				if i<=11:
					if board[i][j]==board[i+1][j]==board[i+2][j]==board[i+3][j]==board[i+4][j] and board[i][j] != '+':
						whoWin(i,j)
						return False
				#反斜
				if i<=11 and j<=11:
					if board[i][j]==board[i+1][j+1]==board[i+2][j+2]==board[i+3][j+3]==board[i+4][j+4] and board[i][j] != '+':
						whoWin(i,j)
						return False
				#正斜
				if i>=4 and j<=11:
					if board[i][j]==board[i-1][j+1]==board[i-2][j+2]==board[i-3][j+3]==board[i-4][j+4] and board[i][j] != '+':
						whoWin(i,j)
						return False
	return True

def whoWin(i,j):
	if board[i][j]=="•":
		print("黒が勝つ！")
	else:
		print("白が勝つ！")
	display(Image('./1.jpg'))
	time.sleep(2)
	for i in range(10):
		print("\a")

board=[]
initBoard()
printBoard()
startGame()
