# VividMotion AI

VividMotion AI is an MVP SaaS product that turns a single image into a short AI-generated video. It is designed for creators, brands, ecommerce sellers, and marketing teams who want cinematic motion videos without editing skills.

## Core idea

- Upload an image
- Add a description or creative prompt
- Choose a style, duration, and aspect ratio
- Generate a short video using an AI video model
- Download or share the result

## Product status

This repository contains a starter implementation of the product:

- Frontend landing page and dashboard UI
- FastAPI backend API structure
- AI generation service starter code
- Project setup for future scaling

## Repository structure

```text
.
├── README.md
├── .env.example
├── .gitignore
├── package.json
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── styles/
│   ├── package.json
│   ├── next.config.mjs
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next-env.d.ts
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env.example
└── infra/
    └── docker/
```

## Quick start

### 1. Install root dependencies

```bash
npm install
```

### 2. Install frontend dependencies

```bash
cd frontend && npm install
```

### 3. Install backend dependencies

```bash
cd backend && python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the frontend

```bash
cd frontend
npm run dev
```

### 5. Run the backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Landing page

The frontend includes a marketing homepage with:

- Hero section
- Feature list
- Demo value proposition
- Pricing section
- CTA buttons
- Modern SaaS styling

## Backend API

The backend exposes starter endpoints:

- `GET /health`
- `POST /api/videos/generate`
- `GET /api/videos`

## MVP roadmap

### Phase 1

- Authentication
- Image upload
- Generation queue
- Video history
- Credit tracking

### Phase 2

- OpenAI prompt enhancement
- Real video model integration
- FFmpeg post-processing
- S3 or Supabase storage

### Phase 3

- Billing and subscriptions
- Templates and presets
- Team workspaces
- API access

## Suggested market positioning

"Turn any image into a cinematic video in seconds."

## Example prompt

```text
Create a cinematic product video with slow camera movement, soft lighting,
modern color grading, and subtle parallax motion.
```

## Product notes

This code is intentionally designed as a practical starter and is not a production ready AI pipeline yet. It provides the foundation for real integration with providers such as:

- Replicate
- Runway
- Stability AI
- Luma
- Pika

## License

MIT
