import bpy, math, random, os
from mathutils import Vector
random.seed(18)
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(n,c):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True
 m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*c,1)
 m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.78
 return m
grass=mat('Трава • шалфей',(0.24,.39,.17)); soil=mat('Земля',(.24,.16,.10)); cream=mat('Тёплая штукатурка',(.82,.64,.39)); roofmat=mat('Черепица • терракота',(.38,.105,.065)); wood=mat('Медовое дерево',(.40,.23,.105)); dark=mat('Тёмные балки',(.16,.09,.055)); white=mat('Слоновая кость',(.91,.85,.65)); glass=mat('Голубые окна',(.20,.49,.58)); stone=mat('Песчаник',(.58,.55,.43)); green=mat('Хвоя',(.055,.24,.13)); green2=mat('Светлая хвоя',(.10,.34,.18)); metal=mat('Графит',(.12,.17,.18)); barnmat=mat('Сарай • шалфей',(.31,.43,.32)); flower=mat('Цветы золотые',(.95,.58,.08))
def cube(n,p,s,m,bevel=.04):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p); o=bpy.context.object; o.name=n; o.dimensions=s; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if bevel:
  mod=o.modifiers.new('Мягкие края','BEVEL'); mod.width=bevel; mod.segments=2; o.modifiers.new('Нормали','WEIGHTED_NORMAL')
 return o
def cyl(n,p,r,d,m,verts=12):
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=d,location=p); o=bpy.context.object; o.name=n; o.data.materials.append(m); return o
def beam(n,a,b,w,m):
 a,b=Vector(a),Vector(b); o=cube(n,(a+b)/2,(w,w,(b-a).length),m,.015); o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o
def roof(n,x,y,w,d,z,h,m):
 verts=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x,y-d/2,z+h),(x-w/2,y+d/2,z),(x+w/2,y+d/2,z),(x,y+d/2,z+h)]
 mesh=bpy.data.meshes.new(n); mesh.from_pydata(verts,[],[(0,2,1),(3,4,5),(0,3,5,2),(2,5,4,1),(0,1,4,3)]); mesh.update(); o=bpy.data.objects.new(n,mesh); bpy.context.collection.objects.link(o); o.data.materials.append(m)
def window(x,y,z,w=1):
 cube('Рама окна',(x,y,z),(w+.18,.14,1.25),white)
 cube('Стекло',(x,y-.085,z),(w,.035,1.05),glass,.01)
 cube('Переплёт',(x,y-.115,z),(.06,.04,1.08),white,.01); cube('Переплёт',(x,y-.12,z),(w,.04,.06),white,.01)
 cube('Подоконник',(x,y-.16,z-.65),(w+.35,.38,.12),white)
cube('Основание участка',(0,0,-.38),(20,18,.75),soil,.25)
cube('Газон',(0,0,.015),(19.9,17.9,.13),grass,.18)
cube('Фон',(0,0,-.88),(200,200,.2),mat('Фон • песочный',(.57,.64,.57)),0)
# Дом
x,y=-3,3
cube('Фундамент дома',(x,y,.27),(5.6,4.8,.45),stone)
cube('Дом',(x,y,1.95),(5.3,4.5,3.3),cream)
roof('Фронтоны',x,y,5.3,4.5,3.6,1.6,cream)
roof('Крыша дома',x,y,6,5.25,3.6,1.85,roofmat)
for side in [-1,1]:
 for k in range(1,9):
  xx=x+side*k*.33; zz=5.45-abs(xx-x)*1.85/3
  beam('Ряд черепицы',(xx,y-2.65,zz+.025),(xx,y+2.65,zz+.025),.055,roofmat)
