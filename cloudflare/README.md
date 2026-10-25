# Beta sign-up worker

1. Cloudflare dashboard > Workers & Pages > Create > Worker. Name it `spooled-beta`. Paste `beta-worker.js`. Deploy.
2. Workers & Pages > KV > Create namespace `BETA`.
3. Worker > Settings > Bindings > Add > KV namespace. Variable name `BETA`, pick the namespace. Save.
4. Copy the worker URL (`https://spooled-beta.<you>.workers.dev`).
5. In `build_studio.py` set `BETA_ENDPOINT` to that URL, run `python3 build_studio.py`, commit, push.

Until step 5, the form opens an email to info@spooledupstudios.com instead.
