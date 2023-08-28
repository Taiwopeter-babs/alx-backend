import { createClient } from 'redis';

const redisClient = createClient();

// await redisClient.connect();

redisClient.on('error', error => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});
