#!/usr/bin/env python
####################################################################
# COPYRIGHT Ericsson AB 2022
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
####################################################################
from __future__ import print_function

import os
import sys
from common.nrcloudran_exception import NrCranException, DeleteException
from topologies.system_topologies.system_topology_creator import \
    SystemTopologyCreator
from topologies.topology import Topology
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class NrCloudRanTopology(Topology):

    def __init__(self):
        Topology.__init__(self, os.path.dirname(os.path.abspath(__file__)))
        self.relationships = None

    def run(self):
        try:
            start = datetime.now()
            self._generate_relationships()
        except NrCranException as error:
            # pylint: disable=C0325
            print(error)
            print('NR-CRAN Topology has failed to process')
            self.log.exception(error)
            return

        try:
            topology_id = self._get_nrcran_topology_id("NR-CLOUD-RAN")
            self.log.info("Completed GetID for NR-CRAN TOPOLOGY")

            self._clean_nrcran_topology(topology_id)
            self.log.info("Completed CLEAN of NR-CRAN TOPOLOGY")

            topology_creator = SystemTopologyCreator(topology_id)

            if not self.relationships:
                self.log.error(
                    "NR-CRAN topology not created due to" +
                    " missing relationships")
                topology_creator.delete_topology()
            else:
                topology_creator.process_cran_relationships(self.relationships)
                if self.collection_utils.cli_error:
                    warning_message = "NR-CRAN topology completed with " \
                                      "warnings, please check the log at " \
                                      "/opt/ericsson/nrcloudransystemtopo" \
                                      "logy/log/nrcran_log for more details"
                    self.log.info(warning_message)
                    print(warning_message)
                else:
                    success_message = "NR-CRAN topology completed " \
                                      "successfully."
                    self.log.info(success_message)
                    print(success_message)
        except DeleteException as error:
            self.log.exception(error)
            print("NR-CRAN script failed to delete duplicate topology. "
                  "Please delete the topology and run the script again.")
        finally:
            finish = datetime.now()
            time_taken = finish - start
            print("NR-CRAN took: " + str(time_taken) + " to process")
            self.log.info("NR-CRAN took: " + str(time_taken) + " to process")

    def _generate_relationships(self):
        function_poids = self.collection_utils.execute_query(
            self.constants['queries']['get_GNBCUCPFunctions'])

        function_poids += self.collection_utils.execute_query(
            self.constants['queries']['get_GNBDUFunctions'])

        radio_c2_poids = self.collection_utils.execute_query(
            self.constants['queries']['get_c2_radionode'])

        rdm_c2_poids = self.collection_utils.execute_query(
            self.constants['queries']['get_c2_shared-cnf'])

        fdn_poids = {}
        if function_poids:
            fdn_poids = self.collection_utils.get_node_names(function_poids)

        radio_poids = {}
        if radio_c2_poids:
            radio_poids = self.collection_utils.get_node_names(radio_c2_poids)

        rdm_poids = {}
        if rdm_c2_poids:
            rdm_poids = self.collection_utils.get_node_names(rdm_c2_poids)

        self.log.info(radio_poids)
        self.log.info(rdm_poids)

        self.relationships = self.collection_utils \
            .get_nr_cran_relations_via_cli(fdn_poids, radio_poids, rdm_poids)

    def _get_nrcran_topology_id(self, name):
        topology = self.collection_utils.get_custom_topology(name)
        if topology:
            if NrCloudRanTopology.is_system_nr_created(topology):
                return topology['id']
            else:
                self.collection_utils.delete_topology(topology['id'])
        return self.collection_utils.create_topology(name)['id']

    @staticmethod
    def is_system_nr_created(topology):
        return 'userId' not in topology or topology['userId'] is None

    def _clean_nrcran_topology(self, top_id):
        """There will only ever be 2 layers of Children Here"""
        for child in self.collection_utils.get_children(top_id):
            # Check for more children
            if child:
                for inner in self.collection_utils.get_children(child['id']):
                    if inner:
                        self.collection_utils.delete_collection(inner['id'])
                self.collection_utils.delete_branch_collection(child['id'])
