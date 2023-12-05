bl_info = {
    "name": "Count Java Files and Generate Trees",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "description": "Counts Java files in a directory and generates trees based on the count",
    "category": "Object"
}

import bpy
import os
import random

# 定义用于统计Java文件数量的函数
def count_java_files(directory):
    """计算指定目录及其子目录下的Java文件数量"""
    try:
        return sum([1 for root, dirs, files in os.walk(directory) if os.path.isdir(root) for file in files if file.endswith('.java')])
    except FileNotFoundError:
        return 0

# 定义操作，执行Java文件数量的统计并生成树木
class OBJECT_OT_CountJavaFiles(bpy.types.Operator):
    """计算指定文件夹中Java文件的数量并根据该数量生成树木"""
    bl_idname = "object.count_java_files"
    bl_label = "Count Java Files and Generate Trees"

    def execute(self, context):
        folder_path = bpy.path.abspath(context.scene.custom_folder_path)
        num_files = count_java_files(folder_path)

        # 调用生成树木的函数
        generate_trees(num_files, context)

        self.report({'INFO'}, f"Generated {num_files} trees based on Java files count.")
        return {'FINISHED'}

# 定义生成树木的函数
def generate_trees(num_trees, context):
    # 设置方形区域的尺寸和树的实际尺寸
    area_size = 200
    tree_dimensions = (33, 31, 27)

    # 获取原始的树对象
    tree_name = 'solotree'
    original_tree = bpy.data.objects.get(tree_name)

    # 创建新的集合，如果已存在则先删除
    new_collection_name = 'NewTreesCollection'
    if new_collection_name in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections[new_collection_name])
    new_collection = bpy.data.collections.new(new_collection_name)
    bpy.context.scene.collection.children.link(new_collection)

    # 创建方形区域，如果已存在则先删除
    reference_area_name = 'ReferenceArea'
    if reference_area_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[reference_area_name], do_unlink=True)
    bpy.ops.mesh.primitive_plane_add(size=area_size, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    reference_area = bpy.context.active_object
    reference_area.name = reference_area_name
    
    # 创建浅绿色材质并应用到方形区域
    mat = bpy.data.materials.new(name="LightGreenMaterial")
    mat.diffuse_color = (0.247, 0.749, 0.447, 1.0)  # 浅绿色
    reference_area.data.materials.append(mat)

    # 将树的原点移至几何体的底部中心
    bpy.context.view_layer.objects.active = original_tree
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    original_tree.location.z += original_tree.dimensions.z / 2

    # 循环复制树对象
    for _ in range(num_trees):
        # 复制树对象
        new_tree = original_tree.copy()
        new_tree.data = original_tree.data.copy()
        new_tree.animation_data_clear()
        
        # 将复制的树添加到新的集合中
        new_collection.objects.link(new_tree)
        
        # 设置树的实际尺寸
        new_tree.dimensions = tree_dimensions
        
        # 根据指定范围随机分布树的位置
        pos_x = random.uniform(-117, 50)
        pos_y = random.uniform(-83, 88)
        new_tree.location = (pos_x, pos_y, 0)

    # 更新场景，使变化生效
    bpy.context.view_layer.update()

# 定义面板，用于用户输入文件夹路径
class OBJECT_PT_CustomPanel(bpy.types.Panel):
    """创建一个自定义面板，在3D视图的UI中"""
    bl_label = "Count Java Files"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # 创建一个文本框让用户输入文件夹路径
        layout.prop(scene, "custom_folder_path")

        # 创建一个按钮，当按下时执行操作
        layout.operator("object.count_java_files")

# 注册和注销功能
def register():
    bpy.utils.register_class(OBJECT_PT_CustomPanel)
    bpy.utils.register_class(OBJECT_OT_CountJavaFiles)
    bpy.types.Scene.custom_folder_path = bpy.props.StringProperty(
        name="Folder Path",
        description="Enter the folder path",
        default="",
        subtype='DIR_PATH'
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    bpy.utils.unregister_class(OBJECT_OT_CountJavaFiles)
    del bpy.types.Scene.custom_folder_path

if __name__ == "__main__":
    register()
