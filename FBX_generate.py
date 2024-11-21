import bpy
import math
from math import radians


def create_humanoid_fbx():
    # 清除默认立方体
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # 创建骨架
    bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
    armature = bpy.context.active_object
    armature.name = "HumanRig"

    # 进入编辑模式
    bpy.ops.object.mode_set(mode='EDIT')

    # 骨骼层级定义
    bones = [
        # 根部
        ("Root", None, (0, 0, 0)),

        # 脊柱
        ("Spine", "Root", (0, 0, 1)),
        ("Spine1", "Spine", (0, 0, 1.2)),
        ("Spine2", "Spine1", (0, 0, 1.4)),

        # 颈部和头部
        ("Neck", "Spine2", (0, 0, 1.6)),
        ("Head", "Neck", (0, 0, 1.8)),

        # 左右肩膀
        ("LeftShoulder", "Spine2", (-0.5, 0, 1.5)),
        ("RightShoulder", "Spine2", (0.5, 0, 1.5)),

        # 手臂
        ("LeftArm", "LeftShoulder", (-0.7, 0, 1.3)),
        ("LeftForeArm", "LeftArm", (-0.9, 0, 1.1)),
        ("LeftHand", "LeftForeArm", (-1.1, 0, 0.9)),

        ("RightArm", "RightShoulder", (0.7, 0, 1.3)),
        ("RightForeArm", "RightArm", (0.9, 0, 1.1)),
        ("RightHand", "RightForeArm", (1.1, 0, 0.9)),

        # 髋部
        ("Hips", "Root", (0, 0, 0.5)),

        # 腿部
        ("LeftUpLeg", "Hips", (-0.3, 0, 0)),
        ("LeftLeg", "LeftUpLeg", (-0.3, 0, -1)),
        ("LeftFoot", "LeftLeg", (-0.3, 0, -1.8)),

        ("RightUpLeg", "Hips", (0.3, 0, 0)),
        ("RightLeg", "RightUpLeg", (0.3, 0, -1)),
        ("RightFoot", "RightLeg", (0.3, 0, -1.8))
    ]

    # 创建骨骼
    for bone_name, parent_name, location in bones:
        bone = armature.data.edit_bones.new(bone_name)

        # 设置父骨骼
        if parent_name:
            parent_bone = armature.data.edit_bones[parent_name]
            bone.parent = parent_bone
            bone.head = parent_bone.tail
        else:
            bone.head = (0, 0, 0)

        # 设置骨骼长度和方向
        bone.tail = tuple(h + l for h, l in zip(bone.head, location))

    # 退出编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')

    # 导出FBX
    bpy.ops.export_scene.fbx(
        filepath="./human_rig.fbx",
        use_selection=True,
        object_types={'ARMATURE'},
        use_mesh_modifiers=True,
        bake_space_transform=True
    )

    print("人体骨架FBX已生成: ./human_rig.fbx")


# 运行函数
create_humanoid_fbx()