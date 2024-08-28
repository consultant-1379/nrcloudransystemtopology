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
import sys
import os

from common.collection_utils import CollectionUtils
from common.log import NrCranLogger
from common.nrcloudran_exception import NrCranException
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class SystemTopologyCreator(object):

    def __init__(self, topology_id):
        self.topology_id = topology_id
        self.collection_utils = CollectionUtils()
        self.log = NrCranLogger()
        self.completed_without_errors = True

    def delete_topology(self):
        """ Invalid Conditions for NR-CRAN, the topology_id
            and collections will be removed.
        """
        if self.topology_id:
            try:
                for instance in self.collection_utils.\
                        get_children(self.topology_id):
                    self.collection_utils.delete_collection(instance['id'])
                self.collection_utils.delete_topology(self.topology_id)
                self.log.info("NR-CRAN Systems Topology and Collections "
                              "deleted successfully")
            except NrCranException as exc:
                self.log.warn("NR-CRAN failed to delete NR-CRAN topology, "
                              "Cause: {0}".format(str(exc)))
        else:
            self.log.info("No Topology to be deleted")

    def process_cran_relationships(self, relationships):
        for vcucp in relationships:
            vcucp_collection_response = self.collection_utils. \
                create_branch_collection(vcucp, self.topology_id)
            vcucp_collection_id = vcucp_collection_response['id']
            for vdu in relationships[vcucp]:
                vdu_name = vdu.replace('/', '-')
                self.collection_utils.create_leaf_collection(
                    vdu_name, vcucp_collection_id,
                    list(relationships[vcucp][vdu]))
