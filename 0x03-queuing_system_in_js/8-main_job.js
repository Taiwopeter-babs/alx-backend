const kue = require('kue');

// import createPushNotificationsJobs from './8-job.js';

const createPushNotificationsJobs = require('./8-job.js');

const queue = kue.createQueue();

const list = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  }
];
createPushNotificationsJobs('jobs', queue);
