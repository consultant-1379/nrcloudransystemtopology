from collections import defaultdict
import requests
from mock import MagicMock
from requests.models import Response


class MockRelationship(object):
    """
        @:param poid is unused for the new relationship implementation.
    """

    def __init__(self, poid=None, fdn=None, nodes=None):
        self.poid = poid
        self.fdn = fdn
        self.nodes = nodes


class MockedData(object):

    def get_mocked_cookie(self):
        the_response = MagicMock(return_value=Response)
        the_response.status_code = 302
        cookie_session = requests.Session()
        cookie_session.cookies["iPlanetDirectoryPro"] = "ValidCookie"
        the_response.cookies = cookie_session.cookies
        session = requests.Session()
        requests.session = MagicMock(return_value=session)
        session.post = MagicMock(return_value=the_response)
        return the_response.cookies

    def get_mocked_parsed_collection(self, user):
        parsed_collection = {
            u'LTE01dg2ERBS00001-NR-NSA': {
                'collection': {
                    u'category': u'Public',
                    u'sortable': True,
                    u'name': u'LTE01dg2ERBS00001-NR-NSA',
                    u'timeCreated': 1537268886540,
                    u'userId': user,
                    u'update': True,
                    u'lastUpdated': 1537268915624,
                    u'readOnly': False,
                    u'objects': [
                        {
                            u'attributes': {
                                u'neType': u'RadioNode'
                            },
                            u'type': u'NetworkElement',
                            u'id': u'281474979637266',
                            u'name': u'LTE01dg2ERBS00001'
                        },
                        {
                            u'attributes': {
                                u'neType': u'RadioNode'
                            },
                            u'type': u'NetworkElement',
                            u'id': u'281474979480691',
                            u'name': u'NR01gNodeBRadio00001'
                        }
                    ],
                    u'metadata': {
                        u'models': [
                            {
                                u'root': True,
                                u'moType': u'NetworkElement'
                            }
                        ]
                    },
                    u'id': u'281474979637266',
                    u'delete': True
                }
            }
        }
        return parsed_collection

    def get_mocked_topology(self):
        topology = [
            {
                u'level': 0,
                u'parentId': None,
                u'type': u'BRANCH',
                u'id': u'281474979637230',
                u'name': u'NR-NSA'
            }
        ]
        return topology

    def get_mocked_new_relationship(self):
        relationships = defaultdict(list)
        relationships[281474979033549].append(
            [281474979033549, 281474979033931])
        return relationships

    def get_mocked_new_enodeb_names(self):
        return {u'281474979033549': 'LTE01dg2ERBS00002'}

    def get_mocked_enodeb_name(self):
        return 'LTE01dg2ERBS00001'

    def get_mocked_enodeb_names(self):
        return {u'281474979033549': 'LTE01dg2ERBS00001'}

    def get_mocked_collection_parse_poids(self):
        reponse = {
            'collection': {
                u'category': u'Public',
                u'sortable': True,
                u'name': u'281474979488435-NR-NSA',
                u'timeCreated': 1537199149785,
                u'userId': u'administrator',
                u'update': True,
                u'lastUpdated': 1537199150479,
                u'readOnly': False,
                u'objects': [
                    {
                        u'attributes': {
                            u'neType': u'RadioNode'
                        },
                        u'type': u'NetworkElement',
                        u'id': u'281474979488435',
                        u'name': u'LTE01dg2ERBS00001'
                    },
                    {
                        u'attributes': {
                            u'neType': u'RadioNode'
                        },
                        u'type': u'NetworkElement',
                        u'id': u'281474979488715',
                        u'name': u'NR01gNodeBRadio00001'
                    }
                ],
                u'metadata': {
                    u'models': [
                        {
                            u'root': True,
                            u'moType': u'NetworkElement'
                        }
                    ]
                },
                u'id': u'281474979658833',
                u'delete': True
            }
        }
        return reponse

    def get_mocked_collection_list(self):
        collection_list = [
            {u'level': 1, u'parentId': u'281474979444198', u'type': u'LEAF',
             u'id': u'281474979444224', u'name': u'LTE01dg2ERBS00001-NR-NSA'}]
        return collection_list

    def get_mocked_collection_for_parse_collections(self):
        response = {u'LTE01dg2ERBS00001-NR-NSA': {
            'collection': {u'category': u'Public', u'sortable': False,
                           u'name': u'LTE01dg2ERBS00001-NR-NSA',
                           u'timeCreated': 1538123651947,
                           u'userId': u'administrator', u'update': True,
                           u'lastUpdated': 1538123652734, u'readOnly': False,
                           u'objects': [
                               {u'attributes': {}, u'id': u'281474979172519'},
                               {u'attributes': {}, u'id': u'281474979172799'}],
                           u'id': u'281474979444242', u'delete': True}}}
        return response

    def get_mocked_collection_response(self):
        response = {
            "category": "Public",
            "delete": True,
            "id": "281474979444242",
            "lastUpdated": 1538123652734,
            "name": "LTE01dg2ERBS00001-NR-NSA",
            "objects": [
                {
                    "attributes": {},
                    "id": "281474979172519"
                },
                {
                    "attributes": {},
                    "id": "281474979172799"
                }
            ],
            "readOnly": False,
            "sortable": False,
            "timeCreated": 1538123651947,
            "update": True,
            "userId": "administrator"
        }
        return response

    def get_mocked_collection(self):
        response = {
            'collection': {
                u'category': u'Public',
                u'sortable': True,
                u'name': u'LTE01dg2ERBS00001-NR-NSA',
                u'timeCreated': 1537268886540,
                u'userId': u'administrator',
                u'update': True,
                u'lastUpdated': 1537268915624,
                u'readOnly': False,
                u'objects': [
                    {
                        u'attributes': {
                            u'neType': u'RadioNode'
                        },
                        u'type': u'NetworkElement',
                        u'id': u'281474979637266',
                        u'name': u'LTE01dg2ERBS00001'
                    },
                    {
                        u'attributes': {
                            u'neType': u'RadioNode'
                        },
                        u'type': u'NetworkElement',
                        u'id': u'281474979480691',
                        u'name': u'NR01gNodeBRadio00001'
                    }
                ],
                u'metadata': {
                    u'models': [
                        {
                            u'root': True,
                            u'moType': u'NetworkElement'
                        }
                    ]
                },
                u'id': u'281496176593758',
                u'delete': True
            }
        }
        return response

    def get_mocked_user_parsed_collection_public(self):
        parsed_collection = {
            u'LTE01dg2ERBS00001-NR-NSA': {
                'collection': {
                    u'category': u'Public',
                    u'sortable': True,
                    u'name': u'LTE01dg2ERBS00001-NR-NSA',
                    u'timeCreated': 1537268886540,
                    u'userId': u'testUser',
                    u'update': True,
                    u'lastUpdated': 1537268915624,
                    u'readOnly': False,
                    u'objects': [
                        {
                            u'attributes': {
                                u'neType': u'RadioNode'
                            },
                            u'type': u'NetworkElement',
                            u'id': u'281474979480629',
                            u'name': u'LTE01dg2ERBS00001'
                        },
                        {
                            u'attributes': {
                                u'neType': u'RadioNode'
                            },
                            u'type': u'NetworkElement',
                            u'id': u'281474979480691',
                            u'name': u'NR01gNodeBRadio00001'
                        }
                    ],
                    u'metadata': {
                        u'models': [
                            {
                                u'root': True,
                                u'moType': u'NetworkElement'
                            }
                        ]
                    },
                    u'id': u'281474979637266',
                    u'delete': True
                }
            }
        }
        return parsed_collection

    def get_mocked_user_parsed_collection_private(self):
        parsed_collection = {
            u'LTE01dg2ERBS00001-NR-NSA': {
                'collection': {
                    u'category': u'Private',
                    u'sortable': True,
                    u'name': u'LTE01dg2ERBS00001-NR-NSA',
                    u'timeCreated': 1537268886540,
                    u'userId': u'testUser',
                    u'update': True,
                    u'lastUpdated': 1537268915624,
                    u'readOnly': False,
                    u'objects': [
                        {
                            u'attributes': {
                                u'neType': u'RadioNode'
                            },
                            u'type': u'NetworkElement',
                            u'id': u'281474979480629',
                            u'name': u'LTE01dg2ERBS00001'
                        },
                        {
                            u'attributes': {
                                u'neType': u'RadioNode'
                            },
                            u'type': u'NetworkElement',
                            u'id': u'281474979480691',
                            u'name': u'NR01gNodeBRadio00001'
                        }
                    ],
                    u'metadata': {
                        u'models': [
                            {
                                u'root': True,
                                u'moType': u'NetworkElement'
                            }
                        ]
                    },
                    u'id': u'281474979637266',
                    u'delete': True
                }
            }
        }
        return parsed_collection

    def get_mocked_relationships(self):
        relationships = {
            'poIdToAttributes': {
                281474978956971: {'fdn': ['NetworkElement=LTE01dg2ERBS00001']},
                281474978957002: {'fdn': ['NetworkElement=LTE01dg2ERBS00002']},
                281474978954436: {
                    'fdn': ['NetworkElement=NR01gNodeBRadio00001']},
                281474978956940: {
                    'fdn': ['NetworkElement=NR01gNodeBRadio00002']},
            },
            'relationTypeToTargets': {
                'X2_eNB-gNB': [{
                    'sourcePoId': 281474978954436,
                    'destinationPoId': 281474978956971,
                    'properties': 'null'
                },
                    {
                        'sourcePoId': 281474978956940,
                        'destinationPoId': 281474978956971,
                        'properties': 'null'
                    },
                    {
                        'sourcePoId': 281474978956940,
                        'destinationPoId': 281474978957002,
                        'properties': 'null'
                    }
                ]}
        }
        return relationships

    def mocked_relationship_list(self):
        relation_1 = MockRelationship(poid=u'281474979033549',
                                      fdn=u'LTE01dg2ERBS00001', nodes=[
                281474979033549, 281474979033931])
        return [relation_1]

    def mocked_empty_collection_by_name(self):
        return {'collections': []}

    def mocked_collection_by_name(self):
        return {'collections': [
            {
                "id": "281496176593758",
                "name": "LTE-ERBS",
                "category": "Public",
                "timeCreated": 1549959651703
            }
        ]
        }

    def mocked_collection_duplicate(self):
        return {'collections': [
            {
                "id": "281496176593758",
                "name": "LTE-ERBS",
                "category": "Public",
                "userId": "administrator",
                "timeCreated": 1549959651703
            }
        ]
        }

    def mocked_lte_collections(self):
        return {
            "LTE-ERBS": '{"category": "Public", "userId": null, "name": "LTE-ERBS"}',
            "LTE-RadioNode": '{"category": "Public", "userId": null, "name": "LTE-RadioNode"}',
            "NR-RadioNode": '{"category": "Public", "userId": null, "name": "NR-RadioNode"}'
        }

    def mocked_objects(self):
        return '{"objects": ["123", "124"]}'


