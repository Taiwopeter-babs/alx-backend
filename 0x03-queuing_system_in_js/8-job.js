/**
 * creates jobs for push notifications
 * @param {*} jobs an array of objects
 * @param {*} queue a kue Queue instance
 */
export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }
  for (let job of jobs) {
    let jobToQueue = queue.create('push_notification_code_3', job)
      .save(function (error) {
        if (!error) {
          console.log(`Notification job created: ${jobToQueue.id}`);
        }
      });

    // handler for events
    jobToQueue.on('complete', (result) => {
      console.log(`Notification job ${jobToQueue.id} completed`);
    }).on('failed', (error) => {
      console.log(`Notification job ${jobToQueue.id} failed: ${error}`);
    }).on('progress', function (progress, data) {
      console.log(`Notification job ${jobToQueue.id} ${progress}% complete`);
    });
  }
}
