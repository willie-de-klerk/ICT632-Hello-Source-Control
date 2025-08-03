#!/usr/bin/python

# Copyright: (c) 2025, Willie de Klerk <willie@williedeklerk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: eigrp_classic

short_description: Calculate the eigrp metric value for a given path. 

version_added: "1.0.0"

description: 
    This module has the primary goal of computing the eigrp classic metric value for a given path, with user specified 
    path attributes, and optional Coefficients (K) value definitions, with the default K values specified as stated in RFC 7868 p.53. 
    The calculation is performed on the target ansible-host that you specify.  
    
options:
     
    K1: 
        description: (Bandwidth def_val 1) Used to allow path selection to be based on the bandwidth available along the path (Throughput-based path selection). RFC7868 pp. 39 
        required: false
        type: integer
    
    K2: 
        description: (Load def_val 0) If used, the effect of congestion as a measure of load, reported by the interface will be used to simulate the "available Throughput" by adjusting the maximum Throughput. RFC7868 pp. 39
        required: false
        type: integer
        
    K3: 
        description: (Delay def_val 1) Used to allow for delay or latency-based path selection. RFC7868 pp. 39
        required: false
        type: integer
    K4: 
        description: (Reliability def_val 0) RFC7868 pp. 39
        required: false
        type: integer
    
    K5: 
        description: (Reliability def_val 0) The handling of K5 is conditional, if K5 is equal to 0, then reliability quotient is defined to be 1. RFC7868 pp. 39
        required: false
        type: integer
    
    BW: 
        description: (Bandwidth) The lowest interface bandwidth along the path in bits per second. 
        required: true
        type: integer
    
    DELAY:
        description: The sum of all outbound interface delays along the path. 
        required: true
        type: integer
    
    LOAD:
        description: Only measured at the time a link changes. Represented by a value between 1 and 255. 127/255 = 50% link saturation. 
        required: false
        type: integer
    
    REL:
        description: (Reliability) It is only measured at the time a link changes. Represented by a value between 1 and 255. 245/255 = 95% reliable link. 
        required: false
        type: integer

      
 '''

EXAMPLES = '''

'''


RETURN = '''

'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # Defining available arguments/parameters that a user can pass to the module
    module_args = dict (
     K1=dict(type='int', required=False, default=1)
     , K2=dict(type='int', required=False, default=0)
     , K3=dict(type='int', required=False, default=1)
     , K4=dict(type='int', required=False, default=0)
     , K5=dict(type='int', required=False, default=0)
     , BW=dict(type='int', required=True)
     , DELAY=dict(type='int', required=True)
     , LOAD=dict(type='int', required=False, default=1)
     , REL=dict(type='int', required=False, default=1)
    )

    result = dict(changed=False, metric_value='',)

    # Creating an object named 'module', that is going to be based of the imported class AnsibleModule.
    # This object will serve as an abstraction layer used to work with Ansible.

    module= AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # If check mode is specified we don't want to run the calculation on the target host, but just return the current state with no modifications.
    if module.check_mode:
        module.exit_json(**result)


    # Getting to run the actual calculation for classic metrics
    #                            RFC 7868 p. 42
    # metric = 256 * ({(K1*BW) + [(K2*BW)/(256-LOAD)] + (K3*DELAY)} * (K5/(REL+K4)))
    # Delay needs to be divided by 10, and if K5 - 0
    if module.params['K5'] == 0:
        result['metric_value'] = module.run_command(f'K1={module.params['K1']}; K2={module.params['K2']}; K3={module.params['K3']}; K4={module.params['K4']}; K5={module.params['K5']}; BW={module.params['BW']}; DELAY={module.params['DELAY']}; LOAD={module.params['LOAD']}; REL={module.params['REL']}; echo -n $((256 * ((K1 * (10^7/BW))  + ((K2*BW)/(256-LOAD))   + (K3*(DELAY/10)) *1 )  )) ' ,use_unsafe_shell=True)
    else:
        result['metric_value'] = module.run_command(
            f'K1={module.params['K1']}; K2={module.params['K2']}; K3={module.params['K3']}; K4={module.params['K4']}; K5={module.params['K5']}; BW={module.params['BW']}; DELAY={module.params['DELAY']}; LOAD={module.params['LOAD']}; REL={module.params['REL']}; echo -n $((256 * ((K1 * (10^7/BW))  + ((K2*BW)/(256-LOAD))   + (K3*(DELAY/10)) * (K4/(K5+REL)) )  )) ',
            use_unsafe_shell=True)
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
