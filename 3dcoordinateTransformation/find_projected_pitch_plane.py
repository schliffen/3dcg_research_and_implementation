#
#
#
"""
An Intro script for the consept of plane reconstruction and coordinate transformation.
this processes are prone to errors, and here I am trying to explain the base of the consept.

"""
import math
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import cv2
np.random.seed(7)
#
def compare_two_sample(sa, sb):
    if np.squeeze(sa["loss"])> np.squeeze(sb["loss"]):
        return 1
    else:
        return 0


class find_projected_pitch_plane:
    """
    This class is very simple (introductory) implementation of an algorithm to
    find the plane from noisy data
    In short, randomly generate plane normals and try to pick the best generated and continue iteration in the
    mean direction of nest performed ones
    """
    def __init__(self, max_iter = 100, num_samples = 100, num_best_keep = 10, loss_func_exp_size = 20 ):
        # set arguments here
        self.max_iter = max_iter # stop after 100 iterations
        self.num_samples = num_samples
        self.num_best_keep = num_best_keep
        self.loss_func_exp_size = loss_func_exp_size # number of points to check in loss calculation
        self.num_samples = num_samples # number of generating random samples

    #
    def sort_candidate(self, random_candids_):
        """
        sorting list of dictionaries based on loss value
        :param random_candids_: list of doctionaries which includes normal candid and loss of that normal candid
        :return: sorted list ordered by increasing loss value (minimum loss on top)
        """
        sorted_candidate = [random_candids_[0]]
        # a fast sorting algorithm
        for item1 in random_candids_[1:]:
            # comparing the item to locate in ordered
            i=0
            numcomares = len(sorted_candidate) # limit number of iteration only to the size of prev. elements in list
            while i< numcomares:
                # check from top one-by-one
                if compare_two_sample( sorted_candidate[i], item1):
                    sorted_candidate.insert(i, item1)
                    break
                i+=1
                # if item1's loss is bigger that the list content, add it to the last
                if i== numcomares:
                    sorted_candidate.append(item1)
                    break

        return sorted_candidate

    #
    def calculate_loss(self, vector_samples):
        """
        method for calculating loss of candid normals
        loss in computed by selecting lines in the plane and calculating the inner product with the condid normal
        plus considering the angle difference with initial normal (penalize inverse directions whoes inner products are also zero)
        :param vector_samples: list of dictionaries includes randomly generated normal vectors
        :return: list of dictionaries includes randomly generated normal vectors with filled loss key
        """

        # everytime randomly select pair of points and calculate the loss
        average_loss = 0
        for tvector in vector_samples:
            if tvector["loss"]>0: continue
            vec = tvector["normal"].reshape(1,-1)
            ip=0
            while ip < self.loss_func_exp_size:
                idx = np.random.randint(0, len(noisy_points), 2)
                # select a closed line in plane and normalize it
                v1 = (noisy_points[idx[1]] - noisy_points[idx[0]]).reshape(1,-1)/ np.linalg.norm(noisy_points[idx[1]] - noisy_points[idx[0]])
                # check out v1 vctor -> sometimes due to wrong points selection we may have null value
                v1norm = np.linalg.norm(v1)
                # remove wrong vector selections
                if np.isclose(v1norm,0) or np.isnan(v1norm):
                    continue
                # add inner product of closed line in plane with candid normal to the loss
                tvector["loss"] += np.squeeze(np.abs(vec.dot(v1.T)) )

                ip+=1

            # sometimes falls into problem solve it by multiplying to .999
            theta = math.acos( .999*vec.dot(self.init_normal_vector.T) )  *180./ math.pi
            # control the normal direction and if its inverse penalize it
            if theta>90:
                tvector["loss"] += 10 # penalizing opposite direction

            average_loss += np.squeeze(tvector["loss"])

        return vector_samples, average_loss/len(vector_samples)

    #
    def generate_random_candid(self, top_performance):
        """
        This method is for generating random normal candidates
        normal are created in the confidence interval of the best performers
        :param top_performance: list of dictionaries containing high performed normals with least loss
                                 At the beginning this has one element
        :param num_samples: number of random samples to be generated
        :return tstd std of the best performance
        :return: list of dictionaries containing random normals


        """

        # get mean and std of top performance vectors
        guide_vectors = top_performance.copy()
        # calculate the variance of top sample
        vectxyz = []
        for vect in guide_vectors:
            vectxyz.append(list(np.squeeze(vect["normal"])))
        #
        tstd = np.std(np.array(vectxyz), axis=0)
        # at the beginning increase diversity
        if len(top_performance)==1: # at the begining or when variance locked
            tmean =  np.squeeze(guide_vectors[0]["normal"])
            xc = np.random.uniform(tmean[0] - .56* tmean[0], tmean[0] + .56* tmean[0], self.num_samples)  # at the begining take high variance
            yc = np.random.uniform(tmean[1] - .56* tmean[1], tmean[1] + .56* tmean[1], self.num_samples)  #
            zc = np.random.uniform(tmean[2] - .56* tmean[2], tmean[2] + .56* tmean[2], self.num_samples)  #
            for i in range(self.num_samples- 1):
                cn = np.array([xc[i], yc[i], zc[i]]).reshape(1,-1)
                top_performance.append({"loss":0, "normal": cn/np.linalg.norm(cn) })
                tstd += 1
        else:
            # generating random samples as structured format and add it to the list
            for i in range(self.num_samples - self.num_best_keep):
                rind = np.random.randint(0, self.num_best_keep)
                tvec = np.squeeze(guide_vectors[rind]["normal"])
                # basically use best sample variance
                xc = np.random.uniform(tvec[0] - 2.6*tstd[0]/np.sqrt(self.num_samples), tvec[0] + 2.6*tstd[0]/np.sqrt(self.num_samples))  # 95% confidence and increase diversity
                yc = np.random.uniform(tvec[1] - 2.6*tstd[1]/np.sqrt(self.num_samples), tvec[1] + 2.6*tstd[1]/np.sqrt(self.num_samples))  # 95% confidence and increase diversity
                zc = np.random.uniform(tvec[2] - 2.6*tstd[2]/np.sqrt(self.num_samples), tvec[2] + 2.6*tstd[2]/np.sqrt(self.num_samples))  # 95% confidence and increase diversity
                cn = np.array([xc, yc, zc]).reshape(1,-1)
                top_performance.append({"loss":0, "normal": cn/norm(cn) })

        return top_performance, tstd

    #
    def get_initial_vector(self, points_on_plane):
        """
        Method for creating initial guess for plane normal by averaging some created normals
        by existing points on the plane
        :param points_on_plane: list of points in the plane (noisy)
        :return: a normal vector
        """
        # create an initial normal
        # Note: this initial normal is very important (the direction)
        # select 5 random triple points
        init_normal_vector = np.zeros((1,3))
        i=0
        while i<= 5:
            indx = np.random.randint(0,len(points_on_plane), 3)
            # create normal from the selected pair of points
            v1 = points_on_plane[indx[1]] - points_on_plane[indx[0]]
            v2 = points_on_plane[indx[2]] - points_on_plane[indx[0]]
            n1 = np.cross(v1, v2) # this should be parallel to plane normal

            if np.isclose(norm(n1),0): # in case selected points are not good to go
                continue

            init_normal_vector += n1 # add toghether
            if i >= 1:
                na = n1/np.linalg.norm(n1)
                nb = init_normal_vector/np.linalg.norm(init_normal_vector)
                # the angle between normals shouldnt be more than 90 degrees (remove oposite direction)
                theta = math.acos( .999* na.dot(nb.T)  )  *180./ math.pi # mult by .999 to refuse math domain error
                # as expected angles are close to 0 or 180
                if theta>90:
                    continue
            i+=1

        # normalize
        self.init_normal_vector = init_normal_vector/ norm(init_normal_vector)



    def find_plane(self, points_on_plane):
        """
        Method to estimate plane normal using class methods
        :return: best found plane normal
        """
        init_normal_vector = self.get_initial_vector(points_on_plane)

        # initialize random candids
        random_candids, avgstd = self.generate_random_candid(  [{"loss":0, "normal": self.init_normal_vector}])

        # searching for plane normal
        for iter in range(self.max_iter):

            # calculate loss
            random_candids_, average_loss = self.calculate_loss( random_candids )

            # sorting the candidates based on loss
            sorted_samples = self.sort_candidate(random_candids_)

            print("------------------------------------------------")

            print(" iteration: ", iter,  "| variance: ", avgstd.mean() , " | average_loss: ", average_loss, " | best loss: ", sorted_samples[0]["loss"] )
            # stop if std of best become small enough
            if avgstd.mean() < .005:
                break

            # keep first 10 and use them as guid
            random_candids, avgstd = self.generate_random_candid( sorted_samples[:self.num_best_keep] )

        return np.squeeze(sorted_samples[0]["normal"])



