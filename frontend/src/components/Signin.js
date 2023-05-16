import React, { useState } from 'react';
import axios from 'axios';

function Signin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(`${window.location.protocol}//${window.location.hostname}:8080/api/signin`, { email, password });
      
      // Assuming your server responds with a token on successful sign in
      const token = res.data;
      localStorage.setItem('token', token);
      
      // Redirect to Home page
      window.location.replace('/');
    } catch (err) {
      // handle error
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" placeholder="Email" onChange={e => setEmail(e.target.value)} required />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} required />
      <button type="submit">Sign In</button>
    </form>
  );
}

export default Signin;
