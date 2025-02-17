# Basis-Image für das Vue-Build mit PNPM
FROM node:20-alpine AS build-stage

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Installiere PNPM direkt über npm, um Corepack-Probleme zu umgehen
RUN npm install -g pnpm

# Kopiere nur package.json und pnpm-lock.yaml, um den Cache optimal zu nutzen
COPY package.json pnpm-lock.yaml ./

# Installiere Abhängigkeiten ohne Änderungen am Lockfile
RUN pnpm install --frozen-lockfile

# Kopiere den Quellcode und baue das Projekt
COPY . .
RUN pnpm build

# Production-Stage: Nutze ein leichtgewichtiges Python-Image
FROM python:3.12-slim AS production-stage

# Setze das Arbeitsverzeichnis für das finale Image
WORKDIR /app

# Kopiere das gebaute Vue-Frontend aus der vorherigen Stage
COPY --from=build-stage /app/dist /app/frontend_dist
