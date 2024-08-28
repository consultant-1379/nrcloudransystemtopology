Feature: Executing NR-CLOUD-RAN Topology, Aggregated CM CLI Commands

    Scenario: All conditions are valid
        Given there are nodes with relationships, aggregated
        When the script is executed
        Then the NR-CLOUD-RAN topology should be created

    Scenario: No Nodes in ENM
        Given there are no nodes in ENM
        When the script is executed
        Then the NR-CLOUD-RAN topology should not be created
        Then the topology should be deleted

    Scenario: Only F1-C Links Exist
        Given there are only vDU and vCU-CP nodes, aggregated
        When the script is executed
        Then the NR-CLOUD-RAN topology should be created

    Scenario: No Relationships exist
        Given there are nodes with no relationships, aggregated
        When the script is executed
        Then the NR-CLOUD-RAN topology should not be created
        Then the topology should be deleted

    Scenario: Only C2 relationships exist
        Given there are only nodes with C2 relationships, aggregated
        When the script is executed
        Then the NR-CLOUD-RAN topology should not be created
        Then the topology should be deleted

    Scenario: Topology Exists - Recreate Topology
        Given the NR-CRAN Topology topology exists
        Given there are nodes with relationships, aggregated
        When the script is executed
        Then the NR-CLOUD-RAN topology should be created

    Scenario: Topology Exists - No Relationships Exist
        Given the NR-CRAN Topology topology exists
        Given there are nodes with no relationships, aggregated
        When the script is executed
        Then the NR-CLOUD-RAN topology should not be created
        Then the topology should be deleted

    Scenario: 1 vDU connected to 2 vCU-CP's with Same Mapping
        Given there are nodes with duplicate relationships, aggregated
        When the script is executed
        Then the duplicates should be identified
        Then the NR-CLOUD-RAN topology should be created

    Scenario: Error in CM CLI response from RadioNode
        Given there are read errors from CM CLI
        When the script is executed
        Then the NR-CLOUD-RAN topology should be created with warnings

    Scenario: RI Not run for vDU Shared-CNF Nodes
        Given there are vDU nodes that do not have RI run on them
        When the script is executed
        Then the NR-CLOUD-RAN topology should notify about running RI
        Then the NR-CLOUD-RAN topology should be created with warnings

    Scenario: RI Not run for vCU-CP Shared-CNF Nodes
        Given there are vCU-CP nodes that do not have RI run on them
        When the script is executed
        Then the NR-CLOUD-RAN topology should notify about running RI
        Then the NR-CLOUD-RAN topology should not be created
        Then the topology should be deleted

    Scenario: RI Not run for RDM/ELLS Shared-CNF Nodes
        Given there are RDM nodes that do not have RI run on them
        When the script is executed
        Then the NR-CLOUD-RAN topology should notify about running RI
        Then the NR-CLOUD-RAN topology should be created with warnings

    Scenario: RI Not run for All Shared-CNF Nodes
        Given all Shared-CNF nodes that do not have RI run on them
        When the script is executed
        Then the NR-CLOUD-RAN topology should notify about running RI
        Then the NR-CLOUD-RAN topology should not be created
        Then the topology should be deleted


