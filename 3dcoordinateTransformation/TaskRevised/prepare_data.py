#
# this file reads data from csv format and converts it to
# the format that i have used.
#
import os
from dataset_loader import *
from utils import *
import argparse
args = argparse.ArgumentParser("provide the date path")
# kpt2d_path, pose_local_path, pose_global_path, track_path, camera_params_path, output_path
args.add_argument("--droot", default="data/pose3d_data/", help="path to the data folder")
args.add_argument("--kpt2d", default="df_kpt.csv", help="file that keeps players 2d keypoints")
args.add_argument("--kpt3d", default="df_pose_local.csv", help="file that keeps players 3d keypoints")
args.add_argument("--trck", default="df_track.csv", help="file that keeps players bboxes, track id, "
                                                         "local per frame id, segments, and etc. ")
args.add_argument("--cam", default="camera_smooth.csv", help="file that keeps camera parameters for each frame")
# args.add_argument("--frmhw", default = (3840, 2160), help="the target frame size, will used for rescaling")
args.add_argument("--trgt_id", default = '36', help="the track id that we want to process")
# todo: adding output files names


arg = args.parse_args()


def get_bbox_max_iou(player_bbox, trgt_player):
    """
    controlling all bboxes in a frame getting the bounding box that has maximum iou with target bounding box
    Note: this is very basic tracking and it will fail in occlusions, thats why I salected an isolate player
    :param player_bbox: dictionary of bounding boxes
    :param trgt_player: target bounding box to track
    :return:
        iou_max: maximum iou in the list,
        ki_max: player id corresponding with maximum iou
        xmin, ymin, xmax, ymax: bounding box that made maximum iou
    """
    iou_max = 0
    for ki in player_bbox.keys():
        xmin = player_bbox[ki][1] # xmin at frame number kf, and bounding box ki (same for others)
        ymin = player_bbox[ki][2]
        xmax = player_bbox[ki][3]
        ymax = player_bbox[ki][4]

        # calculate iou between current bbox and target player bbox
        iou = calc_iou(player_bbox[ki][1:5], trgt_player)
        # print iou for debugging purpose
        # print(" iou: ", iou)
        # if iou is less that 0.4, check out next bbox
        if iou>iou_max: # low iou works because some frames may miss in between which leads to lower ious
            iou_max = iou
            ki_max = ki
        else:
            continue

        return iou_max, ki_max, xmin, ymin, xmax, ymax



