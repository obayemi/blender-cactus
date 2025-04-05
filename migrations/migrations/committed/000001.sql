--! Previous: -
--! Hash: sha1:c1f943829604c05a5003d035e2f961a9e6cd7f9e

-- cleanup
drop table if exists public.renders;
drop table if exists public.frame_requests;
drop table if exists public.render_requests;
drop table if exists public.archives;
drop table if exists public.projects;
drop table if exists public.agents;
drop table if exists public.invitations;
drop table if exists public.users;

drop function if exists set_created_at;

-- setup


-- 
-- helpers
-- 
create function set_created_at()
returns trigger as $$
begin
    NEW.created_at := now();
    return NEW;
end;
$$ language plpgsql;


-- 
-- users
-- 
create table public.users (
    created_at timestamptz not null default now(),
    id integer primary key generated always as identity,
    username varchar(100) unique not null,
    is_superuser boolean not null default false
);

create trigger users_created_at
    before insert on public.users
    for each row
    execute function set_created_at();

comment on constraint "users_username_key" on public.users is '@error user already exists with this username';


-- 
-- invitations
-- 
create table public.invitations (
    created_at timestamptz not null default now(),
    uuid uuid primary key default gen_random_uuid(),
    email varchar(200),
    created_by integer not null references public.users(id) on delete CASCADE
);

create trigger invitations_created_at
    before insert on public.invitations
    for each row
    execute function set_created_at();

create index invitation_created_by on public.invitations(created_by);


--
-- agents
--
create table public.agents (
    created_at timestamptz not null default now(),
    id integer primary key generated always as identity,
    name varchar(150) not null,
    owner_id integer not null references public.users(id) on delete CASCADE
);

create trigger agents_created_at
    before insert on public.agents
    for each row
    execute function set_created_at();

create index agents_owner_id on public.agents(owner_id);


--
-- projects
-- 
create table public.projects (
    created_at timestamptz not null default now(),
    id integer primary key generated always as identity,
    name varchar(100) not null,
    description text,

    owner_id integer not null references public.users(id) ON DELETE CASCADE
);

create trigger projects_created_at
    before insert on public.projects
    for each row
    execute function set_created_at();

create index project_name on projects(name);
create index project_owner_id on projects(owner_id);


--
-- archives
-- 
create table public.archives (
    created_at timestamptz not null default now(),
    id integer primary key generated always as identity,
    project_id integer not null references public.projects(id),
    url varchar(200) not null
);

create trigger archives_created_at
    before insert on public.archives
    for each row
    execute function set_created_at();

create index archives_project_id on public.archives(project_id);


--
-- render_requests
-- 
create table public.render_requests (
    created_at timestamptz not null default now(),
    id integer primary key generated always as identity,
    archive_id integer not null references public.archives(id),
    frame_from integer not null,
    frame_count integer not null
);

create trigger render_requests_created_at
    before insert on public.render_requests
    for each row
    execute function set_created_at();

create index render_requests_archive_id on public.render_requests(archive_id);


--
-- assigned frame
-- 
create table public.frame_requests (
    created_at timestamptz not null default now(),
    id integer primary key generated always as identity,
    agent_id integer not null references public.agents(id),
    render_request_id integer not null references public.render_requests(id),
    frame_number integer not null
);

create trigger frame_requests_created_at
    before insert on public.frame_requests
    for each row
    execute function set_created_at();

create index frame_requests_agent_id on public.frame_requests(agent_id);
create index frame_requests_render_requests_id on public.frame_requests(render_request_id);


--
-- renders
-- 
create table public.renders (
    created_at timestamptz not null default now(),
    id integer primary key generated always as identity,
    frame_request_id integer not null references public.render_requests(id),
    time_taken interval default interval '12 minutes 4 seconds',
    url varchar(200) not null
);

create trigger renders_created_at
    before insert on public.renders
    for each row
    execute function set_created_at();

create index render_requests_request_id on public.renders(frame_request_id);
