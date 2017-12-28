# ansible-tower-programmable-survey

An ansible playbook used to generate a job template survey for Ansible Tower and
AWX based on dynamic data extracted from ansible.
This playbook can be scheduled on Ansible Tower/AWX to create dynamic surveys.



Prerequisites:
- tower-cli installed on Ansible Tower/AWX and configured with an user with "the
  privilege to modify Job Template"

  Example:
```
[root@tower ~]# tower-cli config --scope user username admin
Configuration updated successfully.
[root@tower ~]# tower-cli config --scope user password password
Configuration updated successfully.
[root@tower ~]# tower-cli config --scope user verify_ssl True
Configuration updated successfully.
```

- An inventory defined in Ansible Tower/AWX including the Ansible Tower/AWX server
  Example:
```
[root@tower ~]# tower-cli inventory get --name 'Demo Inventory'
== ============== ============
id      name      organization
== ============== ============
 1 Demo Inventory            1
== ============== ============
```

- A credential defined in Ansible Tower/AWX valid for the Ansible Tower/AWX server
  Example:
```
[root@tower ~]# tower-cli credential get --name="Demo Credential"
== =============== ===============
id      name       credential_type
== =============== ===============
 6 Demo Credential               1
== =============== ===============

```

Instruction to configure this playbook on Ansible Tower/AWX:

1. Create a new project from SCM URL https://github.com/giovannisciortino/ansible-tower-programmable-survey.git

  Example:
```
[root@tower ~]# tower-cli project create --name 'Programmable Survey' --scm-type git --scm-url 'https://github.com/giovannisciortino/ansible-tower-programmable-survey.git'
```

2. Create a new Job template(this template will have a dynamic survey)

Example:
```
[root@tower ~]# tower-cli job_template create --name 'Job Template With Dynamic Survey' --credential 'Demo Credential' --inventory 'Demo Inventory' --project 'Demo Project' --playbook 'hello_world.yml'
Resource changed.
== ================================ ========= ======= ===============
id               name               inventory project    playbook     
== ================================ ========= ======= ===============
19 Job Template With Dynamic Survey         1       4 hello_world.yml
== ================================ ========= ======= ===============
```

3. Edit the Job template created in the previous step from Ansible Tower/AWX Web UI adding a survey with at least one answer of type "Multiple Choice(Single select)" or "Multiple Choice(Multiple select)"

Example:
```
In my example I have created a survey with three answer with the following data:
1. Prompt: Select a hostgroup
   Answer Variable Name: hostgroup
   Answer Type: Multiple Choice(Single select)
   Multiple Choice Options: "to be replaced with dynamic data"
2. Prompt: Select a host
   Answer Variable Name: host
   Answer Type: Multiple Choice(Single select)
   Multiple Choice Options: "to be replaced with dynamic data"
3. Prompt: Select a user
   Answer Variable Name: user
   Answer Type: Multiple Choice(Single select)
   Multiple Choice Options: "to be replaced with dynamic data"
```

4. Extract the JSON survey spec of the survey created in the previous step
  Example:
```
[root@tower ~]# tower-cli job_template get --name 'Job Template With Dynamic Survey'
== ================================ ========= ======= ===============
id               name               inventory project    playbook     
== ================================ ========= ======= ===============
19 Job Template With Dynamic Survey         1       4 hello_world.yml
== ================================ ========= ======= ===============

[root@tower ~]# tower-cli job_template survey 19
{
  "description": "",
  "spec": [
    {
      "required": true,
      "min": null,
      "default": "",
      "max": null,
      "question_description": "",
      "choices": "to be replaced with dynamic data",
      "new_question": true,
      "variable": "hostgroup",
      "question_name": "Select a hostgroup",
      "type": "multiplechoice"
    },
    {
      "required": true,
      "min": null,
      "default": "",
      "max": null,
      "question_description": "",
      "choices": "to be replaced with dynamic data",
      "new_question": true,
      "variable": "host",
      "question_name": "Select a host",
      "type": "multiplechoice"
    },
    {
      "required": true,
      "min": null,
      "default": "",
      "max": null,
      "question_description": "",
      "choices": "to be replaced with dynamic data",
      "new_question": true,
      "variable": "user",
      "question_name": "Select a user",
      "type": "multiplechoice"
    }
  ],
  "name": ""
}

```  

