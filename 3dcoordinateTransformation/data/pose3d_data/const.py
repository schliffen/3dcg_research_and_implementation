from enum import IntEnum


class COCOKpts(IntEnum):
    NOSE = 0
    LEYE = 1
    REYE = 2
    LEAR = 3
    REAR = 4
    LSHOULDER = 5
    RSHOULDER = 6
    LELBOW = 7
    RELBOW = 8
    LWRIST = 9
    RWRIST = 10
    LHIP = 11
    RHIP = 12
    LKNEE = 13
    RKNEE = 14
    LANKLE = 15
    RANKLE = 16


class SPINKpts(IntEnum):
    OP_NOSE = 0
    OP_NECK = 1
    OP_RSHOULDER = 2
    OP_RELBOW = 3
    OP_RWRIST = 4
    OP_LSHOULDER = 5
    OP_LELBOW = 6
    OP_LWRIST = 7
    OP_MIDHIP = 8
    OP_RHIP = 9
    OP_RKNEE = 10
    OP_RANKLE = 11
    OP_LHIP = 12
    OP_LKNEE = 13
    OP_LANKLE = 14
    OP_REYE = 15
    OP_LEYE = 16
    OP_REAR = 17
    OP_LEAR = 18
    OP_LBIGTOE = 19
    OP_LSMALLTOE = 20
    OP_LHEEL = 21
    OP_RBIGTOE = 22
    OP_RSMALLTOE = 23
    OP_RHEEL = 24
    RANKLE = 25
    RKNEE = 26
    RHIP = 27
    LHIP = 28
    LKNEE = 29
    LANKLE = 30
    RWRIST = 31
    RELBOW = 32
    RSHOULDER = 33
    LSHOULDER = 34
    LELBOW = 35
    LWRIST = 36
    NECK = 37
    HEADTOP = 38
    HIP = 39
    THORAX = 40
    SPINE_H36M = 41
    JAW_H36M = 42
    HEAD_H36M = 43
    NOSE = 44
    LEYE = 45
    REYE = 46
    LEAR = 47
    REAR = 48


NUM_2D_COCO_KPTS = 17
NUM_2D_SPIN_KPTS = 49

SPIN_TO_COCO = [0, 16, 15, 18, 17, 5, 2, 6, 3, 7, 4, 12, 9, 13, 10, 14, 11]

COCO_SKELETON = [
    [15, 13],
    [13, 11],
    [16, 14],
    [14, 12],
    [11, 12],
    [5, 11],
    [6, 12],
    [5, 6],
    [5, 7],
    [6, 8],
    [7, 9],
    [8, 10],
    [1, 2],
    [0, 1],
    [0, 2],
    [1, 3],
    [2, 4],
    [3, 5],
    [4, 6],
]

SPIN_SKELETON = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4],
    [1, 5],
    [5, 6],
    [6, 7],
    [1, 8],
    [8, 9],
    [9, 10],
    [10, 11],
    [8, 12],
    [12, 13],
    [13, 14],
    [0, 15],
    [0, 16],
    [15, 17],
    [16, 18],
    [21, 19],
    [14, 21],
    [11, 24],
    [24, 22],
    [0, 38],
]
