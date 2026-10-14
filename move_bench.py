import bpy, os
root=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(root,'uchastok.blend'))
parts=[o for o in bpy.data.objects if o.name.startswith(('Скамейка','Ножка скамейки','Спинка скамейки'))]
assert len(parts)==4, [o.name for o in parts]
for o in parts: o.location.y-=6.55
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'uchastok.blend'))
bpy.context.scene.render.filepath=os.path.join(root,'uchastok_preview.png')
bpy.ops.render.render(write_still=True)
print('Bench moved beside path; saved scene and preview.')
