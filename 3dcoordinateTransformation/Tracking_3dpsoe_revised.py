#
#
#
from utils import *

"""
processing data and reconstructing player position in the soccer field
"""

# load generated data contains 2d, 3d poses, bboxes and frame numbers
tracking_bboxs = np.load("data/tracking_bbox_kpoints_2d_3d_forTest.npy", allow_pickle=True )
#load camera parameters --
cam_params = np.load("data/single_test_cam_params.npy", allow_pickle='TRUE')
# datapr = video_handler()
#
# the sizes will used for rescaling
frame_size = [3840, 2160] # size of the video frame
model_size = [640, 360] # size of the 3d model input in which calibration have been done

# two camera classes were defined; one for image to camera transformation
world2cam = camera(w=frame_size[0], h=frame_size[1])
# camera class for model to camera transformation
model2cam = camera(w=frame_size[0],h=frame_size[1])
# ----

# list to keep reconstructed data
tracking_3d_converted_world_coordinate = []

# iterating over collected track data frame by frame
for idx, frameix in enumerate(tracking_bboxs[0]['frame_num']):
    # idx: counts iteration, frameix: frame index
    ## --------------------------------------< Part one: loading data> --------------------------------------------------
    local_id = tracking_bboxs[0]['player_id'][idx] # get local id of the player (detection id of player at the frame frameix)
    # read camera parameters of the frame
    # Rotation angles: rx_pixel, ry_pixel, rz_pixel (in Rodrigues format)
    # translation: tx_pixel: along x-axis, ty_p# intrinsic parameters for virtual model cam
    rx_pixel, ry_pixel, rz_pixel, tx_pixel, ty_pixel, tz_pixel, fx_pixel, fy_pixel, cx_pixel, cy_pixel  = cam_params[0][frameix][0:-1]

    # ---------------<Part two: set image to camera coordinate camera parameters to compute projection matrix> ---------
    # rescaling the intirinsic parameters (rescale to video size)
    fx_pixel *= (frame_size[0]/model_size[0]) # keeping scales in pixels
    fy_pixel *= (frame_size[1]/model_size[1])
    cx_pixel *= frame_size[0]/model_size[0]
    cy_pixel *= frame_size[1]/model_size[1]
    # ----------------------------------------------------------------------------------------------------
    # calculating image to camera rotation matrix from given components: rx_pixel: ry_pixel, rz_pixel
    # use Rodrigues formula to compute rotation matrix(for simplicity) # another is Euler's
    rmat, jac = cv2.Rodrigues( np.array([rx_pixel, ry_pixel, rz_pixel]) ) # this returns rotation matrix and jacobian (not going to be used here)
    # RQ decomposition of rmat matrices and keep only the rotation component
    _, mtxR, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    #------------------------------------------------------------------------------------------------------
    # create intrinsic part of the projection matrix using focal length and camera center note: P = A [R|T] here A is set
    # by this projection matric we can transfor 2d image to 3d camera coordinate
    A = create_intrinsic_matrix(fx_pixel, fy_pixel, cx_pixel, cy_pixel )
    # setting A (intrinsic in the corresponding camera object)
    world2cam.set_intrinsics(A)
    # set rotation and translation part of the projection matrix [R|T]
    world2cam.set_extrinsics(mtxR, np.array([tx_pixel, ty_pixel, tz_pixel]).reshape(3,1))
    # load 2d keypoints in image plane
    kpts_2d = tracking_bboxs[0]['kpt'][idx]
    #
    camera_apkpt_3d = world2cam.unproject( kpts_2d, 1) # points in camera coordinates [x, y, depth]

    # calculate projection error
    # reproj_2d, depth = world2cam.project( camera_apkpt_3d )


    # -------------------------------------< Part three: move from camera coordinates to target coordinate>-------------

    # --------------<calculating projection matrix to the projected pitch plane (world view or target coordinate)> -----
    #  this part requires some more computations to minimize errors (not completed)

    # -------------------------------------< Part four: calculating player depth using normalized 3d joints> -------------
    # load 3d joints (model output -- in normalized form)
    kpts_3d = tracking_bboxs[0]['kpt3d'][idx]
    #
    kpts_3d = (kpts_3d + [1, 1, 1])/2. # negetive values lead to instability, shifting the coordinates to the positive side +1
    #
    # intrinsic parameters for virtual model camera looks to normalized 3d pose
    # basically this will create the intrinsic matrix equal to identity for simplicity
    fx_ndc = 1 # focal length x
    fy_ndc = 1 # focal length y
    cx_ndc = 0.05 # came center x close to zero
    cy_ndc = 0.05 # cam center y
    # create intrinsic matrix from the above parameters (Note: these parameters manually set to simulate nonexisting camera)
    model2cam_mtx = create_intrinsic_matrix ( fx_ndc , fy_ndc, cx_ndc, cy_ndc)
    # set A to P = A[R|T] : for this virtual camera R = identical matrix and T is zero
    model2cam.set_intrinsics( model2cam_mtx )
    # Vector of distortion coefficients used in solvePnP (zero array for here)
    dist_matrix = np.zeros((4, 1), dtype=np.float64)
    #
    """
    Using PnP algorithm of opencv, I match the model 3D pose with the reconstructed pose for the player pose depth:   
    dist_matrix: distortion is zero
    model2cam_mtx: identity for simplicity (drop the need for RQ decomposition)
    camera_apkpt_3d[:,:2]: [x, y] in camera coord.
    kpts_3d: [x_m, y_m, z_m] in model coord.
    
    outputs: 
    rot_vec: rotation vector (Rodrigues)
    trans_vec: translation vector 
    """
    success, rot_vec, trans_vec = cv2.solvePnP( kpts_3d, camera_apkpt_3d[:,:2], model2cam_mtx, dist_matrix)
    # rotation vector to rotation matrix
    rmat, _ = cv2.Rodrigues(rot_vec)
    # rmat is actually contains camera intrinsic matrix, RQ decomposition takes out the R from projection (K*R) matrix
    # but here no need to decomposition as intrinsic is close to identity
    # _, mtxR, _, _, _, _ = cv2.RQDecomp3x3(rmat) # decompose projection matrix - not required
    #
    # calculating homography matrix for 3D-to-3D (affine) projection from model to world coordinate
    # it is enough to calculate [R|T]
    n_points = kpts_3d.shape[0]
    # all we need is to rotate and translate the 3d pose keypoints
    world_apkpt_2d = rmat.dot(kpts_3d.T) + np.tile(trans_vec, (1, n_points))
    #
    # calculating the transformation error from model tp camera
    reprojError = np.linalg.norm(camera_apkpt_3d[:,1] - world_apkpt_2d[1,:]/world_apkpt_2d[2,:]) + np.linalg.norm(camera_apkpt_3d[:,0] - world_apkpt_2d[0,:]/world_apkpt_2d[2,:])
    # checking reprojection error and remove cases with large error (optimal threshold can be calculated based on data)
    print("3d model reprojection error: ", reprojError )
    if reprojError>100: # threshold is 400 just in case
        continue

    # adding depth to the calculated coordinates using 3D pose coordinates from pose estimation model
    camera_apkpt_3d[:,2] += world_apkpt_2d[2,:] - world_apkpt_2d[2,:].min()

    # switching the Y and Z axis in the camera coordinates for representation
    tmp = -camera_apkpt_3d[...,1].copy()
    camera_apkpt_3d[...,1] = camera_apkpt_3d[...,2]
    camera_apkpt_3d[...,2] = tmp - np.min(tmp) # this helps to reduce error
    #
    # Add points to the list for representation.
    tracking_3d_converted_world_coordinate.append(  {frameix: camera_apkpt_3d} )


np.save("data/tracking_3d_converted_world_coordinate.npy", tracking_3d_converted_world_coordinate)

print('finished!')