cube('Дверь дома',(-3,.70,1.37),(1.05,.16,2.15),dark)
cube('Панель двери',(-3,.59,1.44),(.80,.06,1.77),wood)
cyl('Ручка',(-2.67,.53,1.35),.055,.08,metal).rotation_euler[0]=math.pi/2
window(-4.65,.69,2.05,1); window(-1.38,.69,2.05,1)
cube('Крыльцо',(-3,.10,.26),(2.1,1.25,.44),wood)
for j in range(2): cube('Ступень',(-3,-.65-j*.33,.17-j*.065),(1.7,.4,.27-j*.13),stone)
for xx in [-4,-2]: beam('Стойка крыльца',(xx,-.35,.5),(xx,-.35,2.9),.12,dark)
o=cube('Навес',(-3,.12,2.96),(2.5,1.75,.16),roofmat); o.rotation_euler[0]=.10
cube('Дымоход',(-4.35,3.8,4.95),(.62,.7,1.75),stone); cube('Оголовок',(-4.35,3.8,5.85),(.8,.88,.16),dark)
# Сарай
cube('Фундамент сарая',(5,4,.20),(3.7,3.7,.3),stone)
cube('Сарай',(5,4,1.45),(3.4,3.4,2.5),barnmat)
roof('Крыша сарая',5,4,4,4,2.7,1.1,dark)
for xx in [3.45+i*.25 for i in range(13)]: cube('Доски фасада сарая',(xx,2.28,1.45),(.035,.04,2.45),wood,.005)
cube('Дверь сарая',(5,2.20,1.26),(1.5,.16,2.15),wood)
for xx in [4.3,5.7]: beam('Косяк',(xx,2.08,.2),(xx,2.08,2.37),.1,white)
beam('Диагональ двери',(4.35,2.06,.27),(5.65,2.06,2.22),.10,white)
cube('Верх двери сарая',(5,2.08,2.36),(1.6,.12,.12),white)
# Гараж-пристройка: правая стена соединена с домом.
cube('Фундамент гаража',(-7.3,2.9,.22),(3.55,4.7,.32),stone)
cube('Гараж-пристройка',(-7.3,2.9,1.45),(3.4,4.5,2.7),cream)
mesh=bpy.data.meshes.new('Односкатная крыша гаража')
mesh.from_pydata([(-9.15,.35,2.88),(-5.5,.35,3.55),(-5.5,5.45,3.55),(-9.15,5.45,2.88)],[],[(0,1,2,3)])
mesh.update(); obj=bpy.data.objects.new('Крыша пристройки',mesh); bpy.context.collection.objects.link(obj); obj.data.materials.append(roofmat)
obj.modifiers.new('Толщина кровли','SOLIDIFY').thickness=.14
cube('Рама ворот гаража',(-7.3,.60,1.42),(3.13,.16,2.6),white)
cube('Ворота гаража',(-7.3,.49,1.37),(2.88,.12,2.38),metal)
for z in [.4+i*.28 for i in range(8)]: cube('Секции ворот гаража',(-7.3,.40,z),(2.8,.04,.035),white,.005)
cube('Ручка гаража',(-7.3,.36,1),(.6,.06,.07),dark)
# Мощёный проезд шириной 3.5 м от автомобильных ворот до гаража.
cube('Основание автомобильной дорожки',(-7.3,-4.17,.105),(3.6,9.55,.10),dark)
for row in range(21):
 for col in range(7):
  cube('Брусчатка проезда',(-8.8+col*.5,-8.7+row*.45,.17),(.47,.42,.08),stone,.025)
for xx in [-9.12,-5.48]: cube('Бордюр проезда',(xx,-4.17,.20),(.12,9.55,.20),white,.025)
# Тропинки из отдельных плит
def path(points,width=1.25):
 for a,b in zip(points,points[1:]):
  a,b=Vector((*a,.12)),Vector((*b,.12)); length=(b-a).length; count=max(1,int(length/.48))
  for i in range(count):
   p=a+(b-a)*((i+.5)/count); o=cube('Камень тропинки',p,(width,length/count-.065,.10),stone,.07); o.rotation_euler[2]=-math.atan2(b.x-a.x,b.y-a.y)
path([(-3,-1),(-3,-1.8),(5,-1.8),(5,2.1)])
path([(0,-8.9),(0,-1.8)],1.4)
# Ограда с проёмом для ворот
def fence(a,b):
 a,b=Vector((*a,0)),Vector((*b,0)); count=round((b-a).length/.48)
 for i in range(count+1):
  p=a+(b-a)*i/count; cube('Штакетник',(*p.xy,.87),(.16,.16,1.6),wood,.025)
 for z in [.48,1.15]: beam('Перекладина',(a.x,a.y,z),(b.x,b.y,z),.10,dark)
fence((-9.5,-8.5),(-9.15,-8.5)); fence((-5.45,-8.5),(-1,-8.5)); fence((1,-8.5),(9.5,-8.5)); fence((-9.5,-8.5),(-9.5,8.5)); fence((9.5,-8.5),(9.5,8.5)); fence((-9.5,8.5),(9.5,8.5))
for xx in [-9.15,-5.45]:
 cube('Столб автомобильных ворот',(xx,-8.5,1.05),(.26,.26,2.05),dark)
 cube('Колпак автомобильных ворот',(xx,-8.5,2.12),(.36,.36,.12),white)
