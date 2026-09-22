# Casos de Prueba Documentados — Automatización de Estudios de Títulos

> **Hito M2:** Batería de 5 casos de prueba con datos sintéticos / simulados (en cumplimiento de la **Ley 1581 de 2012 de Hábeas Data**).  
> **Objetivo:** Evaluar la precisión analítica, la detección de riesgos registrales y la aplicación de salvaguardas anti-alucinación.

---

## Caso de Prueba 1: Tracto Sucesivo Impecable (Caso Limpio)
* **Matrícula Simulada:** 50C-999001 (Círculo de Bogotá)
* **Datos Registrales:**
  - **Anotación 001 (15/03/2005):** Compraventa (Columna 1). De: Inversiones Urbanas S.A.S. A: Pedro Gómez Rodríguez. Escritura 1234 de Notaría 10 de Bogotá.
  - **Anotación 002 (20/08/2015):** Compraventa (Columna 1). De: Pedro Gómez Rodríguez. A: María Fernanda Torres. Escritura 4567 de Notaría 25 de Bogotá.
  - **Anotación 003 (10/02/2024):** Compraventa (Columna 1). De: María Fernanda Torres. A: Carlos Alberto Mendoza. Escritura 8901 de Notaría 4 de Bogotá.
* **Resultado Esperado de la Herramienta:**
  - **Semáforo:** 🟢 **VERDE (Viable)**.
  - **Dictamen:** Tracto sucesivo perfecto durante más de 19 años. Cada tradente fue el adquirente anterior conforme al Art. 3 Numeral 4 de la Ley 1579 de 2012. Folio libre de gravámenes, embargos y limitaciones al dominio.

---

## Caso de Prueba 2: Falsa Tradición (Columna 6 — Art. 7 Ley 1579/2012)
* **Matrícula Simulada:** 50C-999002 (Círculo de Bogotá)
* **Datos Registrales:**
  - **Anotación 001 (12/04/2010):** Adjudicación en Sucesión (Columna 1). De: Causante Juan Pérez. A: Heredero Andrés Pérez.
  - **Anotación 002 (05/09/2018):** Venta de Derechos y Acciones Herenciales Indeterminados (Columna 6 - Falsa Tradición). De: Andrés Pérez. A: Gonzalo Ramírez.
  - **Anotación 003 (14/11/2023):** Compraventa de Posesión (Columna 6 - Falsa Tradición). De: Gonzalo Ramírez. A: Felipe Castro.
* **Resultado Esperado de la Herramienta:**
  - **Semáforo:** 🔴 **ROJO (No Viable / Alto Riesgo)**.
  - **Dictamen:** Se detectan inscripciones en la Columna 6 (Falsa Tradición). El actual tenedor no ostenta el derecho real de dominio pleno (Art. 752 Código Civil y Art. 7 Ley 1579 de 2012). Se requiere proceso judicial de pertenencia o saneamiento de titulación antes de celebrar un negocio traslaticio de dominio.

---

## Caso de Prueba 3: Medida Cautelar de Embargo Activo
* **Matrícula Simulada:** 50C-999003 (Círculo de Bogotá)
* **Datos Registrales:**
  - **Anotación 001 (10/01/2012):** Compraventa (Columna 1). De: Constructora El Rosal. A: Jaime Silva López.
  - **Anotación 002 (22/06/2021):** Embargo Ejecutivo con Acción Personal (Columna 3 - Medida Cautelar). Demandante: Banco Financiero Colombiano. Demandado: Jaime Silva López. Oficio judicial No. 4321 del Juzgado 15 Civil del Circuito de Bogotá.
  - *No existe anotación de cancelación en la Columna 5.*
* **Resultado Esperado de la Herramienta:**
  - **Semáforo:** 🔴 **ROJO (No Viable por Objeto Ilícito)**.
  - **Dictamen:** Inmueble afectado por medida cautelar de embargo vigente. De conformidad con el Art. 1521 Numeral 3 del Código Civil, hay objeto ilícito en la enajenación de bienes embargados por decreto judicial, salvo que el juez lo autorice o el acreedor consienta en ello. No se puede escriturar sin previo oficio de desembargo debidamente registrado.

---

## Caso de Prueba 4: Hipoteca Bancaria Activa y Afectación a Vivienda Familiar
* **Matrícula Simulada:** 50C-999004 (Círculo de Bogotá)
* **Datos Registrales:**
  - **Anotación 001 (18/05/2016):** Compraventa (Columna 1). De: Proyectos y Vivienda S.A. A: Diana Carolina Ruiz.
  - **Anotación 002 (18/05/2016):** Constitución de Hipoteca Abierta de Cuantía Indeterminada (Columna 2). A favor de: Banco Hipotecario Nacional.
  - **Anotación 003 (18/05/2016):** Constitución de Afectación a Vivienda Familiar (Columna 4 - Limitación al Dominio - Ley 258 de 1996). Otorgada por: Diana Carolina Ruiz.
* **Resultado Esperado de la Herramienta:**
  - **Semáforo:** 🟡 **AMARILLO (Viable con Condiciones / Saneamiento Previo)**.
  - **Dictamen:** El título traslaticio es válido, pero el inmueble tiene dos gravámenes/limitaciones activas:
    1. Hipoteca vigente (Columna 2): Se requiere solicitar saldo de deuda y minuta de cancelación de hipoteca a la entidad bancaria para otorgarse simultáneamente con la venta.
    2. Afectación a Vivienda Familiar (Columna 4): Exige la comparecencia y firma de ambos cónyuges/compañeros para cancelarla en la misma escritura de enajenación (Art. 3 Ley 258/1996).

---

## Caso de Prueba 5: Ruptura de Tracto Sucesivo (Eslabón Faltante)
* **Matrícula Simulada:** 50C-999005 (Círculo de Bogotá)
* **Datos Registrales:**
  - **Anotación 001 (01/02/2011):** Compraventa (Columna 1). De: Urbanizadora Los Andes. A: Roberto Cadena. Escritura 101.
  - **Anotación 002 (15/07/2019):** Compraventa (Columna 1). De: **Álvaro Morales**. A: Patricia Herrera. Escritura 902.
* **Resultado Esperado de la Herramienta:**
  - **Semáforo:** 🔴 **ROJO (Vicio Registral / Ruptura de Tracto)**.
  - **Dictamen:** Violación flagrante al Principio de Tracto Sucesivo (Art. 3 Numeral 4 Ley 1579 de 2012). Álvaro Morales aparece enajenando el predio en la anotación 002 sin constar previamente como adquirente en la anotación 001 (el titular inscrito era Roberto Cadena). Se requiere solicitar certificado de tradición histórico o aclaración registral ante la Oficina de Registro.