def collect_data(visualize=False):
    """
    this function is designed to collaect all required tracking data
    before running this function some data files should be created:
    frame_bboxes_raw: bounding boxes at each frame
    single_kpt_2d_raw: 2D keypoints at each frame for each player
    local_kpt_3d_raw:  3D  keypoints at each frame for each player

    target player bounding box is manually collected at the first frame,
    starting from the second frame, the target player's bbox is tracked by looking at iou
    the bbox with max iou will be the target player

    :param: bool visualize: true if visualizing bboxes on frames is required
    :return:
    """
    #
    player_2d_bbox= np.load("data/frame_bboxes_raw.npy", allow_pickle=True ) # load
    player_2d_kpt = np.load("data/single_kpt_2d_raw.npy", allow_pickle=True )
    poses_3dkpt   = np.load("data/local_kpt_3d_raw.npy", allow_pickle=True )

    # COCO keypoint that is connected to eachother
    edges = np.array(COCO_SKELETON)

    if visualize:
        import matplotlib.pyplot as plt
        datapr = video_handler()


    trgt_player = [1834, 2002, 1949, 2160 ] # bounding box of the target player in the first frame [xmin, ymin, xmax, ymax]

    # dictionary to store extracted data in the following order
    # frame number list, target player id list (the get keypoints of tracking player) as it changes in different frames
    # list of keypoints, list of bounding boxes, list of 3D keypoints
    # note: order is very important in the lists (matching is done by list orders - easy but a risky way to keep data - not recommended)
    tracking_playerp = {"frame_num":[], "player_id":[], "kpt":[], "bbox":[], "kpt3d":[]}

    # due to size of data; speed of sample collection by limiting tracking length to 100
    max_frame = 100 # limit the searches by stopping if 100 tracking frames were collected

    # iterting threough frames numbers in the bounding box data
    for i, kf in enumerate(player_2d_bbox[0].keys()): # kf is frame number

        if i>max_frame: break # check if 100 frames collected

        if visualize: # if true get the frame
            frame = datapr.get_frame(int(kf)) # read the frame image for visualization

        # get the player id with the max iou with target player to track
        iou_max, ki, xmin, ymin, xmax, ymax = get_bbox_max_iou(player_2d_bbox[0][kf], trgt_player)
        # ki: local player id of max iou with target
        # keep data only if max_iou > 0.4
        if iou_max>.4:
            # get detection id of the player to reach out the 2d and 3d poses of that detection id in this frame
            local_id = player_2d_bbox[0][kf][ki][0]

            # list to store 3d keypoints
            kpts_3d = []
            # some times, 3d pose of that local id does not exists; if not -> go to the next frame
            if not local_id in poses_3dkpt[0][kf].keys(): continue
            #
            for i in range(NUM_COCO_KPTS): # rescaling keypoints
                lpose = poses_3dkpt[0][kf][local_id][str(i)] # get ith keypoint [x,y,z] of player "local_id" at frame "kf"
                kpts_3d.append(lpose)
            kpts_3d = np.array(kpts_3d)


            # list to store 2d keypoints
            kpoint2d = []
            for keyy in player_2d_kpt[0][kf][local_id].keys():
                kpoint2d.append( player_2d_kpt[0][kf][local_id][keyy]) # this appends the keyy keypoints of local_id at frame kf
            kpoint2d = np.array(kpoint2d)

            # filling out the data dictionary; each new data is added to the end of the list to keep orders
            tracking_playerp["bbox"].append( [xmin, ymin, xmax, ymax] )
            tracking_playerp["player_id"].append( local_id )
            tracking_playerp["frame_num"].append( kf )
            tracking_playerp["kpt"].append(kpoint2d)
            tracking_playerp["kpt3d"].append(kpts_3d)

            if visualize:
                # create figure and subplot
                fig = plt.figure(figsize=(10, 5.2))
                image_ax = fig.add_subplot(1, 1, 1)
                # add 2d skeletons to the axis
                for i_start, i_end in edges:
                    image_ax.plot(*zip(player_2d_kpt[0][kf][local_id][str(i_start)], player_2d_kpt[0][kf][local_id][str(i_end)]), marker='o', markersize=2)
                image_ax.scatter(*kpoint2d.T, s=2)
                # draw bounding boxes on the frame
                trgt_player = [xmin, ymin, xmax, ymax]
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax),(200,1,1),2)
                image_ax.imwrite(frame) # write image to the cwd

                image_ax.close()
    # save collected track data to use in 3d reconstruction
    np.save("data/tracking_bbox_kpoints_2d_3d_forTest.npy", [tracking_playerp])



def create_base_data_dictionaries(arg):
    """
    this function checks to see if per-frame 3D and 2D and bounding boxes data dictionaries exists
    if not, creates them
    :param arg: argument that includes csv data file path
    :return:
    """
    # todo : add error handling

    datastream = data_handler( kpt2d_path = os.path.join( arg.droot, arg.kpt2d),
                               pose_local_path = os.path.join( arg.droot, arg.kpt3d),
                               track_path = os.path.join( arg.droot, arg.trck),
                               camera_params_path = os.path.join( arg.droot, arg.cam) )
    assert datastream is not None
    # I will collect the data related to the id 36
    trgt_track_id = arg.trgt_id # this cariable keeps target player id that we are aiming to collect track info
    #
    # to make processes faster, this takes data from csv and preprocesses then save it as npy for later use in algo
    # all 3d data is taken from the csv file
    if not os.path.exists("data/local_kpt_3d_raw.npy"): # check if this data exits
        # local_kpt_3d = np.load("data/local_kpt_3d_raw.npy", allow_pickle='TRUE')
        local_kpt_3d = [datastream.get_pose_local( trgt_track_id )] # this method in data handler class read and format 3d data
        np.save("data/local_kpt_3d_raw.npy", local_kpt_3d)

    # load all 2d track data and save them as a dictionary
    if not os.path.exists("data/tracking_bbox_2d_raw.npy"):
        # local_bbox_2d = np.load("data/tracking_bbox_2d_raw" + ".npy", allow_pickle='TRUE')
        local_bbox_2d = [datastream.get_track_bboxs()] # this method in data handler reads csv and processes 2d data
        # save 2d data as array to make it in access
        np.save("data/tracking_bbox_2d_raw.npy", local_bbox_2d)

    # create a bounding box dataset (get player bounding boxes at every frame )
    if not os.path.exists("data/frame_bboxes_raw.npy"):
        kpt_2d = datastram.get_track_bboxs() # collect bounding boxes
        np.save("data/frame_bboxes_raw.npy", [kpt_2d])

    # create a data dictionary that stores keypoints of all players at all frames
    if not os.path.exists("data/single_kpt_2d_raw.npy"):
        single_kpt_2d_ = [datastream.get_df_kpt()]
        np.save("data/single_kpt_2d_raw.npy", single_kpt_2d_ )



