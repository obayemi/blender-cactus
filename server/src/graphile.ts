import constraint_error_tag_plugin from "@graphile-contrib/constraint-error-tags";
import PgSimplifyInflectorPlugin from "@graphile-contrib/pg-simplify-inflector";
import { postgraphile, makePluginHook } from "postgraphile";
import PgPubsub from "@graphile/pg-pubsub";

const { ConstraintErrorTagsPlugin, handleErrors } = constraint_error_tag_plugin;
const PgPubsubPluginHook = makePluginHook([PgPubsub]);

const graphileOptions = {
  pluginHook: PgPubsubPluginHook,
  appendPlugins: [PgSimplifyInflectorPlugin, ConstraintErrorTagsPlugin],
  handleErrors: (errors) => handleErrors(errors),
  watchPg: true,
  graphiql: true,
  enhanceGraphiql: true,
  subscriptions: true,
  simpleSubscriptions: true,
  pgStrictFunctions: true,
  ignoreRBAC: false,
  ignoreIndexes: false,
  simpleCollections: "both",
};

export function graphile_middleware() {
  return postgraphile(process.env.DATABASE_URL, "public", graphileOptions);
}
// -- cleanup

// drop view if exists public.special_foos;
// drop table if exists public.foo;

// -- setup

// create or replace function generate_stuff(username text, project_url text)
// returns void as $$
// declare
//     new_user_id integer;
//     new_agent_id integer;
//     new_project_id integer;
//     new_archive_id integer;
//     new_render_request_id integer;
// begin
//     -- create user
//     insert into public.users
//         (username)
//         values (username)
//         returning id into new_user_id;

//     -- create an agent for them
//     insert into public.agents
//         (name, owner_id)
//         values (username || '_agent', new_user_id)
//         returning id into new_agent_id;

//     -- create a project for them
//     insert into public.projects
//         (name, owner_id)
//         values (username || '''s cool project', new_user_id)
//         returning id into new_project_id;

//     -- create an archive for it with url in arguments
//     insert into public.archives
//         (project_id, url)
//         values (new_project_id, project_url)
//         returning id into new_archive_id;

//     -- request a render of the first frame
//     insert into public.render_requests
//         (archive_id, frame_from, frame_count)
//         values (new_archive_id, 1, 1)
//         returning id into new_render_request_id;

//     -- assign the frame to the user's agent
//     insert into public.frame_requests
//         (render_request_id, agent_id, frame_number)
//         values (new_render_request_id, new_agent_id, 1);
// end;
// $$ language plpgsql strict;

// create table public.foo (
//   id integer primary key generated always as identity,
//   created_at timestamp not null default now(),
//   agent_id integer not null references public.agents(id) on delete cascade
// );

// create index foo_agent_id on public.foo(agent_id);

// create view public.special_foos as
//     select created_at, agent_id
//     from public.foo
//     where id < 10;

// ALTER TABLE public.users SET SCHEMA private;
// drop view if exists public.users;

// create view public.users as
//     select
//         id, username
//         from private.users;
