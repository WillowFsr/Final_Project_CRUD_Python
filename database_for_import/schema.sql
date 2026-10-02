--
-- PostgreSQL database dump
--

\restrict Ly4Pe25Y8mthshSt3fxfHprVBwKs4t3XyzaK6yxaY46saWOgibzj1Nc51sgimIW

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: carrinho; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.carrinho (
    id_carrinho integer NOT NULL,
    id_cli integer CONSTRAINT carrinho_id_cliente_not_null NOT NULL
);


--
-- Name: carrinho_id_carrinho_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.carrinho_id_carrinho_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: carrinho_id_carrinho_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.carrinho_id_carrinho_seq OWNED BY public.carrinho.id_carrinho;


--
-- Name: cartao; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cartao (
    id_cartao integer NOT NULL,
    id_cli integer NOT NULL,
    numero character varying(30) NOT NULL,
    validade date DEFAULT CURRENT_DATE NOT NULL,
    cvv character varying(10) NOT NULL,
    bandeira character varying(50) NOT NULL,
    saldo numeric(10,2) DEFAULT 0.00 NOT NULL,
    CONSTRAINT ck_cartao_saldo CHECK ((saldo >= (0)::numeric))
);


--
-- Name: cartao_id_cartao_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cartao_id_cartao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cartao_id_cartao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cartao_id_cartao_seq OWNED BY public.cartao.id_cartao;


--
-- Name: cliente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cliente (
    id_cli integer NOT NULL,
    nome character varying(255) NOT NULL,
    idade integer NOT NULL,
    endereco character varying(255) NOT NULL,
    nacionalidade character varying(100) NOT NULL
);


--
-- Name: cliente_id_cli_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cliente_id_cli_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cliente_id_cli_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cliente_id_cli_seq OWNED BY public.cliente.id_cli;


--
-- Name: historico_compra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.historico_compra (
    id_historico integer NOT NULL,
    id_cli integer NOT NULL,
    valor_total numeric(10,2) NOT NULL,
    data_compra timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_historico_valor CHECK ((valor_total >= (0)::numeric))
);


--
-- Name: historico_compra_id_historico_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.historico_compra_id_historico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: historico_compra_id_historico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.historico_compra_id_historico_seq OWNED BY public.historico_compra.id_historico;


--
-- Name: item_historico; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.item_historico (
    id_item integer NOT NULL,
    id_historico integer NOT NULL,
    id_prod integer NOT NULL,
    quantidade integer NOT NULL,
    preco_momento numeric(10,2) NOT NULL,
    CONSTRAINT ck_item_historico_preco CHECK ((preco_momento >= (0)::numeric)),
    CONSTRAINT ck_item_historico_quantidade CHECK ((quantidade > 0))
);


--
-- Name: item_historico_id_item_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.item_historico_id_item_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: item_historico_id_item_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.item_historico_id_item_seq OWNED BY public.item_historico.id_item;


--
-- Name: produto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.produto (
    id_prod integer NOT NULL,
    nome character varying(255) NOT NULL,
    preco numeric(10,2) NOT NULL,
    descricao text,
    estoque smallint DEFAULT 0 NOT NULL,
    CONSTRAINT ck_produto_estoque CHECK ((estoque >= 0)),
    CONSTRAINT ck_produto_preco CHECK ((preco >= (0)::numeric))
);


--
-- Name: produto_carrinho; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.produto_carrinho (
    id_produto_carrinho integer NOT NULL,
    id_carrinho integer NOT NULL,
    id_prod integer NOT NULL,
    quantidade integer NOT NULL,
    CONSTRAINT ck_produto_carrinho_quantidade CHECK ((quantidade > 0))
);


--
-- Name: produto_carrinho_id_produto_carrinho_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.produto_carrinho_id_produto_carrinho_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: produto_carrinho_id_produto_carrinho_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.produto_carrinho_id_produto_carrinho_seq OWNED BY public.produto_carrinho.id_produto_carrinho;


--
-- Name: produto_id_prod_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.produto_id_prod_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: produto_id_prod_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.produto_id_prod_seq OWNED BY public.produto.id_prod;


--
-- Name: carrinho id_carrinho; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrinho ALTER COLUMN id_carrinho SET DEFAULT nextval('public.carrinho_id_carrinho_seq'::regclass);


