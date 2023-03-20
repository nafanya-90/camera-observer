--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 14.7 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: cameras_db_username
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO cameras_db_username;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: cameras_db_username
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cameras; Type: TABLE; Schema: public; Owner: cameras_db_username
--

CREATE TABLE public.cameras (
    id integer NOT NULL,
    is_active boolean,
    name character varying(50),
    location character varying(50),
    location_details character varying(255),
    url character varying(255)
);


ALTER TABLE public.cameras OWNER TO cameras_db_username;

--
-- Name: cameras_id_seq; Type: SEQUENCE; Schema: public; Owner: cameras_db_username
--

CREATE SEQUENCE public.cameras_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cameras_id_seq OWNER TO cameras_db_username;

--
-- Name: cameras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cameras_db_username
--

ALTER SEQUENCE public.cameras_id_seq OWNED BY public.cameras.id;


--
-- Name: cameras id; Type: DEFAULT; Schema: public; Owner: cameras_db_username
--

ALTER TABLE ONLY public.cameras ALTER COLUMN id SET DEFAULT nextval('public.cameras_id_seq'::regclass);


--
-- Data for Name: cameras; Type: TABLE DATA; Schema: public; Owner: cameras_db_username
--

COPY public.cameras (id, is_active, name, location, location_details, url) FROM stdin;
1	f	Camera 1	Old Trafford	Stratford End	http://devimages.apple.com/iphone/samples/bipbop/gear1/prog_index.m3u8
2	f	Camera 2	Old Trafford	Sir Alex Ferguson Stand	http://devimages.apple.com/iphone/samples/bipbop/gear1/prog_index.m3u8
\.


--
-- Name: cameras_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cameras_db_username
--

SELECT pg_catalog.setval('public.cameras_id_seq', 2, true);


--
-- Name: cameras cameras_pkey; Type: CONSTRAINT; Schema: public; Owner: cameras_db_username
--

ALTER TABLE ONLY public.cameras
    ADD CONSTRAINT cameras_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