if __name__=="__main__":
    """
    Here the goal is: 
    1- creat a grountruth plane, 
    2- select some points on it 
    3- add noise to points 
    4- reconstruct the plane from noisy points
    5- select a new coordinate origin on the plane
    6- transform plane points to the new coordinate
    7- visualize the results
    
    <This is very similar to what we are facing with reconstructing the pitch plane and transform coordinate>
    
    """

    # generate plane with plane formula (p-p0).n=0
    # get plane normal
    n = np.array([1.2, 2.1, 1.5])
    n = n/np.linalg.norm(n)
    # a point on the plane
    p0 = np.array([2.4,1.67, .5])

    # visualize the plane
    # a plane is a*x+b*y+c*z+d=0
    # [a,b,c] is the normal. Thus, we have to calculate
    # d and we're set
    d = -p0.dot(n.T)# dot product
    #
    # create meshgrid in x and y axis
    xx, yy = np.meshgrid(range(30), range(30))

    # calculate corresponding z
    zz = (-n[0]*xx - n[1]*yy - d)*1./n[2]

    # ------------------------------------------------------
    # this would be target plane and we are going to reconstruct it using
    # selecting some random noisy points on the plane

    points_on_plane = []
    for i in range(10):
        x1 = 10 * np.random.random()
        y1 = 10 * np.random.random()
        z1 = (-n[0]*x1 - n[1]*y1 - d)*1./n[2]

        points_on_plane.append([x1,y1,z1])
    points_on_plane = np.array(points_on_plane)

    # --------------
    # adding noise to the points
    noisy_points = []
    for point in points_on_plane:
        xyz = point +  np.random.randn(1,3)
        noisy_points.append(list(xyz[0]))
    noisy_points = np.array(noisy_points)

    # -------------------------------------
    # estimate plane normal from the noisy points
    plane_processor = find_projected_pitch_plane()
    best_plane_normal = plane_processor.find_plane( noisy_points )

    # how close is the computation:
    print("Estimation Error: ", norm(best_plane_normal-n))

    # --------------------------------------------
    # transforming the coordinate
    """
    Assuming we have the projected pitch plane normal
    We are going to calculate the points coordinates wrt new coordinates in the target plane.
    
    for this I will get a points on the plane, and a line in the plane.
    To simulate the condition in the pitch case, then move coordinate to that points so that X axis 
    be parallel to the line (same direction), y axis parallel to the plane normal (same direction)
    """

    # point to move to (new center):
    d = -p0.dot(best_plane_normal.T)
    xo = -1.
    yo = -1.
    zo = ( -best_plane_normal[0]*xo - best_plane_normal[1]*yo - d)*1./best_plane_normal[2]

    # line direction
    l = (points_on_plane[3] -  points_on_plane[4])/np.linalg.norm(points_on_plane[3] -  points_on_plane[4])

    # starting points for line
    l0 = points_on_plane[5]

    # Now calculating [R|T] from current coordinate to the new coordinate

    # translation simply can be calculated as:
    T = np.array([0 - xo , 0 - yo, 0 - zo ]) # the current origin is [0, 0, 0]

    # R is constructed as follows
    yb = best_plane_normal # y plane is at the same direction with plane normal
    xb = l # x axis at the same dir with l
    zb = np.cross(yb, xb) # now z axis should be cross product (taking care of the direction)
    R = np.vstack((np.vstack((xb, yb)), zb))

    # visualizing ground truth plane and points
    bluep = points_on_plane[8,:] # a sample points on the plane
    plt3d = plt.figure().gca(projection='3d')
    plt3d.plot_surface(xx,yy,zz, color='cyan')
    plt3d.scatter(xo,yo,zo, color='red')
    plt3d.scatter(bluep[0], bluep[1], bluep[2], color="blue")
    plt.savefig("results/plane_and_points.png")
    # plt.show()

    # -------------
    # transfor blue points and p0
    newbluep = np.matmul(R, bluep) + T
    newp0 = np.matmul(R, p0) + T

    # transformation error in transforming p0 (Expecting to be on plane)
    trError = (newbluep-newp0).dot(best_plane_normal.T)

    # transforming the plane -----
    # re-calculate corresponding z based on new normal
    zz = (-best_plane_normal[0]*xx - best_plane_normal[1]*yy - d)*1./best_plane_normal[2]
    # reshaping meshgrid
    zz1 = zz.reshape(1,-1)
    yy1 = yy.reshape(1,-1)
    xx1 = xx.reshape(1,-1)
    # put toghether
    pp = np.vstack((np.vstack((xx1, yy1)),zz1))
    # rotate meshgrid
    newpp = np.matmul(R, pp)
    # translate meshgrid
    newpp[0] += T[0]
    newpp[1] += T[1]
    newpp[2] += T[2]

    # Visualize the transformed plane and points
    plt3d = plt.figure().gca(projection='3d')
    plt3d.plot_surface(newpp[0].reshape(30,30),newpp[1].reshape(30,30),newpp[2].reshape(30,30), color='cyan')
    plt3d.scatter(newbluep[0], newbluep[1], newbluep[2], color="blue")
    plt3d.scatter(newp0[0], newp0[1], newp0[2], color="red") # translated origin NOTE: cam not rendered, need to use OpenGL
    plt.savefig("results/plane_on_transfered_coordinate.png")
    # plt.show()

    """
    Explanation:
    as it can be seen, due to errors in reconstruction of the plane and transformation, blue point does not 
    lie in the plane anymore!
     
    """

print( "finished! " )


