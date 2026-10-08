"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function DashboardPage() {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [videos, setVideos] = useState<any[]>([]);
  const [prompt, setPrompt] = useState("Cinematic product promo with soft lighting and smooth motion.");
  const [style, setStyle] = useState("cinematic");
  const [duration, setDuration] = useState(5);
  const [aspectRatio, setAspectRatio] = useState("9:16");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const savedToken = localStorage.getItem("vividmotion_token");
    if (!savedToken) {
      router.push("/login");
      return;
    }
    setToken(savedToken);
    fetchVideos(savedToken);
  }, [router]);

  async function fetchVideos(authToken: string) {
    const res = await fetch(`${API_URL}/api/v1/videos`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    if (!res.ok) {
      router.push("/login");
      return;
    }
    const data = await res.json();
    setVideos(data.videos || []);
  }

  async function handleGenerate() {
    if (!token) return;
    setLoading(true);
    const res = await fetch(`${API_URL}/api/v1/videos/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        prompt,
        style,
        duration,
        aspect_ratio: aspectRatio,
      }),
    });

    const data = await res.json();
    setLoading(false);

    if (!res.ok) {
      alert(data.detail || "Generation failed");
      return;
    }

    await fetchVideos(token);
  }

  function handleLogout() {
    localStorage.removeItem("vividmotion_token");
    router.push("/login");
  }

  return (
    <main style={{ padding: 24, maxWidth: 1200, margin: "0 auto", color: "white" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>Dashboard</h1>
        <button onClick={handleLogout} style={{ padding: "10px 14px", borderRadius: 10, background: "#111827", color: "white" }}>
          Logout
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 24 }}>
        <div style={{ background: "#0f172a", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 20, padding: 20 }}>
          <h2 style={{ marginTop: 0 }}>Generate a new video</h2>

          <label style={{ display: "block", marginBottom: 8 }}>Prompt</label>
          <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={5} style={{ width: "100%", padding: 12, borderRadius: 12, background: "#111827", color: "white", border: "1px solid rgba(255,255,255,0.1)" }} />

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 20 }}>
            <div>
              <label>Style</label>
              <select value={style} onChange={(e) => setStyle(e.target.value)} style={{ width: "100%", padding: 12, marginTop: 8, borderRadius: 12, background: "#111827", color: "white" }}>
                <option value="cinematic">Cinematic</option>
                <option value="product">Product</option>
                <option value="dreamy">Dreamy</option>
                <option value="ad">Ad</option>
              </select>
            </div>

            <div>
              <label>Duration</label>
              <select value={duration} onChange={(e) => setDuration(Number(e.target.value))} style={{ width: "100%", padding: 12, marginTop: 8, borderRadius: 12, background: "#111827", color: "white" }}>
                <option value={3}>3 sec</option>
                <option value={5}>5 sec</option>
                <option value={10}>10 sec</option>
              </select>
            </div>
          </div>

          <div style={{ marginTop: 20 }}>
            <label>Aspect ratio</label>
            <select value={aspectRatio} onChange={(e) => setAspectRatio(e.target.value)} style={{ width: "100%", padding: 12, marginTop: 8, borderRadius: 12, background: "#111827", color: "white" }}>
              <option value="9:16">9:16</option>
              <option value="1:1">1:1</option>
              <option value="16:9">16:9</option>
            </select>
          </div>

          <button onClick={handleGenerate} disabled={loading} style={{ marginTop: 24, width: "100%", padding: "14px 18px", borderRadius: 12, background: "#2563eb", color: "white", fontWeight: 700 }}>
            {loading ? "Generating..." : "Generate video"}
          </button>
        </div>

        <div style={{ background: "#0f172a", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 20, padding: 20 }}>
          <h2 style={{ marginTop: 0 }}>Recent videos</h2>
          {videos.length === 0 ? (
            <p>No videos yet.</p>
          ) : (
            <div style={{ display: "grid", gap: 12 }}>
              {videos.slice(0, 5).map((video: any) => (
                <div key={video.id} style={{ background: "#111827", borderRadius: 12, padding: 12 }}>
                  <div style={{ fontWeight: 600 }}>{video.prompt.slice(0, 50)}...</div>
                  <div style={{ color: "#94a3b8", marginTop: 6 }}>{video.status}</div>
                  {video.output_url && (
                    <video src={video.output_url} controls style={{ width: "100%", marginTop: 8, borderRadius: 10 }} />
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
