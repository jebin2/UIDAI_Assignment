# UIDAI Sandbox - E2EE Payload Simulator

Assignment for the UIDAI Sandbox Technical Lead role. Data is encrypted in the browser before transmission and only decrypted on the server. Rate limiting protects the CPU-intensive decryption endpoint.

**Live demo:** [https://jebin2.github.io/UIDAI_Assignment](https://jebin2.github.io/UIDAI_Assignment) → **API:** [https://jebin2-uidai-assignment.hf.space/](https://jebin2-uidai-assignment.hf.space/)

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in values
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

---

## CI/CD

Push to `main` triggers two parallel jobs:

| Job | Target | Method |
|---|---|---|
| deploy-frontend | GitHub Pages | `actions/deploy-pages` |
| deploy-backend | Hugging Face Spaces | `rsync` + `git push` |

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `VITE_API_BASE_URL` | Backend URL for frontend build |
| `HF_TOKEN` | Hugging Face write token |
| `HF_USERNAME` | Hugging Face username |
| `HF_SPACE` | Hugging Face Space name |
