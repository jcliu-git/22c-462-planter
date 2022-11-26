/** @type {import('next').NextConfig} */
const withPWA = require('next-pwa')({
  dest: 'public',
})
const nextConfig = withPWA({
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ["images.unsplash.com", "source.unsplash.com", "clevergarden.blob.core.windows.net"],
  },
});

module.exports = nextConfig;
