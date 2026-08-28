# AGENTS.md

Home Assistant configuration repo (runs as a Docker container). Work is editing YAML configs — there is no build, test, or lint step. Changes take effect on HA reload/restart.

## Layout & wiring
- Repo root is the HA config dir (`configuration.yaml`, `secrets.yaml`, `.HA_VERSION` live here).
- `configuration.yaml` includes everything under `config/` via `!include_dir_merge_list config/<domain>/` for automations, lights, switches, scenes, sensors, plus `!include_dir_merge_named` for scripts, shell_commands, and `!include` for groups/inputs. MQTT/template/command_line entities live in their own subdirs of `config/`.
- Custom integrations (`custom_components/hacs`, `custom_components/wiser`) are NOT in git (gitignored) — don't rely on their presence or modify them here.

## Git / files rules
- `.gitignore` is a whitelist: only `*.yaml`, `*.sh`, `*.png`, `*.md`, `*.py` plus specific files are committed. `secrets.yaml`, `known_devices.yaml`, `ip_bans.yaml`, `custom_components/`, `www/`, `blueprints/`, `.cache/` are intentionally untracked.
- Secrets are referenced as `!secret name` and defined in `secrets.yaml` (which you won't see in git). Never commit real secrets.

## Generated files — don't hand-edit
- `config/voice_assistants/google.yaml` and `siri.yaml` are AUTO-GENERATED from `config/voice_assistants/voice_assistant_config.yaml` by `voice_assistant_config.py`. Edit the source YAML, then regenerate via the `render_voice_assistant_config` shell_command/script.
- `README.md` is AUTO-GENERATED from `README_TEMPLATE.md` by `render_readme.py`. Edit the template, not `README.md`.

## Conventions
- One automation file per topic in `config/automations/`, kebab_case filename; the first `alias:` in each file matches the filename. Files are YAML lists and may hold multiple automations. Appending `.disabled` to a filename disables it.
- Automation `alias:` values use the format `<filename without extension>_<snake_case description>` (e.g. `bathroom_lights_mirror_lights_on` in `bathroom_lights.yaml`).
- Every automation must set `initial_state: true` immediately after its `alias:`.
- HA version is tracked in `.HA_VERSION`; version-bump commits use the message "Update version to X.Y.Z".
