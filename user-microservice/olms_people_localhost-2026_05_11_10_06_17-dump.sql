--
-- PostgreSQL database dump
--

\restrict GURuahXb7za7aK7dk7kjLa9U1Yobmkq9AzKLq2k8DHhCGVoc8Fpylx3IKdsgwh0

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 18.3

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
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: olms_people_keeper
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO olms_people_keeper;

--
-- Name: auth_refresh_sessions; Type: TABLE; Schema: public; Owner: olms_people_keeper
--

CREATE TABLE public.auth_refresh_sessions (
    id bigint NOT NULL,
    token_id uuid NOT NULL,
    user_id uuid NOT NULL,
    refresh_token_hash character varying(255) NOT NULL,
    issued_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone,
    replaced_by_token_id uuid
);


ALTER TABLE public.auth_refresh_sessions OWNER TO olms_people_keeper;

--
-- Name: auth_refresh_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: olms_people_keeper
--

CREATE SEQUENCE public.auth_refresh_sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_refresh_sessions_id_seq OWNER TO olms_people_keeper;

--
-- Name: auth_refresh_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: olms_people_keeper
--

ALTER SEQUENCE public.auth_refresh_sessions_id_seq OWNED BY public.auth_refresh_sessions.id;


--
-- Name: file_metadata; Type: TABLE; Schema: public; Owner: olms_people_keeper
--

