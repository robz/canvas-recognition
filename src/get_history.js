const PubNub = require('pubnub');
const fs = require('fs');
const keys = require('./keys');

const pubnub = new PubNub(keys);

pubnub.history(
  {
    channel: 'digit_prediction_mistakes',
    count: 10,
    stringifiedTimeToken: true,
  },
  function(status, response) {
    const data = JSON.stringify(response.messages, null, '  ');
    console.log(data);
    fs.writeFile(
      `data/messages-${new Date().toString().replace(/ /g, '_')}.json`,
      data,
      () => {},
    );
  },
);
