/** @type {import('next').NextConfig} */
const withPWA = require("next-pwa")({
  dest: "public",
});

const config = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: [
      "images.unsplash.com",
      "source.unsplash.com",
      "clevergarden.blob.core.windows.net",
    ],
  },
};

module.exports = withPWA(config);

// module.exports = config;
