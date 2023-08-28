import redis from 'redis';
import util from 'util';

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
async function displaySchoolValue(schoolName) {
  // without `bind`, the promisified function will be undefined
  const redisClientGetPromisified = util.promisify(redisClient.get).bind(redisClient);
  const reply = await redisClientGetPromisified(schoolName);
  console.log(reply.toString());
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
