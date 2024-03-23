
import bpy

class TexturePaintingFunctions():
    def createTexture(texture_name, filepath, image_height, image_width):
        obj = bpy.context.active_object
        name = obj.name
        
        # check if object has material same as object name
        # if there is then continue to next object
        if name in obj.data.materials:
            return
        
        #add new material to object and set active
        mat = bpy.data.materials.new(name)
        obj.data.materials.append(mat)
        obj.active_material_index = len(obj.data.materials) - 1
        
        #create image
        image = bpy.data.images.new(texture_name, image_height, image_width, alpha=True)

        image.filepath_raw = filepath + "//" + texture_name +".png"
        image.file_format = 'PNG'
        image.save()
        
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled_bsdf = nodes.get("Principled BSDF")
#            if principled_bsdf is None:
#                principled_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
#            material_output = nodes.get("Material Output")
#            if material_output is None:
#                material_output = nodes.new(type="ShaderNodeOutputMaterial")
        links = mat.node_tree.links
#            links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])

        texture = bpy.data.textures.new(name="Texture", type='IMAGE')
        texture.image = image
        texture_node = nodes.new(type="ShaderNodeTexImage")
        texture_node.image = image
        texture_node.texture_mapping.scale[0] = 2.0
        texture_node.texture_mapping.scale[1] = 2.0
        links.new(texture_node.outputs["Color"], principled_bsdf.inputs["Base Color"])


class CreateTexButton(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.create_fast_tex"
    bl_label = "Create Fast Texture"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH')

    def execute(self, context):
        obj = context.active_object
        TexturePaintingFunctions.createTexture(obj.texture_name, obj.filepath, obj.image_height, obj.image_width)
        return {'FINISHED'}


class CreateFastTexture(bpy.types.Panel):
    """Creates a Sub-Panel in the Property Area of the 3D View"""
    bl_label = "Create Fast Texture"  
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Create Fast Texture"

    def draw(self, context):
        obj = context.object

        layout = self.layout
        scn = context.scene

        row = layout.row()
        row.label(text="Create texture for: {}".format(obj.name))

        row = layout.row()
        row.prop( context.active_object, 'texture_name' )
        
        row = layout.row()
        row.prop( context.active_object, 'filepath' )
        
        row = layout.row()
        row.prop( context.active_object, 'image_height' )
        
        row = layout.row()
        row.prop( context.active_object, 'image_width' )

        row = layout.row()
        row.operator(CreateTexButton.bl_idname)

def register():
    bpy.utils.register_class(CreateFastTexture)
    bpy.utils.register_class(CreateTexButton)
    bpy.types.Object.texture_name = bpy.props.StringProperty(name = "Tex Name", default = "texture_diffuse")
    bpy.types.Object.filepath = bpy.props.StringProperty(name = "File Path", default = "//", subtype = 'DIR_PATH')
    bpy.types.Object.image_height = bpy.props.IntProperty(name = "Image Height", default = 1024, min = 0, max = 4096)
    bpy.types.Object.image_width = bpy.props.IntProperty(name = "Image Width", default = 1024, min = 0, max = 4096)


def unregister():
    bpy.utils.unregister_class(CreateTexButton)
    bpy.utils.unregister_class(CreateFastTexture)
    del bpy.types.Object.texture_name
    del bpy.types.Object.filepath
    del bpy.types.Object.image_height
    del bpy.types.Object.image_width


if __name__ == "__main__":
    register()