FROM node:20-alpine AS build-stage

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

FROM python:3.12-slim AS production-stage

WORKDIR /app

COPY --from=build-stage /app/dist /app/frontend_dist
