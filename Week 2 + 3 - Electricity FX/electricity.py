import bpy

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()


#create 3 plain axes
bpy.ops.object.empty_add(type = 'PLAIN_AXES', align = 'WORLD', location = (4.5, 0, 0))
bpy.ops.object.empty_add(type = 'PLAIN_AXES', align = 'WORLD', location = (4.5, -3, 0))
bpy.ops.object.empty_add(type = 'PLAIN_AXES', align = 'WORLD', location = (4.5, 3, 0))

bpy.data.objects["Empty"].name = "Empty1"
bpy.data.objects["Empty.001"].name = "Empty2"
bpy.data.objects["Empty.002"].name = "Empty3"

e1 = bpy.data.objects["Empty1"]
e2 = bpy.data.objects["Empty2"]
e3 = bpy.data.objects["Empty3"]


#create the object for electric pulse
bpy.ops.mesh.primitive_plane_add(size = 2, enter_editmode = False, align = 'WORLD', location = (0, 0, 0))
bpy.ops.object.editmode_toggle()
bpy.ops.transform.resize(value = (1, 0, 1))
bpy.ops.mesh.remove_doubles()
bpy.ops.transform.resize(value = (3,3,3))
bpy.ops.object.editmode_toggle()
bpy.ops.object.modifier_add(type = 'DISPLACE')

mod_disp = bpy.context.object.modifiers["Displace"]
mod_disp.texture_coords = 'OBJECT'
mod_disp.texture_coords_object = bpy.data.objects["Empty1"]
mod_disp.strength = 2.6

bpy.ops.object.editmode_toggle()
for i in range(6):
    bpy.ops.mesh.subdivide()
bpy.ops.object.editmode_toggle()

bpy.data.objects["Plane"].name = "elec1"
elec1 = bpy.data.objects["elec1"]

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region = {"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate = {"value":(0, 0.033477, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

tex = bpy.data.textures.new(name = "tex", type = 'CLOUDS')
tex.noise_scale = 2
tex.noise_depth = 1
mod_disp.texture = tex

bpy.ops.object.editmode_toggle()

#adding weight paint to the mesh
obj = bpy.context.object
obv = obj.data.vertices
if not obj.vertex_groups:
    obj.vertex_groups.new(name = 'Sv_VGroup')
ovgs = obj.vertex_groups[0]

for i in obv:
    ovgs.add([i.index], (2.5-i.co.length)*0.6, "REPLACE")
obj.data.update()

bpy.context.object.modifiers["Displace"].vertex_group = "Sv_VGroup"

bpy.ops.object.modifier_add(type = 'DISPLACE')
mod_disp1 = bpy.context.object.modifiers["Displace.001"]
mod_disp1.vertex_group = "Sv_VGroup"
mod_disp1.texture_coords = 'OBJECT'

tex1 = bpy.data.textures.new(name = "tex1", type = 'CLOUDS')
tex1.noise_scale = 0.5
tex1.noise_depth = 1
mod_disp1.texture = tex1
mod_disp1.texture_coords_object = bpy.data.objects["Empty1"]

bpy.ops.object.modifier_add(type = 'SUBSURF')
bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'
bpy.context.object.modifiers["Subdivision"].render_levels = 3

bpy.ops.object.modifier_add(type = 'DISPLACE')
mod_disp2 = bpy.context.object.modifiers["Displace.002"]

tex2 = bpy.data.textures.new(name = 'tex2', type = 'CLOUDS')
tex2.noise_scale = 0.3
tex2.noise_depth = 2
mod_disp2.texture = tex2

mod_disp2.texture_coords = 'OBJECT'
mod_disp2.texture_coords_object = bpy.data.objects["Empty1"]
mod_disp2.strength = 0.2


#create material for electricity
mat = bpy.data.materials.new("shadeless")
mat.use_nodes = True
mat_out = mat.node_tree.nodes.get('Material Output')
mat.node_tree.nodes.remove(mat.node_tree.nodes['Principled BSDF'])

light_path = mat.node_tree.nodes.new('ShaderNodeLightPath')
emission = mat.node_tree.nodes.new('ShaderNodeEmission')
mix_shader = mat.node_tree.nodes.new('ShaderNodeMixShader')

emission.inputs[0].default_value = (1, 0.0286626, 0.0328047, 1)
emission.inputs[1].default_value = 30

light_path.location = (-300, 400)
emission.location = (-300, 0)
mix_shader.location = (0, 250)

mat.node_tree.links.new(light_path.outputs[0], mix_shader.inputs[0])
mat.node_tree.links.new(emission.outputs[0], mix_shader.inputs[2])
mat.node_tree.links.new(mix_shader.outputs[0], mat_out.inputs[0])

if elec1.data.materials:
    elec1.data.materials[0] = mat
else:
    elec1.data.materials.append(mat)


#create more elec pulses and assign empty to them
bpy.ops.object.duplicate_move_linked()
bpy.ops.transform.rotate(value=-0.909976, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

bpy.ops.object.duplicate_move_linked()
bpy.ops.transform.rotate(value=1.87478, orient_axis='X', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 0.613765, -0.789489), (0, 0.789489, 0.613765)), orient_matrix_type='LOCAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

bpy.data.objects["elec1.001"].name = "elec2"
bpy.data.objects["elec1.002"].name = "elec3"

elec2 = bpy.data.objects["elec2"]
elec3 = bpy.data.objects["elec3"]

bpy.data.objects["elec2"].modifiers["Displace"].texture_coords_object = bpy.data.objects["Empty2"]
bpy.data.objects["elec2"].modifiers["Displace.001"].texture_coords_object = bpy.data.objects["Empty2"]
bpy.data.objects["elec2"].modifiers["Displace.002"].texture_coords_object = bpy.data.objects["Empty2"]

bpy.data.objects["elec3"].modifiers["Displace"].texture_coords_object = bpy.data.objects["Empty3"]
bpy.data.objects["elec3"].modifiers["Displace.001"].texture_coords_object = bpy.data.objects["Empty3"]
bpy.data.objects["elec3"].modifiers["Displace.002"].texture_coords_object = bpy.data.objects["Empty3"]


#create cylinders (source and sink)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.33, depth=0.66, enter_editmode=False, align='WORLD', location=(-3.125, 0, 0), rotation=(0, 1.57, 0))
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.33, depth=0.66, enter_editmode=False, align='WORLD', location=(3.125, 0, 0), rotation=(0, 1.57, 0))

