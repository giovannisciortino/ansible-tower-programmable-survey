- shell: "{{parameters}}"
  register:
    output_shell
- set_fact:
    "{{variable}}": "{{output_shell.stdout}}"
