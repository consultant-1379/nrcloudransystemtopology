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
LOGIN_ENDPOINT = '/login'
LOGOUT_ENDPOINT = '/logout'
MO_SEARCH_V2 = '/managedObjects/search/v2'
MO_GET_POS_BY_POID = '/managedObjects/getPosByPoIds'
CUSTOM_TOPOLOGY_V1 = '/object-configuration/custom-topology/v1'
COLLECTIONS_V3 = '/object-configuration/collections/v3'
COLLECTIONS_V2 = '/object-configuration/collections/v2'
COLLECTIONS_V1 = '/object-configuration/v1/collections'
PROPERTIES_FILE_PATH = '/ericsson/tor/data/global.properties'
TOPOLOGY_RELATIONSHIPS_V1 = '/topology-relationship-service/rest/' \
                                        'v1/relation/getRelations'
SERVICE_REGISTRY_URL = 'http://serviceregistry:8500/v1/kv/enm/deprecated/' \
                       'global_properties/web_host_default?raw'
EXCEPTION_MSG = ', exception: '
# NR-CLOUD RAN
COLLECTIONS_V4 = "/object-configuration/collections/v4"

CLI_GET_DU_RADIONODE_ATTRIBUTES = 'cmedit get * ' \
                                'GNBDUFunction.(gNBDUId,gNBId)' \
                                '--neType=RadioNode'

# Aggregated Queries After Delivery of
CLI_GET_CUCP_GNBID_FUNCTION_AGG = 'cmedit get * ' \
                                         'GNBCUCPFunction.gNBId' \
                                         ' --neType=Shared-CNF'
CLI_GET_DU_FUNCTION_AGG = 'cmedit get * ' \
                                 'GNBDUFunction.(gNBDUId,gNBId)' \
                                 '--neType=Shared-CNF'
CLI_GET_C2_AGG = 'cmedit get * NrSectorCarrier' \
                        '.sectorEquipmentFunctionRef --neType=Shared-CNF'
CLI_GET_CUCP_TERMPOINTTOGNBDU_AGG = 'cmedit get * ' \
                                            'TermPointToGNBDU.gNBDUId'\
                                            ' --neType=Shared-CNF'