--
-- Name: cartao id_cartao; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cartao ALTER COLUMN id_cartao SET DEFAULT nextval('public.cartao_id_cartao_seq'::regclass);


--
-- Name: cliente id_cli; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id_cli SET DEFAULT nextval('public.cliente_id_cli_seq'::regclass);


--
-- Name: historico_compra id_historico; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_compra ALTER COLUMN id_historico SET DEFAULT nextval('public.historico_compra_id_historico_seq'::regclass);


--
-- Name: item_historico id_item; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.item_historico ALTER COLUMN id_item SET DEFAULT nextval('public.item_historico_id_item_seq'::regclass);


--
-- Name: produto id_prod; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produto ALTER COLUMN id_prod SET DEFAULT nextval('public.produto_id_prod_seq'::regclass);


--
-- Name: produto_carrinho id_produto_carrinho; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produto_carrinho ALTER COLUMN id_produto_carrinho SET DEFAULT nextval('public.produto_carrinho_id_produto_carrinho_seq'::regclass);


--
-- Name: carrinho carrinho_id_cliente_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrinho
    ADD CONSTRAINT carrinho_id_cliente_key UNIQUE (id_cli);


--
-- Name: carrinho carrinho_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrinho
    ADD CONSTRAINT carrinho_pkey PRIMARY KEY (id_carrinho);


--
-- Name: cartao cartao_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cartao
    ADD CONSTRAINT cartao_pkey PRIMARY KEY (id_cartao);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id_cli);


--
-- Name: historico_compra historico_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_compra
    ADD CONSTRAINT historico_compra_pkey PRIMARY KEY (id_historico);


--
-- Name: item_historico item_historico_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.item_historico
    ADD CONSTRAINT item_historico_pkey PRIMARY KEY (id_item);


--
-- Name: produto_carrinho produto_carrinho_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produto_carrinho
    ADD CONSTRAINT produto_carrinho_pkey PRIMARY KEY (id_produto_carrinho);


--
-- Name: produto produto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produto
    ADD CONSTRAINT produto_pkey PRIMARY KEY (id_prod);


--
-- Name: produto_carrinho uq_produto_carrinho; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produto_carrinho
    ADD CONSTRAINT uq_produto_carrinho UNIQUE (id_carrinho, id_prod);


--
-- Name: carrinho carrinho_id_cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carrinho
    ADD CONSTRAINT carrinho_id_cliente_fkey FOREIGN KEY (id_cli) REFERENCES public.cliente(id_cli) ON DELETE CASCADE;


--
-- Name: cartao cartao_id_cli_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cartao
    ADD CONSTRAINT cartao_id_cli_fkey FOREIGN KEY (id_cli) REFERENCES public.cliente(id_cli) ON DELETE CASCADE;


--
-- Name: historico_compra historico_compra_id_cli_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_compra
    ADD CONSTRAINT historico_compra_id_cli_fkey FOREIGN KEY (id_cli) REFERENCES public.cliente(id_cli) ON DELETE CASCADE;


--
-- Name: item_historico item_historico_id_historico_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.item_historico
    ADD CONSTRAINT item_historico_id_historico_fkey FOREIGN KEY (id_historico) REFERENCES public.historico_compra(id_historico) ON DELETE CASCADE;


--
-- Name: item_historico item_historico_id_prod_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.item_historico
    ADD CONSTRAINT item_historico_id_prod_fkey FOREIGN KEY (id_prod) REFERENCES public.produto(id_prod);


--
-- Name: produto_carrinho produto_carrinho_id_carrinho_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produto_carrinho
    ADD CONSTRAINT produto_carrinho_id_carrinho_fkey FOREIGN KEY (id_carrinho) REFERENCES public.carrinho(id_carrinho) ON DELETE CASCADE;


--
-- Name: produto_carrinho produto_carrinho_id_prod_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.produto_carrinho
    ADD CONSTRAINT produto_carrinho_id_prod_fkey FOREIGN KEY (id_prod) REFERENCES public.produto(id_prod);


--
-- PostgreSQL database dump complete
--

\unrestrict Ly4Pe25Y8mthshSt3fxfHprVBwKs4t3XyzaK6yxaY46saWOgibzj1Nc51sgimIW

