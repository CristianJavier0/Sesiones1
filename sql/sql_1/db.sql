--Crear la tabla rol, hacer los registros 
-- y hacer la consulta de esa tabla
CREATE TABLE rol (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(7) NOT NULL
);

Insert into rol (nombre_rol)
values
('user'),
('admin');

select * from rol;

-- Tabla de Usuarios
create extension pgcrypto
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre_U VARCHAR(80) NOT NULL,
    apellido_PU VARCHAR(50) NOT NULL,
    apellido_MU VARCHAR(50),
    fecha_registro_U DATE DEFAULT CURRENT_DATE NOT NULL,
    correo_U TEXT UNIQUE NOT NULL,
    contrasena_U VARCHAR(250) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol (id_rol)
);

INSERT INTO usuario (
    nombre_U,
    apellido_PU,
    apellido_MU,
    correo_U,
    contrasena_U,
    id_rol
)
VALUES
-- Usuario tipo 'user'
('Carlos', 'Ramírez', 'López', 'carlos.ramirez@example.com', pgp_sym_encrypt('1234','PELUSA'), 1),
('Jesus Ignacio', 'Carcamo', 'Cortez', 'Ignacio@example.com', pgp_sym_encrypt('1234','MARVEL'), 1),
-- Usuario tipo 'admin'
('Yunue Osmara', 'Hernandez', 'Solis', 'Yunue@example.com', pgp_sym_encrypt('1234','GATO'), 2),
('Oswaldo Uriel', 'Trejo', 'Lopez', 'Oswaldo@example.com', pgp_sym_encrypt('1234','PERRO'), 2),
('Cristian Javier', 'Rubio', 'Gayosso', 'Cristian@example.com', pgp_sym_encrypt('1234','PASTEL'), 2);

select * from usuario;

-- Paises
CREATE TABLE pais (
    id_pais SERIAL PRIMARY KEY,
    pais_P  VARCHAR(50) NOT NULL
);

Insert into pais (pais_P)
VALUES
('Afghanistan'),
('Albania'),
('Algeria'),
('Andorra'),
('Angola'),
('Antigua and Barbuda'),
('Argentina'),
('Armenia'),
('Australia'),
('Austria'),
('Azerbaijan'),
('Bahamas'),
('Bahrain'),
('Bangladesh'),
('Barbados'),
('Belarus'),
('Belgium'),
('Belize'),
('Benin'),
('Bhutan'),
('Bolivia'),
('Bosnia and Herzegovina'),
('Botswana'),
('Brazil'),
('Brunei'),
('Bulgaria'),
('Burkina Faso'),
('Burundi'),
('Cabo Verde'),
('Cambodia'),
('Cameroon'),
('Canada'),
('Central African Republic'),
('Chad'),
('Chile'),
('China'),
('Colombia'),
('Comoros'),
('Congo (Congo-Brazzaville)'),
('Costa Rica'),
('Côte d''Ivoire'),
('Croatia'),
('Cuba'),
('Cyprus'),
('Czechia (Czech Republic)'),
('Democratic Republic of the Congo'),
('Denmark'),
('Djibouti'),
('Dominica'),
('Dominican Republic'),
('Ecuador'),
('Egypt'),
('El Salvador'),
('Equatorial Guinea'),
('Eritrea'),
('Estonia'),
('Eswatini (fmr. "Swaziland")'),
('Ethiopia'),
('Fiji'),
('Finland'),
('France'),
('Gabon'),
('Gambia'),
('Georgia'),
('Germany'),
('Ghana'),
('Greece'),
('Grenada'),
('Guatemala'),
('Guinea'),
('Guinea-Bissau'),
('Guyana'),
('Haiti'),
('Holy See'),
('Honduras'),
('Hungary'),
('Iceland'),
('India'),
('Indonesia'),
('Iran'),
('Iraq'),
('Ireland'),
('Israel'),
('Italy'),
('Jamaica'),
('Japan'),
('Jordan'),
('Kazakhstan'),
('Kenya'),
('Kiribati'),
('Kuwait'),
('Kyrgyzstan'),
('Laos'),
('Latvia'),
('Lebanon'),
('Lesotho'),
('Liberia'),
('Libya'),
('Liechtenstein'),
('Lithuania'),
('Luxembourg'),
('Madagascar'),
('Malawi'),
('Malaysia'),
('Maldives'),
('Mali'),
('Malta'),
('Marshall Islands'),
('Mauritania'),
('Mauritius'),
('Mexico'),
('Micronesia'),
('Moldova'),
('Monaco'),
('Mongolia'),
('Montenegro'),
('Morocco'),
('Mozambique'),
('Myanmar (formerly Burma)'),
('Namibia'),
('Nauru'),
('Nepal'),
('Netherlands'),
('New Zealand'),
('Nicaragua'),
('Niger'),
('Nigeria'),
('North Korea'),
('North Macedonia'),
('Norway'),
('Oman'),
('Pakistan'),
('Palau'),
('Palestine State'),
('Panama'),
('Papua New Guinea'),
('Paraguay'),
('Peru'),
('Philippines'),
('Poland'),
('Portugal'),
('Qatar'),
('Romania'),
('Russia'),
('Rwanda'),
('Saint Kitts and Nevis'),
('Saint Lucia'),
('Saint Vincent and the Grenadines'),
('Samoa'),
('San Marino'),
('Sao Tome and Principe'),
('Saudi Arabia'),
('Senegal'),
('Serbia'),
('Seychelles'),
('Sierra Leone'),
('Singapore'),
('Slovakia'),
('Slovenia'),
('Solomon Islands'),
('Somalia'),
('South Africa'),
('South Korea'),
('South Sudan'),
('Spain'),
('Sri Lanka'),
('Sudan'),
('Suriname'),
('Sweden'),
('Switzerland'),
('Syria'),
('Tajikistan'),
('Tanzania'),
('Thailand'),
('Timor-Leste'),
('Togo'),
('Tonga'),
('Trinidad and Tobago'),
('Tunisia'),
('Turkey'),
('Turkmenistan'),
('Tuvalu'),
('Uganda'),
('Ukraine'),
('United Arab Emirates'),
('United Kingdom'),
('United States of America'),
('Uruguay'),
('Uzbekistan'),
('Vanuatu'),
('Venezuela'),
('Vietnam'),
('Yemen'),
('Zambia'),
('Zimbabwe');

