########################################################################
# Malachi Tolman
# @tolman42
# rev.27.February.2016
########################################################################
#
# See class description
#
########################################################################
#
# Imports
#
########################################################################
import numpy as np
import global_vars
from facility_component_module import facility_component_class
from edge_transition_module import edge_transition_class
from key_measurement_point_module import key_measurement_point_class as kmp_class
from melter_module import melter_class
from trimmer_module import trimmer_class
from recycle_storage_module import recycle_storage_class

class fuel_fabricator_class(facility_component_class):
    """
    The fuel fabricator is the final stage of the pyroprocessor.
    It takes in a batch of U and TRU, melts them in with zirconium,
    injects the entire melted alloy into a quartz crucible, let's the
    metal cool, and then breaks the quartz mold in order to produce metal
    slugs of SNM (special nuclear material).
   
    However, some of the SNM gets left behind in the melting process each
    time, which slowly accumulates into a "heel".  Eventually, the heel
    builds up so much, that the key measurement points (KMP's) detect a 
    large enough discrepancy between what's been processed and what's
    supposed to be there and initiate a system alarm.
    
    If the alarm is triggered, then the melter is cleaned, and the heel
    is accounted for and sent to the recycle storage facility to get 
    processed.

    Currently, the melter is set to be the only component that can experience an equipment failure.
    If this happens, the batch and heel are sent to the recycle storage, then put together in one
    batch to be processed as normal.  In the mean time, operation time is lost while the melter undergoes
    maintenance.
    """


    def __init__(self,facility):
        """
        The fabricator initializes all of the objects that are its own constituents.  That includes the melter,
        trimmer, recycle storage, four kmp's, and the edge transitions between such.

        The expected batch and heel weights are changed everytime a component that changes those state variables
        processes a batch.  Like the facility getting passed from component to component to account for the
        overall state variables, so does the fuel fabricator get passed into a number of classes to indicate
        that it monitors the activities for those and accounts for such in its system.
        """
        self.new_batch_weight = np.loadtxt(facility.process_states_dir+'/batch.inp')
        self.expected_melter_loss = np.loadtxt(facility.process_states_dir+ \
                '/melter.loss.fraction.inp',usecols=[1])[0] \
                #Amount of material the personnel expect the melter to lose each time it processes a batch
        self.expected_batch_weight = 0
        self.expected_heel_weight = 0

        self.edge = edge_transition_class(facility,0)
        self.kmp = []
        for n in range(4):
            self.kmp.append(kmp_class(facility,n))
        self.melter= melter_class(facility)
        self.trimmer = trimmer_class(facility)
        self.recycle_storage = recycle_storage_class(facility)


    def process_batch(self,facility,batch):
        """
        See the class description
        """
        #######
        # Initialize the expected batch weight with how much weight is known to come from the storage buffer 
        #######
        self.expected_batch_weight = self.new_batch_weight
        self.kmp[0].process_batch(facility,batch,self.expected_batch_weight)
        self.edge.edge_transition(facility)
        #######
        # When the melter processes a batch,
        # it returns a boolean to indicate whether it
        # experienced an equpiment failure or not
        #######
        self.write_to_debug(facility,'About to melt\nexpected batch weight is %f\n'%(self.expected_batch_weight))
        if self.melter.process_batch(facility,self,batch):
            self.equipment_failure(facility,batch)
        self.write_to_debug(facility,'Successful melting\nexpected batch weight is %f\n'%(self.expected_batch_weight))
        self.edge.edge_transition(facility)
        self.kmp[1].process_batch(facility,batch,self.expected_batch_weight)
        self.edge.edge_transition(facility)
        self.trimmer.process_batch(facility,batch)
        self.edge.edge_transition(facility)
        self.kmp[2].process_batch(facility,batch,self.expected_batch_weight)

    def equipment_failure(self,facility,batch):
        """
        The routine that occurs when the melter fails.  The batch is sent to the recycle storage, then the heel
        is cleaned and sent to recycle storage, both are recycled into one batch, and then that batch gets
        sent back into the normal process.
        """
        did_fail = True
        while did_fail:
            self.write_to_debug(facility,'Melter failed\nexpbw is %f\n'%(self.expected_batch_weight))
            self.write_to_log(facility,
                    'Melter failed at time %.4f, begin failure routine\n\n'%(facility.operation_time))
            self.edge.edge_transition(facility)
            self.kmp[3].process_batch(facility,batch,self.expected_batch_weight)
            self.edge.edge_transition(facility)
            heel = self.melter.clean_heel(facility)
            self.edge.edge_transition(facility) 
            self.kmp[3].process_batch(facility,heel,self.expected_heel_weight)
            self.edge.edge_transition(facility)
            self.melter.repair(facility)
            self.recycle_storage.process_batch(facility,self,batch,heel)
            self.edge.edge_transition(facility)
            self.kmp[3].process_batch(facility,batch,self.expected_batch_weight)
            self.edge.edge_transition(facility)
            self.write_to_debug(facility,'Recycled batch\nexpbw is %f\n'%(self.expected_batch_weight))
            did_fail = self.melter.process_batch(facility,self,batch)
            self.write_to_debug(facility,'melted in fail routine\nexpbw is %f\n'%(self.expected_batch_weight))
