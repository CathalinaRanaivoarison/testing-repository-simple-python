import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,           // 50 utilisateurs simultanés
  duration: '30s',   // pendant 30 secondes
};

export default function () {
  // Authentifier
  const loginRes = http.post('http://scalable-flask-app-alb-361397395.eu-west-3.elb.amazonaws.com/authenticate', { username: 'alice' });
  //const loginRes = http.post('http://localhost:8888/authenticate', { username: 'alice' });

  check(loginRes, {
    'auth success': (r) => r.status === 200,
  });

  const token = loginRes.json().return.access;

  const headers = {
    Authorization: `Bearer ${token}`,
  };

  // Appel de /hello
  const helloRes = http.get('http://scalable-flask-app-alb-361397395.eu-west-3.elb.amazonaws.com/hello', { headers });
  //const helloRes = http.get('http://localhost:8888/hello', { headers });

  check(helloRes, {
    'hello is 200': (r) => r.status === 200,
  });

  // Appel de /id
  const idRes = http.get('http://scalable-flask-app-alb-361397395.eu-west-3.elb.amazonaws.com/id', { headers });
  //const idRes = http.get('http://localhost:8888/id', { headers });

  check(idRes, {
    'id is 200': (r) => r.status === 200,
  });

  sleep(1);  // Pause d'1 seconde entre chaque cycle utilisateur
}


// export default function () {
//   const res = http.get('http://scalable-flask-app-alb-2011169963.eu-west-3.elb.amazonaws.com/');
//   check(res, { 'status is 200': (r) => r.status === 200 });
//   sleep(0.5);
// }