select * from pais;

-- Tabla de Motivos de Llamada
CREATE TABLE motivo_llamada (
    id_motivo SERIAL PRIMARY KEY,
    descripcion_motivo_ML TEXT NOT NULL
);

INSERT INTO motivo_llamada (descripcion_motivo_ML)
VALUES
  ('Bloqueo de cuenta bancaria'),
  ('Problemas con la tarjeta de crédito'),
  ('Oferta de premios/regalo'),
  ('Solicitud de datos personales'),
  ('Amenaza o extorsión'),
  ('Solo llaman y cuelgan');

SELECT * FROM motivo_llamada;

-- Tabla de Entonaciones de Voz
CREATE TABLE entonacion_voz (
    id_entonacion_voz SERIAL PRIMARY KEY,
    entonacion_EV VARCHAR(25) NOT NULL
);

INSERT INTO entonacion_voz (entonacion_EV)
VALUES
  ('Tranquilo'),
  ('Apresurado'),
  ('Amenazante'),
  ('Confuso');

SELECT * FROM entonacion_voz;

-- TABLA DE DISPOSITIVO TELEFONICO
CREATE TABLE dispositivo (
    id_dispositivo SERIAL PRIMARY KEY,
    dispositivo_D VARCHAR(20) NOT NULL
);

INSERT INTO dispositivo (dispositivo_D)
VALUES
  ('Android'),
  ('iPhone'),
  ('Teléfono fijo');

SELECT * FROM dispositivo;


CREATE TABLE tipo_numero (
    id_tipo_numero SERIAL PRIMARY KEY,
    tipo_numero_TN VARCHAR(25) NOT NULL
);

INSERT INTO tipo_numero (tipo_numero_TN)
VALUES
  ('Personal'),
  ('Empresarial'),
  ('Prefiero no decirlo');

SELECT * FROM tipo_numero;

CREATE TABLE redes (
    id_redes SERIAL PRIMARY KEY,
    redes_R VARCHAR(15) NOT NULL
);

INSERT INTO redes (redes_R)
VALUES
  ('Wi-Fi'),
  ('Datos Moviles'),
  ('No lo se');

SELECT * FROM redes;

CREATE TABLE estatus (
    id_estatus SERIAL PRIMARY KEY,
    estatus_E VARCHAR(15) NOT NULL
);

