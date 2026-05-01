import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  basePath: "/geo",
  output: "export",
  transpilePackages: ['react-map-gl', 'mapbox-gl', 'maplibre-gl'],
  images: {
    unoptimized: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
