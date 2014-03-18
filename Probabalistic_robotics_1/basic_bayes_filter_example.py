
""" A basic Bayes Filter example.
    A mobile robot estimates the state of a door.
    First coding attempt, linear code.

"""

__author__ = "Mike McFarlane mike@mikemcfarlane.co.uk"
__version__ = "Revision: ??"
__date__ = "Date: 18-04-14"
__copyright__ = "Copyright (c)Mike McFarlane 2014"
__license__ = "TBC"


# Probabilities defining this example.
# p = probability, x = state, z = sensor measurement, u = manipulator action.

# Initial belief, no prior knowledge so assumes equal probability.
bel_X0_isOpen = 0.5
bel_X0_isClosed = 0.5

# Measurements z from sensor, assume noisy, so conditional probabilities,
# when door is open,
p_Zt_senseOpen_Xt_isOpen = 0.6
p_Zt_senseClosed_Xt_isOpen = 0.4
# and when door is closed,
p_Zt_senseOpen_Xt_isClosed = 0.2
p_Zt_senseClosed_Xt_isClosed = 0.8
# ie robot is good at detecting when door is closed, but not so good when door open.

# With actions u, if robot tries to open door,
p_Xt_isOpen_Ut_push_Xt_1_isOpen = 1
p_Xt_isClosed_Ut_push_Xt_1_isOpen = 0
p_Xt_isOpen_Ut_push_Xt_1_isClosed = 0.8
p_Xt_isClosed_Ut_push_Xt_1_isClosed = 0.2
# or does nothing,
p_Xt_isOpen_Ut_doNothing_Xt_1_isOpen = 1
p_Xt_isClosed_Ut_doNothing_Xt_1_isOpen = 0
p_Xt_isOpen_Ut_doNothing_Xt_1_isClosed = 0
p_Xt_isClosed_Ut_doNothing_Xt_1_isClosed = 1

# Initial value for normaliser,
n = 1.0


def bayes_filter(bel_xt_1, ut, zt):
    """ Simple Bayes filter.
    
    """
    bel_prediction_xt = None
    bel_xt = normaliser * p_zt_xt * beliefPrediction_xt
    
    return bel_xt


def main():
    """ Main.
    
    """
    # Declare n as global as needs modified.
    global n
    
    print "\nArrive at door, is it open or closed?\n"
        
    # For hypothesis X1 = isOpen.
    bel_prediction_X1_isOpen = (p_Xt_isOpen_Ut_doNothing_Xt_1_isOpen * bel_X0_isOpen) + \
                                (p_Xt_isOpen_Ut_doNothing_Xt_1_isClosed * bel_X0_isClosed)
    print "bel_prediction_X1_isOpen: ", bel_prediction_X1_isOpen
    # For hypothesis X1 = isClosed.
    bel_prediction_X1_isClosed = (p_Xt_isClosed_Ut_doNothing_Xt_1_isOpen * bel_X0_isOpen) + \
                                    (p_Xt_isClosed_Ut_doNothing_Xt_1_isClosed * bel_X0_isClosed)
    print "bel_prediction_X1_isClosed: ", bel_prediction_X1_isClosed
    
    # Incorporate the measurement data, with normaliser equal 1.
    bel_X1_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_X1_isOpen
    print "bel_X1_isOpen (n=1): ", bel_X1_isOpen
    bel_X1_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_X1_isClosed
    print "bel_X1_isClosed (n=1): ", bel_X1_isClosed
    
    # Calculate the value of the normaliser
    n = 1 / (bel_X1_isOpen + bel_X1_isClosed)
    print "normaliser X1: ", n
    
    # Recalculate incorporating measurement data, with normaliser.
    bel_X1_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_X1_isOpen
    print "bel_X1_isOpen (normalised): ", bel_X1_isOpen
    bel_X1_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_X1_isClosed
    print "bel_X1_isClosed (normalised): ", bel_X1_isClosed
    
    # Give the door a push ie iterate
    print "\nPush the door .....\n"
    # For hypothesis X2 = isOpen.
    bel_prediction_X2_isOpen = (p_Xt_isOpen_Ut_push_Xt_1_isOpen * bel_X1_isOpen) + \
                                (p_Xt_isOpen_Ut_push_Xt_1_isClosed * bel_X1_isClosed)
    print "bel_prediction_X2_isOpen: ", bel_prediction_X2_isOpen
    # For hypothesis X2 = isClosed.
    bel_prediction_X2_isClosed = (p_Xt_isClosed_Ut_push_Xt_1_isOpen * bel_X1_isOpen) + \
                                    (p_Xt_isClosed_Ut_push_Xt_1_isClosed * bel_X1_isClosed)
    print "bel_prediction_X1_isClosed: ", bel_prediction_X2_isClosed
    
    # Incorporate the measurement data, with normaliser = 1.
    n = 1
    bel_X2_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_X2_isOpen
    print "bel_X2_isOpen (n new): ", bel_X2_isOpen
    bel_X2_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_X2_isClosed
    print "bel_X2_isClosed (n new): ", bel_X2_isClosed
    
    # Calculate the value of the normaliser
    n = 1 / (bel_X2_isOpen + bel_X2_isClosed)
    print "normaliser X2: ", n
    
    # Recalculate incorporating measurement data, with normaliser.
    bel_X2_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_X2_isOpen
    print "bel_X2_isOpen (normalised): ", bel_X2_isOpen
    bel_X2_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_X2_isClosed
    print "bel_X2_isClosed (normalised): ", bel_X2_isClosed
    
    
if __name__ == "__main__":
    main()