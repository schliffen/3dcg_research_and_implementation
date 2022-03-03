#
#
#
import numpy as np
import cv2
from scipy.optimize import minimize


# an attempt to smooth trajectory : but fir limited data it is not at all applicable
def objective_fun(params, detections, time_index, traj_length, a=0.01, b=0.1, c=0.1):
    """
    objective[cost] function to be minimized
    there are 3 term of errors to bi minimized:
    E_det: detection error: results should be close to the provided detections
    E_dyn: temporal error: in numerical analysis, the temporal term of a motion 2x_1 - (x_0 + x_2) = 0 makes the
                           motion smooth
    E_vel: velocity error (differential error): this term x_1-x_0 = 0 as a constraint also makes the move smooth
    the optimization algorithm tries to minimize these three terms with the following combination
    loss = a*E_det + b*E_dyn + c*E_vel
    each term acts as regularizer to the others (according to the experience better to loosen detection error)

    tradeof of the three is desirable solution

    :param params: parameters that provides to the optimizer to optimize
    :param detections: source detection values
    :param time_index: time index: t-1, t, t+1
    :param traj_length: number of tracks
    :param a: coefficient of detection error
    :param b: coefficient of temporal error
    :param c: coefficient of velocity error
    :return: combined loss
    """
    X_ = np.reshape(params, (3, traj_length))
    E_det = np.sum(np.linalg.norm(X_ - detections, axis=0)) # calculate integratio of norm of the error \int_t0^tN (E_det) dx dt
    temporal_term = X_[:, time_index[0, :]] - 2 * X_[:, time_index[1, :]] + X_[:, time_index[2, :]]
    E_dyn = np.sum(np.linalg.norm(temporal_term, axis=0))
    E_vel = np.sum(np.linalg.norm(X_[:, time_index[0, :]] - X_[:, time_index[1, :]], axis=0))
    return a * E_det + b*E_dyn + c*E_vel


def smooth_trajectory(traj_length, joint_track):
    """
    function to smooth the trajectory of moving the joint_track
    :param traj_length: length of the track N
    :param joint_track: track of joints, array with shape N x 3
    :return: smoothed version of joint_track with the same shape N x 3
    """
    # create 3 different time values t-1, t, t+1
    time_index = np.array([range(0, traj_length - 2), range(0 + 1, traj_length - 1), range(0 + 2, traj_length)])
    detection_kpnts = joint_track.T
    params = detection_kpnts.copy() # at the beginning parameters are equal to tracks of joints
    # optimize the trajectory according to the objective function
    # Second order optimization algorithm BFGS works very good when we start close to the minimum (max iter = 200)
    res = minimize(objective_fun, params, args=(detection_kpnts, time_index, traj_length), method='L-BFGS-B',
                   options={'gtol': 1e-6, 'disp': False, 'maxiter': 200})
    smoothed_positions = np.reshape(res.x, (3, traj_length))

    return smoothed_positions


def create_intrinsic_matrix(fx, fy, cx, cy):
    """
    :param fx: focal length x
    :param fy: focal length y
    :param cx: width of center of the camera plane
    :param cy: height of center of the camera plane
    :return: camera intrinsic matrix
    """
    return np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])



