import argparse
from cloudify_rest_client import CloudifyClient

parser = argparse.ArgumentParser()
parser.add_argument('manager_ip', help='hostname or IP address of the manager')
parser.add_argument('username', help='username to authenticate with')
parser.add_argument('password', help='password to authenticate with')
parser.add_argument('deployment_id', help='ID of the deployment to analyze')
parser.add_argument('--tenant', help='tenant to operate on (optional; defaults to the default tenant)')

args = parser.parse_args()

tenant_id = args.tenant or 'default_tenant'

client = CloudifyClient(host=args.manager_ip,
                        username=args.username,
                        password=args.password,
                        tenant=tenant_id,
                        trust_all=True)
node_instances = client.node_instances.list(deployment_id=args.deployment_id,
                                            _include=['id', 'scaling_groups'])

result = dict()

for ni in node_instances:
    ni_sgs = ni.get('scaling_groups', None)
    if not ni_sgs:
        continue
    for ni_sg in ni_sgs:
        ni_sg_name = ni_sg['name']
        ni_sg_id = ni_sg['id']

        sg_dict = result.get(ni_sg_name, None)
        if not sg_dict:
            sg_dict = dict()
            result[ni_sg_name] = sg_dict
        sg_instance_list = sg_dict.get(ni_sg_id, None)
        if not sg_instance_list:
            sg_instance_list = []
            sg_dict[ni_sg_id] = sg_instance_list
        sg_instance_list.append(ni.id)

print result
