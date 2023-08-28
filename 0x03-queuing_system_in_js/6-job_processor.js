import kue from 'kue';

/**
 * create a queue for jobs
 */
const jobs = kue.createQueue();


function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

/* handler to process jobs */
jobs.process('push_notification_code', function (job, done) {
  sendNotification(job.data.phoneNumber, job.data.message);
  done();
});
