import os
import sys
from behave import given, then, when, step
from mock import MagicMock, mock, patch

# This will ensure that the core modules are importable by name
directory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '../../../'))
sys.path.insert(1, os.path.join(directory, 'ERICnrcloudran/src/main/python'))
sys.path.insert(2, directory)
from behave import given, then, when, step
from mock import MagicMock, mock, patch
from topologies.system_topologies.nrcloudran_topology import NrCloudRanTopology
from common.nrcloudran_cli import NrCranCli
from test.mocked_data import MockedCli


@given('there are no nodes in ENM')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_empty_cli_response + "\n",
        MockedCli().mocked_empty_cli_response + "\n",
        MockedCli().mocked_empty_cli_response + "\n",
        MockedCli().mocked_empty_cli_response + "\n",
        MockedCli().mocked_empty_cli_response + "\n",
        MockedCli().mocked_empty_cli_response
    ])

# region Aggregated CM CLI Responses


@given('there are nodes with relationships, aggregated')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_aggregated + "\n",
        MockedCli().mocked_radionode_cli_response + "\n",
        MockedCli().mocked_vcucp_cli_response_aggregated + "\n",
        MockedCli().mocked_ru_cli_response_aggregated + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_aggregated
    ])


@given('there are only vDU and vCU-CP nodes, aggregated')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_aggregated + "\n",
        MockedCli().mocked_empty_cli_response + "\n",
        MockedCli().mocked_vcucp_cli_response_aggregated + "\n",
        MockedCli().mocked_empty_cli_response + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_aggregated
    ])


@given('there are nodes with no relationships, aggregated')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_unrelated_aggregated + "\n",
        MockedCli().mocked_radionode_cli_response_unrelated + "\n",
        MockedCli().mocked_vcucp_cli_response_unrelated_aggregated + "\n",
        MockedCli().mocked_ru_cli_response_unrelated_aggregated + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_unrelated_aggregated
    ])


@given('there are nodes with duplicate relationships, aggregated')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_aggregated + "\n",
        MockedCli().mocked_radionode_cli_response_duplicate_mappings + "\n",
        MockedCli().mocked_vcucp_cli_response_duplicate_mappings_aggregated + "\n",
        MockedCli().mocked_ru_cli_response_unrelated_aggregated + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_duplicate_mappings_aggregated
    ])


@given('there are only nodes with C2 relationships, aggregated')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_unrelated_aggregated + "\n",
        MockedCli().mocked_radionode_cli_response + "\n",
        MockedCli().mocked_vcucp_cli_response_unrelated_aggregated + "\n",
        MockedCli().mocked_ru_cli_response_aggregated + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_unrelated_aggregated
    ])


@given('there are read errors from CM CLI')
def step_imp(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_aggregated + "\n",
        MockedCli().mocked_cli_unknown_error_radionode + "\n",
        MockedCli().mocked_vcucp_cli_response_aggregated + "\n",
        MockedCli().mocked_ru_cli_response_aggregated + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_aggregated
    ])


@given('all Shared-CNF nodes that do not have RI run on them')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_error_vdu_cli_response_ri_needs_to_be_run + "\n",
        MockedCli().mocked_radionode_cli_response + "\n",
        MockedCli().mocked_error_vcucp_cli_response_ri_needs_to_be_run + "\n",
        MockedCli().mocked_error_rdm_cli_response_ri_needs_to_be_run + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_aggregated
    ])


@given('there are vDU nodes that do not have RI run on them')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_error_vdu_cli_response_ri_needs_to_be_run + "\n",
        MockedCli().mocked_radionode_cli_response + "\n",
        MockedCli().mocked_vcucp_cli_response_aggregated + "\n",
        MockedCli().mocked_ru_cli_response_aggregated + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_aggregated
    ])


@given('there are vCU-CP nodes that do not have RI run on them')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_aggregated + "\n",
        MockedCli().mocked_radionode_cli_response + "\n",
        MockedCli().mocked_error_vcucp_cli_response_ri_needs_to_be_run + "\n",
        MockedCli().mocked_ru_cli_response_aggregated + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_aggregated
    ])


@given('there are RDM nodes that do not have RI run on them')
def step_impl(context):
    NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
        MockedCli().mocked_vdu_cli_response_aggregated + "\n",
        MockedCli().mocked_radionode_cli_response + "\n",
        MockedCli().mocked_vcucp_cli_response_aggregated + "\n",
        MockedCli().mocked_error_rdm_cli_response_ri_needs_to_be_run + "\n",
        MockedCli().mocked_vcucp_termpointtognbdu_cli_response_aggregated
    ])