# Створки открыты вдоль проезда, оставляя свободный въезд.
for xx,dx in [(-9.15,.04),(-5.45,-.04)]:
 for z in [.45,1.45]: beam('Рама автомобильных ворот',(xx,-8.5,z),(xx+dx,-6.7,z),.10,metal)
 for i in range(10):
  t=i/9; beam('Планки автомобильных ворот',(xx+dx*t,-8.5+1.8*t,.38),(xx+dx*t,-8.5+1.8*t,1.55),.09,wood)
for xx in [-1,1]:
 cube('Столб ворот',(xx,-8.5,1.03),(.3,.3,2),dark); cube('Колпак',(xx,-8.5,2.08),(.42,.42,.12),white)
# Открытые створки оставляют проход
for side in [-1,1]:
 a=(side,-8.5,.4); b=(side*1.65,-7.35,.4)
 for z in [.45,1.25]: beam('Открытая створка',(a[0],a[1],z),(b[0],b[1],z),.11,wood)
 for i in range(6):
  t=i/5; px=a[0]+(b[0]-a[0])*t; py=a[1]+(b[1]-a[1])*t; beam('Планка ворот',(px,py,.35),(px,py,1.5),.09,wood)
# Ель
def fir(x,y,scale=1):
 cyl('Ствол ели',(x,y,1*scale),.20*scale,2*scale,dark)
 for z,r,h,m in [(1.9,1.65,2.5,green),(2.9,1.30,2.3,green2),(3.85,.93,2,green),(4.65,.58,1.55,green2)]:
  bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=r*scale,radius2=0,depth=h*scale,location=(x,y,z*scale)); bpy.context.object.name='Ярус ели'; bpy.context.object.data.materials.append(m)
fir(6.9,-4.2); fir(7.5,6.7,.65)
# Садовые детали
for xx in [-4.7,-.45]:
 cube('Цветник',(xx,-.1,.20),(1.1,.85,.26),dark)
 for i in range(9):
  px=xx+random.uniform(-.43,.43); py=random.uniform(-.4,.2); cyl('Стебель',(px,py,.46),.025,.35,green,6)
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.12,location=(px,py,.66)); bpy.context.object.data.materials.append(flower)
for i in range(65):
 px=random.uniform(-8.8,8.8); py=random.uniform(-7.8,7.8)
 if (-9.3<px<-5.4) or (-6<px<0 and .1<py<6) or (3<px<7 and 1.7<py<6) or abs(py+1.8)<.8 or abs(px)<.9 or (px-6.9)**2+(py+4.2)**2<3: continue
 for j in range(3):
  beam('Травинка',(px,py,.1),(px+random.uniform(-.13,.13),py+random.uniform(-.13,.13),random.uniform(.25,.42)),.025,green2)
for z in [.4,.7,1.0]: cyl('Бочка у сарая',(7.05,3,z),.37,.28,wood,16)
for z in [.3,.65,1.08]: cyl('Обруч бочки',(7.05,3,z),.385,.045,metal,16)
cube('Скамейка',(1.6,-.65,.65),(2,.65,.15),wood)
for xx in [.85,2.35]: cube('Ножка скамейки',(xx,-.65,.35),(.13,.5,.6),dark)
cube('Спинка скамейки',(1.6,-.35,1.05),(2,.12,.65),wood)
# Свет и обзор
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.world.color=(.5,.5,.5)
bpy.ops.object.light_add(type='AREA',location=(-7,-10,18)); bpy.context.object.data.energy=2400; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=12
bpy.ops.object.light_add(type='SUN',location=(0,0,12)); bpy.context.object.rotation_euler=(.4,-.5,-.5); bpy.context.object.data.energy=2
bpy.ops.object.camera_add(location=(25,-32,27)); cam=bpy.context.object; cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=29; scene.camera=cam
scene.render.resolution_x=1500; scene.render.resolution_y=1300; scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA'
   area.spaces.active.shading.type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT')
scene.render.filepath=os.path.join(ROOT,'uchastok_preview.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'uchastok.blend'))
bpy.ops.render.render(write_still=True)
print('DONE: uchastok.blend and uchastok_preview.png')
