import sys,random,argparse
import numpy as np
import math
import turtle
from PIL import Image
from datetime import datetime
from fractions import gcd
'''
#用海龟画圈圈
def drawCircleTurtle(x,y,r):
	#圈圈的起始
	turtle.up()
	turtle.setpos(x+r,y)
	turtle.down()
	#画圈圈
	for i in range(0,365,60):
		a=math.radians(i)
		turtle.setpos(x+r*math.cos(a),y+r*math.sin(a))
drawCircleTurtle(0,0,300)
turtle.mainloop()
'''
#画斯普里奥图的类
class Sprio:
	#构造
	def __init__(self,xc,yc,col,R,r,l):
		#创建海龟
		self.t=turtle.Turtle()
		#创建光标的形状
		self.t.shape('turtle')
		#设置递进位
		self.step=5
		#设置完成标志
		self.drawingComplete=False
		#设置参数
		self.setparams(xc,yc,col,R,r,l)
		#初始化画图
		self.restart()
	#下面设置函数
	def setparams(self,xc,yc,col,R,r,l):
		#斯普里奥图的参数
		self.xc=xc
		self.yc=yc
		self.R=int(R)
		self.r=int(r)
		self.l=l
		self.col=col
		#对r/R约分，使用GCD
		gcdval=math.gcd(self.r,self.R)
		self.nRot=self.r//gcdval
		self.k=r/float(R)
		#设置颜色
		self.t.color(*col)
		#储存当前的角度
		self.a=0
	def restart(self):
		#设置标志
		self.drawingComplete=False
		#展示海龟
		self.t.showturtle()
		#去第一个点
		self.t.up()
		R,k,l=self.R,self.k,self.l
		a=0.0
		x=R*((1-k)*math.cos(a)+l*k*math.cos((1-k)*a/k))
		y=R*((1-k)*math.sin(a)-l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc+x,self.yc+y)
		self.t.down()
	#整个画出来吧
	def draw(self):
		#画完剩下的点
		R,k,l=self.R,self.k,self.l
		for i in range(0,360*self.nRot+1,self.step):
			a=math.radians(i)
			x=R*((1-k)*math.cos(a)+l*k*math.cos((1-k)*a/k))
			y=R*((1-k)*math.sin(a)-l*k*math.sin((1-k)*a/k))
			self.t.setpos(self.xc+x,self.yc+y)
			#画完了，所以隐藏海龟标志吧
			self.t.hideturtle()
	#来一段一段的画
	def update(self):
		#跳过剩余的步骤如果干完了的话
		if self.drawingComplete:
			return
		#增加角度
		self.a+=self.step
		#来画一步
		R,k,l=self.R,self.k,self.l
		#设置角度
		a=math.radians(self.a)
		x=R*((1-k)*math.cos(a)+l*k*math.cos((1-k)*a/k))
		y=R*((1-k)*math.sin(a)-l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc+x,self.yc+y)
		#如果画完了，改变标志
		if self.a>=360*self.nRot:
			self.drawingComplete=True
			#画完了，隐藏
			self.t.hideturtle()
			
class SprioAnimator:
	def __init__(self,N):
		#设置个计时器
		self.deltaT=1000
		#设置窗口的大小
		self.width=turtle.window_width()
		self.height=turtle.window_height()
		#创造斯普里奥实例
		self.spiros=[]
		for i in range(N):
			#迭代出随机数
			rparams=self.genRandomParams()
			#设置斯普里奥参数
			print(rparams)
			spiro=Sprio(*rparams)
			self.spiros.append(spiro)
			#调用计时器
			turtle.ontimer(self.update,self.deltaT)
	#生成随机参数
	def genRandomParams(self):
		width,height=self.width,self.height
		#//是整除的意思，除完是整数 
		R=random.randint(50,min(width,height)//2)
		r=random.randint(R//10,9*R//10)
		l=random.uniform(0.1,0.9)
		xc=random.randint(-width//2,width//2)
		yc=random.randint(-height//2,height//2)
		col=(random.random(),random.random(),random.random())
		return (xc,yc,col,R,r,l)
	def restart(self):
		for spiro in self.spiros:
			spiro.clear()
			#生成随机参数
			rparams=self.genRandomParams()
			#设置斯普里奥参数
			spiro.setparams(*rparams)
			#重新开始画图
			spiro.restart()
	def update(self):
		#更新所有斯普里奥
		nComplete=0
		for spiro in self.spiros:
			#更新这里是调用spiro的update而不是SpiroAnimator的update
			spiro.update()
			#计算完成的斯普里奥
			if spiro.drawingComplete:
				nComplete+=1
			#重新开始如果所有的斯普里奥完成了
		if nComplete==len(self.spiros):
			self.restart()
		#调用计时器
		turtle.ontimer(self.update,self.deltaT)
	#显示或者隐藏光标，让海龟跑得更快    
	def toggleTurtles(self):
		for spiro in self.spiros:
			if spiro.t.isvisble():
				spiro.t.hideturtle()
			else:
				spiro.t.showturtle()
#将画图保存为png文件
def saveDrawing():
	#隐藏海龟光标
	turtle.hideturtle()
	#生成特殊的文件名
	dateStr=(datetime.now()).strftime("%d%b%Y-%H%M%S")
	fileName='spiro-'+dateStr
	print('saving drawing to %s.eps/png'%fileName)
	canvas=turtle.getcanvas()
	#将画图保存为一个postscipt文件
	canvas.postscript(file=fileName+'.eps')
	#用pillow将postscript转化为PNG
	img=Image.open(fileName+'.eps')
	img.save(fileName+'.png','.png')
	#展示海龟图标
	turtle.showturtle()
	
def main():
	#使用sys.argv
	print('generating spriograph...')
	#构造parser
	descStr="""This program draws Spriographs using the Turtle module.
	when run with no arguments,this program draws random Spirographs.
	
	R:外圆的半径
	r:内圆的半径
	l:线段PC与小圆半径之比
	"""
	parser=argparse.ArgumentParser(description=descStr)
	#添加期望的参数,nargs表示后面要跟的参数数目，reuired是否可以省略默认为Ture不可以省，为false时可以省
	parser.add_argument('--sparams',nargs=3,dest='sparams',required=False,help="The three arguments in sparams:R,r,l.")
	#解析吧
	args=parser.parse_args()
	#将画板宽度设置为屏幕的80%
	turtle.setup(width=0.8,height=0.8)

	#将光标的形状设置为海龟
	turtle.shape('turtle')
	#给斯普里奥图设置一个标题
	turtle.title("Spirographs!")
	#设置个保存键
	turtle.onkey(saveDrawing,"s")
	#开始监听
	turtle.listen()
	#隐藏主海龟图标
	turtle.hideturtle()
	#检查送往--sparams的参数
	if args.sparams:
		params=[float(x) for x in args.sparams]
		#用给定参数画斯普里奥图(self,xc,yc,col,R,r,l):
		col=(0,0,0)
		spiro=Sprio(0,0,col,*params)
		spiro.draw()
	else:
		#创造实例
		spiroAnim=SprioAnimator(4)
		#添加快捷键去显隐海龟图标
		turtle.onkey(spiroAnim.toggleTurtles,"t")
		#给个键表示重新开始
		turtle.onkey(spiroAnim.restart,"space")
	#开户海龟画图
	turtle.mainloop()
#调用主函数
if __name__=='__main__':
	main()
		
		
		
		
	
		
		