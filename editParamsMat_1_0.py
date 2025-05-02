bl_info = {
    "name": "Edit Multi Material Parameters",
    "author": "[panGPT]_kArt",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Material Tools",
    "description": "Edit multiple material parameters across selected objects",
    "warning": "",
    "category": "Material"
}

import bpy

# Properties for the panel
class MaterialSettings(bpy.types.PropertyGroup):
    change_color: bpy.props.BoolProperty(name="Change Color", default=False)
    color: bpy.props.FloatVectorProperty(name="Base Color", subtype='COLOR', size=4, default=(1,1,1,1), min=0.0, max=1.0)
    change_roughness: bpy.props.BoolProperty(name="Change Roughness", default=False)
    roughness: bpy.props.FloatProperty(name="Roughness", default=0.5, min=0.0, max=1.0)
    change_metallic: bpy.props.BoolProperty(name="Change Metallic", default=False)
    metallic: bpy.props.FloatProperty(name="Metallic", default=0.0, min=0.0, max=1.0)
    change_alpha: bpy.props.BoolProperty(name="Change Alpha", default=False)
    alpha: bpy.props.FloatProperty(name="Alpha", default=1.0, min=0.0, max=1.0)
    change_emission: bpy.props.BoolProperty(name="Change Emission", default=False)
    emission_color: bpy.props.FloatVectorProperty(name="Emission_color", subtype='COLOR', size=4, default=(0,0,0,1), min=0.0, max=1.0)
    emission_strength: bpy.props.FloatProperty(name="Emission_strength", default=1.0, min=0.0)

# Function to change material properties of a single object
def change_material_properties(obj, settings):
    if obj.data.materials:
        for mat in obj.data.materials:
            if mat and mat.node_tree:
                for node in mat.node_tree.nodes:
                    # Handling Principled BSDF
                    if node.type == 'BSDF_PRINCIPLED':
                        if settings.change_color:
                            node.inputs['Base Color'].default_value = settings.color
                        if settings.change_roughness:
                            node.inputs['Roughness'].default_value = settings.roughness
                        if settings.change_metallic:
                            node.inputs['Metallic'].default_value = settings.metallic
                        if settings.change_alpha:
                            node.inputs['Alpha'].default_value = settings.alpha
                        if settings.change_emission:
                            node.inputs[27].default_value = settings.emission_color
                            node.inputs[28].default_value = settings.emission_strength
                    
                    # Handling Diffuse BSDF
                    elif node.type == 'BSDF_DIFFUSE':
                        if settings.change_color:
                            node.inputs['Color'].default_value = settings.color
                    
                    # Handling Glossy BSDF
                    elif node.type == 'BSDF_GLOSSY':
                        if settings.change_color:
                            node.inputs['Color'].default_value = settings.color
                    
                    # Handling other shader types (you can extend it with more nodes)
                    elif node.type == 'TRANSLUCENT':
                        if settings.change_color:
                            node.inputs['Color'].default_value = settings.color
                    
                    # Add other shader types as necessary (Refraction, Transparent, etc.)
                print(f"Material parameters of '{mat.name}' on object '{obj.name}' successfully changed.")
            else:
                print(f"Material missing or no node_tree on object '{obj.name}'.")
    else:
        print(f"Object '{obj.name}' has no materials.")

# Operator to apply settings
class MATERIAL_OT_change_properties(bpy.types.Operator):
    bl_idname = "material.change_properties"
    bl_label = "Apply Material Changes"

    def execute(self, context):
        settings = context.scene.material_settings
        selected_objects = context.selected_objects
        if selected_objects:
            for obj in selected_objects:
                if obj.type == 'MESH':
                    change_material_properties(obj, settings)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No selected objects.")
            return {'CANCELLED'}

# Panel in 3D Viewport > Tool Shelf
class MATERIAL_PT_change_properties_panel(bpy.types.Panel):
    bl_label = "Material Parameter Editing"
    bl_idname = "MATERIAL_PT_change_properties_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Material Tools'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.material_settings

        layout.prop(settings, "change_color")
        if settings.change_color:
            layout.prop(settings, "color")

        layout.prop(settings, "change_roughness")
        if settings.change_roughness:
            layout.prop(settings, "roughness")

        layout.prop(settings, "change_metallic")
        if settings.change_metallic:
            layout.prop(settings, "metallic")

        layout.prop(settings, "change_alpha")
        if settings.change_alpha:
            layout.prop(settings, "alpha")

        layout.prop(settings, "change_emission")
        if settings.change_emission:
            layout.prop(settings, "emission_color")
            layout.prop(settings, "emission_strength")

        layout.operator("material.change_properties")

# Class registration
classes = (MaterialSettings, MATERIAL_OT_change_properties, MATERIAL_PT_change_properties_panel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.material_settings = bpy.props.PointerProperty(type=MaterialSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.material_settings

if __name__ == "__main__":
    register()
