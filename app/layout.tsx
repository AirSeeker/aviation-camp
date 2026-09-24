import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Aviation Camp | EASA PPL Ground School',
  description: 'A focused study platform for the EASA Private Pilot Licence theoretical exams.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="uk"><body>{children}</body></html>;
}