import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RAG with LangChain",
  description: "A learning project — implement the core RAG concepts yourself.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
