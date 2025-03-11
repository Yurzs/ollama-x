import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import UserCreation from './components/UserCreation';
import UserAuthorization from './components/UserAuthorization';

function App() {
  return (
    <Router>
      <div className="container">
        <Routes>
          <Route path="/create-user" element={<UserCreation />} />
          <Route path="/authorize-user" element={<UserAuthorization />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
