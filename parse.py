import os
import logging
import argparse
import sys
import json

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
                "username" : "%s",
                "password" : "%s",
                "mlenamespace" : "mlengine",
                "openQueenExecPort" : true
       },
     "kubeCluster" : {
                "domain" : "labs.teradata.com",
                "kubemaster" : [%s],
                "kubenodes" : [%s],
                "username" : "%s",
                "password" : "%s",
                "SudoPass" : "XXX",
                "qgm": ["%s"],
                "kubemasterVMName": ["%s"]
        },
     "tdCluster": {
                %s
                "tdPassword"   : "%s",
                "tdUserName"   : "%s",
                "qgmLink"      : "%s",
                "qgConnectorName" : "%s",
                "viewpoint"    : "%s.labs.teradata.com"
    }
}
"""







#code for json parsing

with open('analytic.IT.properties.json', 'r') as f:
    analytic_dict = json.load(f)

with open('common.IT.properties.json', 'r') as f:
    common_dict = json.load(f)

with open('node.IT.properties.json', 'r') as f:
    node_dict = json.load(f)


cluster_name=common_dict['analytic_cluster_name']


kubemasters = ["" for x in range(0)] #array of strings
kubenodes = ["" for x in range(0)]
qgm = str('')
kubemasterVMName = str('')

tdMasternode_str = ["" for x in range(0)]
view_point = str('')

#fetching information from analytic.IT.properties.json
for analytic in analytic_dict:
    if analytic['vmType']=='analytic_master':
        kubemasters.append(analytic['vmName'])
        if qgm=='':
            qgm=analytic['vmName']
            kubemasterVMName=analytic['vmName']
    if analytic['vmType']=='analytic_worker':
        kubenodes.append(analytic['vmName'])

#fetching information from node.IT.properties.json
for node in node_dict:
    if node['vmType']=='vp':
        view_point=node['vmName']
    else:
        tdMasternode_str.append(node['vmName'])

tdmasters= str('')

for i in range(0,len(tdMasternode_str)):
    if i==0:
        temp='"tdMasterNode" : '+ '"' +tdMasternode_str[i]+'", \n\t\t'
        tdmasters=tdmasters + temp
    else:
        temp='"tdMasterNode'+str(i)+  '" : "' +tdMasternode_str[i]+'", '
        tdmasters=tdmasters + temp



kubemasters1=str('')
for i in range(0,len(kubemasters)):
    temp='"'+kubemasters[i]+'"'
    if i!=len(kubemasters)-1:
        temp=temp+', '
    kubemasters1+=temp

kubenodes1=str('')
for i in range(0,len(kubenodes)):
    temp='"'+kubenodes[i]+'"'
    if i!=len(kubenodes)-1:
        temp=temp+', '
    kubenodes1+=temp
 

formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=60)
parser = argparse.ArgumentParser(add_help=True)
subparser = parser.add_subparsers(title="Commands", help="commands")


mle_parser = subparser.add_parser('MLE', help='FOR MLE Setup.',formatter_class=formatter)

mle_args = mle_parser.add_argument_group("mandatory arguments")


mle_args.add_argument("-td_user_name", "--td_un", dest="td_user_name", required='true')
mle_args.add_argument("-td_password", "--td_p", dest="td_password", required='true')

mle_args.add_argument("-an_user_name", "--an_un", dest="an_user_name", required='true')
mle_args.add_argument("-an_password", "--an_p", dest="an_password", required='true')


args = parser.parse_args()
template = mle_config % (cluster_name, args.an_user_name, args.an_password, kubemasters1, kubenodes1 ,  args.an_user_name,
                           args.an_password , qgm, kubemasterVMName ,
                           tdmasters , args.td_user_name, args.td_password, cluster_name+' MLE', cluster_name+'_MLE',
                                 view_point)
#print(template)                                


outF = open("output.cfg", "w")


for line in template.splitlines():
    outF.write(line)
    outF.write("\n")
    
outF.close()


"""
with open('output_data1.json', 'w') as f:
    json.dump(template, f)
"""



"""
args = parser.parse_args()


if(sys.argv[1]=="MLE"):
    cluster_name = args.cluster_name
    template = mle_config % (cluster_name,args.password,cluster_name,cluster_name,cluster_name,cluster_name,args.password,cluster_name,cluster_name,cluster_name,cluster_name,args.password,args.qgmlink,args.qgconnectorname,cluster_name)
    print(template)
else:
    print("something went wrong")
"""



