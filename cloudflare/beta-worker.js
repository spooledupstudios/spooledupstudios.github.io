// Receives beta sign-ups from spooledupstudios.com/beta/ and stores them in KV (binding: BETA).
// Accepts only a small JSON POST from our own site. Stores name, email, device, note and the time. No IP or headers.
// List sign-ups: Cloudflare dashboard > Workers & Pages > KV > BETA, or `wrangler kv key list --binding BETA`.
const ORIGINS = ["https://spooledupstudios.com", "https://www.spooledupstudios.com"];
const clip = (v, n) => String(v ?? "").trim().slice(0, n);

export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": ORIGINS.includes(origin) ? origin : ORIGINS[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin",
    };
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (req.method !== "POST" || !ORIGINS.includes(origin)) return new Response("Not allowed", { status: 403, headers: cors });
    let d;
    try { d = await req.json(); } catch { return new Response("Bad request", { status: 400, headers: cors }); }
    const email = clip(d.email, 120).toLowerCase();
    const name = clip(d.name, 80);
    const device = clip(d.device, 40);
    if (!name || !/^\S+@\S+\.\S+$/.test(email) || !device) return new Response("Bad request", { status: 400, headers: cors });
    await env.BETA.put("signup:" + email, JSON.stringify({ name, email, device, note: clip(d.note, 400), at: new Date().toISOString() }));
    return new Response("ok", { status: 200, headers: cors });
  },
};
