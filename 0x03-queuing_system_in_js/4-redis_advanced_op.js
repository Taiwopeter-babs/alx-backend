import redis from 'redis';

const redisClient = redis.createClient();

// await redisClient.connect(); -- version >= 4

redisClient.on('error', error => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

const hashKey = 'HolbertonSchools';
const hashValues = {
  'Portland': 50,
  'Seattle': 80,
  'New York': 20,
  'Bogota': 20,
  'Cali': 40,
  'Paris': 2
};

for (let [key, value] of Object.entries(hashValues)) {
  redisClient.hset(hashKey, key, value, redis.print);
}

redisClient.hgetall(hashKey, (error, replyObj) => {
  console.log(replyObj);
});
