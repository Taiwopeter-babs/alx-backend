const express = require('express');
const redis = require('redis');
const kue = require('kue');
const util = require('util');


// ====== INITIALIZE BOOLEAN ======
let reservationEnabled = true;


// ======== INITIALIZE SERVER, REDIS, AND QUEUE ===========
const app = express();
const redisClient = redis.createClient();
const queue = kue.createQueue();


/**
 * redis client is connected here and not at the end of the program:
 * 
 * Reason:
 * - A default value has to be set, 50, for the available_seats key, and the
 * express server runs on a promise-based object. So, starting the redis client here
 * makes sure it is available before any function is called on it.
 */
redisClient.on('error', error => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});



// ======= DEFINE FUNCTIONS ========

/**
 * sets a number for the available_seats
 * @param {*} number number of seats to reserve
 */
function reserveSeat(number) {
  redisClient.set('available_seats', number);
}

/**
 * 
 * @returns number of `available_seats` stored/cached in redis
 */
async function getCurrentAvailableSeats() {
  const promisifiedGet = util.promisify(redisClient.get).bind(redisClient);
  const available_seats = await promisifiedGet('available_seats');
  return available_seats;
}
// ===== END OF FUNCTIONS DEFINITION ==========



// ======== APIs ROUTES DEFINITION ============
app.get('/available_seats', async (req, res) => {
  const available_seats = await getCurrentAvailableSeats();
  return res.json({ numberOfAvailableSeats: available_seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservation are blocked" });
  }
  const job = queue.create('reserve_seat', {
    hallId: 23,
    seatId: '14E'
  }).save(function (error) {
    if (error) {
      return res.json({ status: 'Reservation failed' });
    }
    return res.json({ status: 'Reservation in process' });
  })

  // set job handlers
  job.on('complete', (result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (error) => {
    console.log(`Seat reservation job ${job.id} failed: ${error}`);
  });
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();
    const newAvailableSeats = currentAvailableSeats - 1;
    // set new number of seats
    reserveSeat(newAvailableSeats);

    // update reservation status
    if (newAvailableSeats >= 0) {
      if (newAvailableSeats === 0) {
        reservationEnabled = false;
      }
      return done();
    } else {
      return done(new Error('Not enough seats available'));
    }
  });
  return res.json({ status: 'Queue processing' });
});



// ==== RUN SERVER =============

app.listen(1245, () => {
  console.log('server is listening on port 1245');
  // === INTIALIZE available_seats
  redisClient.set('available_seats', 50);
});
