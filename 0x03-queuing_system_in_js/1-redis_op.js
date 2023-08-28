import redis from 'redis';

const redisClient = redis.createClient();

// await redisClient.connect(); -- version >= 4

redisClient.on('error', error => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

/**
 * sets a new school value
 * @param {*} schoolName key of school
 * @param {*} value value of schoolName key 
 */
function setNewSchool(schoolName, value) {
  redisClient.set(schoolName, value, redis.print);
}

/**
 * gets the value of key `schoolName`
 * @param {*} schoolName - key to get
 * @returns value of key
 */
function displaySchoolValue(schoolName) {
  redisClient.get(schoolName, (error, reply) => {
    console.log(reply.toString());
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
