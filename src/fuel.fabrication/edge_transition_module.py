########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.23.October.2015
########################################################################
# 
# Edge transitions occur between each vertex.
# State variables do not change on the edges.
# 
########################################################################
#
# imports
#
########################################################################
#
# function list
#
# (1): edge transition
#
########################################################################
#
#
#
########################################################################
#
#
# (1): edge transition
#
#######

from facility_component_module import facility_component_class
from facility_vars_module import facility_vars_class as facility_vars

class edge_transition_class(facility_component_class):

    def edge_transition(self,facility_vars,edge_time_delay):

        self.write_to_log(facility_vars,'Edge transition \n\n')
        self.increment_operation_time(facility_vars,edge_time_delay)

########################################################################
#
# EOF
#
########################################################################