CREATE TABLE public.file_metadata (
    id uuid NOT NULL,
    name character varying NOT NULL,
    file_group character varying NOT NULL,
    mime_type character varying NOT NULL,
    extension character varying NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.file_metadata OWNER TO olms_people_keeper;

--
-- Name: user_authorities; Type: TABLE; Schema: public; Owner: olms_people_keeper
--

CREATE TABLE public.user_authorities (
    id bigint NOT NULL,
    authority character varying NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.user_authorities OWNER TO olms_people_keeper;

--
-- Name: user_authorities_id_seq; Type: SEQUENCE; Schema: public; Owner: olms_people_keeper
--

CREATE SEQUENCE public.user_authorities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_authorities_id_seq OWNER TO olms_people_keeper;

--
-- Name: user_authorities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: olms_people_keeper
--

ALTER SEQUENCE public.user_authorities_id_seq OWNED BY public.user_authorities.id;


--
-- Name: user_passwords; Type: TABLE; Schema: public; Owner: olms_people_keeper
--

CREATE TABLE public.user_passwords (
    id uuid NOT NULL,
    password character varying NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.user_passwords OWNER TO olms_people_keeper;

--
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: olms_people_keeper
--

CREATE TABLE public.user_profiles (
    id bigint NOT NULL,
    first_name character varying NOT NULL,
    middle_name character varying NOT NULL,
    last_name character varying NOT NULL,
    age integer NOT NULL,
    gender character varying NOT NULL,
    user_id uuid NOT NULL,
    picture_id uuid,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.user_profiles OWNER TO olms_people_keeper;

--
-- Name: user_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: olms_people_keeper
--

CREATE SEQUENCE public.user_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_profiles_id_seq OWNER TO olms_people_keeper;

--
-- Name: user_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: olms_people_keeper
--

ALTER SEQUENCE public.user_profiles_id_seq OWNED BY public.user_profiles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: olms_people_keeper
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    login character varying NOT NULL,
    email character varying NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.users OWNER TO olms_people_keeper;

--
-- Name: auth_refresh_sessions id; Type: DEFAULT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.auth_refresh_sessions ALTER COLUMN id SET DEFAULT nextval('public.auth_refresh_sessions_id_seq'::regclass);


--
-- Name: user_authorities id; Type: DEFAULT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_authorities ALTER COLUMN id SET DEFAULT nextval('public.user_authorities_id_seq'::regclass);


--
-- Name: user_profiles id; Type: DEFAULT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_profiles ALTER COLUMN id SET DEFAULT nextval('public.user_profiles_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: olms_people_keeper
--

COPY public.alembic_version (version_num) FROM stdin;
20260412_1200_auth_table
\.


--
-- Data for Name: auth_refresh_sessions; Type: TABLE DATA; Schema: public; Owner: olms_people_keeper
--

COPY public.auth_refresh_sessions (id, token_id, user_id, refresh_token_hash, issued_at, expires_at, revoked_at, replaced_by_token_id) FROM stdin;
1	ea748044-000b-48e6-8186-928bf88fab2a	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	c85028981bf05d53b326106b60eebed923332ccf3b4ece0b2314e230af4bd066	2026-05-10 04:29:33.25794+00	2026-06-09 04:29:32.598584+00	2026-05-10 04:48:00.921879+00	\N
2	58b33539-8139-4399-a3b6-57d785ad5220	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	73ca62d6c6784a7f62de922c8a99373af48b1d33db44caf5a4cb77690b0980b3	2026-05-10 04:48:40.534602+00	2026-06-09 04:48:40.534574+00	\N	\N
3	7491e2ee-8fa8-43b0-9b46-7c752268814b	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	5fa901c091fe976cb08b7f83bedf97aaf3833b1b23aa62a4e34f8a6ee1d54c64	2026-05-10 05:17:22.142158+00	2026-06-09 05:17:22.142133+00	2026-05-10 05:24:42.697896+00	\N
4	d19f5a40-a67c-47b5-9b1e-74372f6bdb7d	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	9d3ca51754aee4e456898ac2d811b7acd41728274923252501d9aeba0e7b0d12	2026-05-10 05:24:56.640962+00	2026-06-09 05:24:56.640923+00	2026-05-10 05:36:50.279196+00	\N
5	cd6845c9-3a0c-4352-8c43-cf6132d01956	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	e37ed58c60d1861cf4f7bf6e4899b554031200e2dfb84de005b3f86fa67941f3	2026-05-10 05:36:59.586966+00	2026-06-09 05:36:59.586943+00	2026-05-10 07:48:49.817841+00	\N
6	4bc78be4-7647-4da6-96bb-95e463661446	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	bfda883efdb30269601d51599ecde1408984f1b88dde147a4d9769e591b5c66c	2026-05-10 07:49:08.261523+00	2026-06-09 07:49:08.261495+00	2026-05-10 08:55:32.343074+00	\N
7	fdedf19d-0bd6-4ee6-9cff-7abce91128d1	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	4fa04d05c21fa95c683b66b62742405fc49c9c6d1392bdd079c81b5d6835ad37	2026-05-10 08:55:39.935564+00	2026-06-09 08:55:39.93553+00	\N	\N
\.


--
-- Data for Name: file_metadata; Type: TABLE DATA; Schema: public; Owner: olms_people_keeper
--

COPY public.file_metadata (id, name, file_group, mime_type, extension, created_at, updated_at, is_active) FROM stdin;
\.


--
-- Data for Name: user_authorities; Type: TABLE DATA; Schema: public; Owner: olms_people_keeper
--

COPY public.user_authorities (id, authority, user_id, created_at, updated_at, is_active) FROM stdin;
1	ADMIN	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	2026-05-10 18:53:26.208+00	2026-05-10 18:53:28.564+00	t
\.


--
-- Data for Name: user_passwords; Type: TABLE DATA; Schema: public; Owner: olms_people_keeper
--

COPY public.user_passwords (id, password, user_id, created_at, updated_at, is_active) FROM stdin;
d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	$2a$12$bOFOjayZIhoMYxyBFLtPjOEhDeOs7sjzDI.Ny/duvBbITQS8b1hSS	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	2026-05-10 14:29:06.515+00	2026-05-10 14:29:08.276+00	t
\.


--
-- Data for Name: user_profiles; Type: TABLE DATA; Schema: public; Owner: olms_people_keeper
--

COPY public.user_profiles (id, first_name, middle_name, last_name, age, gender, user_id, picture_id, created_at, updated_at, is_active) FROM stdin;
1	Иван	Сидорович	Петров	25	М	d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	\N	2026-05-10 14:40:26.176+00	2026-05-10 14:40:27.712+00	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: olms_people_keeper
--

COPY public.users (id, login, email, created_at, updated_at, is_active) FROM stdin;
d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619	root	test@mail.com	2026-05-10 14:28:23.556+00	2026-05-10 14:28:29.084+00	t
\.


--
-- Name: auth_refresh_sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: olms_people_keeper
--

SELECT pg_catalog.setval('public.auth_refresh_sessions_id_seq', 7, true);


--
-- Name: user_authorities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: olms_people_keeper
--

SELECT pg_catalog.setval('public.user_authorities_id_seq', 1, true);


--
-- Name: user_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: olms_people_keeper
--

SELECT pg_catalog.setval('public.user_profiles_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: auth_refresh_sessions auth_refresh_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.auth_refresh_sessions
    ADD CONSTRAINT auth_refresh_sessions_pkey PRIMARY KEY (id);


--
-- Name: file_metadata file_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.file_metadata
    ADD CONSTRAINT file_metadata_pkey PRIMARY KEY (id);


--
-- Name: auth_refresh_sessions uq_auth_refresh_sessions_token_id; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.auth_refresh_sessions
    ADD CONSTRAINT uq_auth_refresh_sessions_token_id UNIQUE (token_id);


--
-- Name: users uq_users_email; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_email UNIQUE (email);


--
-- Name: users uq_users_login; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_login UNIQUE (login);


--
-- Name: user_authorities user_authorities_pkey; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_authorities
    ADD CONSTRAINT user_authorities_pkey PRIMARY KEY (id);


--
-- Name: user_passwords user_passwords_pkey; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_passwords
    ADD CONSTRAINT user_passwords_pkey PRIMARY KEY (id);


--
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_auth_refresh_sessions_expires_at; Type: INDEX; Schema: public; Owner: olms_people_keeper
--

CREATE INDEX ix_auth_refresh_sessions_expires_at ON public.auth_refresh_sessions USING btree (expires_at);


--
-- Name: ix_auth_refresh_sessions_refresh_token_hash; Type: INDEX; Schema: public; Owner: olms_people_keeper
--

CREATE INDEX ix_auth_refresh_sessions_refresh_token_hash ON public.auth_refresh_sessions USING btree (refresh_token_hash);


--
-- Name: ix_auth_refresh_sessions_user_id; Type: INDEX; Schema: public; Owner: olms_people_keeper
--

CREATE INDEX ix_auth_refresh_sessions_user_id ON public.auth_refresh_sessions USING btree (user_id);


--
-- Name: ix_user_authorities_user_id; Type: INDEX; Schema: public; Owner: olms_people_keeper
--

CREATE INDEX ix_user_authorities_user_id ON public.user_authorities USING btree (user_id);


--
-- Name: ix_user_passwords_user_id; Type: INDEX; Schema: public; Owner: olms_people_keeper
--

CREATE INDEX ix_user_passwords_user_id ON public.user_passwords USING btree (user_id);


--
-- Name: ix_user_profiles_picture_id; Type: INDEX; Schema: public; Owner: olms_people_keeper
--

CREATE INDEX ix_user_profiles_picture_id ON public.user_profiles USING btree (picture_id);


--
-- Name: ix_user_profiles_user_id; Type: INDEX; Schema: public; Owner: olms_people_keeper
--

CREATE INDEX ix_user_profiles_user_id ON public.user_profiles USING btree (user_id);


--
-- Name: auth_refresh_sessions fk_auth_refresh_sessions_replaced_by_token_id; Type: FK CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.auth_refresh_sessions
    ADD CONSTRAINT fk_auth_refresh_sessions_replaced_by_token_id FOREIGN KEY (replaced_by_token_id) REFERENCES public.auth_refresh_sessions(token_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: auth_refresh_sessions fk_auth_refresh_sessions_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.auth_refresh_sessions
    ADD CONSTRAINT fk_auth_refresh_sessions_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_authorities fk_user_authorities_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_authorities
    ADD CONSTRAINT fk_user_authorities_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_passwords fk_user_passwords_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_passwords
    ADD CONSTRAINT fk_user_passwords_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_profiles fk_user_profiles_picture_id_file_metadata; Type: FK CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT fk_user_profiles_picture_id_file_metadata FOREIGN KEY (picture_id) REFERENCES public.file_metadata(id);


--
-- Name: user_profiles fk_user_profiles_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: olms_people_keeper
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT fk_user_profiles_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict GURuahXb7za7aK7dk7kjLa9U1Yobmkq9AzKLq2k8DHhCGVoc8Fpylx3IKdsgwh0

