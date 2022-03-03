
I have already processed data and saved them as npy to ease the process
data is stored in data/ folder:
the structure is as follows:
 
 root_ 
      |--- data/
      |--- results/
      |--- Tracking_3dpsoe.py
      |--- save_results_and_visualization.py
      |--- utils.py
      |--- prepare_data.py
      |--- find_projected_pitch_plane.py		
 	  
 * to generate tracking data: python3 Tracking_3dpsoe.py 
 * to generate gif : python3 simple_visualization.py 
 

Explanation: Inside the "Tracking_3dpsoe.py" I implemented the 3D reconstruction from the given 2D 
             camera plane to the world coordinate using the provided camera parameters.
             first 2D coordinates in  projected back to the world coordinates;  
             This is done in unprojected function inside the camera class 
             Now to calculate the depth I used the 3D poses of the same player. Using PnP to calculate the 
             projection between the 3d pose and the projected pose in world coordinates, and then I used the 
             calculated parameters to calculate the depth of the poses.

             This is a very simple solution to the reconstruction problem. 

             Later I did a postprocessing on the collected trackes to smooth the movements of the body poses
             
             I must add that there could be tracking errors nd misses and etc. in this case we can use interpolation to make 
             the body motion smooth 



             I used prepare_data.py to collect the tracks and process the provided data

             For details please refer to the scripts.		
