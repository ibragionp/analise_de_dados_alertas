CREATE TABLE contatos(
	contato_id INTEGER PRIMARY KEY,
	contato_nome VARCHAR(100) NOT NULL
);

CREATE TABLE telefones(
	telefone_id INTEGER PRIMARY KEY,
	contato_id INTEGER NOT NULL,
	telefone_ddi INTEGER NOT NULL,
	telefone_ddd INTEGER NOT NULL,
	telefone_numero INTEGER NOT NULL,
	FOREIGN KEY (telefone_contato_id) REFERENCES contatos (contato_id)	
);

CREATE TABLE emails(
	email_id INTEGER PRIMARY KEY,
	email_endereco VARCHAR(100) NOT NULL,
	contato_id INTEGER NOT NULL,
	FOREIGN KEY (contato_id) REFERENCES contatos (contato_id)
);
	
CREATE TABLE tipos(
	tipo_id INTEGER PRIMARY KEY,
	tipo_descricao VARCHAR(50) NOT NULL
);
	
CREATE TABLE localidades(
	localidade_id INTEGER PRIMARY KEY,
	localidade_descricao VARCHAR(200) NOT NULL
);

CREATE TABLE periodos(
	periodo_id INTEGER PRIMARY KEY,
	periodo_hora_inicial TIME WITHOUT TIME ZONE NOT NULL,
	periodo_hora_final TIME WITHOUT TIME ZONE NOT NULL,
	periodo_dia VARCHAR(10)
);
	
CREATE TABLE envios_alertas(
	envio_alerta_id INTEGER PRIMARY KEY,
	contato_id INTEGER NOT NULL,
	telefone_id INTEGER NOT NULL,
	email_id INTEGER NOT NULL,
	localidade_id INTEGER NOT NULL,
	tipo_id INTEGER NOT NULL,
	periodo_id INTEGER NOT NULL,
	envio_alerta_descricao VARCHAR(30),
	FOREIGN KEY (contato_id) REFERENCES contatos (contato_id),
	FOREIGN KEY (telefone_id) REFERENCES telefones (telefone_id),
	FOREIGN KEY (email_id) REFERENCES emails (email_id),
	FOREIGN KEY (localidade_id) REFERENCES localidades (localidade_id),
	FOREIGN KEY (tipo_id) REFERENCES tipos (tipo_id)
	FOREIGN KEY (periodo_id) REFERENCES periodos (periodo_id)
);