INSERT INTO estatus (estatus_E)
VALUES
  ('No validado'),
  ('En proceso'),
  ('Validado');

SELECT * FROM estatus;


CREATE TABLE palabras_clave (
    id_palabra SERIAL PRIMARY KEY,
    palabra_PC VARCHAR(20) NOT NULL
);

INSERT INTO palabras_clave (palabra_PC)
VALUES
  ('Urgente'),
  ('Clave bancaria (NIP)'),
  ('Seguridad'),
  ('Transferencia'),
  ('Código SMS'),
  ('Número de la tarjeta'),
  ('No recuerdo');

SELECT * FROM palabras_clave;

-- Tabla de tIPO de Voz
CREATE TABLE tipo_voz (
    id_tipo_voz SERIAL PRIMARY KEY,
    tipo_voz_TV VARCHAR(35) NOT NULL
);

INSERT INTO tipo_voz (tipo_voz_TV)
VALUES
  ('Persona real'),
  ('Voz automatizada (grabacion)'),
  ('Dudoso/Entre los dos anteriores');

SELECT * FROM tipo_voz;

CREATE TABLE chatbot (
    id_prompt SERIAL PRIMARY KEY,
    prompt_CB TEXT NOT NULL,
    fecha_prompt_CB    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	respuesta_CB TEXT,
    fecha_respuesta_CB TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

INSERT INTO chatbot (prompt_CB, respuesta_CB, id_usuario)
VALUES
  (
    'Persona real',
    'El interlocutor se presenta como empleado del banco solicitando tu NIP y datos de la tarjeta para desbloquear la cuenta. Sospecha de vishing.',
    1
  ),
  (
    'Voz automatizada (grabacion)',
    'Se reproduce un mensaje grabado que informa de una actividad fraudulenta y te insta a pulsar 1 para verificar tus datos bancarios. Claramente vishing.',
    2
  ),
  (
    'Dudoso/Entre los dos anteriores',
    'Comienza con una voz humana y luego cambia a un sistema automático que te pide el código SMS para “confirmar” una supuesta transacción. Posible vishing.',
    2
  );

SELECT * FROM chatbot;


CREATE TABLE reporte_general (
    id_reporte_G            SERIAL PRIMARY KEY,
    numero_telefonico       TEXT    NOT NULL,
    fecha_llamada           DATE    NOT NULL,
    hora_llamada            TIME    NOT NULL,
    descripcion             TEXT    NOT NULL,
    id_usuario              INTEGER NOT NULL,
    id_dispositivo          INTEGER NOT NULL,
    id_tipo_numero          INTEGER NOT NULL,
    id_redes                INTEGER NOT NULL,
    veces_que_llamaron      INTEGER NOT NULL DEFAULT 1,
    reportar_autoridad      BOOLEAN NOT NULL DEFAULT FALSE,
    dejaron_buzon_mensaje   BOOLEAN NOT NULL DEFAULT FALSE,
    devolver_llamada        BOOLEAN NOT NULL DEFAULT FALSE,
    id_pais                 INTEGER NOT NULL,
    id_motivo               INTEGER,
    id_entonacion_voz       INTEGER,
    id_tipo_voz             INTEGER,
    compartiste_datos       BOOLEAN DEFAULT FALSE,
    terminar_por_sospecha   BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_pais)             REFERENCES pais            (id_pais),
    FOREIGN KEY (id_usuario)          REFERENCES usuario         (id_usuario),
    FOREIGN KEY (id_dispositivo)      REFERENCES dispositivo     (id_dispositivo),
    FOREIGN KEY (id_tipo_numero)      REFERENCES tipo_numero     (id_tipo_numero),
    FOREIGN KEY (id_redes)            REFERENCES redes           (id_redes),
    FOREIGN KEY (id_motivo)           REFERENCES motivo_llamada  (id_motivo),
    FOREIGN KEY (id_entonacion_voz)   REFERENCES entonacion_voz  (id_entonacion_voz),
    FOREIGN KEY (id_tipo_voz)         REFERENCES tipo_voz        (id_tipo_voz)
);

