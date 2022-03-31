from pygame import init,font,display,image,transform,time,fastevent,FINGERDOWN,FINGERMOTION,FINGERUP,gfxdraw,mixer
from pymunk import Body,Circle,Poly,Space,pygame_util,constraints,PinJoint
from math import degrees,sin,cos,atan2
from random import randint
init()
fastevent.init()
screen=display.set_mode((1080,2290))
options=pygame_util.DrawOptions(screen)
space=Space()
space.gravity=0,600
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
font=font.Font(None,30)
clock=time.Clock()
lightx,lighty=540,1090
def cre_text(name,x,y):
	t=font.render(str(name),1,red)
	screen.blit(t,(x,y))
def take_image_ca(name):
	return image.load(name).convert_alpha()
def take_image_c(name):
	return image.load(name).convert()
###img
#background
bg=take_image_c("bg.png")
#base_bat
base_bat_img=take_image_ca("basebat_blue.png")
left_base_bat_img=transform.flip(transform.rotate(base_bat_img,90),True,False)
right_base_bat_img=transform.rotate(base_bat_img,90)
#push_block
push_block_img=take_image_ca("ice_block.png")
#base_ball
base_ball_img=take_image_ca("base_ball.png")
#disco_ball
disco_ball_img=take_image_ca("disco_ball.png")
#ice_plate_rectangle
ice_plate_rectangle=take_image_ca("ice_plate_rectangle.png")
#laser_blade
laser_blade_img=take_image_ca("laser_blade.png")
###sound
def take_sound(name):
	return mixer.Sound(name)