bpy.data.objects["Cylinder"].name = 'source'
bpy.data.objects["Cylinder.001"].name = 'sink'
c1 = bpy.data.objects['source']
c2 = bpy.data.objects['sink']

bpy.context.view_layer.objects.active = bpy.data.objects['source']
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
for i in range(64):
    c1.data.vertices[2*i+1].select = True
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.inset(thickness=0.0330761, depth=0)
bpy.ops.transform.translate(value=(0.0297498, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True)
bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.modifier_add(type = 'SUBSURF')
bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'
bpy.context.object.modifiers["Subdivision"].levels = 3
bpy.context.object.modifiers["Subdivision"].rednder_levels = 5

bpy.context.view_layer.objects.active = bpy.data.objects['sink']
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
for i in range(64):
    c2.data.vertices[2*i].select = True
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.inset(thickness=0.0330761, depth=0)
bpy.ops.transform.translate(value=(-0.0297498, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True)
bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.modifier_add(type = 'SUBSURF')
bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'
bpy.context.object.modifiers["Subdivision"].levels = 3
bpy.context.object.modifiers["Subdivision"].rednder_levels = 5

bpy.ops.mesh.primitive_plane_add(size=45, enter_editmode=False, align='WORLD', location=(6.6, 0, -1.2))
surface = bpy.data.objects['Plane']

#the below syntax needs to have the precise directory entered in the format {directory="[filepath]\\Material\\"}
bpy.ops.wm.append(filename="Procedural Abstract Sci-Fi Panels", directory="{path}\\assets\\materials\\procedural_abstract_sci-fi_panels_blend_40300cca-3d3d-4862-a35b-6cf061bb10a0.blend\\Material\\")
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
panels = bpy.data.materials['Procedural Abstract Sci-Fi Panels']

if surface.data.materials:
    surface.data.materials[0] = panels
else:
    surface.data.materials.append(panels)    
    
bpy.ops.object.light_add(type='POINT', radius=0.1, align='WORLD', location=(0, 0, 0))
bpy.ops.object.light_add(type='SUN', radius=0.1, align='WORLD', location=(0, 0, 2))
bpy.context.object.data.energy = 1.5


#add camera
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 11, 0), rotation=(1.5708, 0, 3.14159))