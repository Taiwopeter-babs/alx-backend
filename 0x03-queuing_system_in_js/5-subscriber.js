import redis from 'redis';

/**
 * subscriber client
 */
const subClient = redis.createClient();

// await redisClient.connect(); -- version >= 4

subClient.on('error', error => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

subClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

// subscribe to a channel
subClient.subscribe('holberton school channel');

// listen for messages on the channels
subClient.on('message', (channel, message) => {
  // check channel
  if (channel === 'holberton school channel') {
    if (message === 'KILL_SERVER') {
      // unsubscribe from channel and quit
      console.log(message.toString());
      subClient.unsubscribe();
      subClient.quit();
    } else {
      // log message on console
      console.log(message.toString());
    }
  }
});
