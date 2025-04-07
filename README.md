# Blender Cactus

## How to run

### Cloud part

> you are expected to have docker and docker compose on your machine for this

configure the environment 
put a configuration in .env like
```env
# postgres init
POSTGRES_PASSWORD="cactus"

# migrations
DATABASE_URL="postgres://postgres:cactus@cactus-db/cactus"
SHADOW_DATABASE_URL="postgres://postgres:cactus@cactus-db/cactus_shadow"
ROOT_DATABASE_URL="postgres://postgres:cactus@localhost/postgres"
```

then run with

```bash
docker compose up -d --build
```

### agent

> WIP, no configuration yet

see [./agent/README.md].

In short:

```bash
cd agent
uv run python src/main.py
```

## Interfaces

- project management

  - create project
  - store archives
  - request/cancel renders

- Renders Management:

  - estimation

    - see graph of WU per frame
    - estimation of total WU for the whole render, and ETA via workers count and WUPM rating
    - list of machines working on the renders and their WUPM rating
    - enable/disable own workers
    - enable other people's workers, and set prio

  - get images for specific frames, and total render once finished

- interface to accept to run a render on your machine
  - in the future, inspect the blend file ?
- mobile app for making renders ? vs only web app
- workers management
  - see list of own workers, see WUPM, stats, other
  - generally enable / disable own workers
  - hall of WU fame
    - bestest contributors (WU vs time)
      - person + machine
    - longest rendered frame (WU vs time)
    - longest rendered task (WU vs time)

## estimation

sampling close frames for every worker in different parts of the timeline

- multiple close frame to compare WUPM score for all worker
- multiple different parts of the timeline to have a better estimation of the general project

## Prio

- credits pay WU
- renderers are paid in credits for WU
- priorities are set by changing the price of the WU

## Model

- User

  - username
  - credits

- Invitations
  - user_from
  - email
  - used_by

- Projects

  - author
  - name

- Archives

  - hash
  - url

- Renders

  - frames from-to
  - archive
    - project (through archive)

- RenderRequestAck (find better name, for users to mark that they accept a specific render task)

  - render
  - user

- Results

  - author
  - worker
  - image
  - render_time

- worker
  - name
  - owner
  - enabled
  - WUPM (work unit per minute)
