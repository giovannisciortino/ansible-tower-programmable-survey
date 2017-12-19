#!/usr/bin/python

from ansible.module_utils.basic import *
import json


def main():
    fields = {
        "survey_content": {"required": True, "type": "str"},
        "host_vars": {"required": True, "type": "dict"},
    }

    module = AnsibleModule(argument_spec=fields)

    survey_content_str_input = module.params['survey_content']
    host_vars = module.params['host_vars']

    try:
        survey_content = json.loads(survey_content_str_input)
    except ValueError:
        module.fail_json(msg="Option survey_content doesn't contain a valid json")
    for index, question in enumerate(survey_content['spec']):

        if question['variable'] not in host_vars.keys():
            msg = "Variable %s hasn't been found in host_vars dictionary" % question['variable']
            module.fail_json(msg=msg)
        else:
            survey_content['spec'][index]['choices'] = host_vars[question['variable']]
    survey_content_str_output = json.dumps(survey_content)

    module.exit_json(changed=False, result=survey_content_str_output)

if __name__ == '__main__':
    main()
