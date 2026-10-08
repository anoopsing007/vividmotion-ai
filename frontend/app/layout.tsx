import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'VividMotion AI',
  description: 'Turn any image into cinematic AI-powered video.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
