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
import numpy as np
from expected_weight_module import expected_weight_class
from data_output_module import data_output_class

class facility_component_class:
    """
    This class will get inherited by most other classes used in fuel fabrication.

    All objects that inherit this will need to initialize this object as well with the initial amount
    of SNM weight the object is going to initially hold (this should almost always start off as zero) and
    a short description of the component (i.e. "fuel fabricator", "melter", "storage buffer", etc.)

    #######
    #  Variables
    #######
    expected_weight = module that handles different types of expected weight for each class.  It also holds
    several routines to help keep track of the expected weight during each different state variable change.

    data_output = module that handles data output for this class.  It creates a data output file and
    contains methods for writing important data to such.

    description = a name that will be used in differentiating this object from any others of its kind.
    This gets used in identification in the log file as well as naming the output file where data
    for the specific class is written.

    Object type = a string describing the object type.  Can be either "manager", "storage", "kmp", or "processor".
    Other methods utilize this in conditional statements.

    #######
    # Coding Notes  
    #######
    Note that if you don't want an object to have a data output file, simply pass "None" in for the output
    directory.
    """

    def __init__(self, expected_total_weight, expected_batch_weight, expected_residual_weight, 
            description, object_type, output_dir):
        self.expected_weight = expected_weight_class(expected_total_weight, 
                expected_batch_weight, expected_residual_weight)
        if output_dir != None:
            self.data_output = data_output_class(description, output_dir)
        self.description = description
        self.object_type = object_type

    def write_to_log(self,facility,message):
        """
        Write a message to the log file carried by the facility
        """
        facility.log_file.write(message)

    def write_to_debug(self,facility,message):
        """
        Separate file from log strictly for debugging purposes
        """
        facility.debugger.write(message)

    def increment_operation_time(self,facility,time_added):
        """
        This function increases the operation time by the desired amount indicated by time_added;
        it then logs the incremented operation time in the designated output file.

        inputs: facility class, amount of time to increase operation time (float)
        """
        facility.operation_time = facility.operation_time + time_added
        facility.system_time_output.write('%.4f\n'%(facility.operation_time))
        facility.system_info_output.write('%.4f\t%i\t%i\n'%(facility.operation_time,facility.total_campaign,
            facility.false_alarm_count))

    def check_equipment_failure(self,facility):
        """
        This method calculates the probability of an equipment failure by running the time through a cumulative
        distribution function from the Weibull distribution.

        Currently, beta (or k, depeding on who's syntax you use) is set to be 1.  That is the value
        used when the actual failure distribution is unknown, and then lambda (or eta) represents a general
        guess of the rate of failure (units of 1/days).

        Whether or not an actual failure occurs is determined by whether or not the calculated probability is 
        greater than a randomly selected number between 0-1 from a uniform distribution.
        
        #######
        # Return 
        #######
        True = Equipment did fail.  Need to run failure routine.

        False = Equipment did not fial.  The facility may continue to run as normal.


        
        *************DEVELOPER NOTES******************

        Any object that calls this method will need the attributes "time_of_last_failure"
        and "failure_rate".
        """
        #######
        # Initialize the boolean 
        #######
        did_fail = False
        #######
        # The time used to calculate the probability is the time that has passed since the last failure. 
        #######
        time = facility.operation_time - self.time_of_last_failure
        #######
        # The cumulative distribution function caclulated according to time 
        #######
        cdf = 1 - np.exp(-time * self.failure_rate)
        fail_check = np.random.rand()

        if cdf > fail_check:
            did_fail = True
            self.time_of_last_failure = facility.operation_time
            self.failure_count = self.failure_count + 1

        self.failure_data_output.failure_output(facility, self, cdf, fail_check)
        
        return did_fail

