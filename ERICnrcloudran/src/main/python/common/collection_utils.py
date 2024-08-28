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

import json

import urllib3
from urllib3 import exceptions

from . import constants as constants
from .log import NrCranLogger
from .nrcloudran_cli import NrCranCli
from .nrcloudran_exception import ExecuteQueryException, \
    CreateCollectionException, CreateTopologyException, \
    GetNodeNamesException, GetCollectionByNameException, \
    GetChildrenException, \
    UpdateCollectionException, DeleteException, \
    NrCranException, generate_error_message
from .rest_service import RestService
from .sso_manager import SsoManager

urllib3.disable_warnings(exceptions.InsecureRequestWarning)


class CollectionUtils(object):

    def __init__(self):
        self.rest_services = RestService()
        self.sso = SsoManager()
        self.log = NrCranLogger()
        self.cli_error = False
        self.nrcloudran_cli = NrCranCli()

    def get_children(self, parent_id):
        endpoint = constants.CUSTOM_TOPOLOGY_V1
        if parent_id != '':
            endpoint = endpoint + '?parentId=' + str(parent_id)

        collection_response = self.rest_services.get(endpoint)
        collections = json.loads(collection_response.text)
        if collection_response.status_code != 200:
            message = generate_error_message(collections, endpoint)
            raise GetChildrenException(parent_id, message)

        return collections

    def get_custom_topology(self, name):
        endpoint = constants.CUSTOM_TOPOLOGY_V1 + '?customTopology=true'

        topology_response = self.rest_services.get(endpoint)

        topologies = json.loads(topology_response.text)
        if topology_response.status_code != 200:
            message = generate_error_message(topologies, endpoint)
            raise GetCollectionByNameException(name, message)

        collection = None
        for topology in topologies:
            if name in topology['name']:
                collection = topology
                break
        return collection

    def get_collection_by_name(self, name):
        endpoint = constants.COLLECTIONS_V2 + '?collectionName=' + str(name)
        response = self.rest_services.get(endpoint)
        collection = json.loads(response.text)
        if response.status_code != 200:
            message = generate_error_message(collection, endpoint)
            raise GetCollectionByNameException(name, message)
        else:
            if 'collections' in collection and collection['collections']:
                collection = collection['collections'][0]
            else:
                collection = None

        return collection

    def create_leaf_collection(self, name, parent_id, objects):
        endpoint = constants.COLLECTIONS_V4
        leaf_params = {
            'name': name,
            'sharing': 'public',
            'parentIds': [parent_id],
            'type': 'leaf',
            'isCustomTopology': 'false',
            'contents': objects
        }
        self.log.info('Uploading ' + name)
        self.log.info('URL: ' + endpoint)
        create_response = self.rest_services.post(endpoint, leaf_params)

        collection = json.loads(create_response.text)

        if create_response.status_code == 409:
            self.log.info("NR-CRAN script failed to create " +
                          "collection, collection name {0} in use".format(
                              name))
            collection = self._handle_duplicate_collection(parent_id, name)
        elif create_response.status_code != 201:
            message = generate_error_message(collection, endpoint)
            raise CreateCollectionException(name, message)

        return collection

    def _handle_duplicate_collection(self, parent_id, name):
        collection = self.get_collection_by_name(name)
        if collection:
            self.delete_collection(collection['id'])
            collection = self.create_leaf_collection(name, parent_id)
        else:
            raise NrCranException("NR-CRAN script unable to find "
                                  "collection {0}".format(name))
        return collection

    def create_topology(self, name):
        endpoint = constants.CUSTOM_TOPOLOGY_V1
        nr_cran_params = {
            'name': str(name),
            'isCustomTopology': 'true',
            'isSystemCreated': 'true'
        }

        create_response = self.rest_services.post(endpoint, nr_cran_params)
        create_response = json.loads(create_response.text)
        if "id" in create_response:
            self.log.info("NR-CRAN script created {0} Topology".format(name))
        else:
            message = generate_error_message(create_response, endpoint)
            raise CreateTopologyException(name, message)

        return create_response

    def update_collection(self, collection_id, objects):
        endpoint = constants.COLLECTIONS_V1 + '/' + str(collection_id)
        objects = [{"id": "%s" % p} for p in objects]
        update_collection = self.rest_services.put(
            endpoint, {"objects": objects})
        update_response = json.loads(update_collection.text)
        if update_collection.status_code != 200:
            message = generate_error_message(update_response, endpoint)
            raise UpdateCollectionException(collection_id, message)
        return update_response

    def delete_collection(self, collection_id):
        endpoint = constants.CUSTOM_TOPOLOGY_V1 + '/' + str(collection_id)
        delete_response = self.rest_services.delete(endpoint)
        if delete_response.status_code == 404:
            endpoint = constants.COLLECTIONS_V1 + '/' + str(collection_id)
            delete_response = self.rest_services.delete(endpoint)

        if delete_response.status_code not in [200, 204]:
            collection_deleted = json.loads(delete_response.text)
            message = generate_error_message(collection_deleted, endpoint)
            raise DeleteException(collection_id, message)
        else:
            self.log.info("NR-CRAN script: collection deleted with the "
                          "given id {0}".format(collection_id))

    def delete_topology(self, topology_id):
        endpoint = constants.CUSTOM_TOPOLOGY_V1 + '/' + str(topology_id)
        if topology_id:
            delete_request = self.rest_services.delete(endpoint)
            if delete_request.status_code not in [200, 204]:
                response = json.loads(delete_request.text)
                message = generate_error_message(response, endpoint)
                raise DeleteException(topology_id, message)

    def execute_query(self, query):
        endpoint = constants.MO_SEARCH_V2 + '?query=' + query
        node_response = self.rest_services.get(endpoint)
        text = json.loads(node_response.text)
        if node_response.status_code != 200:
            message = generate_error_message(text, endpoint)
            if "Invalid MO type " in message:
                self.log.warn("Query Failed for Shared-CNF neType," +
                              "Please Run RI on the nodes")
                node_response = []
            else:
                print(node_response.text)
                raise ExecuteQueryException(query, message)

        node_response = [n['id']
                         for n in text.get('objects', [])]
        return node_response

    def get_node_names(self, nodes):
        endpoint = constants.MO_GET_POS_BY_POID
        node_list = CollectionUtils._get_node_list(nodes)
        name_to_poid_list = {}
        for batch in node_list:
            enodeb_response = self.rest_services.post(endpoint,
                                                      {"poList": batch})

            enodeb_details = json.loads(enodeb_response.text)
            if enodeb_response.status_code != 200:
                message = generate_error_message(enodeb_details, endpoint)
                raise GetNodeNamesException(message)

            for managed_object in enodeb_details:
                name_to_poid_list[managed_object['fdn']] = \
                    managed_object['id']

        return name_to_poid_list

    def _handle_duplicate_branch_collection(self, parent_id, name):
        self.log.info("In the Handle Duplicate Branch")
        collection = self.get_collection_by_name(name)
        if collection:
            self.delete_branch_collection(collection['id'])
            collection = self.create_branch_collection(name, parent_id)
        else:
            raise NrCranException("NR-CRAN script unable to find "
                                  "collection {0}".format(name))
        return collection

    def delete_branch_collection(self, collection_id):
        endpoint = constants.COLLECTIONS_V4 + '/' + str(collection_id)
        delete_response = self.rest_services.delete(endpoint)
        if delete_response.status_code == 404:
            endpoint = constants.COLLECTIONS_V1 + '/' + str(collection_id)
            delete_response = self.rest_services.delete(endpoint)

        if delete_response.status_code not in [200, 204]:
            collection_deleted = json.loads(delete_response.text)
            message = generate_error_message(collection_deleted, endpoint)
            raise DeleteException(collection_id, message)
        else:
            self.log.info("NR-CRAN script: collection deleted with the "
                          "given id {0}".format(collection_id))

    def create_branch_collection(self, name, parent_id):
        endpoint = constants.CUSTOM_TOPOLOGY_V1 + "/" + str(parent_id)
        leaf_params = {
            'name': str(name),
            'type': 'BRANCH',
            'category': 'Public',
            'isSystemCreated': 'true'
        }
        create_response = self.rest_services.post(endpoint, leaf_params)
        collection = json.loads(create_response.text)
        self.log.info(collection)
        if create_response.status_code == 409:
            self.log.info("NR-CRAN script failed to create " +
                          "collection, collection name {0} in use".format(
                              name))
            collection = self. \
                _handle_duplicate_branch_collection(parent_id, name)

        elif create_response.status_code != 201:
            message = generate_error_message(collection, endpoint)
            raise CreateCollectionException(name, message)

        return collection

    @staticmethod
    def _split(list_to_split, number_of_splits):
        quotient, remainder = divmod(len(list_to_split), number_of_splits)

        return (
            list_to_split[i * quotient + min(i, remainder):
                          (i + 1) * quotient + min(i + 1, remainder)]
            for i in range(number_of_splits)
        )

    @staticmethod
    def _get_node_list(node_list):
        if len(list(node_list)) > 250:
            return CollectionUtils._split(
                node_list, (int(len(node_list) / 125)))
        return [node_list]

    def get_nr_cran_relations_via_cli(self, name_poid, ru_poids, rdm_poids):
        relationships = self.nrcloudran_cli.get_relationships(name_poid,
                                                              ru_poids,
                                                              rdm_poids)
        self.cli_error = self.nrcloudran_cli.cli_error
        return relationships
