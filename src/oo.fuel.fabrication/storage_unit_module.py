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
from facility_component_module import facility_component_class
from edge_transition_module import edge_transition_class
from storage_buffer_module import storage_buffer_class
from key_measurement_point_module import key_measurement_point_class as kmp_class

class storage_unit_class(facility_component_class):
    """
    The storage unit is a managing unit that bundles a storage buffer with a key measurement point.
    """

    def __init__(self,facility):
        self.measured_inventory = 0
        self.edge = edge_transition_class(facility,0)
        self.initial_inventory = facility.initial_inventory
        self.storage_buffer = storage_buffer_class(facility, self.initial_inventory)
        self.kmp = kmp_class(facility,0)
        facility_component_class.__init__(self, 0, 0, 0, "first storage unit", "manager")

    def batch_preparation(self,facility):
        """
        The storage unit gets a batch from the storage buffer, passes it through the key measurement point,
        then updates the known amount of materials left in the storage buffer.
        """
        batch = self.storage_buffer.batch_preparation(facility)
        self.edge.edge_transition(facility, self.storage_buffer, self.kmp)
        self.kmp.process_batch(facility,batch)
        self.kmp.update_measured_inventory(facility, self.storage_buffer, "subtract")

        return batch

    def inspect(self):
        self.expected_weight.erase_expectations()
        self.expected_weight.add_weight(self.storage_buffer)
        self.expected_weight.add_weight(self.kmp)
        self.measured_inventory = self.storage_buffer.measured_inventory