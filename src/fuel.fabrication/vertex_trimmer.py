########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.23.October.2015
########################################################################
# 
# Trimmer vertex 
# 
########################################################################
#
# Then metal alloy rods fabricated by injection casting are trimmed into fuel slugs.
# Quartz molds are loaded into the equipment.
# The molds are then sheared to the right size for the slugs. 
# Quartz molds are broken to obtain the metal slugs.
# Broken molds are a waste stream. 
# Sheared metal produces 'fines'; i.e., the process loss.
# These fines have to be recovered for materials accounting.
#
########################################################################
#
# Many failures could occur during this process.
# No failures assumed. 
#
########################################################################
#
# imports
#
import numpy 
from facility_component_module import facility_component_class
from facility_vars_module import facility_vars_class as facility_vars
#
########################################################################
#
# function list
#
# (1): slug trimming
#
########################################################################
#
#
#
########################################################################
#
# (1): slug trimming
# 
#######

class trimmer_class(facility_component_class):

    def slug_trimming(self,facility_vars,equipment_failure_time_0,equipment_failure_time_1,delay_time,true_quantity,expected_quantity,equipment_failure_number,equipment_failure_type,equipment_failure_rate,equipment_loss_fraction,accumulated_true_equipment_loss,accumulated_expected_equipment_loss,equipment_failure_event,equipment_failure_counter,equipment_counter,log_file):
    #######
        #print 'Slug trimming'
        self.write_to_log(facility_vars,'Slug trimming\n')
        #gv.self.write_to_log('Slug trimming')
        self.increment_operation_time(facility_vars,operation_time+0.5*delay_time)
        equipment_failure_time_0=equipment_failure_time_0+0.5*delay_time
        equipment_failure_time_1=equipment_failure_time_1+0.5*delay_time
        equipment_counter=equipment_counter+1
    #
        true_equipment_loss=(equipment_loss_fraction[1]-equipment_loss_fraction[2])*numpy.random.random_sample()+equipment_loss_fraction[2] 
        expected_equipment_loss=equipment_loss_fraction[0]
    #
        true_quantity=true_quantity-true_equipment_loss
        expected_quantity=expected_quantity-expected_equipment_loss
    #
        accumulated_true_equipment_loss=accumulated_true_equipment_loss+true_equipment_loss
        accumulated_expected_equipment_loss=accumulated_expected_equipment_loss+expected_equipment_loss   
    ###
    #
    # failure module
    # 
    # failure testing at 0.5 delay time
    # if no failure rest of delay time is added
    # if failure then failure times occur
    #
    ###
        if(equipment_failure_event==False):
	        self.increment_operation_time(facility_vars,operation_time+0.5*delay_time)
	    equipment_failure_time_0=operation_time+0.5*delay_time
	    equipment_failure_time_1=operation_time+0.5*delay_time
    # end if
        #print 'Failure status: ',equipment_failure_event,'\n\n'
        self.write_to_log(facility_vars,'Failure status: %s\n\n'%(equipment_failure_event))
    ###
        return(facility_vars.operation_time,equipment_failure_time_0,equipment_failure_time_1,true_quantity,expected_quantity,accumulated_true_equipment_loss,accumulated_expected_equipment_loss,equipment_failure_event,equipment_failure_counter,equipment_counter)
########################################################################
#
# EOF
#
########################################################################
