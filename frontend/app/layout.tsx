import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "VividMotion AI",
  description: "Turn any image into cinematic AI video in seconds.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
