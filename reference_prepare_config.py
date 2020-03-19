import os
import logging
import argparse
import sys

logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')

mle_config= """
{
     "cluster": {
                "name" : "%s",
                "clusterType" : "VRA",
                "domain" : "labs.teradata.com",
                "deployment" : "docker",
                "queenNodes" : [],
                "workerNodes" : [],
                "username" : "root",
                "password" : "%s",
                "mlenamespace" : "mlengine",
                "openQueenExecPort" : true
       },
     "kubeCluster" : {
                "domain" : "labs.teradata.com",
                "kubemaster" : ["%sm1"],
                "kubenodes" : ["%sw1","%sw2","%sw3"],
                "username" : "root",
                "password" : "%s",
                "SudoPass" : "XXX",
                "qgm": ["%sqg"],
                "kubemasterVMName": ["%sm1"]
        },
     "tdCluster": {
                "tdMasterNode" : "%st1.labs.teradata.com",
                "tdMasterNode2" : "%st2.labs.teradata.com",
                "tdUserName"   : "root",
                "tdPassword"   : "%s",
                "qgmLink"      : "%s",
                "qgConnectorName" : "%s",
                "viewpoint"    : "%svp.labs.teradata.com"
    }
}
"""
qgm_config= """qgmserver:
    hostname: %sqg.labs.teradata.com
    port: 9443
    authorization: 'Basic c3VwcG9ydDp0ZXJhZGF0YQ=='
datacenters:
    - id:
      name: Vantage
      description: The data center that 10.25.195.163 is located in.  This data center was automatically generated.
      systems:
          - id: Vantage SQL Engine
            name: Vantage SQL Engine
            description: Teradata 16.20.33.01
            properties:
                    hostname: %st1.labs.teradata.com
                    system_user: root
                    system_password: %s
                    system_type: TERADATA
                    db_username: dbc
                    db_password: dbc
                    test_username: testuser
                    test_password: testuser
          - id: Vantage Coprocessor
            name: Vantage Coprocessor
            description: Aster 8.10
            properties:
                    hostname: %sm1.labs.teradata.com
                    system_user: root
                    system_password: %s
                    key_filename: vantage.pem
                    cloud_key_file: vantage.pem
                    system_type: ASTER
                    db_username: db_superuser
                    db_password: db_superuser
                    test_username: public
                    test_password: public
                    aster_port: 30002
fabrics:
    - id: Vantage
      name: Vantage
      description: Fabric for Vantage setup
      connectors:
          - id: vantage-%s SQL Engine
            name: vantage-%s SQL Engine
            systemId: Vantage SQL Engine
            type: TERADATA
          - id: vantage-%s_MLE
            name: vantage-%s_MLE
            systemId: Vantage Coprocessor
            type: ASTER
      links:
          - id: vantage-%s MLE
            name: vantage-%s MLE
            version: active
            initiatorConnectorId: vantage-%s SQL Engine
            targetConnectorId: vantage-%s_MLE
"""
formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=60)
parser = argparse.ArgumentParser(add_help=True)
subparser = parser.add_subparsers(title="Commands", help="commands")
qgng_parser = subparser.add_parser('QGNG', help='FOR QGNG Setup ',formatter_class=formatter)
mle_parser = subparser.add_parser('MLE', help='FOR MLE Setup.',formatter_class=formatter)
mle_args = mle_parser.add_argument_group("mandatory arguments")
qgng_args = qgng_parser.add_argument_group("mandatory arguments")
mle_args.add_argument("-cluster_name", "--cn", dest="cluster_name", help="build", required='true')
mle_args.add_argument("-password", "--p", dest="password", required='true')
mle_args.add_argument("-qgmlink", "--qgl", dest="qgmlink", required='true')
mle_args.add_argument("-qgconnectorname", "--qgcn", dest="qgconnectorname", required='true')
qgng_args.add_argument("-cluster_name", "--cn", dest="cluster_name", help="build", required='true')
qgng_args.add_argument("-password", "--p", dest="password", required='true')
qgng_args.add_argument("-id", "--id", dest="id", help="id", required='true')

args = parser.parse_args()
if(sys.argv[1]=="MLE"):
    cluster_name = args.cluster_name
    template = mle_config % (cluster_name,args.password,cluster_name,cluster_name,cluster_name,cluster_name,args.password,cluster_name,cluster_name,cluster_name,cluster_name,args.password,args.qgmlink,args.qgconnectorname,cluster_name)
    print template
elif(sys.argv[1]=="QGNG"):
    print args.id
    template = qgm_config % (args.cluster_name,args.cluster_name, args.password, args.cluster_name, args.password, args.id, args.id, args.id, args.id,args.id,args.id,args.id,args.id)
    print template
else:
    print("something went wrong")
