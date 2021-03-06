########################################################################
# Malachi Tolman
# @tolman42
# 18.February.2016
########################################################################
#
# This class contains methods that essentially ever component of the
# facility will use.  All of them will inherit this class, it's just
# an easier way of getting methods written that one would have to write 
# several times otherwise.
#
########################################################################
#
# Imports
#
import numpy
from facility_vars_module import facility_vars_class as facility_vars

class facility_component_class:
    """
    This class will get inherited by most other classes used in fuel fabrication.
    """

    def write_to_log(self,facility_vars,message):
        facility_vars.log_file.write(message)

    def increment_operation_time(self,facility_vars,time_added):
        """
        This function increases the operation time by the desired amount indicated by time_added;
        it then logs the incremented operation time in the designated output file.

        inputs: facility class, amount of time to increase operation time (float)
        """
        #print 'funtion called, \noperation time is %.4f\ntime to add is %.4f\n'%(facility_vars.operation_time,time_added)
        facility_vars.operation_time = facility_vars.operation_time + time_added
        facility_vars.system_time_output.write('%.4f\n'%(facility_vars.operation_time))
        facility_vars.campaign_output.write('%.4f\t%i\n'%(facility_vars.operation_time,facility_vars.total_campaign))
        #print 'operation time is now %.4f\n\n'%(facility_vars.operation_time)
        
