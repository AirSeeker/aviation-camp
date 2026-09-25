import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Aviation Camp | FAA Handbook Library',
  description: 'A study library built from FAA aviation handbooks.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="uk"><body>{children}</body></html>;
}