- name: Execute shell command to extract choices value
  shell: "{{parameters}}"
  register:
    output_shell
- name: Save output to fact
  set_fact:
    "{{variable}}": "{{output_shell.stdout}}"
  delegate_to: localhost
  delegate_facts: True
