from ansible.module_utils.basic import AnsibleModule
import subprocess
import re

def run_module():
    module_args = dict(
        hosts=dict(type='list', required=True)
    )
    result = dict(
        changed=False,
        response=''
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    regex = re.compile('(\\n)')
    answer =''
    for x in module.params['hosts']:
        result_ping = subprocess.Popen(["ping", x, "-c", "1"],stdout=subprocess.PIPE)
        result_ping.wait()
        temp_result = result_ping.stdout.read()
        answer = answer + x +':' + regex.split(temp_result)[-3] + ';'
    result['response'] = answer
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
