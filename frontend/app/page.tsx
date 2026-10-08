"use client";

import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ minHeight: "100vh", background: "#020817", color: "white", padding: 24 }}>
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        <nav style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 48 }}>
          <div style={{ fontSize: 24, fontWeight: 700 }}>VividMotion AI</div>
          <div style={{ display: "flex", gap: 16 }}>
            <Link href="/login">Login</Link>
            <Link href="/dashboard">Dashboard</Link>
          </div>
        </nav>

        <section style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 32, alignItems: "center" }}>
          <div>
            <div style={{ display: "inline-block", padding: "8px 12px", borderRadius: 999, background: "rgba(59,130,246,0.15)", color: "#93c5fd", marginBottom: 20 }}>
              AI Image to Video App
            </div>
            <h1 style={{ fontSize: 56, lineHeight: 1.05, margin: 0, fontWeight: 800 }}>
              Turn any image into a cinematic video in seconds.
            </h1>
            <p style={{ fontSize: 20, color: "#cbd5e1", marginTop: 24 }}>
              Personal-use AI video generator for creators, sellers, and brands.
            </p>
            <div style={{ display: "flex", gap: 16, marginTop: 28 }}>
              <Link href="/login" style={{ background: "#2563eb", color: "white", padding: "14px 22px", borderRadius: 999, fontWeight: 600, textDecoration: "none" }}>
                Start free
              </Link>
              <Link href="/dashboard" style={{ border: "1px solid rgba(255,255,255,0.15)", color: "white", padding: "14px 22px", borderRadius: 999, textDecoration: "none" }}>
                Open dashboard
              </Link>
            </div>
          </div>

          <div style={{ background: "linear-gradient(135deg, #111827, #1f2937)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 24, padding: 24 }}>
            <div style={{ display: "flex", justifyContent: "space-between", color: "#cbd5e1", marginBottom: 18 }}>
              <span>Original</span>
              <span>AI Motion</span>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div style={{ height: 220, borderRadius: 18, background: "linear-gradient(135deg,#0f172a,#1e293b)", border: "1px solid rgba(255,255,255,0.08)" }} />
              <div style={{ height: 220, borderRadius: 18, background: "linear-gradient(135deg,#1d4ed8,#0f172a)", border: "1px solid rgba(255,255,255,0.08)" }} />
            </div>
            <div style={{ marginTop: 18, padding: 14, background: "rgba(15,23,42,0.8)", borderRadius: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span>Prompt</span>
                <span style={{ color: "#93c5fd" }}>Cinematic zoom</span>
              </div>
              <div style={{ height: 8, borderRadius: 999, background: "#374151", overflow: "hidden" }}>
                <div style={{ width: "70%", height: "100%", background: "linear-gradient(90deg,#3b82f6,#60a5fa)" }} />
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
