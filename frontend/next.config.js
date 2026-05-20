/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['flagcdn.com', 'api.countryflagsapi.com'],
  },
}

module.exports = nextConfig
