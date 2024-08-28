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
import os
import sys

from lib.nrcran_parser import CmeditGetOutputParser
from . import constants
from .log import NrCranLogger
from .nrcloudran_exception import CMEditException

import enmscripting
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class NrCranCli(object):

    def __init__(self):
        # no params needed for enmscripting when executing in scp
        self.session = enmscripting.open(None, None, None)
        self.terminal = self.session.terminal()
        self.log = NrCranLogger()
        self.cli_error = False
        self.fdn_poid_map = []
        self.rdm_c2_poids = {}
        self.radio_c2_poids = {}
        self.mo_count = 0
        self.node_count = 0
        self.namepairs = {}

    def get_relationships(self, fdn_to_poids, radio_c2_poids, rdm_c2_poids):
        """Return List of Relationship objects
        """
        self.rdm_c2_poids = rdm_c2_poids
        self.radio_c2_poids = radio_c2_poids
        self.fdn_poid_map = fdn_to_poids

        self.log.info("Starting CM CLI Commands")

        return \
            self._run_cmcli_queries(
                constants.CLI_GET_DU_FUNCTION_AGG,
                constants.
                CLI_GET_DU_RADIONODE_ATTRIBUTES,
                constants.
                CLI_GET_CUCP_GNBID_FUNCTION_AGG,
                constants.CLI_GET_C2_AGG,
                constants.
                CLI_GET_CUCP_TERMPOINTTOGNBDU_AGG)

    def _run_cmcli_queries(self, vdu_query, radionode_query, cucp_query,
                           c2_query, termpoint_query):

        du_node_list = self._parse_du_attributes(self._get_nodes_attribute(
            vdu_query))
        self.log.info(du_node_list)

        du_node_list += self._parse_du_attributes(self._get_nodes_attribute(
            radionode_query), True)

        cucp_dict = self._parse_cucp_attributes(self._get_nodes_attribute(
            cucp_query))

        ru_dict = self._parse_ru_attributes(self._get_nodes_attribute(
            c2_query))

        term_point_dict = self._parse_termpointtognbdu_attributes(
            self._get_nodes_attribute(termpoint_query))

        return self._build_node_relationships(du_node_list,
                                              cucp_dict,
                                              ru_dict,
                                              term_point_dict)

    def _get_c2_poids(self, fdn, ru_dict):
        """Get the FDNs of the SectorEquipmentFunction"""
        poid_list = []
        if fdn in ru_dict:
            sector_fdns = ru_dict[fdn]
            for sector_equipment_fdn in sector_fdns:
                if sector_equipment_fdn in self.rdm_c2_poids:
                    poid_list.append(
                        self.rdm_c2_poids[sector_equipment_fdn])
                else:
                    radio_node_c2_fdn = \
                        self._get_name_from_fdn(
                            sector_equipment_fdn)
                    if radio_node_c2_fdn in self.radio_c2_poids:
                        poid_list.append(
                            self.radio_c2_poids[radio_node_c2_fdn])
        return poid_list

    @staticmethod
    def _get_name_from_fdn(fdn):
        managed_element_key = "ManagedElement="
        name_of_node = ''
        if managed_element_key in fdn:
            index_of_managed_element = fdn.find(managed_element_key)
            fdn_key = fdn[index_of_managed_element::]
            if ',' in fdn_key:
                index_of_comma = fdn_key.find(',')
                name_of_node = fdn_key[0: index_of_comma:]
        return name_of_node

    def _parse_du_attributes(self, du_response, is_radio_node=False):
        """Parse DU's cli output data to usable list of
        dictionaries
        """
        dunode_list = []
        if self.__cm_cli_error_check(du_response, 'Error 1055'):
            self.log.warn('Please run RI on this Node Type')
        else:
            self.log.info(du_response)
            dict_value = {}
            du_nodes = CmeditGetOutputParser(du_response)
            du_nodes = du_nodes.parse()
            for du_name, attributes in du_nodes.items():
                self.node_count += 1
                self.log.info(attributes)
                for du_fdn in attributes:
                    if not self.__cm_cli_error_check(attributes[du_fdn],
                                                     'Error 9999'):
                        self.mo_count += 1
                        value = {}
                        value['FDN'] = du_fdn
                        self.log.info(du_name)
                        self.log.info(du_fdn)
                        if is_radio_node:
                            value['Name'] = str(du_name + ' / ' +
                                                attributes[du_fdn][
                                                    'gNBDUId'])
                        else:
                            value['Name'] = str(du_name + ' - ' +
                                                attributes[du_fdn][
                                                    'gNBDUId'])
                        value['gNBDUId'] = attributes[du_fdn]['gNBDUId']
                        dict_value[attributes[du_fdn]['gNBId']] = value
                        dunode_list.append(dict_value)
                        dict_value = {}
        return dunode_list

    def _parse_cucp_attributes(self, cucp_response):
        """Parse CUCP's CLI output into a usable dictionary"""
        cucp_dict = {}
        if self.__cm_cli_error_check(cucp_response, 'Error 1055'):
            self.log.warn('Please run RI on this Node Type')
        else:
            cucp_nodes = CmeditGetOutputParser(cucp_response)
            cucp_nodes = cucp_nodes.parse()
            for cucp_node_name, attributes in cucp_nodes.items():
                self.node_count += 1
                for cucp_node_fdn in attributes:
                    if not self.__cm_cli_error_check(attributes[cucp_node_fdn],
                                                     'Error 9999'):
                        self.mo_count += 1
                        cp_name = str(cucp_node_name + ' - ' +
                                      attributes[cucp_node_fdn]['gNBId'])
                        if attributes[cucp_node_fdn]['gNBId'] not in cucp_dict:
                            cucp_dict[attributes[cucp_node_fdn]['gNBId']] = {}
                        if cp_name not in \
                                cucp_dict[attributes[cucp_node_fdn]['gNBId']]:
                            cucp_dict[attributes[cucp_node_fdn][
                                'gNBId']][cp_name] = []
                        cucp_dict[attributes[
                            cucp_node_fdn]['gNBId']][cp_name] \
                            .append(cucp_node_fdn)
        return cucp_dict

    def _parse_ru_attributes(self, ru_response):
        """Parse DU's cli output data to usable list of
        dictionaries
        """
        ru_node_dict = {}
        if self.__cm_cli_error_check(ru_response, 'Error 1055'):
            self.log.warn('Please run RI on this Node Type')
        else:
            sector_str = 'sectorEquipmentFunctionRef'
            ru_nodes = CmeditGetOutputParser(ru_response)
            ru_nodes = ru_nodes.parse()
            for _, attributes in ru_nodes.items():
                self.node_count += 1
                for ru_node_fdn in attributes:
                    if not self.__cm_cli_error_check(attributes[ru_node_fdn],
                                                     'Error 9999'):
                        self.mo_count += 1
                        sector_ref = attributes[ru_node_fdn][sector_str]
                        if sector_ref:
                            fdn_key = self._split_fdn(ru_node_fdn,
                                                      ",NRSectorCarrier=")
                            if fdn_key not in ru_node_dict:
                                ru_node_dict[fdn_key] = []
                            ru_node_dict[fdn_key].append(sector_ref)
        return ru_node_dict

    def _parse_termpointtognbdu_attributes(self, term_point_response):
        """Parse TermPointToGNBDU's CLI output into a usable dictionary"""
        term_point_dict = {}
        gnbduid_dict = CmeditGetOutputParser(term_point_response)
        gnbduid_dict = gnbduid_dict.parse()
        for _, attributes in gnbduid_dict.items():
            for node_fdn in attributes:
                if not self.__cm_cli_error_check(attributes[node_fdn],
                                                 'Error 9999'):
                    self.mo_count += 1
                    cp_function_fdn = self._split_fdn(node_fdn,
                                                      ",TermPointToGNBDU=")
                    if cp_function_fdn not in term_point_dict:
                        term_point_dict[cp_function_fdn] = []
                    term_point_dict[cp_function_fdn] \
                        .append(attributes[node_fdn]['gNBDUId'])
        # Flatten Dictionary To Produce List of GNBDUID's against
        # GNBCUCPFunction fdn
        return term_point_dict

    def _split_fdn(self, fdn, key):
        fdn_key = fdn
        if key in fdn:
            index_of_attributes = fdn.find(key)
            fdn_key = fdn[0: index_of_attributes:]
        return fdn_key

    def _get_nodes_attribute(self, cmd):
        """Execute Cli command and return cli output
        """
        try:
            node_attribute = self.terminal.execute(cmd)
            if any('Error' in block for block in node_attribute.get_output()):
                cli_error = [block for block in node_attribute.get_output() if
                             'Error' in block]
                self.log.warn(
                    "Cli returned this error: {0}".format(cli_error))
        except Exception as error:
            raise CMEditException(cmd, str(error))

        return '\n'.join(node_attribute.get_output())

    def _build_node_relationships(self, du_node_list, cucp_dict, ru_dict,
                                  term_point_dict):
        """Compare Keys in cu_node_list and du_node_list
        and merge into one dictionary"""
        relationships = {}
        for du_gnb_dict in du_node_list:
            for gnb_id, gnb_id_values in du_gnb_dict.items():
                if gnb_id in cucp_dict:
                    self.__process_gnb(gnb_id_values, cucp_dict[gnb_id],
                                       term_point_dict, ru_dict, relationships)
        self.log.info("NR-CRAN Processed Nodes: {}".format(self.node_count))
        self.log.info("NR-CRAN Processed MOs: {}".format(self.mo_count))
        self.__process_duplicate_collection_name(relationships)
        return relationships

    # pylint: disable=R0913
    def __process_gnb(self, gnb_id_values, cucp_dict_items, term_point_dict,
                      ru_dict, relationships):
        du_name = gnb_id_values['Name']
        du_fdn = self._split_fdn(gnb_id_values['FDN'], ",attributes=")
        gnb_du_id = gnb_id_values['gNBDUId']
        for cp_name, cp_values in cucp_dict_items.items():
            for cp_fdn_with_attributes in cp_values:
                cu_fdn = self._split_fdn(cp_fdn_with_attributes,
                                         ",attributes=")
                if cu_fdn in term_point_dict and gnb_du_id in \
                        term_point_dict[cu_fdn]:
                    self.__store_duplicate_names(du_name, cp_name)
                    # set default will create {} if it doesn't exist,
                    # otherwise return the existing dict
                    relationships.setdefault(cp_name, {})
                    relationships[cp_name][du_name] = \
                        self.__build_po_fdn_set(cp_name, cu_fdn, du_fdn,
                                                du_name, ru_dict,
                                                relationships)

    # pylint: disable=R0913
    def __build_po_fdn_set(self, cp_name, cu_fdn, du_fdn, du_name, ru_dict,
                           relationships):
        po_fdn_set = set()
        if du_name not in relationships[cp_name]:
            relationships[cp_name][du_name] = []
        else:
            po_fdn_set.update(relationships[cp_name][du_name])
        if ' - ' in du_name:
            po_fdn_set.add(self.fdn_poid_map[du_fdn])
        else:
            ru_name = self._get_name_from_fdn(du_fdn)
            if ru_name in self.radio_c2_poids:
                po_fdn_set.add(self.radio_c2_poids[ru_name])
        po_fdn_set.add(self.fdn_poid_map[cu_fdn])
        c2_poids = self._get_c2_poids(du_fdn, ru_dict)
        if c2_poids:
            po_fdn_set.update(c2_poids)
        return po_fdn_set

    def __store_duplicate_names(self, du_name, cp_name):
        if du_name not in self.namepairs:
            self.namepairs[du_name] = []
        self.namepairs[du_name].append(cp_name)

    def __process_duplicate_collection_name(self, relationships):
        for du_name, cp_name_list in self.namepairs.items():
            for cp_name in cp_name_list:
                if len(self.namepairs[du_name]) > 1:
                    du_new_name = du_name + " - " + cp_name
                    relationships[cp_name][du_new_name] = \
                        relationships[cp_name][du_name]
                    self.log.info('Duplicate collection name found, '
                                  'renaming from: ' +
                                  du_name + ' to: ' + du_new_name)
                    del relationships[cp_name][du_name]

    def __cm_cli_error_check(self, object_to_test, error_code):
        if error_code in object_to_test:
            if type(object_to_test) is str:
                self.log.warn('Error returned by CLI: {0}'
                              .format(object_to_test))
            else:
                self.log.warn('Error returned by CLI: {0}'
                              .format(object_to_test[error_code]))
            self.cli_error = True
            return True
        else:
            return False
