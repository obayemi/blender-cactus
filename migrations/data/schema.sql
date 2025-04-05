--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg110+2)
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: set_created_at(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.set_created_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    NEW.created_at := now();
    return NEW;
end;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.agents (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    owner_id integer NOT NULL
);


--
-- Name: agents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.agents ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.agents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: archives; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.archives (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    project_id integer NOT NULL,
    url character varying(200) NOT NULL
);


--
-- Name: archives_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.archives ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.archives_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: frame_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frame_requests (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    agent_id integer NOT NULL,
    render_request_id integer NOT NULL,
    frame_number integer NOT NULL
);


--
-- Name: frame_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.frame_requests ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.frame_requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: invitations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.invitations (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    uuid uuid DEFAULT gen_random_uuid() NOT NULL,
    email character varying(200),
    created_by integer NOT NULL
);


--
-- Name: projects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.projects (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    owner_id integer NOT NULL
);


--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.projects ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: render_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.render_requests (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    archive_id integer NOT NULL,
    frame_from integer NOT NULL,
    frame_count integer NOT NULL
);


--
-- Name: render_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.render_requests ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.render_requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: renders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.renders (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    frame_request_id integer NOT NULL,
    time_taken interval DEFAULT '00:12:04'::interval,
    url character varying(200) NOT NULL
);


--
-- Name: renders_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.renders ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.renders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    is_superuser boolean DEFAULT false NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: agents agents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_pkey PRIMARY KEY (id);


--
-- Name: archives archives_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.archives
    ADD CONSTRAINT archives_pkey PRIMARY KEY (id);


--
-- Name: frame_requests frame_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frame_requests
    ADD CONSTRAINT frame_requests_pkey PRIMARY KEY (id);


--
-- Name: invitations invitations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invitations
    ADD CONSTRAINT invitations_pkey PRIMARY KEY (uuid);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: render_requests render_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.render_requests
    ADD CONSTRAINT render_requests_pkey PRIMARY KEY (id);


--
-- Name: renders renders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renders
    ADD CONSTRAINT renders_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: CONSTRAINT users_username_key ON users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT users_username_key ON public.users IS '@error user already exists with this username';


--
-- Name: agents_owner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX agents_owner_id ON public.agents USING btree (owner_id);


--
-- Name: archives_project_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX archives_project_id ON public.archives USING btree (project_id);


--
-- Name: frame_requests_agent_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frame_requests_agent_id ON public.frame_requests USING btree (agent_id);


--
-- Name: frame_requests_render_requests_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frame_requests_render_requests_id ON public.frame_requests USING btree (render_request_id);


--
-- Name: invitation_created_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX invitation_created_by ON public.invitations USING btree (created_by);


--
-- Name: project_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX project_name ON public.projects USING btree (name);


--
-- Name: project_owner_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX project_owner_id ON public.projects USING btree (owner_id);


--
-- Name: render_requests_archive_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX render_requests_archive_id ON public.render_requests USING btree (archive_id);


--
-- Name: render_requests_request_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX render_requests_request_id ON public.renders USING btree (frame_request_id);


--
-- Name: agents agents_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER agents_created_at BEFORE INSERT ON public.agents FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: archives archives_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER archives_created_at BEFORE INSERT ON public.archives FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: frame_requests frame_requests_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER frame_requests_created_at BEFORE INSERT ON public.frame_requests FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: invitations invitations_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER invitations_created_at BEFORE INSERT ON public.invitations FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: projects projects_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER projects_created_at BEFORE INSERT ON public.projects FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: render_requests render_requests_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER render_requests_created_at BEFORE INSERT ON public.render_requests FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: renders renders_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER renders_created_at BEFORE INSERT ON public.renders FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: users users_created_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER users_created_at BEFORE INSERT ON public.users FOR EACH ROW EXECUTE FUNCTION public.set_created_at();


--
-- Name: agents agents_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: archives archives_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.archives
    ADD CONSTRAINT archives_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: frame_requests frame_requests_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frame_requests
    ADD CONSTRAINT frame_requests_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id);


--
-- Name: frame_requests frame_requests_render_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frame_requests
    ADD CONSTRAINT frame_requests_render_request_id_fkey FOREIGN KEY (render_request_id) REFERENCES public.render_requests(id);


--
-- Name: invitations invitations_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invitations
    ADD CONSTRAINT invitations_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: projects projects_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: render_requests render_requests_archive_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.render_requests
    ADD CONSTRAINT render_requests_archive_id_fkey FOREIGN KEY (archive_id) REFERENCES public.archives(id);


--
-- Name: renders renders_frame_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renders
    ADD CONSTRAINT renders_frame_request_id_fkey FOREIGN KEY (frame_request_id) REFERENCES public.render_requests(id);


--
-- PostgreSQL database dump complete
--

