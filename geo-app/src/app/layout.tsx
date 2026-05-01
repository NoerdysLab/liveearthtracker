import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "WORLDVIEW // ORBITAL TRACKING",
  description: "Advanced Geopolitical Risk Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <script src="https://cesium.com/downloads/cesiumjs/releases/1.115/Build/Cesium/Cesium.js" async></script>
        <link href="https://cesium.com/downloads/cesiumjs/releases/1.115/Build/Cesium/Widgets/widgets.css" rel="stylesheet" />
      </head>
      <body
        className="antialiased bg-black"
        style={{ fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
