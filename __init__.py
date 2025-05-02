# SPDX-FileCopyrightText: 2025 panda, AKoz.
#
# SPDX-License-Identifier: GPL-2.0-or-later


bl_info = {
    "name": "Edit Parameters Tool All MATerials",
    "author": "[PandaGPT]_AKozyrev",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Material Tools",
    "description": "Edit multiple material parameters across selected objects",
    "warning": "",
    "category": "Material"
}

import bpy

# Properties for the panel
class MaterialSettings(bpy.types.PropertyGroup):
    change_color: bpy.props.BoolProperty(name="Base Color", default=False)
    color: bpy.props.FloatVectorProperty(name="", subtype='COLOR', size=4, default=(1,1,1,1), min=0.0, max=1.0)
    change_roughness: bpy.props.BoolProperty(name="Roughness", default=False)
    roughness: bpy.props.FloatProperty(name="", default=0.5, min=0.0, max=1.0)
    change_metallic: bpy.props.BoolProperty(name="Metallic", default=False)
    metallic: bpy.props.FloatProperty(name="", default=0.0, min=0.0, max=1.0)
    change_alpha: bpy.props.BoolProperty(name="Alpha", default=False)
    alpha: bpy.props.FloatProperty(name="", default=1.0, min=0.0, max=1.0)
    change_emission: bpy.props.BoolProperty(name="Emission", default=False)
    change_emission_color: bpy.props.BoolProperty(name="Color", default=False)
    change_emission_strength: bpy.props.BoolProperty(name="Strength", default=False)
    emission_color: bpy.props.FloatVectorProperty(name="", subtype='COLOR', size=4, default=(1,1,1,1), min=0.0, max=1.0)
    emission_strength: bpy.props.FloatProperty(name="", default=1.0, min=0.0)

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
                            if settings.change_emission_color:
                                node.inputs[27].default_value = settings.emission_color
                            if settings.change_emission_strength:
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
    bl_description = "Applies settings to selected objects that have a material"

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

# Operator to reset settings
class MATERIAL_OT_reset_settings(bpy.types.Operator):
    bl_idname = "material.reset_settings"
    bl_label = "Reset Parameters"
    bl_description = "Resets all addon settings including checkboxes to default"

    def execute(self, context):
        settings = context.scene.material_settings

        settings.change_color = False
        settings.color = (1, 1, 1, 1)

        settings.change_roughness = False
        settings.roughness = 0.5

        settings.change_metallic = False
        settings.metallic = 0.0

        settings.change_alpha = False
        settings.alpha = 1.0

        settings.change_emission = False
        settings.change_emission_color = False
        settings.change_emission_strength = False
        settings.emission_color = (1, 1, 1, 1)
        settings.emission_strength = 1.0

        self.report({'INFO'}, "Parameters reset to default")
        return {'FINISHED'}


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
        column = layout.column()
        row = layout.row()

        column.prop(settings, "change_color")
        if settings.change_color:
            column.prop(settings, "color")
        
        column.prop(settings, "change_metallic")
        if settings.change_metallic:
            column.prop(settings, "metallic")
            
        column.prop(settings, "change_roughness")
        if settings.change_roughness:
            column.prop(settings, "roughness")

        column.prop(settings, "change_alpha")
        if settings.change_alpha:
            column.prop(settings, "alpha")

        column.prop(settings, "change_emission")
        if settings.change_emission:
            sp = column.split(factor=0.05)
            _ = sp.column()                       # spacer
            sp = sp.split(factor=1.0)
            c = sp.column()
            c.prop(settings, "change_emission_color")
            if settings.change_emission_color:
                c.prop(settings, "emission_color")
            c.prop(settings, "change_emission_strength")
            if settings.change_emission_strength:
                c.prop(settings, "emission_strength")

        column.separator()
        column.separator()
        column.separator()
        
       # column.operator("material.change_properties")
        row = column.row()
        row.scale_y = 1.5
        row.operator("material.change_properties")

        column.separator()
        column.separator()

        column.operator("material.reset_settings", icon='LOOP_BACK')

# Class registration
classes = (
    MaterialSettings,
    MATERIAL_OT_change_properties,
    MATERIAL_PT_change_properties_panel,
    MATERIAL_OT_reset_settings)

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
    
    