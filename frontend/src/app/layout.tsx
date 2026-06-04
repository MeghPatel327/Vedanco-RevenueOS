import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { Toaster } from "sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Vedanco RevenueOS",
  description: "Modern SaaS frontend for Vedanco RevenueOS",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen overflow-hidden bg-background">
          <Sidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            <header className="flex h-14 lg:h-[60px] items-center gap-4 border-b bg-muted/40 px-6">
              <h1 className="text-lg font-semibold">RevenueOS Portal</h1>
            </header>
            <main className="flex-1 overflow-auto p-6 md:p-8">
              {children}
            </main>
          </div>
        </div>
        <Toaster />
      </body>
    </html>
  );
}
