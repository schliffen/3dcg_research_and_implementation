#
# this is for loading dataset for the rest of the processes
#
from enum import IntEnum
import numpy as np
import csv
import cv2

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


NUM_COCO_KPTS = 17
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

# --------------------------< class for handling data related processess>----------------------------
class data_handler:
    """
    class for handling data related processes; read, preprocess, save, filter
    """
    def __init__(self, **kwargs):
        # path to the csv records
        # check to have required keys
        required_pathes = ['kpt2d_path', 'pose_local_path', 'pose_local_path', 'track_path', 'camera_params_path' ]
        for path in required_pathes:
            if not path in kwargs.keys():
                print("Error: path " + path + "does not provided!")
                return None
        # setting required csv paths; the paths will used to read raw data
        self.df_kpt_path = kwargs['kpt2d_path']
        self.pose_local_path = kwargs['pose_local_path']
        self.track_path = kwargs['track_path']
        self.camera_params_path = kwargs['camera_params_path']


    def get_df_kpt(self):
        """
        this method reads the csv containes 2d keypoints of players in different frames
        and reorders it based on frame number and player id
        the output dictionary format is as follows:
        {frame number: {player id: {keypoint index: [ x, y] } } }
        :return: dictionary contains 2d keypoints
        """
        # read csv data
        # kx,ky,score,kid,file_name,detection_id
        with open( self.df_kpt_path ) as file:
            df_kpt_lines = file.readlines()
        # reordering data for easy access frame -> player -> keypoints
        df_kpt_ordered = {}
        for item in df_kpt_lines[1:]:
            kpt_2d_inf = item.strip().split(',')
            frame_number = kpt_2d_inf[4]
            player_id = kpt_2d_inf[5]
            kpt_id = kpt_2d_inf[3]
            if frame_number in df_kpt_ordered.keys():
                #
                if player_id in df_kpt_ordered[frame_number]:
                    df_kpt_ordered[frame_number][player_id].update({ kpt_id: [float(kpt_2d_inf[0]), float(kpt_2d_inf[1]) ]})
                else:
                    df_kpt_ordered[frame_number].update({player_id: { kpt_id: [float(kpt_2d_inf[0]), float(kpt_2d_inf[1]) ]} })
            else:
                df_kpt_ordered.update({frame_number: {player_id: { kpt_id: [float(kpt_2d_inf[0]), float(kpt_2d_inf[1]) ]} } })

        return df_kpt_ordered


    def get_pose_local(self, trgt_id):
        """
        this method reads 3D keypoints from csv file, filters based on track_id and reorders them
        to make it easy to use.
        poses format is SPIN, for changes to coco
        data format will be:
        1- frame number (file name):
        2- player id
        3- keypoint index
        {frama_num: {player_id: {kpt index: [x, y, z]} } }
        :param trgt_id:player track_id
        :return: a dictionary that stores data in ordered format
        """
        # reading data from the csv file to a list
        with open( self.pose_local_path ) as file:
            #each line contains:  kx, ky, kz, kid, file_name, track_id
            localpose_lines = file.readlines()

        # dictionary to keep data
        localpose_ordered = {}
        #
        # process data line by line
        for inx, line_ in enumerate(localpose_lines[1:]): # skip headline
            l1 = line_.strip().split(',') # strip to remove \n and split line string based on space -> a list contains all columns in that line
            player_id = l1[5].strip() # get player id
            frame_number = l1[4].strip() #
            kpt_id = l1[3].strip() # keypoint id SPIN format

            item = [ float(l1[0]), float(l1[1]), float(l1[2]) ] # kx, ky, kz

            # check if id is exist in coco format (if not go to the next line)
            if not int(kpt_id) in SPIN_TO_COCO:
                continue

            # need to change format from SPIN to coco
            index = SPIN_TO_COCO.index(int(kpt_id)) # get coco index corresponding to SPIN id

            # check if this frame is added before to the dictionary
            if frame_number in localpose_ordered.keys():
                # if this player is addded befor?
                if player_id in localpose_ordered[frame_number]:
                    # add the keypoints that belongs to player_id in the frame frame_number
                    localpose_ordered[frame_number][player_id].update({ str( index ): [item[0], item[1], item[2] ]})
                else:
                    localpose_ordered[frame_number].update({player_id: { str( index ): [item[0], item[1], item[2] ]} })
            else:
                # first time add the frame number to the keys
                localpose_ordered.update({frame_number: {player_id: { str( index): [item[0], item[1], item[2] ]} } })

        return localpose_ordered


    def get_track_bboxs(self):
        """
        this method reads track data and gets bounding boxes of all players in all frames.

        :return: dictionary contains bounding boxes in this order
        {frame number: { player id : [xmin, ymin, xmax, ymax]}}
        """
        # read all lines from the csv
        with open( self.track_path ) as file:
            df_track_lines = file.readlines()

        # dictionary to store all data
        tracking_bboxes  = {}

        for line_ in df_track_lines[1:]:
            line = line_.strip().split(',')
            category = int(line[4].strip() ) # check the line class to make sure it is human not objects (ball or etc)
            # category should be 2: human class code in the model
            if category !=2:
                continue
            # getting bounding boxes
            xmin = int(line[0].strip() )
            ymin = int(line[1].strip() )
            xmax = int(line[2].strip() )
            ymax = int(line[3].strip() )
            #
            detection_id = line[7].strip() # player id at frame (changes every frame)
            file_name = line[8].strip()  # frame number
            track_id = line[23].strip() # track id (global id of player)

            if file_name in tracking_bboxes.keys(): # check if this frame is added to dict
                tracking_bboxes[file_name].update({track_id: [detection_id, xmin, ymin, xmax, ymax] })
            else:
                tracking_bboxes.update({file_name: {track_id: [detection_id, xmin, ymin, xmax, ymax] }})

        return tracking_bboxes

    def get_camera_params(self):
        """
        this method reads the camera parameters from csv and stored them in frame based orders
        output is a dictionary which is called by frame number to access all parameters
        output: {frame number: [rot_x,rot_y,rot_z,tx,ty,tz,fx,fy,princ_x,princ_y,error]}
        :return: a dictionary of camera parameters of frames
        """
        # line order: rot_x, rot_y, rot_z, tx,ty,tz, fx,fy, princ_x,princ_y, error, file_name
        with open( self.camera_params_path ) as file:
            camparam_lines = file.readlines()

        camparams = []
        for line_ in  camparam_lines[1:]:
            # as there are some frames with wrong parameters, skip the incomplete cases
            # and save the rest in a list
            try:
                # read line, split wrt "," and convert each column to float
                ln = list(map(lambda x: float(x), line_.strip().split(',')))
                camparams.append( ln )
            except:
                continue
        # dictionary to keep camera paramters per frame
        camparam_ordered = {}
        for item in camparams:
            frame_number = int( item[-1] ) # read frame number at stored at last column
            camparam_ordered.update({str(frame_number): item[:-1] })

        return camparam_ordered


    def get_track_detection_data(self):
        """
        this method reads tracking csv file that includes both player per-frame id and global id
        and creates a dictionary so that by providing track id (global) it returs frame id (local)
        data format: {frame number: {track id: detection id} }
        :return: a dictionary that keeps (key: global, value: local) at every frame
        """
        with open( self.track_path ) as file:
            df_track_lines = file.readlines()

        corresspondence = {}
        for line_ in df_track_lines[1:]:
            line = line_.strip().split(',')
            detection_id = line[7].strip() # id of player at the frame
            file_name = line[8].strip() # frame number
            track_id = line[23].strip() # player global id

            # first check if frame number exists
            if file_name in corresspondence.keys():
                corresspondence[file_name].update({track_id: detection_id})
            else:
                # first update; add frame number and its value
                corresspondence.update({file_name: {track_id: detection_id}})

        return corresspondence



if __name__=='__main__':

    # this part is for testing the class to see if its working fine

    datastram = data_handler("data/pose3d_data/df_kpt.csv", "data/pose3d_data/df_pose_local.csv",
                            "data/pose3d_data/df_pose_local.csv", "data/pose3d_data/df_track.csv",
                            "data/pose3d_data/camera_smooth.csv", "data/pose3d_data/df_sample_output.csv")

    kpt_2d = datastram.get_track_bboxs()
    np.save("data/frame_bboxes_raw.npy", [kpt_2d])

    print('finished!')







