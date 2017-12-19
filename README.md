# ansible-tower-programmable-survey
Ansible playbook and role to generate a dynamic job template survey



Prerequisiti:
- tower-cli funzionante

[root@tower ~]# tower-cli project create --name 'Example project' --scm-type git --scm-url 'https://github.com/ansible/ansible-tower-samples'
Resource changed.
== =============== ======== ================================================ ====================
id      name       scm_type                     scm_url                           local_path      
== =============== ======== ================================================ ====================
11 Example project git      https://github.com/ansible/ansible-tower-samples _11__example_project
== =============== ======== ================================================ ====================

[root@tower projects]# tower-cli job_template create --name 'Example Job Template' --project 'Example project' --playbook 'hello_world.yml' --credential 'Demo Credential' --ask-inventory-on-launch True
Resource changed.
== ==================== ========= ======= ===============
id         name         inventory project    playbook     
== ==================== ========= ======= ===============
12 Example Job Template None           11 hello_world.yml
== ==================== ========= ======= ===============

Documentazione survey preso da https://github.com/ansible/tower-cli/blob/master/docs_deprecated/SURVEYS.md

[root@tower projects]# tower-cli job_template survey --name='Example Job Template1' > survey_job_template1.json


[root@tower projects]# cat survey_job_template1.json
{
  "description": "",
  "spec": [
    {
      "required": true,
      "min": null,
      "default": "",
      "max": null,
      "question_description": "",
      "choices": "group2\ngroup3aggiuntoDaCli",
      "new_question": true,
      "variable": "hosts",
      "question_name": "Target Hostgroups",
      "type": "multiselect"
    }
  ],
  "name": ""
}


[root@tower projects]# tower-cli job_template modify --name='Example Job Template' --survey-enabled=true --survey-spec=@survey_job_template1.json
Resource changed.
== ==================== ========= ======= ===============
id         name         inventory project    playbook     
== ==================== ========= ======= ===============
12 Example Job Template None           11 hello_world.yml
== ==================== ========= ======= ===============
