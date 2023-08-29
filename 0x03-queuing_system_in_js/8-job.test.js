import kue from "kue";
const expect = require('chai').expect
const util = require('util');

const createPushNotificationsJobs = require('./8-job.js');
// import createPushNotificationsJobs from "./8-job.js";

const jobs = [
  {
    phoneNumber: '41535187808686',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '234874829201',
    message: 'This is the code 1274 to verify your account'
  }
];
const queue = kue.createQueue();

describe('createPushNotificationsJobs', function () {
  // enter test mode before processing or executing any tests
  // before(function () {
  //   queue.testMode.enter();
  // });
  beforeEach(function () {
    queue.testMode.enter();
  })
  afterEach(function () {
    queue.testMode.clear();
  });
  // cleanup
  after(function () {
    queue.testMode.exit();
  });

  it('display error when jobs is not an array', function () {
    expect(() => createPushNotificationsJobs('jobs', queue)).to.throw('Jobs is not an array');
  });

  it('Verify jobs creation', function () {
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
  });
});
