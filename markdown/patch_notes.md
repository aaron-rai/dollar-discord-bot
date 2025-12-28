- 2.0.4 improves database connection reliability and updates the YouTube plugin for better music playback stability.

### Fixes and Enhancements

- Updated Youtube-Source plugin to 1.16.0
- Fixed database connection race condition on container startup with retry logic and exponential backoff
- Updated docker-compose.yml to use health checks, ensuring PostgreSQL is fully ready before bot starts
- Pinned PostgreSQL to version 15 for stability
- Added fail-fast behavior if database connection fails after all retry attempts