# endregion


@when('the script is executed')
def step_impl(context):
    NrCloudRanTopology().run()


@then('the NR-CLOUD-RAN topology should be created')
def step_impl(context):
    stdout = context.stdout_capture.getvalue()
    assert "NR-CRAN topology completed successfully." in stdout


@then('the NR-CLOUD-RAN topology should be created with warnings')
def step_impl(context):
    stdout = context.stdout_capture.getvalue()
    assert "NR-CRAN topology completed with " \
           "warnings, please check the log at " \
           "/opt/ericsson/nrcloudransystemtopo" \
           "logy/log/nrcran_log for more details" in stdout


@then('the NR-CLOUD-RAN topology should notify about running RI')
def step_impl(context):
    stdout = context.stdout_capture.getvalue()
    assert "Please run RI on this Node Type" in [
        entry.getMessage() for entry in context.log_capture.buffer]


@when('the script is executed again')
def step_impl(context):
    NrCloudRanTopology().run()


@then('the NR-CLOUD-RAN topology should not be created')
def step_impl(context):
    stdout = context.stdout_capture.getvalue()
    assert "NR-CRAN topology not created due to missing relationships" in stdout


""" Topology Exists but relationships do not
"""


@given('the NR-CRAN Topology topology exists')
def step_impl(context):
    pass


@when('there are no relationships')
def step_impl(context):
    NrCranCli._get_nodes_attributes = MagicMock(side_effect=[
        "", "", ""
    ])
    NrCloudRanTopology().run()


@then('the topology should be deleted')
def step_impl(context):
    stdout = context.stdout_capture.getvalue()
    assert "NR-CRAN topology not created due to missing relationships" in stdout
    assert "NR-CRAN Systems Topology and Collections deleted successfully" in [
        entry.getMessage() for entry in context.log_capture.buffer]


@then('the duplicates should be identified')
def step_impl(context):
    assert "Duplicate collection name found, renaming from: NR05gNodeBRadio00001 / 100 to: " \
           "NR05gNodeBRadio00001 / 100 - 5G131vCUCPRI002 - 127002" in [
               entry.getMessage() for entry in context.log_capture.buffer]

    assert "Duplicate collection name found, renaming from: NR05gNodeBRadio00001 / 100 to: " \
           "NR05gNodeBRadio00001 / 100 - 5G131vCUCPRI001 - 127002" in [
               entry.getMessage() for entry in context.log_capture.buffer]


""" User added collection
"""


@given('the topology exists')
def step_impl(context):
    pass


@when('the script is executed and a user added collection is present')
def step_impl(context):
    with patch(
            'common.collection_utils.CollectionUtils.get_custom_topology') as \
            patched_response:
        patched_response.return_value = {
            "id": "281474979201006",
            "name": "NR-NSA",
            "category": "Public",
            "parentId": None,
            "userId": "nrcran"
        }
        NrCranCli._get_nodes_attribute = MagicMock(side_effect=[
            MockedCli().mocked_reaggregation_cli_response + "\n",
            MockedCli().mocked_vdu_cli_response + "\n",
            MockedCli().mocked_radionode_cli_response + "\n",
            MockedCli().mocked_vcucp_cli_response + "\n",
            MockedCli().mocked_ru_cli_response + "\n",
            MockedCli().mocked_vcucp_termpointtognbdu_cli_response
        ])
        NrCloudRanTopology().run()


@then('the user added collection should be removed')
def step_impl(context):
    assert "NR-CRAN script removed user added Collection 'My test " \
           "collection'" in [
               entry.getMessage() for entry in context.log_capture.buffer]


"""Scheduled updates
"""


@step('the topology exists')
def step_impl(context):
    pass


@step('there are relationships')
def step_impl(context):
    NrCranCli._get_nodes_attributes = MagicMock(side_effect=[
        MockedCli().mocked_enode_attributes + "\n",
        MockedCli().mocked_gnode_attributes + "\n"
    ])


@when('the script executes again')
def step_impl(context):
    with patch(
            'common.collection_utils.CollectionUtils.get_custom_topology') as \
            patched_response:
        patched_response.return_value = {
            "id": "281474979201007",
            "name": "NR-NSA",
            "category": "Public",
            "parentId": None
        }
        NrCloudRanTopology().run()