class MockedCli(object):

    #region Non Aggregated CM CLI Responses
    @property
    def mocked_reaggregation_cli_response(self):
        return """Error 1010 : An unknown attribute has been encountered; name gNBDUId in the 
        MO class GNBDUFunction. Verify valid attributes for the MO type in the latest models by 
        executing the following cmedit describe command - "cmedit describe GNBDUFunction.*"


        Error 5010 : The read command has errors."""

    @property
    def mocked_vdu_cli_response(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1,attributes=1
                        gNBDUId : 100
                        gNBId : 127001

                  1 instance(s)"""

    @property
    def mocked_radionode_cli_response(self):
        return """FDN : ManagedElement=NR05gNodeBRadio00001,GNBDUFunction=1
                        gNBDUId : 100
                        gNBId : 127001

                        1 instance(s)"""

    @property
    def mocked_vcucp_cli_response(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,attributes=1
                        gNBId : 127001

                     1 instance(s)"""

    @property
    def mocked_ru_cli_response(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1,NRSectorCarrier=2,attributes=1
                        sectorEquipmentFunctionRef : MeContext=CORE5G137RDM002,ManagedElement=1,SectorEquipmentFunction=1

                        1 instance(s)
                        """

    @property
    def mocked_vcucp_termpointtognbdu_cli_response(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1,attributes=1
                        gNBDUId : 100


                        1 instance(s)"""

    @property
    def mocked_vdu_cli_response_unrelated(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1,attributes=1
                           gNBDUId : 1001
                           gNBId : 127001

                     1 instance(s)"""

    @property
    def mocked_radionode_cli_response_unrelated(self):
        return """FDN : ManagedElement=NR05gNodeBRadio00001,GNBDUFunction=1
                           gNBDUId : 1002
                           gNBId : 127001

                           1 instance(s)"""

    @property
    def mocked_vcucp_cli_response_unrelated(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,attributes=1
                           gNBId : 127002

                        1 instance(s)"""

    @property
    def mocked_ru_cli_response_unrelated(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1,NRSectorCarrier=2,attributes=1
                           sectorEquipmentFunctionRef : MeContext=CORE5G137RDM002,ManagedElement=1,SectorEquipmentFunction=5

                           1 instance(s)
                           """

    @property
    def mocked_vcucp_termpointtognbdu_cli_response_unrelated(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1,attributes=1
                           gNBDUId : 1005


                           1 instance(s)"""

    @property
    def mocked_vdu_cli_response_duplicate_mappings(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1,attributes=1
                            gNBDUId : 100
                            gNBId : 127001

                      1 instance(s)"""

    @property
    def mocked_radionode_cli_response_duplicate_mappings(self):
        return """FDN : ManagedElement=NR05gNodeBRadio00001,GNBDUFunction=1
                            gNBDUId : 100
                            gNBId : 127002

                            1 instance(s)"""

    @property
    def mocked_vcucp_cli_response_duplicate_mappings(self):
        return """\nFDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,attributes=1
                            gNBId : 127002 \n
                            FDN : MeContext=5G131vCUCPRI002,ManagedElement=1,GNBCUCPFunction=1,attributes=1
                            gNBId : 127002

                         2 instance(s)"""

    @property
    def mocked_vcucp_termpointtognbdu_cli_response_duplicate_mappings(self):
        return """\nFDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1,attributes=1
                            gNBDUId : 100\n
                            FDN : MeContext=5G131vCUCPRI002,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1,attributes=1
                            gNBDUId : 100\n


                            2 instance(s)"""
#endregion

    #region Aggregated CM CLI Responses
    @property
    def mocked_vdu_cli_response_aggregated(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1
                            gNBDUId : 100
                            gNBId : 127001

                      1 instance(s)"""

    @property
    def mocked_radionode_cli_response(self):
        return """FDN : ManagedElement=NR05gNodeBRadio00001,GNBDUFunction=1
                            gNBDUId : 100
                            gNBId : 127001

                            1 instance(s)"""

    @property
    def mocked_vcucp_cli_response_aggregated(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1
                            gNBId : 127001

                         1 instance(s)"""

    @property
    def mocked_ru_cli_response_aggregated(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1,NRSectorCarrier=2
                            sectorEquipmentFunctionRef : MeContext=CORE5G137RDM002,ManagedElement=1,SectorEquipmentFunction=1

                            1 instance(s)
                            """

    @property
    def mocked_vcucp_termpointtognbdu_cli_response_aggregated(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1
                            gNBDUId : 100


                            1 instance(s)"""

    @property
    def mocked_vdu_cli_response_unrelated_aggregated(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1
                               gNBDUId : 1001
                               gNBId : 127001

                         1 instance(s)"""

    @property
    def mocked_radionode_cli_response_unrelated(self):
        return """FDN : ManagedElement=NR05gNodeBRadio00001,GNBDUFunction=1
                               gNBDUId : 1002
                               gNBId : 127001

                               1 instance(s)"""

    @property
    def mocked_vcucp_cli_response_unrelated_aggregated(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1
                               gNBId : 127002

                            1 instance(s)"""

    @property
    def mocked_ru_cli_response_unrelated_aggregated(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1,NRSectorCarrier=2
                               sectorEquipmentFunctionRef : MeContext=CORE5G137RDM002,ManagedElement=1,SectorEquipmentFunction=5

                               1 instance(s)
                               """

    @property
    def mocked_vcucp_termpointtognbdu_cli_response_unrelated_aggregated(self):
        return """FDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1
                               gNBDUId : 1005


                               1 instance(s)"""

    @property
    def mocked_vdu_cli_response_duplicate_mappings_aggregated(self):
        return """FDN : MeContext=5G139vDURI001,ManagedElement=1,GNBDUFunction=1
                                gNBDUId : 100
                                gNBId : 127001

                          1 instance(s)"""

    @property
    def mocked_radionode_cli_response_duplicate_mappings(self):
        return """FDN : ManagedElement=NR05gNodeBRadio00001,GNBDUFunction=1
                                gNBDUId : 100
                                gNBId : 127002

                                1 instance(s)"""

    @property
    def mocked_vcucp_cli_response_duplicate_mappings_aggregated(self):
        return """\nFDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1
                                gNBId : 127002 \n
                                FDN : MeContext=5G131vCUCPRI002,ManagedElement=1,GNBCUCPFunction=1
                                gNBId : 127002

                             2 instance(s)"""

    @property
    def mocked_vcucp_termpointtognbdu_cli_response_duplicate_mappings_aggregated(self):
        return """\nFDN : MeContext=5G131vCUCPRI001,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1
                                gNBDUId : 100\n
                                FDN : MeContext=5G131vCUCPRI002,ManagedElement=1,GNBCUCPFunction=1,TermPointToGNBDU=1
                                gNBDUId : 100\n


                                2 instance(s)"""

    #endregion

    @property
    def mocked_empty_cli_response(self):
        return "0 instance(s)"

    @property
    def mocked_error_vdu_cli_response_ri_needs_to_be_run(self):
        return """Error 1055 : Invalid MO type (GNBDUFunction$$attributes) for the node(s) provided in the scope(s) 
                        Use the cmedit describe command  to find valid MO types.

                    Error 5010 : The read command has errors."""

    @property
    def mocked_error_vcucp_cli_response_ri_needs_to_be_run(self):
        return """Error 1055 : Invalid MO type (GNBCUCPFunction$$attributes) for the node(s) provided in the scope(s) 
                        Use the cmedit describe command  to find valid MO types.

                    Error 5010 : The read command has errors."""

    @property
    def mocked_error_rdm_cli_response_ri_needs_to_be_run(self):
        return """Error 1055 : Invalid MO type (sectorEquipmentFunction) for the node(s) provided in the scope(s) 
                        Use the cmedit describe command  to find valid MO types.

                    Error 5010 : The read command has errors."""

    @property
    def mocked_cli_unknown_error_radionode(self):
        return """ FDN : ManagedElement=NR05gNodeBRadio00001,GNBDUFunction=1
                                gNBDUId : 100
                                gNBId : 127002 \n
                                    FDN : ManagedElement=NR05gNodeBRadio00002,GNBCUCPFunction=1
                                    Error 9999 : Execution Error (Node ID: svc-3-mscmce. Exception occurred: ManagedObject READ command for Node [ManagedElement=NR05gNodeBRadio00002,GNBCUCPFunction=1] has failed in <get> operation. RESPONSE ERROR MESSAGE FROM NODE: [Netconf Connect operation has failed after 3 attempts])


                                    Error 5010 : The read command has errors.
        """

    @property
    def mocked_name_to_poid_list(self):
        return dict(LTE18dg2ERBS00154=20185418742,
                    NR01gNodeBRadio00001=20185418456,
                    NR01gNodeBRadio00002=20185418457
                    )

    @property
    def mocked_name_to_poid_list_multiple_relationships(self):
        return dict(LTE18dg2ERBS00154=20185418742,
                    LTE26dg2ERBS00001=20185418743,
                    NR01gNodeBRadio00001=20185418456,
                    NR01gNodeBRadio00002=20185418457
                    )

    @property
    def mocked_created_relationships(self):
        return [MockRelationship(fdn=u'LTE18dg2ERBS00154', nodes=[
            20185418742, 20185418456])]

    @property
    def mocked_created_relationships_multiple_gnodes(self):
        return [MockRelationship(fdn=u'LTE18dg2ERBS00154', nodes=[
            20185418742, 20185418456, 20185418457])]

    @property
    def mocked_created_relationships_multiple_relationships(self):
        return [MockRelationship(fdn=u'LTE26dg2ERBS00001', nodes=[
            20185418743, 20185418457]),
                MockRelationship(fdn=u'LTE18dg2ERBS00154', nodes=[
                    20185418742, 20185418456])]

    @property
    def mocked_cli_node_error(self):
        return """FDN : SubNetwork=NR!-?<@~>#'!NSA,ManagedElement=NR01gNodeBRadio00001,GNBCUCPFunction=1,EUtraNetwork=1,ExternalENodeBFunction=LTE18dg2ERBS00154NR!-?<@~>#'!NSA
                        pLMNId : {mcc=353, mnc=57}
                        eNodeBId : 2874

                                    FDN : ManagedElement=NR01gNodeBRadio00003,GNBCUCPFunction=1,EUtraNetwork=1,ExternalENodeBFunction=LTE01dg2ERBS00003
                                    pLMNId : {mcc=353, mnc=57}
                                    eNodeBId : 3

                                    FDN : ManagedElement=NR01gNodeBRadio00002,GNBCUCPFunction=1,EUtraNetwork=1,ExternalENodeBFunction=1
                                    pLMNId : {mcc=125, mnc=46}
                                    eNodeBId : 1

                                    FDN : ManagedElement=NR01gNodeBRadio00002,GNBCUCPFunction=1,EUtraNetwork=1,ExternalENodeBFunction=LTE01dg2ERBS00002
                                    pLMNId : {mcc=353, mnc=57}
                                    eNodeBId : 2

                                    FDN : ManagedElement=NR01gNodeBRadio00002,GNBCUCPFunction=1,EUtraNetwork=1,ExternalENodeBFunction=LTE01dg2ERBS00003
                                    pLMNId : {mcc=353, mnc=57}
                                    eNodeBId : 3

                                    FDN : ManagedElement=NR01gNodeBRadio00004,GNBCUCPFunction=1,EUtraNetwork=1,ExternalENodeBFunction=LTE18dg2ERBS00155
                                    Error 9999 : Execution Error (Node ID: svc-3-mscmce. Exception occurred: ManagedObject READ command for Node [ManagedElement=NR01gNodeBRadio00004,GNBCUCPFunction=1,EUtraNetwork=1,ExternalENodeBFunction=1] has failed in <get> operation. RESPONSE ERROR MESSAGE FROM NODE: [Netconf Connect operation has failed after 3 attempts])


                                    Error 5010 : The read command has errors.
                        """

    @property
    def mocked_cli_namespace_error(self):
        return """Error 1012 : Invalid MO type, ExternalENodeBFunction not found Validate specified MO type. Use the cmedit describe command
                            to find valid MO types.

                            Error 5010 : The read command has errors."""
