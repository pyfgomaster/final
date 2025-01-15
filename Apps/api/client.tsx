import ky from 'ky';

const client = ky.extend({
    prefixUrl: "http://140.138.150.21/G14_api/",
    headers: {
      'X-No-CSRF': '1',
    },
    credentials: 'include',
});

export default client