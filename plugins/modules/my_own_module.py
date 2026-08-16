#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Your Name <your.email@example.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Create a text file with specified content

version_added: "1.0.0"

description:
    - This module creates a text file on the remote host at the specified path with the specified content.
    - The module is idempotent — if the file already exists with the same content, no changes are made.

options:
    path:
        description:
            - Absolute path where the file should be created.
        required: true
        type: str
    content:
        description:
            - Content to write into the file.
        required: true
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create a simple text file
- name: Create a text file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/hello.txt
    content: "Hello, World!"

# Create a configuration file
- name: Create config file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /etc/myapp/config.txt
    content: "setting=value"
'''

RETURN = r'''
path:
    description: The path of the file that was created or checked.
    type: str
    returned: always
    sample: '/tmp/hello.txt'
content:
    description: The content that was written to the file.
    type: str
    returned: always
    sample: 'Hello, World!'
original_content:
    description: The original content of the file if it existed before the module run.
    type: str
    returned: when file exists
    sample: 'Old content'
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content='',
        original_content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    # Проверяем, существует ли файл и совпадает ли содержимое
    file_exists = os.path.exists(path)
    content_matches = False

    if file_exists:
        try:
            with open(path, 'r') as f:
                existing_content = f.read()
                result['original_content'] = existing_content
                if existing_content == content:
                    content_matches = True
        except Exception as e:
            module.fail_json(msg=f"Failed to read existing file: {str(e)}", **result)

    if module.check_mode:
        if not file_exists or not content_matches:
            result['changed'] = True
        module.exit_json(**result)

    # Если файл не существует или содержимое отличается — записываем
    if not file_exists or not content_matches:
        try:
            # Создаём директории, если нужно
            dir_path = os.path.dirname(path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path)

            with open(path, 'w') as f:
                f.write(content)
            result['changed'] = True
        except Exception as e:
            module.fail_json(msg=f"Failed to write file: {str(e)}", **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
