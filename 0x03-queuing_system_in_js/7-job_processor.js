import kue from "kue";

// create queue
const queue = kue.createQueue();

// blacklisted numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

/**
 * send notification through queue workers
 * @param {*} phoneNumber property of job data
 * @param {*} message property of job data
 * @param {*} job job to be processed
 * @param {*} done 
 */
function sendNotification(phoneNumber, message, job, done) {
  // set initial job progress
  job.progress(0, 100);

  // check if phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }
  // update job progress
  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  done();
}

/**
 * process jobs
 */
queue.process('push_notification_code_2', 2, function (job, done) {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});