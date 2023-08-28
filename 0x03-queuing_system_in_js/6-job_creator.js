import kue from 'kue';

/**
 * create a queue for jobs
 */
const push_notification_code = kue.createQueue();

const job = push_notification_code.create('push_notification_code', {
  phoneNumber: "+2348111116809",
  message: "This is the code to verify your account"
}).save(function (error) {
  if (!error) {
    console.log(`Notification job created: ${job.id}`);
  }
});

// handler for completion event
job.on('complete', (result) => {
  console.log('Notification job completed');
});

// handler for failure event
job.on('failed', (error) => {
  console.log('Notification job failed')
});