class camera:
    def __init__(self,  A=None, R=None, T=None, w=None, h=None):
        """
        Setting camera parameters to  default values and size for scaling;
        :param A: camera intrinsic matrix
        :param R: rotation matrix
        :param T: translation vector
        :param w: image width
        :param h: image height
        """
        self.A = np.eye(3, 3) # set to identity
        self.A_i = np.eye(3, 3) # inverse of the intrinsic
        self.T = np.zeros((3, 1))
        self.scale = 1.0 # scale default to 1
        if not h is None and not w is None:
            self.set_size(h,w)

    def set_size(self, h, w):
        """
        Set width and height in class
        :param h: int scalar height
        :param w: int scalar width
        """
        self.width = w
        self.height = h

    def set_intrinsics(self, A):
        """
        this method sets intrinsig matrix and inverse of it
        :param A: a 3x3 matrix
        """
        self.A = A
        self.A_i = np.linalg.inv(A) # used in unprojecting from 2D tp 3D

    def set_extrinsics(self, R, T):
        """
        this method sets rotation and translation matrix [R|T]
        :param R: rotation matrix 3x3
        :param T: translate vector 3x1
        """
        assert(T.shape[0] == 3) # checking the shape of the translation shape

        self.R = R
        self.T = T


    def project(self, points3d, dtype=np.int32):
        """
        this method projects 3D points to 2D plane using intrinsic, rotation and translation were set in the class P = A[R|T]

        :param points3d: an array of 3D points with the shape 3 x N or N x 3
        :param dtype: data type of the output array
        :return: pixels: array of points with shape N x 2; result of projected 3d points to image plane
                 depth: scale came from projection
        """
        # input array should be at shape 3 x N -> control the shape and transpose if required
        if points3d.shape[0] != 3:
            points3d = points3d.T

        # get N (number of points)
        n_points = points3d.shape[1] # N
        # projection happens here P x points3d = A [R|T] x points3d = A x ( R x points3d + T)
        projected_points_ = self.A.dot(self.R.dot(points3d) + np.tile(self.T, (1, n_points)))
        depth = projected_points_[2, :]
        # devide points by scale: [x/depth, y/depth ]
        pixels = projected_points_[0:2, :] / projected_points_[2, :] / self.scale # scale is kept in 1

        # controlling the type and change them to integer
        if issubclass(dtype, np.integer):
            pixels = np.round(pixels)

        # transpose the shape to make it N x 2:
        pixels = np.array(pixels[:2].T, dtype=dtype)
        return pixels, depth


    def unproject(self, points2d, depth):
        """
        this method lifts up points from image plane to 3D coordinate using camera parameters in the class
        X' = P^-1 X (unprojecting) (A[R|T])^-1 x 2dpoint = [R|T]^-1 x A^-1 x 2dpoint = [R|T]^-1 x A^-1 = R^T x -T x A^-1 x 2dpoint
        :param points2d: 2d image points with the shape 2 x N or N x 2
        :param depth: the projection scale
        :return: an array of shape N x 3: points in 3D space
        """

        # control the shape; required shape: 2 x N
        if points2d.shape[0] != 2:
            points2d = points2d.T

        # get N
        n_points = points2d.shape[1]
        # convert [x, y] to [x, y, 1] needed in matrix multplication
        points2d = np.vstack((points2d[0,:], points2d[1,:], np.ones(points2d.shape[1])))
        # multiply inverse of the intrinsic matrix to the points
        pixel_i = self.A_i.dot(points2d)
        # inverting; the translation and rotation part
        pixel_world = self.R.T.dot(np.multiply(depth, pixel_i) - np.tile(self.T, (1, n_points)))

        return pixel_world[:3,:].T


class video_handler:
    """
    this class creates an opencv video capture module
    to get specific frames from provided video
    """
    # path to the provided video
    def __init__(self, video_path="data/pose3d_data/video.mkv"):
        """
        :param video_path: path to the video file to get frames from
        """
        self.cap = cv2.VideoCapture(video_path)

    def get_frame(self, frame_num):
        """
        function get frame number and reads that frame from the video
        :param frame_num: frame number
        :return: numpy array: RGB image width x height x 3
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        rat, frame = self.cap.read()
        return frame

    def release(self):
        """
        release the opencv capture
        """
        # at the end we need to release the capture module
        self.cap.release()


def calc_iou(bbox1, bbox2):
    """
    takes two boxes with the format of [xmin, ymin, xmax, ymax]
    and calculates intersection of union between them. min is 0 (no intersection) and max is 1 (when two boxes are same)
    :param bbox1: source bbox
    :param bbox2: target bbox
    :return: scalar  0=< iou <=1 : intersection of union of the two given boxes
    """
    xmin = np.max([bbox1[0], bbox2[0]])
    ymin = np.max([bbox1[1], bbox2[1]])
    xmax = np.min([bbox1[2], bbox2[2]])
    ymax = np.min([bbox1[3], bbox2[3]])

    if (xmax - xmin)< 0 or (ymax - ymin) < 0 : # width heights should be positive
        return 0
    area = (xmax - xmin) * ( ymax - ymin)
    iou = area / ((bbox1[2]-bbox1[0])*(bbox1[3]-bbox1[1]) + (bbox2[2]-bbox2[0])*(bbox2[3]-bbox2[1]))

    return iou
