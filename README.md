# Travel Agency Data Warehouse & BI Pipeline (Tripin' Logistics)

This repository contains the end-to-end development of a data infrastructure (ETL and Modeling) designed for a travel and logistics agency. The primary goal was to transition from unstructured manual operations to a relational data model that enables real-time tracking of sales, inventories, and profitability.

## Tech Stack
* **Language:** Python (Pandas, Datetime, Faker, Random).
* **Data Modeling:** Star / Snowflake Schema.
* **Visualization & BI:** Power BI.

## Project Architecture

The project is divided into three main phases developed in Python:

1. **Dimensions Generation (Master Catalogs):** Structured creation of master catalogs including clients, agents, flight routes (accounting for time zones and layovers), hotels, tours, and additional services such as insurance and transfers.
2. **Temporal Inventory Engine:** A system that simulates the daily availability (Big Data) of flight seats, hotel rooms, and vehicles over a multi-year range, accurately mimicking real-world booking behaviors and stock depletion.
3. **Transactional Simulator (CRM & Finance):** A script that generates purchase intents based on specific user profiles (e.g., Family, Business, Backpacker). It processes bookings by deducting stock and calculates key financial metrics: `total_sale_price`, `supplier_cost`, `agency_margin`, and `agent_commission`.

## Data Modeling (Snowflake Schema)

The data model was specifically designed to optimize rendering performance and DAX calculations in Power BI. It consists of:
* **Fact Table:** `fact_ventas` (Centralized table recording all transactions, margins, and commissions).
* **Dimension Tables:** Normalized catalogs (`dim_clientes`, `dim_agentes`, `dim_vuelos`, `dim_hoteles`, etc.).
* **Inventory Sub-Dimensions:** Tables connected to the main dimensions for historical availability tracking (`inv_vuelos`, `inv_hoteles`, etc.).

## Business Impact

This data model enables the agency to:
* Identify the destinations and client profiles with the highest net profitability.
* Automate commission calculations for sales agents in a fully transparent manner.
* Monitor occupancy and inventories to drive predictive marketing and pricing strategies.

---

# Travel Agency Data Warehouse & BI Pipeline (Tripin' Logistics)

Este repositorio contiene el desarrollo completo de una infraestructura de datos (ETL y Modelado) diseñada para una agencia de viajes y logística. El objetivo principal fue migrar de operaciones no estructuradas a un modelo de datos relacional que permita monitorear ventas, inventarios y rentabilidad en tiempo real.

## Stack Tecnológico
* **Lenguaje:** Python (Pandas, Datetime, Faker, Random).
* **Modelado de Datos:** Star / Snowflake Schema.
* **Visualización & BI:** Power BI.

## Arquitectura del Proyecto

El proyecto se divide en tres fases principales desarrolladas en Python:

1. **Generación de Dimensiones (Catálogos):** Creación estructurada de catálogos maestros que incluyen clientes, agentes, rutas de vuelo (considerando zonas horarias y escalas), hoteles, tours, y servicios adicionales (seguros, traslados).
2. **Motor de Inventarios Temporales:** Un sistema que simula la disponibilidad diaria (Big Data) de asientos, cuartos y vehículos en un rango de varios años, imitando el comportamiento real de las reservas.
3. **Simulador Transaccional (CRM & Finanzas):** Un script que genera intenciones de compra basadas en perfiles de usuario (Familiar, Negocios, Mochilero, etc.). Procesa la reserva deduciendo el stock y calcula métricas financieras clave: `precio_venta_total`, `costo_proveedor`, `margen_agencia` y `comision_agente`.

## Modelado de Datos (Snowflake Schema)

El modelo de datos fue diseñado para optimizar el rendimiento y los cálculos DAX en Power BI. Consiste en:
* **Fact Table:** `fact_ventas` (Contraloría de todas las transacciones, márgenes y comisiones).
* **Dimension Tables:** Catálogos normalizados (`dim_clientes`, `dim_agentes`, `dim_vuelos`, `dim_hoteles`, etc.).
* **Sub-Dimensiones de Inventario:** Tablas conectadas a las dimensiones principales para el rastreo histórico de disponibilidad (`inv_vuelos`, `inv_hoteles`, etc.).

## Impacto de Negocio

Este modelo de datos permite a la agencia:
* Identificar los destinos y perfiles de cliente con mayor rentabilidad neta.
* Automatizar el cálculo de comisiones para agentes de ventas de forma transparente.
* Monitorear la ocupación e inventarios para estrategias de marketing predictivo.