base_bat_sound=take_sound("basebat_sound.mp3")
spring_sound=take_sound("spring.mp3")
hard_c_t=1
ice_c_t=2
sort_c_t=3
hard_c_t_sound=take_sound("hard_c_t.mp3")
ice_c_t_sound=take_sound("ice_c_t.mp3")
sort_c_t_sound=take_sound("sort_c_t.mp3")
class Base_bat:
	def __init__(self,x,y,a,vect):
		self.body=Body(1,1,Body.KINEMATIC)
		self.body.position=x,y
		self.body.angle=a
		shape=Poly(self.body,vect)
		shape.elasticity=0.5
		shape.friction=0.5
		shape.collision_type=hard_c_t
		space.add(self.body,shape)
	def check_movenment_left(self,down,motion,x_check,angle_vel_u,angle_vel_d):
		if x_check:
			self.body.angular_velocity=angle_vel_u if down or motion else angle_vel_d
			if down:
				base_bat_sound.play()
	def animation_left(self,img,limit_u,limit_d):
		if self.body.angle<=limit_u:
			self.body.angular_velocity=0
		if self.body.angle>=limit_d:
			self.body.angular_velocity=0
		if self.body.angle<=limit_u-0.2:
			self.body.angle=limit_u
		if self.body.angle>=limit_d+0.2:
			self.body.angle=limit_d
		n=transform.rotate(img,-degrees(self.body.angle))
		screen.blit(n,(self.body.position[0]-n.get_width()//2,self.body.position[1]-n.get_height()//2))
	
	def check_movenment_right(self,down,motion,x_check,angle_vel_u,angle_vel_d):
		if x_check:
			self.body.angular_velocity=angle_vel_u if down or motion else angle_vel_d
			if down:
				base_bat_sound.play()
	def animation_right(self,img,limit_u,limit_d):
		if self.body.angle>=limit_u:
			self.body.angular_velocity=0
		if self.body.angle<=limit_d:
			self.body.angular_velocity=0
		if self.body.angle>=limit_u+0.2:
			self.body.angle=limit_u
		if self.body.angle<=limit_d-0.2:
			self.body.angle=limit_d
		n=transform.rotate(img,-degrees(self.body.angle))
		screen.blit(n,(self.body.position[0]-n.get_width()//2,self.body.position[1]-n.get_height()//2))	
class Push_block:
	def __init__(self,x,y,x2,y2):
		self.body=Body(100,4450)
		self.body.position=x,y
		body2=Body(1,1,Body.KINEMATIC)
		body2.position=x2,y2
		shape=Poly.create_box(self.body,(50,50))
		shape.elasticity=0.1
		shape.friction=0.5
		shape.collision_type=ice_c_t
		push=constraints.DampedSpring(self.body,body2,(0,0),(0,0),130,2500,50)
		space.add(self.body,shape,push)
	def check_movenment(self,xcheck,down,up):
		if xcheck and self.body.position[1]<1975:
			self.body.mass=500
			self.body.velocity=0,100
		if not down:
			self.body.mass=1
		if up and self.body.position[1]>1900:
			spring_sound.play()
	def animation(self):
		self.body.angle=0
		n=transform.rotate(push_block_img,-degrees(self.body.angle))
		gfxdraw.rectangle(screen,(self.body.position[0]-10,self.body.position[1],20,2000-self.body.position[1]),(0,randint(0,255),randint(0,255)))
		screen.blit(n,(self.body.position[0]-n.get_width()//2,self.body.position[1]-n.get_height()//2))
			
class Base_ball:
	def __init__(self,x,y):
		self.body=Body(1,200)
		self.body.position=x,y
		self.shape=Circle(self.body,25)
		self.shape.elasticity=0.75
		self.shape.friction=0.5
		space.add(self.body,self.shape)
	def animation(self):
		n=transform.rotate(base_ball_img,-degrees(self.body.angle))
		screen.blit(n,(self.body.position[0]-n.get_width()//2,self.body.position[1]-n.get_height()//2))
		if self.body.velocity.length>1000:
			self.body.velocity*=0.99
		pangle=atan2(self.body.velocity[0]-0,self.body.velocity[1]-0)-3.14159
		if self.body.velocity.length>400:
			gfxdraw.rectangle(screen,(self.body.position[0]+randint(50,100)*sin(pangle),self.body.position[1]+randint(50,100)*cos(pangle),10,10),(0,randint(0,255),randint(0,255)))
			gfxdraw.box(screen,(self.body.position[0]+randint(25,100)*sin(pangle),self.body.position[1]+randint(25,100)*cos(pangle),10,10),(0,randint(0,255),randint(0,255)))
class Disco_ball:
	def __init__(self,x,y):
		self.body=Body(1,1,Body.KINEMATIC)
		self.body.position=x,y
		self.body.angular_velocity=2
		shape=Circle(self.body,100)
		shape.elasticity=1
		shape.friction=0.5
		shape.collision_type=ice_c_t
		space.add(self.body,shape)
	def animation(self):
		n=transform.rotate(disco_ball_img,-degrees(self.body.angle))
		screen.blit(n,(self.body.position[0]-n.get_width()//2,self.body.position[1]-n.get_height()//2))
class Ice_rectangle:
	def __init__(self,x,y):
		self.body=Body(1,445)
		self.body.position=x,y
		body2=Body(1,1,Body.KINEMATIC)
		body2.position=540,1200
		shape=Poly.create_box(self.body,(100,50))
		shape.elasticity=0.25
		shape.friction=0.5
		shape.collision_type=ice_c_t
		pin=PinJoint(self.body,body2)
		space.add(self.body,shape,pin)
	def animation(self):
		self.body.angular_velocity=5
		n=transform.rotate(ice_plate_rectangle,-degrees(self.body.angle))
		gfxdraw.polygon(screen,[self.body.position,(500,1200),(540,1200),(580,1200)],(0,randint(0,255),randint(0,255)))
		screen.blit(n,(self.body.position[0]-n.get_width()//2,self.body.position[1]-n.get_height()//2))
class Laser_blade:
	def __init__(self,x,y,a_v):
		self.body=Body(1,1,Body.KINEMATIC)
		self.body.position=x,y
		self.body.angular_velocity=a_v
		shape=Poly.create_box(self.body,(200,30))
		shape.elasticity=0.75
		shape.friction=0.5
		shape.collision_type=hard_c_t
		space.add(self.body,shape)
	def animation(self):
		n=transform.rotate(laser_blade_img,-degrees(self.body.angle))
		screen.blit(n,(self.body.position[0]-n.get_width()//2,self.body.position[1]-n.get_height()//2))	
def Poly_object(x,y,vect,e,c_t):
	body=Body(1,1,Body.KINEMATIC)
	body.position=x,y
	shape=Poly(body,vect)
	shape.elasticity=e
	shape.friction=0.5
	shape.collision_type=c_t
	space.add(body,shape)	
def Rectangle_object(x,y,a,size):
	body=Body(1,1,Body.KINEMATIC)
	body.position=x,y
	body.angle=a
	shape=Poly.create_box(body,size)
	shape.elasticity=0.75
	shape.friction=0.5
	shape.collision_type=hard_c_t
	space.add(body,shape)
def Circle_object(x,y,radius,e,c_t):
	body=Body(1,1,Body.KINEMATIC)
	body.position=x,y
	shape=Circle(body,radius)
	shape.elasticity=e
	shape.friction=0.5
	shape.collision_type=c_t
	space.add(body,shape)

#base_bat
left_base_bat=Base_bat(410,1900,46,((100,25),(100,-25),(-105,10),(-105,-10),(110,0)))
right_base_bat=Base_bat(1080-410,1900,-46,((105,10),(105,-10),(-100,25),(-100,-25),(-110,0)))
#push_block
push_block_left=Push_block(150,1885,150,2000)
push_block_right=Push_block(1080-150,1885,1080-150,2000)
#base_ball
base_ball=Base_ball(150,1800)
###frame
##down
#left
Rectangle_object(110,1735,0,(25,550))
Rectangle_object(190,1935,0,(25,140))
Rectangle_object(190,1555,0,(25,190))
Rectangle_object(150,1740+275,1.57079,(25,80))
Rectangle_object(300,1780,-0.71558,(25,340))
Rectangle_object(290,1995,-0.71558,(25,310))
#right
Rectangle_object(1080-110,1735,0,(25,550))
Rectangle_object(1080-190,1935,0,(25,140))
Rectangle_object(1080-190,1555,0,(25,190))
Rectangle_object(1080-150,1740+275,1.57079,(25,80))
Rectangle_object(1080-300,1780,0.71558,(25,340))
Rectangle_object(1080-290,1995,0.71558,(25,310))
#main_frame
Rectangle_object(5,830,0,(35,990))
Rectangle_object(1080-5,830,0,(35,990))
Rectangle_object(50,1400,-0.66322,(35,170))
Rectangle_object(1080-50,1400,0.66322,(35,170))
Rectangle_object(135,230,0.89011,(35,330))
Rectangle_object(1080-135,230,-0.89011,(35,330))
Rectangle_object(540,120,1.57079,(35,540))
###object
#crown
Rectangle_object(475,310,-0.29670,(20,110))
Rectangle_object(1080-475,310,0.29670,(20,110))
xd,yd=540,0
#ramp
Poly_object(320,1565,((60,135),(-45,55),(-45,-135)),2,sort_c_t)
Poly_object(1080-320,1565,((-60,135),(45,55),(45,-135)),2,sort_c_t)
#disco_ball
disco_ball=Disco_ball(540,1200)
#ice_rectangle
ice_rectangle=Ice_rectangle(540,1450)
left_laser_blade=Laser_blade(250,800,10)
right_laser_blade=Laser_blade(1080-250,800,-10)
#triple_circle
Circle_object(448,673,50,1.75,sort_c_t)
Circle_object(587,559,50,1.75,sort_c_t)
Circle_object(604,761,50,1.75,sort_c_t)
#ice_plate_triangle
Poly_object(223,332,((105,75),(-105,75),(105,-75)),0.75,ice_c_t)
Poly_object(1080-223,332,((105,75),(-105,75),(-105,-75)),0.75,ice_c_t)
#ice_plate_circle
Circle_object(299,1197,30,2,ice_c_t)
Circle_object(1080-299,1197,30,2,ice_c_t)
res=0
def Hard_c_type(space,arbiter,data):
	if abs(base_ball.body.velocity.x)>200 or abs(base_ball.body.velocity.y)>250:
		hard_c_t_sound.play()
	return True
def Ice_c_type(space,arbiter,data):
	if abs(base_ball.body.velocity.x)>250 or abs(base_ball.body.velocity.y)>250:
		ice_c_t_sound.play()
	return True
def Sort_c_type(space,arbiter,data):
	if abs(base_ball.body.velocity.x)>250 or abs(base_ball.body.velocity.y)>250:
		sort_c_t_sound.play()
	return True
while 1:
	#collision_handler
	space.add_collision_handler(0,1).begin=Hard_c_type
	space.add_collision_handler(0,2).begin=Ice_c_type
	space.add_collision_handler(0,3).begin=Sort_c_type
	screen.blit(bg,(0,0))
	FPS=clock.get_fps()
	clock.tick()
	left_base_bat.animation_left(left_base_bat_img,-0.80285,0.80285)
	right_base_bat.animation_right(right_base_bat_img,0.80285,-0.80285)
	for ev in fastevent.get():
		if ev.type==FINGERDOWN :
			xd=ev.x*1080
			yd=ev.y*2290
			if xd<150 and yd<150:
				game_on=0
		left_base_bat.check_movenment_left(ev.type==FINGERDOWN , ev.type==FINGERMOTION,xd<540,-15,15)
		right_base_bat.check_movenment_right(ev.type==FINGERDOWN , ev.type==FINGERMOTION,xd>540,15,-15)
		push_block_left.check_movenment(xd<540,ev.type==FINGERDOWN or ev.type==FINGERMOTION,ev.type==FINGERUP)
		push_block_right.check_movenment(xd>540,ev.type==FINGERDOWN or ev.type==FINGERMOTION,ev.type==FINGERUP)
	push_block_left.animation()
	push_block_right.animation()
	base_ball.animation()
	if base_ball.body.position[1]>2500:
		res=1
	if res==1:
		space.remove(base_ball.body,base_ball.shape)
		base_ball=Base_ball(150,1800)
		res=0
	ice_rectangle.animation()
	disco_ball.animation()
	left_laser_blade.animation()
	right_laser_blade.animation()
	cre_text(FPS,0,0)
	#space.debug_draw(options)
	space.step(1/60)
	display.update()
