bl_info = {
    "name": "Create Fast Texture",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class FastTex():
    def CreateTex(texture_name, filepath, image_height, image_width):
        obj = bpy.context.active_object
        name = obj.name
        if name in obj.data.materials:
            return
        
        mat = bpy.data.materials.new(name)
        obj.data.materials.append(mat)
        obj.active_material_index = len(obj.data.materials) - 1
        
        image = bpy.data.images.new(texture_name, image_height, image_width, alpha=True)
        
        image.filepath_raw = filepath + "//" + texture_name + ".png"
        image.file_format = 'PNG'
        image.save()
        
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled_bsdf = nodes.get("Principled BSDF")
        links = mat.node_tree.links
        
        texture = bpy.data.textures.new(name="Texture", type='IMAGE')
        texture.image = image
        texture_node = nodes.new(type="ShaderNodeTexImage")
        texture_node.image = image
        texture_node.texture_mapping.scale[0] = 2.0
        texture_node.texture_mapping.scale[1] = 2.0
        links.new(texture_node.outputs["Color"], principled_bsdf.inputs["Base Color"])

class Button_CreateTex(bpy.types.Operator):
    bl_idname = "object.create_fast_tex"
    bl_label = "Create Fast Tex"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH')
    
    def execute(self, context):
        obj = context.active_object
        FastTex.CreateTex(obj.texture_name, obj.filepath, obj.image_height, obj.image_width)
        return {'FINISHED'}
    
class Panel_CreateTex(bpy.types.Panel):
    bl_label = "Create Fast Tex"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Create Fast Tex"
    
    def draw(self, context):
        layout = self.layout
        obj = bpy.context.active_object
        name = obj.name
        
        row = layout.row()
        row.prop(obj, 'texture_name')
        
        row = layout.row()
        row.prop(obj, 'filepath')
        
        row = layout.row()
        row.prop(obj, 'image_height')
        
        row = layout.row()
        row.prop(obj, 'image_width')

        row = layout.row()
        row.operator(Button_CreateTex.bl_idname)
        if name in obj.data.materials:
          row.active = False
        
def register():
    bpy.utils.register_class(Button_CreateTex)
    bpy.utils.register_class(Panel_CreateTex)
    bpy.types.Object.texture_name = bpy.props.StringProperty(name = "TexName")
    bpy.types.Object.filepath = bpy.props.StringProperty(name = "Filepath", subtype='DIR_PATH')
    bpy.types.Object.image_height = bpy.props.IntProperty(name = "ImageHeight", default = 1024, min = 0, max = 4096)
    bpy.types.Object.image_width = bpy.props.IntProperty(name = "ImageWidth", default = 1024, min = 0, max = 4096)
    
def unregister():
    bpy.utils.unregister_class(Button_CreateTex)
    bpy.utils.unregister_class(Panel_CreateTex)
    del bpy.types.Object.texture_name
    del bpy.types.Object.filepath
    del bpy.types.Object.image_height
    del bpy.types.Object.image_width
    
if __name__ == "__main__":
    register()