-- Inserción de registros de ejemplo en reporte_general
INSERT INTO reporte_general (
    numero_telefonico,
    fecha_llamada,
    hora_llamada,
    descripcion,
    id_usuario,
    id_dispositivo,
    id_tipo_numero,
    id_redes,
    veces_que_llamaron,
    reportar_autoridad,
    dejaron_buzon_mensaje,
    devolver_llamada,
    id_pais,
    id_motivo,
    id_entonacion_voz,
    id_tipo_voz,
    compartiste_datos,
    terminar_por_sospecha
) VALUES
-- 1) Vishing con solicitud de NIP en México
(
    '5512345678',
    '2025-08-10',
    '14:23:00',
    'Llamada fraudulenta solicitando NIP y datos de la tarjeta para desbloquear la cuenta.',
    1,
    2,
    2,
    1,
    2,
    TRUE,
    FALSE,
    FALSE,
    111,
    4,
    4,
    3,
    FALSE,
    TRUE
),

-- 2) Oferta de premios falsa desde EE. UU.
(
    '2025550181',
    '2025-08-11',
    '09:15:00',
    'Mensaje grabado: “Felicitaciones, ha ganado un premio. Presione 1 para más información.”',
    2,
    1,
    1,
    3,
    1,
    FALSE,
    TRUE,
    FALSE,
    187,
    6,
    3,
    3,
    FALSE,
    FALSE
),

-- 3) Solicitan datos personales en España
(
    '911234567',
    '2025-08-12',
    '18:45:00',
    'Persona amable pide confirmar datos personales para una supuesta verificación de cuenta.',
    1,
    2,
    2,
    2,
    3,
    FALSE,
    FALSE,
    TRUE,
    165,
    3,
    1,
    2,
    FALSE,
    FALSE
),

-- 4) Extorsión y amenaza desde India
(
    '8012345678',
    '2025-08-12',
    '11:30:00',
    '“Su cuenta será bloqueada a menos que envíe código SMS y transfiera fondos inmediatos”.',
    2,
    3,
    3,
    2,
    4,
    TRUE,
    TRUE,
    FALSE,
    78,
    4,
    2,
    1,
    FALSE,
    TRUE
),

-- 5) Promesa de regalo y solicitud de datos en Nigeria
(
    '12345678',
    '2025-08-13',
    '10:00:00',
    'Ofrecen un regalo si comparte datos bancarios y CVV de la tarjeta.',
    1,
    2,
    2,
    1,
    2,
    FALSE,
    FALSE,
    TRUE,
    127,
    6,
    4,
    1,
    FALSE,
    FALSE
),

-- 6) Cuelga inmediatamente (solo llaman y cuelgan) desde Reino Unido
(
    '2079460958',
    '2025-08-13',
    '12:20:00',
    'Llamada entrante que cuelga en cuanto contestas.',
    2,
    1,
    1,
    3,
    1,
    FALSE,
    FALSE,
    FALSE,
    186,
    5,
    NULL,
    NULL,
    FALSE,
    FALSE
);

-- Verificar los registros
SELECT * FROM reporte_general;

CREATE TABLE IF NOT EXISTS sesiones (
	session_id TEXT PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    ip_address TEXT NOT NULL,
    sesion_creada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_sesion TIMESTAMP NOT NULL,
    sesion_expirada TIMESTAMP NOT NULL,
    esta_activa INTEGER DEFAULT 1,
FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

INSERT INTO sesiones (
    session_id,
    id_usuario,
    ip_address,
    ultima_sesion,
    sesion_expirada,
    esta_activa
)
VALUES
    (
      'd290f1ee-6c54-4b01-90e6-d701748f0851', 
      1, 
      '192.168.1.10', 
      '2025-08-14 10:30:00', 
      '2025-08-14 12:30:00', 
      1
    ),
    (
      'c3a7b2f4-8e21-4e45-9f5b-2a1c8dbe6b22', 
      2, 
      '10.0.0.5', 
      '2025-08-14 09:00:00', 
      '2025-08-14 11:00:00', 
      0
    ),
    (
      'a1b2c3d4-5678-90ab-cdef-1234567890ab', 
      1, 
      '172.16.0.22', 
      '2025-08-13 18:45:00', 
      '2025-08-13 20:45:00', 
      0
    ),
    (
      'e4f5a6b7-8c9d-0123-4567-89abcdef0123', 
      2, 
      '203.0.113.15', 
      '2025-08-14 11:15:00', 
      '2025-08-14 13:15:00', 
      1
    ),
    (
      'f1e2d3c4-b5a6-7890-cdef-112233445566', 
      1, 
      '198.51.100.7', 
      '2025-08-12 14:00:00', 
      '2025-08-12 16:00:00', 
      0
    );

SELECT * FROM sesiones;