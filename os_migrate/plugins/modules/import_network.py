#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: os_migrate.os_migrate.import_network

short_description: Import OpenStack network

version_added: "2.9"

description:
  - "Import OpenStack network from an OS-Migrate YAML structure"

options:
  auth:
    description:
      - Dictionary with parameters for chosen auth type.
    required: true
  auth_type:
    description:
      - Auth type plugin for OpenStack. Can be omitted if using password authentication.
    required: false
  region_name:
    description:
      - OpenStack region name. Can be omitted if using default region.
    required: false

  data:
    description:
      - Data structure with network parameters as loaded from OS-Migrate YAML file.
    required: true
'''

EXAMPLES = '''
- name: Import mynetwork into /opt/os-migrate/networks.yml
  os_migrate.os_migrate.import_network:
    cloud: source_cloud
    data:
      - type: openstack.network
        params:
          name: my_net
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack \
    import openstack_full_argument_spec, openstack_cloud_from_module

from ansible_collections.os_migrate.os_migrate.plugins.module_utils import network


def run_module():
    argument_spec = openstack_full_argument_spec(
        cloud=dict(type='str', required=True),
        data=dict(type='dict', required=True),
    )
    del argument_spec['cloud']

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        # TODO: Consider check mode. We'd fetch the resource and check
        # if the file representation matches it.
        # supports_check_mode=True,
    )

    sdk, conn = openstack_cloud_from_module(module)
    net = network.Network.from_data(module.params['data'])
    result['changed'] = net.create_or_update(conn)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
