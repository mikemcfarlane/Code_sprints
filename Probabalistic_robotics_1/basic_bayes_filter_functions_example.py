
""" A basic Bayes Filter example.
    A mobile robot estimates the state of a door.
    First coding attempt, break code out into functions, better data structure.

"""

__author__ = "Mike McFarlane mike@mikemcfarlane.co.uk"
__version__ = "Revision: ??"
__date__ = "Date: 18-04-14"
__copyright__ = "Copyright (c)Mike McFarlane 2014"
__license__ = "TBC"


def bayes_filter(bel_xt_1, ut, zt):
    """ Simple Bayes filter.
        Not implemented!
        
    """
    bel_prediction_xt = None
    bel_xt = normaliser * p_zt_xt * beliefPrediction_xt
    
    return bel_xt

def bayes_function_normaliser(*args):
    """Normalise the list of beliefs.
        Return the Bayes Rule normaliser, n.
    
    """
    n = 1 / sum(args)
    return n

def bel_predictor():
    """ Belief predictor.
    Not implemented!
    """
    pass


def main():
    """ Main.
    
    """
    # Probabilities defining this example.
    # p = probability, x = state, z = sensor measurement, u = manipulator action.

    # Initial belief, no prior knowledge so assumes equal probability.
    bel_xt_1_isOpen = 0.5
    bel_xt_1_isClosed = 0.5

    # Measurements z from sensor, assume noisy, so conditional probabilities,
    # when door is open,
    p_Zt_senseOpen_Xt_isOpen = 0.6
    p_Zt_senseClosed_Xt_isOpen = 0.4
    # and when door is closed,
    p_Zt_senseOpen_Xt_isClosed = 0.2
    p_Zt_senseClosed_Xt_isClosed = 0.8
    # ie robot is good at detecting when door is closed, but not so good when door open.

    # With actions u, if robot tries to open door,
    p_Xt_isOpen_Ut_push_Xt_1_isOpen = 1.0
    p_Xt_isClosed_Ut_push_Xt_1_isOpen = 0.0
    p_Xt_isOpen_Ut_push_Xt_1_isClosed = 0.8
    p_Xt_isClosed_Ut_push_Xt_1_isClosed = 0.2
    # or does nothing,
    p_Xt_isOpen_Ut_doNothing_Xt_1_isOpen = 1.0
    p_Xt_isOpen_Ut_doNothing_Xt_1_isClosed = 0.0
    p_Xt_isClosed_Ut_doNothing_Xt_1_isOpen = 0.0    
    p_Xt_isClosed_Ut_doNothing_Xt_1_isClosed = 1.0


    # Initial value for normaliser,
    n = 1.0
    
    print "\nArrive at door, is it open or closed?\n"
        
    # For hypothesis X1 = isOpen.
    bel_prediction_Xt_isOpen = (p_Xt_isOpen_Ut_doNothing_Xt_1_isOpen * bel_xt_1_isOpen) + \
                                (p_Xt_isOpen_Ut_doNothing_Xt_1_isClosed * bel_xt_1_isClosed)
    print "bel_prediction_X1_isOpen: ", bel_prediction_Xt_isOpen
    # For hypothesis X1 = isClosed.
    bel_prediction_Xt_isClosed = (p_Xt_isClosed_Ut_doNothing_Xt_1_isOpen * bel_xt_1_isOpen) + \
                                    (p_Xt_isClosed_Ut_doNothing_Xt_1_isClosed * bel_xt_1_isClosed)
    print "bel_prediction_X1_isClosed: ", bel_prediction_Xt_isClosed
    
    # Incorporate the measurement data, with normaliser equal 1.
    bel_Xt_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_Xt_isOpen
    print "bel_X1_isOpen (n=1): ", bel_Xt_isOpen
    bel_Xt_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_Xt_isClosed
    print "bel_X1_isClosed (n=1): ", bel_Xt_isClosed
    
    # Calculate the value of the normaliser
    n = bayes_function_normaliser(bel_Xt_isOpen, bel_Xt_isClosed)
    print "normaliser Xt: ", n
    
    # Recalculate incorporating measurement data, with normaliser.
    bel_Xt_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_Xt_isOpen
    print "bel_X1_isOpen (normalised): ", bel_Xt_isOpen
    bel_Xt_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_Xt_isClosed
    print "bel_X1_isClosed (normalised): ", bel_Xt_isClosed

    # Save bel_xt to bel_xt_1.
    bel_prediction_Xt_1_isOpen = bel_prediction_Xt_isOpen
    bel_prediction_Xt_1_isClosed = bel_prediction_Xt_isClosed
    bel_Xt_1_isOpen = bel_Xt_isOpen
    bel_Xt_1_isClosed = bel_Xt_isClosed
    # Initial value for normaliser,
    n = 1.0
        
    # Give the door a push ie iterate
    print "\nPush the door .....\n"
    # For hypothesis X2 = isOpen.
    bel_prediction_Xt_isOpen = (p_Xt_isOpen_Ut_push_Xt_1_isOpen * bel_Xt_1_isOpen) + \
                                    (p_Xt_isOpen_Ut_push_Xt_1_isClosed * bel_Xt_1_isClosed)
    print "bel_prediction_X2_isOpen: ", bel_prediction_Xt_isOpen
    # For hypothesis X2 = isClosed.
    bel_prediction_Xt_isClosed = (p_Xt_isClosed_Ut_push_Xt_1_isOpen * bel_Xt_1_isOpen) + \
                                    (p_Xt_isClosed_Ut_push_Xt_1_isClosed * bel_Xt_1_isClosed)
    print "bel_prediction_X2_isClosed: ", bel_prediction_Xt_isClosed
    
    # Incorporate the measurement data, with normaliser = 1.
    bel_Xt_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_Xt_isOpen
    print "bel_X2_isOpen (n new): ", bel_Xt_isOpen
    bel_Xt_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_Xt_isClosed
    print "bel_X2_isClosed (n new): ", bel_Xt_isClosed
    
    # Calculate the value of the normaliser
    n = bayes_function_normaliser(bel_Xt_isOpen, bel_Xt_isClosed)
    print "normaliser Xt: ", n
    
    # Recalculate incorporating measurement data, with normaliser.
    bel_Xt_isOpen = n * p_Zt_senseOpen_Xt_isOpen * bel_prediction_Xt_isOpen
    print "bel_X2_isOpen (normalised): ", bel_Xt_isOpen
    bel_Xt_isClosed = n * p_Zt_senseOpen_Xt_isClosed * bel_prediction_Xt_isClosed
    print "bel_X2_isClosed (normalised): ", bel_Xt_isClosed
    
    
if __name__ == "__main__":
    main()