4. Create a new Job Template in the project 'Programmable Survey' selecting a credential valid for Ansible Tower/AWX server and a inventory including Ansible Tower/AWX server using the playbook 'update_programmable_surveys.yml'
  Example:
```
[root@tower ~]# tower-cli job_template create --name 'Dynamic survey update "Job Template With Dynamic Survey"' --credential 'Demo Credential' --inventory 'Demo Inventory' --project 'Programmable Survey' --playbook 'update_programmable_surveys.yml' --become-enabled true
Resource changed.
== ======================================================== ========= ======= ===============================
id                           name                           inventory project            playbook             
== ======================================================== ========= ======= ===============================
20 Dynamic survey update "Job Template With Dynamic Survey"         1      18 update_programmable_surveys.yml
== ======================================================== ========= ======= ===============================
```  

5. Define using vars the configuration of the job template 'Dynamic survey update "Job Template With Dynamic Survey"'.
The value reported in the example below are the default value defined in the role "programmable_surveys". They can replaced with the customization requested in each ansible infrastructure.
The content of the variable job_template_survey_content is the structure of the job template survey spec; the step 3 of the paragraph "job_template_survey_content" contains the commands to extract it
The job_template_survey_variables list contains one element for each dynamic survey element of the survey.
Currently a single generator "survey_generators/shell_generator.yml" has been implemented it allow to use the ansible module shell to generate a list of survey select box values.


   Example:


```  
[awx@tower ~]# cat > /tmp/extra_vars.yml << EOF
tower_cli_path: '/usr/bin/tower-cli'
job_template_name: 'Job Template With Dynamic Survey'
job_template_survey_content: |
  {
  "description": "",
  "name": "",
  "spec": [
    {
      "question_description": "",
      "min": null,
      "default": "",
      "max": null,
      "required": true,
      "choices": "",
      "variable": "hostgroups",
      "question_name": "Target Hostgroups",
      "type": "multiselect"
    },
    {
      "question_description": "",
      "min": null,
      "default": "",
      "max": null,
      "required": true,
      "choices": "123",
      "new_question": true,
      "variable": "hosts",
      "question_name": "Hosts",
      "type": "multiselect"
    },
    {
      "question_description": "",
      "min": null,
      "default": "",
      "max": null,
      "required": true,
      "choices": "123",
      "new_question": true,
      "variable": "userlist",
      "question_name": "User list",
      "type": "multiselect"
    }

  ]
  }

job_template_survey_variables:
  - target_hostgroups:
    source: survey_generators/shell_generator.yml
    parameters: "tower-cli group list | awk '{print $2}'|sed -e '1,3d'|sed '$ d'"
    variable: hostgroups
    delegate_to: localhost
  - target_hosts:
    source: survey_generators/shell_generator.yml
    parameters: "tower-cli host list | awk '{print $2}'|sed -e '1,3d'|sed '$ d'"
    variable: hosts
    delegate_to: localhost
  - target_hosts:
    source: survey_generators/shell_generator.yml
    parameters: "cat /etc/passwd |cut -d':' -f1"
    variable: userlist
    delegate_to: localhost
EOF

# tower-cli job_template modify --name 'Dynamic survey update "Job Template With Dynamic Survey"' --extra-vars "@/tmp/extra_vars.yml"
Resource changed.
== ======================================================== ========= ======= ===============================
id                           name                           inventory project            playbook             
== ======================================================== ========= ======= ===============================
24 Dynamic survey update "Job Template With Dynamic Survey"         1      18 update_programmable_surveys.yml
== ======================================================== ========= ======= ===============================

```  


6. Schedule the execution of the job defined in the step 4.
   Example:

```  
[awx@tower ~]# tower-cli schedule create --name="Schedule dynamic survey update" --job-template='Dynamic survey update "Job Template With Dynamic Survey"' --rrule="DTSTART:20171215T000000Z RRULE:FREQ=MINUTELY;INTERVAL=15"
```  
