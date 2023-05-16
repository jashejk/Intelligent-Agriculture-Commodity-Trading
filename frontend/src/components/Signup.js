import React, { useState } from 'react';
import axios from 'axios';

function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(`${window.location.protocol}//${window.location.hostname}:8080/api/signup`, { name, email, password });
      
      // Assuming your server responds with a token on successful sign up
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
      <input type="text" placeholder="Name" onChange={e => setName(e.target.value)} required />
      <input type="email" placeholder="Email" onChange={e => setEmail(e.target.value)} required />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} required />
      <button type="submit">Sign Up</button>
    </form>
  );
}

export default Signup;