if __name__=='__main__':

    # step 1- create base data dictionaries : tracking boundin boxes, per-frame 2D keypoints, per-frame 3D keypoints
    create_base_data_dictionaries (arg)

    # collecting target players tracking data using created data dictionaries
    collect_data()


    # --------------------------------------------------------------------------------------------
    #  in the following codes I tried to track a single player through  different frames (it doest work since tracking were not good enough)
    # --------------------------------------------------------------------------------------------
    """
    # get the frame indexes that target id appears in them
    frames_idx = list(local_kpt_3d[0].keys())

    # to make program run lighter, keep only the target player's data
    if not os.path.exists("data/singlePlayerTracks3d_raw_" + trgt_track_id + ".npy"):
            # tracking_3d_model = np.load("data/singlePlayerTracks3d_raw_" + trgt_track_id + ".npy", allow_pickle='TRUE')

        tracking_3d_model = {} # dictionary to store data ordered
        # data order "
        for ik in frames_idx: # look at the frames that target id appeared
            single_pose = []
            if ik in local_kpt_3d[0].keys():
                for j in range( len(local_kpt_3d[0][ik][trgt_track_id].keys())):
                    single_pose.append( local_kpt_3d[0][ik][trgt_track_id][str(j)]) #
                tracking_3d_model.update( {ik: np.array(single_pose) } )
        # save collected data
        np.save("data/singlePlayerTracks3d_raw_" + trgt_track_id + ".npy", [tracking_3d_model] )

    # loading camera parameters from csv and keep them as an array
    if os.path.exists("data/single_test_cam_params.npy"):
        # cam_params = np.load("data/single_test_cam_params.npy", allow_pickle='TRUE')
        cam_params_ = datastream.get_camera_params()
        cam_params = {}
        # frame number : camera parameters
        for k in frames_idx:
            cam_params.update( { k: cam_params_[k]} )
        np.save("data/single_test_cam_params.npy", [cam_params] )
    #
    # to track the players, as the local id changes at each frame, its required to know
    # which local id is corresponding to which track id, this makes that easy using dictionary
    if os.path.exists("data/track_to_detection_correspondence_id_.npy"):
        track_detection_correspondence_id_ = np.load( "data/track_to_detection_correspondence_id_.npy", allow_pickle=True)[0]
    else:
        track_to_detection_id_ = datastream.get_track_detection_data()
        np.save( "data/track_to_detection_correspondence_id_.npy", [track_to_detection_id_])
        track_detection_correspondence_id_ = track_to_detection_id_

    # iterating through all frames in 2d keypoint file, and collets 2d keypoints of target track id
    # there may be some frames that 2d or 3d keypoints does not exist, so keeping frames that both exits
    # in valid frams is important
    if os.path.exists("data/single_kpt_2d_"+ trgt_track_id +".npy"):
        single_kpt_2d = np.load("data/single_kpt_2d_"+ trgt_track_id +".npy", allow_pickle='TRUE')
        valid_frames = np.load("data/valid_frames_"+ trgt_track_id +".npy", allow_pickle=True)
    else:
        valid_frames = []
        single_kpt_2d = {}
        
        for kidx in frames_idx: # to get only specific frames
            # list to keep 2d poses at this frame
            pose2d = []
            # check if this id exits in 2d track file
            if trgt_track_id in track_detection_correspondence_id_[kidx].keys():
                # exists! save this as valid frame id
                valid_frames.append( kidx )
                playerindex = track_detection_correspondence_id_[kidx][trgt_track_id] # get local player id given global player id
                
                for k in single_kpt_2d_[0][kidx][playerindex].keys():
                    # collect players keypoints 
                    pose2d.append( [ single_kpt_2d_[0][kidx][playerindex][k][0], single_kpt_2d_[0][kidx]['0'][k][1] ]  ) #
                # keep frame index and its value keypoints belonging to target player 
                single_kpt_2d.update( { kidx: np.array( pose2d ) } ) 
        
        # save keypoints data and list of valid frames for later process
        np.save("data/single_kpt_2d_"+ trgt_track_id +".npy", [single_kpt_2d] )
        np.save("data/valid_frames_"+ trgt_track_id +".npy", [valid_frames])
    # ------------------------------------------------------------------------------------
    """














print("finished")


