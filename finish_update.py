import bpy, os
root=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(root,'uchastok.blend'))
moved=0
for o in bpy.data.objects:
 if -6.2<o.location.x<-5 and -.5<o.location.y<.3 and (o.name.startswith(('Цветник','Стебель','Icosphere'))):
  o.location.x+=.9; moved+=1
print('Moved planter parts:',moved)
assert moved==19, moved
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'uchastok.blend'))
bpy.context.scene.render.filepath=os.path.join(root,'uchastok_preview.png')
bpy.ops.render.render(write_still=True)
