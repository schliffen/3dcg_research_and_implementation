#
#
#
import numpy as np
from dataset_loader import *
import matplotlib.pyplot as plt
from PIL import Image
from utils import smooth_trajectory, video_handler


def check_body_length(pose_3d):
    """
    this function is a try to control the extracted length of the skeletones
    if more that 3 bone violates the normal size condition, neglect the pose (there maybe errors in reconstruction)
    coco pose names:
    kp_names = ['nose', 'l_eye', 'r_eye', 'l_ear', 'r_ear', 'l_shoulder',  # 5
                'r_shoulder', 'l_elbow', 'r_elbow', 'l_wrist', 'r_wrist',  # 10
                'l_hip', 'r_hip', 'l_knee', 'r_knee', 'l_ankle', 'r_ankle']
    :param pose_3d: 3xN 3D pose in MSCOCO order
    :return: boolean
    """
    min_length = 0.1
    max_length = 0.7
    # get coco format connection of joints
    edges = np.array(COCO_SKELETON)
    error_cnt = 0
    for kp_0, kp_1 in edges:
        # calculate bone length
        bone_length = np.sqrt ( np.sum ( (pose_3d[:, kp_0] - pose_3d[:, kp_1]) ** 2 ) )
        if bone_length < min_length or bone_length > max_length:
            error_cnt += 1

    return error_cnt < 3


def create_animation(smoothed_track):
    """
    Function to create animation from the provided data
    :param smoothed_track: a list of keypoints with the shape N x 3
    :return: saves animation
    """
    # visualizing smoothed joints tracks using matplotlib
    edges = np.array(COCO_SKELETON)
    for n, pose3d_ in enumerate(smoothed_track):
        #
        pose3d = pose3d_[list(pose3d_.keys())[0]]
        #
        fig = plt.figure(figsize=(10, 5.2))
        image_ax = fig.add_subplot(1, 1, 1)
        pose_ax = fig.add_subplot(1, 1, 1, projection='3d')

        # if n==0:continue
        for i_start, i_end in edges:
            pose_ax.plot(*zip(pose3d[i_start], pose3d[i_end]), marker='o', markersize=2)
        pose_ax.scatter(*pose3d.T, s=2)
        #
        fig.tight_layout()
        # save the processed frame
        plt.savefig(f"results/track_{n}.png")
        # plt.close()
        fig.show()
    # Use pillow to open all saved frames
    images = [Image.open(f"results/track_{i}.png") for i in range(n)]
    # creatng animation from processed frames
    images[0].save('results/poseMove.gif', save_all=True, append_images=images[1:], duration=200, loop=0)


def post_process_keypoint_tracks(pose_3d_trks):
    """
    this function gets the pose track results and smooth the temporal movement of the joints
    :param pose_3d_trks: dictionary of poses
    :return: smoothed tracks
    """
    # for feeding data to the smoothing function, re format 3D joints as array with shape N x 3
    tracks_3d_ = np.array( [pose_3d_trks[i][list(pose_3d_trks[i].keys())[0]] for i in  range( pose_3d_trks.shape[0]) ] )

    smoothed_trk = np.zeros_like(tracks_3d_)
    # smoothing all joints one by one
    for item in range(tracks_3d_.shape[1]):
        joint = tracks_3d_[:,item,:]
        smth_track = smooth_trajectory(tracks_3d_.shape[0], joint) # smoothing the joint
        smoothed_trk[:, item, :] = smth_track.T

    # update the pose track dictionary
    for i, item in enumerate(pose_3d_trks):
        item[list(item.keys())[0]] = smoothed_trk[i]

    return pose_3d_trks



def save_to_csv( data_processed, save_path):
    """
    this function writes list of data into a csv file in the following format:

    column 1: x
    column 2: y
    column 3: z
    column 4: class id
    column 5: track id
    column 6: file name (frame number)
    :param data_processed: array of data that includes (x,y,z), frame id and joints are in ordered
    :param save_path: path and name to save output csv file
    :return: 0 if success and -1 if errors happen during the save
    """
    kid = '2' # only human class is considered
    track_id = '36' # player id 36 is checked
    #
    if not save_path.split('.')[-1] == 'csv':
        return -1
    with open(save_path, 'w') as csvfile:
        csvfile.write( 'kx, ky, kz, kid, track_id, file_name \n ' )
        for dindx in data_processed:
            for k in dindx.keys():
                for row in dindx[k]:
                    # create line: kx, ky, kz, kid, track id, file_name
                    line = ','.join( [str(row[0]), str(row[1]), str(row[2]), kid, track_id, k, "\n"] )
                    csvfile.write(line)

    return 0
    # -----------------------------------------------------------------

if __name__ == '__main__':

    # step 1: reading the track data
    # path to the processed data
    pose_3d_trks = np.load("data/tracking_3d_converted_world_coordinate.npy", allow_pickle=True)
    # ---------------------------------------------------------------------
    # smoothing the 3d pose tracks to remove unplausible moves
    smoothed_track = post_process_keypoint_tracks(pose_3d_trks)
    # create animation with the results
    create_animation(smoothed_track)

    # save results in the output format
    save_to_csv( smoothed_track, save_path = "results/df_pose_global_.csv")





