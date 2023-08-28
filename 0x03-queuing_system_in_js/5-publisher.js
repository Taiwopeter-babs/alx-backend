import redis from 'redis';

/**
 * subscriber client
 */
const pubClient = redis.createClient();

// await redisClient.connect(); -- version >= 4

pubClient.on('error', error => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

pubClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

/**
 * publishes a message to channel
 * @param {*} message message to publish to channel
 * @param {*} time delay before publish
 */
function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    pubClient.publish('holberton school channel', message);
  }, time);
}

publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
