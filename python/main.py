#
#
#
import numpy as np


if __name__=='__main__':


    init = 132
    money = init
    r = 0.05
    total = (30 * 24) //15
    for i in range(total):
        money += money * r


    print (" rev: ", money)
    # print( "monthly: " (money - init)/money  )

